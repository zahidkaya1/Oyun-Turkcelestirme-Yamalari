#!/usr/bin/env python3
from pathlib import Path
import argparse
import base64
import gzip
import hashlib
import json
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BACKUP_DIR = '.turkce_yama_backup'


def sha_file(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def game_ids():
    games = ROOT / 'games'
    return sorted(p.name for p in games.iterdir() if p.is_dir() and (p / 'manifest.json').exists())


def load_manifest(game):
    p = ROOT / 'games' / game / 'manifest.json'
    if not p.exists():
        raise SystemExit(f'Bilinmeyen oyun: {game}')
    return json.loads(p.read_text(encoding='utf-8'))


def backup(root, rel):
    src = root / rel
    if not src.exists():
        return
    dst = root / BACKUP_DIR / rel
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def allowed_anchor_hashes(manifest):
    allowed = {manifest['anchor']['sha256']}
    for patch in manifest['patches']:
        if patch['target'] == manifest['anchor']['path']:
            allowed.add(patch['target_sha256'])
    return allowed


def validate_root(manifest, root):
    if not root.exists():
        raise SystemExit('Oyun klasörü bulunamadı.')
    anchor = root / manifest['anchor']['path']
    if not anchor.exists():
        raise SystemExit(f'Yanlış klasör: {manifest["anchor"]["path"]} bulunamadı.')
    if sha_file(anchor) not in allowed_anchor_hashes(manifest):
        raise SystemExit('Bu oyun sürümü yama manifestiyle eşleşmiyor. Dosyalara dokunulmadı.')


def patch_state(root, item):
    source = root / item['source']
    target = root / item['target']

    if target.exists() and sha_file(target) == item['target_sha256']:
        return 'patched'
    if source.exists() and sha_file(source) == item['source_sha256']:
        return 'ready'
    return 'mismatch'


def text_edit_state(root, edit):
    path = root / edit['path']
    if not path.exists():
        return 'missing'
    try:
        text = path.read_bytes().decode(edit.get('encoding', 'utf-8'))
    except UnicodeDecodeError:
        return 'mismatch'
    if edit['replacement'] in text:
        return 'patched'
    if re.search(edit['pattern'], text):
        return 'ready'
    return 'mismatch'


def verify(game, game_root):
    manifest = load_manifest(game)
    root = Path(game_root).expanduser().resolve()
    validate_root(manifest, root)

    print(f'Oyun: {manifest["display_name"]}')
    print(f'Klasör: {root}\n')

    problems = 0
    for item in manifest['patches']:
        state = patch_state(root, item)
        label = {'ready': 'HAZIR', 'patched': 'YAMALI', 'mismatch': 'UYUŞMUYOR'}[state]
        print(f'[{label}] {item["target"]}')
        if state == 'mismatch':
            problems += 1

    for edit in manifest.get('text_edits', []):
        state = text_edit_state(root, edit)
        label = {'ready': 'HAZIR', 'patched': 'YAMALI', 'missing': 'EKSİK', 'mismatch': 'UYUŞMUYOR'}[state]
        print(f'[{label}] {edit["path"]}')
        if state in {'missing', 'mismatch'}:
            problems += 1

    if problems:
        print(f'\nKontrol tamamlandı: {problems} uyumsuz/eksik öğe bulundu. Kurulum yapmayın.')
        raise SystemExit(1)

    print('\nKontrol başarılı. Bu klasör mevcut yama manifestiyle uyumlu.')


def apply_delta(root, game, item):
    source = root / item['source']
    target = root / item['target']

    if target.exists() and sha_file(target) == item['target_sha256']:
        print(f'[OK] Zaten yamalı: {item["target"]}')
        return
    if not source.exists():
        raise RuntimeError(f'Kaynak dosya bulunamadı: {item["source"]}')

    actual = sha_file(source)
    if actual != item['source_sha256']:
        raise RuntimeError(
            f'Sürüm uyuşmuyor: {item["source"]}\n'
            f'Beklenen: {item["source_sha256"]}\n'
            f'Bulunan:  {actual}'
        )

    backup(root, item['target'])
    patch_path = ROOT / 'games' / game / item['patch']
    with gzip.open(patch_path, 'rb') as f:
        obj = json.loads(f.read().decode('utf-8'))

    base = source.read_bytes()
    out = bytearray()
    for op in obj['operations']:
        if op['op'] == 'copy':
            out.extend(base[op['start']:op['start'] + op['length']])
        elif op['op'] == 'data':
            out.extend(base64.b64decode(op['data']))
        else:
            raise RuntimeError('Bilinmeyen patch işlemi')

    out = bytes(out)
    if hashlib.sha256(out).hexdigest() != item['target_sha256']:
        raise RuntimeError(f'Patch doğrulaması başarısız: {item["target"]}')

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(out)
    print(f'[YAMA] {item["target"]}')


def apply_text_edit(root, edit):
    path = root / edit['path']
    if not path.exists():
        raise RuntimeError(f'Dosya bulunamadı: {edit["path"]}')

    raw = path.read_bytes()
    enc = edit.get('encoding', 'utf-8')
    text = raw.decode(enc)

    if edit['replacement'] in text:
        print(f'[OK] Metin ayarı zaten uygulanmış: {edit["path"]}')
        return

    new, count = re.subn(edit['pattern'], edit['replacement'], text, count=1)
    if count == 0:
        raise RuntimeError(f'Beklenen ayar bulunamadı: {edit["path"]}')

    backup(root, edit['path'])
    path.write_bytes(new.encode(enc))
    print(f'[AYAR] {edit["path"]}')


def install(game, game_root):
    manifest = load_manifest(game)
    root = Path(game_root).expanduser().resolve()
    validate_root(manifest, root)

    try:
        for patch in manifest['patches']:
            apply_delta(root, game, patch)
        for edit in manifest.get('text_edits', []):
            apply_text_edit(root, edit)
    except Exception as exc:
        print(f'\nHATA: {exc}', file=sys.stderr)
        print('Mevcut yedekler korunuyor. `restore` komutuyla geri dönebilirsiniz.', file=sys.stderr)
        raise SystemExit(1)

    print('\nTürkçe yama başarıyla uygulandı.')


def restore(game, game_root):
    root = Path(game_root).expanduser().resolve()
    backup_root = root / BACKUP_DIR
    if not backup_root.exists():
        raise SystemExit('Yedek klasörü bulunamadı.')

    files = [p for p in backup_root.rglob('*') if p.is_file()]
    for src in files:
        rel = src.relative_to(backup_root)
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f'[GERİ] {rel}')

    manifest = load_manifest(game)
    backed = {str(p.relative_to(backup_root)).replace('\\', '/') for p in files}
    for patch in manifest['patches']:
        if patch['source'] != patch['target'] and patch['target'] not in backed:
            target = root / patch['target']
            if target.exists():
                target.unlink()
                print(f'[SİL] {patch["target"]}')
                parent = target.parent
                while parent != root and parent.exists() and not any(parent.iterdir()):
                    parent.rmdir()
                    parent = parent.parent

    # Restore tamamlandıktan sonra eski yedekleri temizle. Böylece sonraki
    # kurulum güncel orijinal dosyaları yeniden yedekler.
    shutil.rmtree(backup_root)
    print('\nOrijinal yedekler geri yüklendi ve yedek klasörü temizlendi.')


def main():
    ids = game_ids()
    parser = argparse.ArgumentParser(description='Oyun Türkçeleştirme Yamaları')
    sub = parser.add_subparsers(dest='cmd', required=True)

    for cmd in ('verify', 'install', 'restore'):
        p = sub.add_parser(cmd)
        p.add_argument('game', choices=ids)
        p.add_argument('game_root')

    args = parser.parse_args()
    actions = {'verify': verify, 'install': install, 'restore': restore}
    actions[args.cmd](args.game, args.game_root)


if __name__ == '__main__':
    main()
