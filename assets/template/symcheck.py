#!/usr/bin/env python3
"""符号登记表检查（lacia-symbols 配套）。只报告，不修改任何文件。

用法：python3 symcheck.py [--registry symbols.tex] [--ignore symcheck-ignore.txt]
                           [--min N] [--strict] 正文.tex 或目录 ...

报告四类问题：
  A 裸写：已登记、带宏的符号在正文中被直接写出（应改用宏，否则没有旁注）
  B 未登记：正文中反复出现、看起来像记号的写法，但登记表里没有
  C 歧义：登记表用 \\LaciaSymWatch 标记的记号在正文中被裸写，需要人工判断该用哪个宏
  D 未使用：登记了但正文从未用到
--strict 时 A、C 非空则返回码为 1（可接到 make 里阻止构建）。
"""
import argparse, os, re, sys
from collections import Counter, defaultdict

def args_after(s, i, n):
    """从 s[i] 起读 n 个 {...} 参数（允许空白），返回 (参数列表, 结束位置)。"""
    out = []
    for _ in range(n):
        while i < len(s) and s[i] in ' \t\n': i += 1
        if i >= len(s) or s[i] != '{': return None, i
        depth, j = 0, i
        while j < len(s):
            c = s[j]
            if c == '\\': j += 2; continue
            if c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0: break
            j += 1
        out.append(s[i + 1:j]); i = j + 1
    return out, i

def strip_comments(t):
    return re.sub(r'(?<!\\)%.*', '', t)

def norm(t):
    return re.sub(r'\s+', '', t)

def load_registry(path):
    t = strip_comments(open(path, encoding='utf-8').read())
    macros, entries, watch = [], [], []
    for m in re.finditer(r'\\LaciaNewSym\b', t):
        a, _ = args_after(t, m.end(), 7)
        if a: macros.append(dict(cs=a[0].strip(), key=a[1], group=a[2], body=a[3],
                                 show=a[4] or a[3], note=a[5]))
    for m in re.finditer(r'\\LaciaSymEntry\b', t):
        a, _ = args_after(t, m.end(), 4)
        if a: entries.append(dict(key=a[0], group=a[1], show=a[2]))
    for m in re.finditer(r'\\LaciaSymWatch\b', t):
        a, _ = args_after(t, m.end(), 2)
        if a: watch.append(dict(raw=a[0].strip(), hint=a[1]))
    return macros, entries, watch

def tex_files(paths, exclude):
    for p in paths:
        if os.path.isdir(p):
            for root, _, fs in os.walk(p):
                for f in sorted(fs):
                    if f.endswith('.tex'):
                        q = os.path.join(root, f)
                        if os.path.abspath(q) not in exclude: yield q
        elif os.path.abspath(p) not in exclude:
            yield p

# 看起来像“记号”的写法：带修饰的箭头/关系、成对的 \mathrm{NAME}( 或 [
CANDIDATE = [
    (r'\\overset\{[^{}]*\}\{\\[A-Za-z]+\}', '带上标的符号'),
    (r'\\underset\{[^{}]*\}\{\\[A-Za-z]+\}', '带下标的符号'),
    (r'\\mathrm\{[A-Za-z][A-Za-z-]*\}\s*[\[(]', '函数/集合名'),
    (r'\\operatorname\{[^{}]*\}', '函数名'),
]

def similar(g, k):
    """\\overset{(3)}{\\Rightarrow} 与登记的 \\overset{(k)}{\\Rightarrow} 视为同一记号：把单个数字/字母参数泛化后比较。"""
    gen = lambda x: re.sub(r'\{\(?[0-9A-Za-z]\)?\}', '{#}', x)
    return gen(g) in gen(k)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='+')
    ap.add_argument('--registry', default='symbols.tex')
    ap.add_argument('--ignore', default='symcheck-ignore.txt')
    ap.add_argument('--min', type=int, default=2, help='B 类最少出现次数')
    ap.add_argument('--strict', action='store_true')
    o = ap.parse_args()

    macros, entries, watch = load_registry(o.registry)
    ignore, ignore_re = set(), []
    if os.path.exists(o.ignore):
        for l in open(o.ignore, encoding='utf-8'):
            l = l.split('#', 1)[0].strip()
            if l.startswith('re:'): ignore_re.append(re.compile(l[3:].strip()))
            elif l: ignore.add(norm(l))
    exclude = {os.path.abspath(o.registry)}
    files = list(tex_files(o.paths, exclude))
    texts = {f: strip_comments(open(f, encoding='utf-8').read()) for f in files}

    def where(pat_re):
        hits = []
        for f, t in texts.items():
            for m in pat_re.finditer(t):
                hits.append((f, t.count('\n', 0, m.start()) + 1, m.group(0)))
        return hits

    def loc(h, k=3):
        s = ', '.join(f'{os.path.relpath(f)}:{n}' for f, n, _ in h[:k])
        return s + (f' 等 {len(h)} 处' if len(h) > k else '')

    # 已登记的展示形式（规范化后）用于排除 B 类
    known = [norm(m['body']) for m in macros] + [norm(m['show']) for m in macros] + [norm(e['show']) for e in entries]

    # A 裸写
    A = []
    watched = {norm(w['raw']) for w in watch}
    for m in macros:
        body = norm(m['body'])
        if body in watched: continue            # 一符多义的交给 C 类
        if len(body) < 4 or not body.startswith('\\'): continue
        pat = re.compile(r'\s*'.join(re.escape(c) for c in body) + r'(?![A-Za-z])')
        h = where(pat)
        if h: A.append((m['cs'], m['body'], h))
    # C 歧义
    C = []
    for w in watch:
        # 跳过 \overset{..}{\Rightarrow} 这类已带修饰、含义明确的写法
        pat = re.compile(r'(?<!\}\{)' + re.escape(w['raw']) + r'(?![A-Za-z])')
        h = where(pat)
        if h: C.append((w, h))
    # B 未登记
    cand = defaultdict(list)
    for pat, kind in CANDIDATE:
        for f, n, g in where(re.compile(pat)):
            g2 = norm(re.sub(r'\s*[\[(]$', '', g))
            if g2 in ignore or any(r.fullmatch(g2) for r in ignore_re): continue
            if any(g2 in k for k in known) or any(similar(g2, k) for k in known): continue
            cand[(kind, g2)].append((f, n, g))
    B = sorted(((k, h) for k, h in cand.items() if len(h) >= o.min), key=lambda x: -len(x[1]))
    # D 未使用
    D = []
    alltext = '\n'.join(texts.values())
    for m in macros:
        if not re.search(re.escape(m['cs']) + r'(?![A-Za-z])', alltext):
            D.append(f"{m['cs']}（{m['key']}）")
    # 只进符号表的条目：取展示形式里有辨识度的部分去匹配；取不到就不判，单独计数
    SIG = re.compile(r'\\(?:mathrm|mathit|operatorname)\{[A-Za-z-]+\}|\\text\{-?[A-Za-z-]+\}|\\xrightarrow|\\overset\{[^{}]+\}\{\\[A-Za-z]+\}')
    flat = norm(alltext); unchecked = 0
    for e in entries:
        sig = SIG.search(norm(e['show']))
        if not sig: unchecked += 1; continue
        if sig.group(0) not in flat and not similar(sig.group(0), flat):
            D.append(f"{e['show']}（{e['key']}，只进符号表）")

    print(f'登记：{len(macros)} 个宏（其中 {sum(1 for m in macros if m["note"])} 个带旁注），'
          f'{len(entries)} 条只进符号表；扫描 {len(files)} 个文件\n')
    print(f'A 裸写已登记符号：{len(A)}')
    for cs, body, h in A: print(f'  {body}  → 改用 {cs}    {loc(h)}')
    print(f'\nB 疑似记号但未登记（出现 ≥{o.min} 次）：{len(B)}')
    for (kind, g), h in B: print(f'  [{kind}] {g}  ×{len(h)}    {loc(h, 2)}')
    print(f'\nC 需要人工判断的裸写：{len(C)}')
    for w, h in C: print(f'  {w["raw"]} ×{len(h)}：{w["hint"]}    {loc(h, 2)}')
    print(f'\nD 登记但未使用：{len(D)}（另有 {unchecked} 条只进符号表的条目无法自动判断）')
    for d in D: print(f'  {d}')
    if o.strict and (A or C):
        sys.exit(1)

if __name__ == '__main__':
    main()
