#!/usr/bin/env python3
"""פיצול שלב (כרטיס) אחד לכמה שלבים, כך שבכל שלב יש דבר אחד: שאלה, תשובה, מקור...

שימוש:  python3 .claude/tools/split_beat.py spec.json
spec.json = [ { "key": "4b:8:4", "parts": [ {beat, wbw, punct, takhles, context, span}, ... ] }, ... ]
  beat    = [role, 'מי', 'html']   (כמו בשורה ב־scenes)
  wbw/punct/takhles/context = מחרוזות לשלב החדש
  span    = [מילה_ראשונה, מילה_אחרונה] ל־BEAT_SPAN

מה הכלי עושה:
  * מחליף את השלב בשלבים החדשים ב־amudim[ref].scenes[s].beats
  * מזיז +N-1 את כל המפתחות 'ref:s:j' (j > b) ב־taanit.html, context-data.js, tree-data.js
  * מעדכן BEAT_LOC ו־BEAT_SPAN
  * ב־TREE_CX: ההופעה ה־k של 'ref:s:b' (לפי סדר הצמתים) הופכת לחלק ה־k
אחרי הריצה: daf_tool.py marks, report, check.js.
"""
import json, re, sys

def jq(s):  # מחרוזת JS בגרש בודד
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"

def load_obj(src, name):
    i = src.index(f'const {name} = ') + len(f'const {name} = ')
    j = src.index(';\n', i)
    return i, j, json.loads(src[i:j])

def keyed_line(src, const, key, newlines):
    """מחליף את השורה 'key': ... בתוך האובייקט const בשורות חדשות"""
    start = src.index(f'const {const} = {{')
    m = re.compile(r"^" + re.escape(f"'{key}'") + r": .*$", re.M).search(src, start)
    if not m:
        raise SystemExit(f'לא נמצא {key} ב־{const}')
    return src[:m.start()] + '\n'.join(newlines) + src[m.end():]

def main(spec_path):
    spec = json.load(open(spec_path, encoding='utf-8'))
    T = open('taanit.html', encoding='utf-8').read()
    C = open('context-data.js', encoding='utf-8').read()
    R = open('tree-data.js', encoding='utf-8').read()
    # מבצעים מהסוף להתחלה בתוך אותו קטע, כדי שהמספרים לא יזוזו מתחת לרגליים
    spec.sort(key=lambda x: tuple(int(p) if p.isdigit() else p for p in x['key'].split(':')), reverse=True)
    for item in spec:
        ref, s, b = item['key'].split(':'); s, b = int(s), int(b)
        parts = item['parts']; n = len(parts); add = n - 1
        # 1. הזזת מפתחות j>b (מהגבוה לנמוך)
        def shift(text):
            ks = sorted({int(m) for m in re.findall(rf"'{ref}:{s}:(\d+)'", text)}, reverse=True)
            for j in ks:
                if j > b:
                    text = text.replace(f"'{ref}:{s}:{j}'", f"'{ref}:{s}:{j + add}'")
            return text
        T, C, R = shift(T), shift(C), shift(R)
        new_keys = [f'{ref}:{s}:{b + k}' for k in range(n)]
        # 2. WBW / PUNCT / TAKHLES / CONTEXT
        for const, fld in (('WBW', 'wbw'), ('PUNCT', 'punct'), ('TAKHLES', 'takhles')):
            T = keyed_line(T, const, item['key'], [f"{jq(k)}: {jq(p[fld])}," for k, p in zip(new_keys, parts)])
        C = keyed_line(C, 'CONTEXT', item['key'], [f"{jq(k)}: {jq(p['context'])}," for k, p in zip(new_keys, parts)])
        # 3. שורת השלב ב־scenes
        si = T.index(f"amudim['{ref}'].scenes = [")
        pos = si
        for _ in range(s + 1):
            pos = T.index('beats:', pos + 1)
        rows = list(re.finditer(r"^(\s*)\[('[a-z]'), .*\],?$", T[pos:pos + 20000], re.M))
        row = rows[b]
        ind = row.group(1)
        newrows = [ind + '[' + ', '.join(jq(x) for x in p['beat']) + '],' for p in parts]
        a0, a1 = pos + row.start(), pos + row.end()
        T = T[:a0] + '\n'.join(newrows) + T[a1:]
        # 4. BEAT_LOC / BEAT_SPAN
        i, j, L = load_obj(T, 'BEAT_LOC')
        arr = L[ref][str(s)]; val = arr[b]
        L[ref][str(s)] = arr[:b] + [val if val is not None else [0, 0, 0, 1]] * n + arr[b + 1:]
        T = T[:i] + json.dumps(L, ensure_ascii=False) + T[j:]
        i, j, S = load_obj(T, 'BEAT_SPAN')
        old = S[ref].get(str(s), {}); new = {}
        for k, v in old.items():
            k = int(k)
            if k < b: new[str(k)] = v
            elif k > b: new[str(k + add)] = v
        for k, p in enumerate(parts):
            if p.get('span'): new[str(b + k)] = p['span']
        S[ref][str(s)] = dict(sorted(new.items(), key=lambda x: int(x[0])))
        T = T[:i] + json.dumps(S, ensure_ascii=False) + T[j:]
        # 5. TREE_CX: ההופעה ה־k → החלק ה־k
        ci = R.index('const TREE_CX = {')
        blk = R.index(f"'{ref}': [", ci); blk_end = R.index('\n],', blk)
        seg = R[blk:blk_end]; cnt = [0]
        def rep(m):
            k = min(cnt[0], n - 1); cnt[0] += 1
            return f"'{new_keys[k]}'"
        seg = re.sub(re.escape(f"'{item['key']}'"), rep, seg)
        R = R[:blk] + seg + R[blk_end:]
        print(f"{item['key']} → {', '.join(new_keys)}  (בעץ: {cnt[0]} הופעות)")
    open('taanit.html', 'w', encoding='utf-8').write(T)
    open('context-data.js', 'w', encoding='utf-8').write(C)
    open('tree-data.js', 'w', encoding='utf-8').write(R)

if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    main(sys.argv[1])
