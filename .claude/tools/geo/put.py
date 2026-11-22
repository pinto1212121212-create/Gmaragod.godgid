"""מכניס/מחליף ED_GEO[ref] (רש״י ותוספות שורה־שורה כמו בדף) מקובץ .claude/tools/geo/<ref>.py.
בקובץ: PAGE=(X,Y,W,H); G=[(x0,x1,y_center,p,'narrow'|'wide'|'full'),...];
BLOCKS=[('t'|'r', x0, x1, y_center, p, [שורות], k?)...]; DJ={'r':[...],'t':[...]}  (שלב לכל דיבור {…} לפי הסדר)
התחביר בשורות: {…} דיבור המתחיל, *מילה* אות גדולה, ~ שורה באמצע, < סוף פסקה (צמודה להתחלה), >N הזחה.
שימוש: python3 .claude/tools/geo/put.py 9b   (ואז build.py)"""
import sys, os, importlib.util, re
ref = sys.argv[1]; here = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location('g', os.path.join(here, ref + '.py')); g = importlib.util.module_from_spec(sp); sp.loader.exec_module(g)
q = lambda x: "'" + x.replace("'", "\\'") + "'"
X, Y, W, H = g.PAGE
for c in ('r', 't'):
    n = sum(l.count('{') for b in g.BLOCKS if b[0] == c for l in b[5])
    assert n == len(g.DJ.get(c, [])), (c, n, len(g.DJ.get(c, [])))
rows = [f"    {{ c: 'g', x: [{a}, {b}], y: {y - p / 2:.2f}, p: {p}, from: '{f}' }}" for a, b, y, p, f in g.G]
for blk in g.BLOCKS:
    c, a, b, y, p, L = blk[:6]; k = ', k: 1' if len(blk) > 6 and blk[6] else ''
    rows.append(f"    {{ c: '{c}', x: [{a}, {b}], y: {y - p / 2:.2f}, p: {p}{k}, L: [\n" + ',\n'.join('      ' + q(l) for l in L) + '] }')
dj = ', '.join(f"{c}: [{', '.join(q(x) for x in v)}]" for c, v in g.DJ.items())
E = f"  '{ref}': {{ W: {W}, X: {X}, Y: {Y}, H: {H}, dj: {{ {dj} }}, B: [\n" + ',\n'.join(rows) + ' ] },\n'
P = os.path.join(here, '..', '..', 'src', 'taanit.src.html'); s = open(P, encoding='utf-8').read()
gi = s.index('const ED_GEO = {'); body0 = s.index('\n', gi) + 1
m = re.compile(r"^  '%s': \{ W:" % ref, re.M).search(s, gi)
if m:   # מחליפים: עד הבלוק הבא ברמה העליונה
    nx = re.compile(r"^  '\d+[ab]': \{|^\};", re.M).search(s, m.end()); s = s[:m.start()] + E + s[nx.start():]
else: s = s[:body0] + E + s[body0:]
open(P, 'w', encoding='utf-8').write(s); print(ref, 'ED_GEO:', len(rows), 'בלוקים')
