#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
from dataclasses import dataclass
from pathlib import Path

MAGIC = b"FFAS"
VERSION = 1
HASH_SEED = 0x53414646  # "FFAS" little-endian
MASK32 = 0xFFFFFFFF

_MD5_S = (
    [7, 12, 17, 22] * 4
    + [5, 9, 14, 20] * 4
    + [4, 11, 16, 23] * 4
    + [6, 10, 15, 21] * 4
)
_MD5_K = [
    int(abs(math.sin(i + 1)) * (1 << 32)) & MASK32
    for i in range(64)
]


@dataclass
class SafEntry:
    path: str
    offset: int
    size: int
    content_hash: bytes


@dataclass
class SafArchive:
    header_version: int
    index_offset: int
    index_version: int
    toc_hash: bytes
    entries: list[SafEntry]


def _rol32(value: int, count: int) -> int:
    return ((value << count) | (value >> (32 - count))) & MASK32


def sprout_hash(data: bytes, seed: int = HASH_SEED) -> bytes:
    """
    Sprout Games FFAS hash.

    It is MD5 with a custom initial state derived from the 32-bit seed.
    With seed=0 this is ordinary MD5.
    """
    a0 = (0x67452301 + seed * 0x0B) & MASK32
    b0 = (0xEFCDAB89 + seed * 0x47) & MASK32
    c0 = (0x98BADCFE + seed * 0x25) & MASK32
    d0 = (0x10325476 + seed * 0x61) & MASK32

    bit_length = (len(data) * 8) & 0xFFFFFFFFFFFFFFFF

    padded = bytearray(data)
    padded.append(0x80)
    while len(padded) % 64 != 56:
        padded.append(0)
    padded += struct.pack("<Q", bit_length)

    A, B, C, D = a0, b0, c0, d0

    for chunk_start in range(0, len(padded), 64):
        words = struct.unpack(
            "<16I", padded[chunk_start:chunk_start + 64]
        )
        a, b, c, d = A, B, C, D

        for i in range(64):
            if i < 16:
                f = (b & c) | ((~b) & d)
                g = i
            elif i < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * i) % 16

            f &= MASK32

            old_d = d
            d = c
            c = b
            b = (
                b
                + _rol32(
                    (a + f + _MD5_K[i] + words[g]) & MASK32,
                    _MD5_S[i],
                )
            ) & MASK32
            a = old_d

        A = (A + a) & MASK32
        B = (B + b) & MASK32
        C = (C + c) & MASK32
        D = (D + d) & MASK32

    return struct.pack("<4I", A, B, C, D)


def _u32(data: bytes, pos: int) -> tuple[int, int]:
    return struct.unpack_from("<I", data, pos)[0], pos + 4


def _u16(data: bytes, pos: int) -> tuple[int, int]:
    return struct.unpack_from("<H", data, pos)[0], pos + 2


def parse_saf(path: Path, verify_hashes: bool = True) -> tuple[SafArchive, bytes]:
    raw = path.read_bytes()

    if len(raw) < 36 or raw[:4] != MAGIC:
        raise ValueError("Geçersiz FFAS/SAF dosyası.")

    header_version = struct.unpack_from("<I", raw, 4)[0]
    index_offset = struct.unpack_from("<I", raw, 8)[0]

    if header_version != VERSION:
        raise ValueError(f"Desteklenmeyen SAF header version: {header_version}")
    if not (12 <= index_offset < len(raw)):
        raise ValueError("Geçersiz SAF index ofseti.")

    pos = index_offset
    index_version, pos = _u32(raw, pos)

    if index_version != VERSION:
        raise ValueError(f"Desteklenmeyen SAF index version: {index_version}")

    toc_hash = raw[pos:pos + 16]
    pos += 16

    file_count, pos = _u32(raw, pos)
    entries: list[SafEntry] = []

    expected_payload_offset = 12

    for _ in range(file_count):
        offset, pos = _u32(raw, pos)
        size, pos = _u32(raw, pos)

        content_hash = raw[pos:pos + 16]
        pos += 16

        name_size, pos = _u16(raw, pos)
        if name_size < 1 or pos + name_size > len(raw):
            raise ValueError("Geçersiz SAF dosya adı.")

        encoded_name = raw[pos:pos + name_size]
        pos += name_size

        if encoded_name[-1:] != b"\x00":
            raise ValueError("SAF dosya adı NUL ile bitmiyor.")

        name_bytes = encoded_name[:-1]
        try:
            name = name_bytes.decode("utf-8")
        except UnicodeDecodeError:
            name = name_bytes.decode("latin-1")

        if offset != expected_payload_offset:
            raise ValueError(
                f"Payload sırası bozuk: {name} "
                f"(beklenen {expected_payload_offset}, bulunan {offset})"
            )
        if offset + size > index_offset:
            raise ValueError(f"Geçersiz payload aralığı: {name}")

        payload = raw[offset:offset + size]

        if verify_hashes:
            calculated = sprout_hash(payload)
            if calculated != content_hash:
                raise ValueError(
                    f"İçerik hash doğrulaması başarısız: {name}\n"
                    f"Arşiv: {content_hash.hex()}\n"
                    f"Hesap:  {calculated.hex()}"
                )

        entries.append(
            SafEntry(
                path=name,
                offset=offset,
                size=size,
                content_hash=content_hash,
            )
        )
        expected_payload_offset = offset + size

    if expected_payload_offset != index_offset:
        raise ValueError("Payload bölümü index başlangıcında bitmiyor.")
    if pos != len(raw):
        raise ValueError(
            f"Index sonunda beklenmeyen {len(raw) - pos} bayt var."
        )

    if verify_hashes:
        # TOC hash covers file_count + every entry record.
        toc_data = raw[index_offset + 20:]
        calculated_toc = sprout_hash(toc_data)
        if calculated_toc != toc_hash:
            raise ValueError(
                "TOC hash doğrulaması başarısız.\n"
                f"Arşiv: {toc_hash.hex()}\n"
                f"Hesap:  {calculated_toc.hex()}"
            )

    return (
        SafArchive(
            header_version=header_version,
            index_offset=index_offset,
            index_version=index_version,
            toc_hash=toc_hash,
            entries=entries,
        ),
        raw,
    )


def unpack_saf(
    saf_path: Path,
    output_dir: Path,
    verify_hashes: bool = True,
) -> None:
    archive, raw = parse_saf(saf_path, verify_hashes=verify_hashes)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest_entries = []

    for index, entry in enumerate(archive.entries):
        target = output_dir / entry.path
        target.parent.mkdir(parents=True, exist_ok=True)

        payload = raw[entry.offset:entry.offset + entry.size]
        target.write_bytes(payload)

        manifest_entries.append(
            {
                "index": index,
                "path": entry.path,
                "original_offset": entry.offset,
                "original_size": entry.size,
                "original_content_hash": entry.content_hash.hex(),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )

    metadata = {
        "format": "FFAS-SAF",
        "header_version": archive.header_version,
        "index_version": archive.index_version,
        "original_index_offset": archive.index_offset,
        "original_toc_hash": archive.toc_hash.hex(),
        "source_filename": saf_path.name,
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "entries": manifest_entries,
    }

    (output_dir / "_saf_manifest.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    label = "Çıkarıldı ve doğrulandı" if verify_hashes else "Çıkarıldı"
    print(f"{label}: {len(archive.entries)} dosya")
    print(f"Hedef: {output_dir}")


def repack_saf(
    input_dir: Path,
    output_path: Path,
    verify_output_hashes: bool = True,
    reuse_unchanged_hashes: bool = True,
) -> None:
    manifest_path = input_dir / "_saf_manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError("_saf_manifest.json bulunamadı.")

    metadata = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries_meta = metadata["entries"]

    payloads: list[bytes] = []
    records = []
    current_offset = 12

    for item in entries_meta:
        rel_path = item["path"]
        source = input_dir / rel_path

        if not source.is_file():
            raise FileNotFoundError(f"Arşiv dosyası eksik: {rel_path}")

        payload = source.read_bytes()
        encoded_name = rel_path.encode("utf-8") + b"\x00"

        if len(encoded_name) > 0xFFFF:
            raise ValueError(f"Dosya adı çok uzun: {rel_path}")

        # Yama kurulumu sırasında orijinal SAF arşivi SHA-256 ile zaten
        # doğrulandığından, değişmemiş iç dosyaların Sprout hashini tekrar
        # Python'da hesaplamak gereksiz derecede pahalıdır. Unpack manifestinde
        # saklanan orijinal hash güvenle yeniden kullanılabilir. Değişen dosyalar
        # için Sprout hash normal şekilde yeniden hesaplanır.
        original_sha = item.get("sha256")
        original_content_hash = item.get("original_content_hash")
        if (
            reuse_unchanged_hashes
            and original_sha
            and original_content_hash
            and hashlib.sha256(payload).hexdigest() == original_sha
        ):
            content_hash = bytes.fromhex(original_content_hash)
        else:
            content_hash = sprout_hash(payload)

        payloads.append(payload)
        records.append(
            {
                "offset": current_offset,
                "size": len(payload),
                "hash": content_hash,
                "name": encoded_name,
            }
        )
        current_offset += len(payload)

    index_offset = current_offset

    toc = bytearray()
    toc += struct.pack("<I", len(records))

    for record in records:
        toc += struct.pack("<I", record["offset"])
        toc += struct.pack("<I", record["size"])
        toc += record["hash"]
        toc += struct.pack("<H", len(record["name"]))
        toc += record["name"]

    toc_hash = sprout_hash(bytes(toc))

    out = bytearray()
    out += MAGIC
    out += struct.pack("<I", int(metadata["header_version"]))
    out += struct.pack("<I", index_offset)

    for payload in payloads:
        out += payload

    out += struct.pack("<I", int(metadata["index_version"]))
    out += toc_hash
    out += toc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(out)

    # CLI kullanımında varsayılan olarak tüm hash katmanlarını doğrulamaya
    # devam ederiz. Patcher ise bilinen hedef SHA-256 ile doğruladığı için
    # pahalı ikinci Sprout-hash turunu kapatabilir.
    parsed, rebuilt_raw = parse_saf(
        output_path,
        verify_hashes=verify_output_hashes,
    )

    label = "Paketlendi ve doğrulandı" if verify_output_hashes else "Paketlendi"
    print(f"{label}: {len(parsed.entries)} dosya")
    print(f"Index ofseti: {parsed.index_offset}")
    print(f"TOC hash: {parsed.toc_hash.hex()}")
    print(f"Çıktı: {output_path}")
    print(f"SHA-256: {hashlib.sha256(rebuilt_raw).hexdigest()}")


def list_saf(saf_path: Path) -> None:
    archive, raw = parse_saf(saf_path, verify_hashes=True)
    print(f"Dosya: {saf_path}")
    print(f"Boyut: {len(raw)}")
    print(f"Index offset: {archive.index_offset}")
    print(f"Dosya sayısı: {len(archive.entries)}")
    print(f"TOC hash: {archive.toc_hash.hex()}")
    print("Hash doğrulaması: BAŞARILI")
    for entry in archive.entries:
        print(
            f"{entry.offset:10} {entry.size:10} "
            f"{entry.content_hash.hex()}  {entry.path}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sprout Games Feeding Frenzy FFAS/SAF aracı"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list")
    p_list.add_argument("saf", type=Path)

    p_unpack = sub.add_parser("unpack")
    p_unpack.add_argument("saf", type=Path)
    p_unpack.add_argument("output", type=Path)

    p_repack = sub.add_parser("repack")
    p_repack.add_argument("input", type=Path)
    p_repack.add_argument("output", type=Path)

    args = parser.parse_args()

    if args.command == "list":
        list_saf(args.saf)
    elif args.command == "unpack":
        unpack_saf(args.saf, args.output)
    else:
        repack_saf(args.input, args.output)


if __name__ == "__main__":
    main()
