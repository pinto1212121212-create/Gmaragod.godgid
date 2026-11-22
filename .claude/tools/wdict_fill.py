"""משלים את WDICT (המילון של ״מילה במילה״ ושל לימוד המילים) מתוך WBW של דף: כל מילה שאין לה ערך מקבלת את התרגום שלה מ־WBW.
שימוש: python3 .claude/tools/wdict_fill.py 10b   (ואז build.py)"""
import sys, re, json, os
ref = sys.argv[1]; P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'taanit.src.html')
s = open(P, encoding='utf-8').read()
i = s.index('const WDICT = {'); e = s.index('};', i) + 1; W = json.loads(s[i + len('const WDICT = '):e])
j = s.index('const WBW = {'); k = s.index('\n};', j); n = 0
for m in re.finditer(r"^'%s:\d+:\d+': '(.*)',?$" % re.escape(ref), s[j:k], re.M):
    for part in m.group(1).replace("\\'", "'").split(' | '):
        if '=' not in part: continue
        w, g = part.split('=', 1); w, g = w.strip(), g.strip()
        if not w or ' ' in w or w in W or g == w: continue
        W[w] = g; n += 1
W = dict(sorted(W.items()))
s = s[:i] + 'const WDICT = ' + json.dumps(W, ensure_ascii=False, separators=(',', ':')) + s[e:]
open(P, 'w', encoding='utf-8').write(s); print(ref, 'נוספו', n, 'מילים ל־WDICT (סה״כ', len(W), ')')
