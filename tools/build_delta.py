#!/usr/bin/env python3
"""Yeni oyunlar için iki klasörden delta üretmeye yardımcı olan geliştirici aracı.
Tam oyun dosyalarını repoya kopyalamaz; yalnızca seçtiğiniz kaynak/hedef dosya için delta üretir.
"""
from pathlib import Path
import argparse, hashlib, gzip, json, base64, difflib

def sha(b): return hashlib.sha256(b).hexdigest()
def ops(base,target):
    if len(base)==len(target):
        diff=[]; s=p=None
        for i,(a,b) in enumerate(zip(base,target)):
            if a!=b:
                if s is None:s=p=i
                elif i-p<=64:p=i
                else:diff.append((s,p));s=p=i
        if s is not None:diff.append((s,p))
        out=[]; c=0
        for s,e in diff:
            if s>c:out.append({'op':'copy','start':c,'length':s-c})
            out.append({'op':'data','data':base64.b64encode(target[s:e+1]).decode()});c=e+1
        if c<len(base):out.append({'op':'copy','start':c,'length':len(base)-c})
        return out
    m=min(len(base),len(target)); pre=0
    while pre<m and base[pre]==target[pre]: pre+=1
    suf=0
    while suf<(m-pre) and base[-1-suf]==target[-1-suf]: suf+=1
    out=[]
    if pre:out.append({'op':'copy','start':0,'length':pre})
    end=len(target)-suf if suf else len(target)
    if end>pre:out.append({'op':'data','data':base64.b64encode(target[pre:end]).decode()})
    if suf:out.append({'op':'copy','start':len(base)-suf,'length':suf})
    return out

def main():
    a=argparse.ArgumentParser();a.add_argument('source');a.add_argument('target');a.add_argument('output');a.add_argument('--source-rel');a.add_argument('--target-rel');x=a.parse_args()
    sp,tp=Path(x.source),Path(x.target);b,t=sp.read_bytes(),tp.read_bytes()
    obj={'format':'turkce-yama-delta-v1','source':x.source_rel or sp.name,'target':x.target_rel or tp.name,'source_sha256':sha(b),'target_sha256':sha(t),'source_size':len(b),'target_size':len(t),'operations':ops(b,t)}
    with gzip.open(x.output,'wb',9) as f:f.write(json.dumps(obj,separators=(',',':')).encode())
    print('Yazıldı:',x.output)
if __name__=='__main__':main()
