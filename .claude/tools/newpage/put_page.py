"""מכניס דף חדש לכל קבצי המקור מתוך .claude/tools/newpage/<ref>.py (התבנית: 10b.py).
שימוש: python3 .claude/tools/newpage/put_page.py 10b   ואז: rashi/merge.py, words/add.py, psuk/build.py, geo/put.py, build.py, page_check.js
הדף החדש נכנס אחרי PREV (הדף הקודם) בכל מקום."""
import json, sys, os, importlib.util
ref = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '..', '..', '..') + '/'
sp = importlib.util.spec_from_file_location('d', os.path.join(HERE, ref + '.py')); D = importlib.util.module_from_spec(sp); sp.loader.exec_module(D)
S, P = D.S, D.PREV
J = lambda x: json.dumps(x, ensure_ascii=False)
q = lambda x: "'" + x.replace('\\', '\\\\').replace("'", "\\'") + "'"
keys = [(si, bi) for si, sc in enumerate(S) for bi in range(len(sc['beats']))]
K = lambda si, bi: f'{ref}:{si}:{bi}'
def once(s, old, new):
    assert s.count(old) == 1, (old[:70], s.count(old)); return s.replace(old, new)
def after_last_key(s, const, prefix, text):   # אחרי השורה האחרונה של הדף הקודם בתוך הקבוע
    i = s.index(const); end = s.index('\n};', i); j = s.rindex(f"\n'{prefix}:", i, end) + 1; e = s.index('\n', j)
    if not s[j:e].rstrip().endswith(','): s = s[:e] + ',' + s[e:]; e += 1
    return s[:e + 1] + text + s[e + 1:]

src = open(R + '.claude/src/taanit.src.html', encoding='utf-8').read()
assert f"amudim['{ref}'].scenes" not in src, 'כבר קיים'
# --- קטעים, תרגום, רש״י (מסוכם מתוך rashi/<ref>.py), תוספות
rp = os.path.join(HERE, '..', 'rashi', ref + '.py')
RS = {}
if os.path.exists(rp):
    sp2 = importlib.util.spec_from_file_location('r', rp); rm = importlib.util.module_from_spec(sp2); sp2.loader.exec_module(rm); RS = rm.R
out = [f"\namudim['{ref}'].translation = ["]
for t in D.TRANS:
    out.append(f"  {{ type: 'section', title: {q(t[1])} }}," if t[0] == 'section' else f"  {{ type: 'quote', aramaic: {q(t[1])},\n    translation: {q(t[2])} }},")
out += ['];\n', f"amudim['{ref}'].rashi = ["] + [f"  {{ dh: {q(e[0])}, content: {q('<p>' + e[1] + '</p>')} }}," for k in RS for e in RS[k]] + ['];\n']
out += [f"amudim['{ref}'].tosafot = ["] + [f"  {{ dh: {q(t[1])}, content: {q('<p>' + t[2] + '</p>')} }}," for t in D.TOS] + ['];\n', f"amudim['{ref}'].scenes = ["]
for sc in S:
    bl = ',\n'.join(f"      [{q(b[0])}, {q(b[1])}, {q(b[2])}]" for b in sc['beats'])
    out.append(f"  {{ tag: {q(sc['tag'])}, title: {q(sc['title'])},\n    beats: [\n{bl}\n    ],\n    viz: {sc['viz']},\n    bottom: {q(sc['bottom'])} }},\n")
out.append("  { tag: 'חזרה', title: 'שאלות <span class=\"accent\">לחזרה</span>', beats: [],\n    quiz: [\n" + ',\n'.join(f"      [{q(a)}, {q(b)}]" for a, b in D.QUIZ) + "\n    ] }\n];\n")
i = src.index(f"amudim['{P}'].scenes = ["); j = src.index('\n];\n', i) + 4
src = src[:j] + '\n'.join(out) + src[j:]
# --- שם הדף
i = src.index('const AMUD_NAME = {'); e = src.index('};', i); src = src[:e].rstrip() + f", '{ref}': '{D.NAME}' " + src[e:]
# --- ED_LINES
assert sum(l.count('‖') for l in D.NARROW + D.WIDE) == len(keys) - 1, (sum(l.count('‖') for l in D.NARROW + D.WIDE), len(keys) - 1)
ed = f"  '{ref}': {{ side: 'tos', tos: [\n" + ''.join(f"    [{q(a)}, {q(b)}, {q(c)}],\n" for a, b, c in D.TOS) + "  ], narrow: [\n" + \
     ''.join(f"    {q(l)},\n" for l in D.NARROW) + "  ], wide: [\n" + ''.join(f"    {q(l)},\n" for l in D.WIDE) + "  ] },\n"
src = once(src, f"  '{P}': {{ side: 'tos', tos: [", ed + f"  '{P}': {{ side: 'tos', tos: [")
# --- WBW / PUNCT / TAKHLES
for const, col in (('const WBW = {', 4), ('const PUNCT = {', 3), ('const TAKHLES = {', 5)):
    src = after_last_key(src, const, P, ''.join(f"{q(K(si, bi))}: {q(S[si]['beats'][bi][col])},\n" for si, bi in keys))
# --- BEAT_LOC + DAF_SRC (דף מהדורה: תיבה כלשהי לכל קטע, אחרת אין סימון בתצוגה הרגילה)
for const, val in (('const BEAT_LOC = {', {str(si): [[0, 0, 0, 1]] * len(sc['beats']) for si, sc in enumerate(S)}),
                   ('const DAF_SRC = {', {str(si): [30.0, 10.0, 40.0, 8.0] for si in range(len(S))})):
    i = src.index(const); e = src.index('\n', i); assert src[i:e].endswith('};')
    src = src[:e - 2] + ', ' + J(ref) + ': ' + json.dumps(val) + '};' + src[e:]
# --- זה מול זה
if getattr(D, 'MISHNA', None):
    i = src.index('const MISHNA = {'); e = src.index('\n', i) + 1
    src = src[:e] + ''.join(f"  {k}: {v},\n" for k, v in D.MISHNA.items()) + src[e:]
    name, val, si, tags = D.PAIR
    i = src.index('const PAIRS = {'); e = src.index('\n', i) + 1; src = src[:e] + f"  {name}: {val},\n" + src[e:]
    i = src.index('for (const [ref, i, cfg] of ['); e = src.index('\n', i) + 1
    src = src[:e] + f"  ['{ref}', {si}, {{ pair: '{name}', pairOpen: true, pairTags: {J(tags)} }}],\n" + src[e:]
open(R + '.claude/src/taanit.src.html', 'w', encoding='utf-8').write(src)
# --- CONTEXT
c = open(R + '.claude/src/context-data.js', encoding='utf-8').read()
c = after_last_key(c, 'const CONTEXT = {', P, ''.join(f"{q(K(si, bi))}: {q(S[si]['beats'][bi][6])},\n" for si, bi in keys))
open(R + '.claude/src/context-data.js', 'w', encoding='utf-8').write(c)
# --- עץ
RM = {'s': 'm', 'n': 'n', 'k': 'k', 'q': 'q', 'a': 'a', 'x': 'x'}; order = []
def node(k, ch, d):
    order.append(k); si, bi = map(int, k.split(':')); b = S[si]['beats'][bi]; t, e = D.NODE[k]
    r = 'c' if 'מסקנה' in b[1] else RM[b[0]]
    s = '  ' * d + f"{{ r: '{r}', w: {q(b[1])}, t: {q(t)}, e: {q(e)}, s: {si}"
    if ch: s += ', k: [\n' + ',\n'.join(node(c2, cc, d + 1) for c2, cc in ch) + ' ]'
    return s + ' }'
roots = ',\n'.join(node(k, ch, 1) for k, ch in D.TREE_SHAPE)
assert order == [f'{si}:{bi}' for si, bi in keys], 'סדר העץ חייב להיות סדר השלבים'
assert len(D.TOP) == len(D.TREE_SHAPE) and len(D.SN) == len(S) + 1
t = open(R + '.claude/src/tree-data.js', encoding='utf-8').read()
t = once(t, f"'{P}': {{ title:", f"'{ref}': {{ title: {q(D.NAME)}, sum: {q(D.TITLE_SUM)},\n  roots: [\n{roots}\n  ] }},\n'{P}': {{ title:")
i = t.index('const SECTION_NAMES = {'); e = t.index('\n', i) + 1; t = t[:e] + f"  '{ref}': {J(D.SN)},\n" + t[e:]
i = t.index('const SUGYA_TOPIC = {'); e = t.index('\n', i) + 1; t = t[:e] + f"'{ref}': {J(D.TOP)},\n" + t[e:]
i = t.index('const TREE_CX = {'); e = t.index('\n', i) + 1; t = t[:e] + f"'{ref}': [\n  " + ', '.join(q(f'{ref}:{k}') for k in order) + "\n],\n" + t[e:]
open(R + '.claude/src/tree-data.js', 'w', encoding='utf-8').write(t)
# --- אנשים
pp = open(R + '.claude/src/people-data.js', encoding='utf-8').read()
i = pp.index('const PEOPLE = {'); e = pp.index('\n', i) + 1; pp = pp[:e] + D.PEOPLE + pp[e:]
open(R + '.claude/src/people-data.js', 'w', encoding='utf-8').write(pp)
# --- EDITION, AM, AMN
L = open(R + 'loader.js', encoding='utf-8').read(); L = once(L, f"'{P}']);", f"'{P}', '{ref}']);"); open(R + 'loader.js', 'w', encoding='utf-8').write(L)
for f, nm in (('index.html', 'AM'), ('words.html', 'AMN')):
    h = open(R + f, encoding='utf-8').read(); i = h.index(f'const {nm} = {{'); e = h.index('}', i)
    h = h[:e].rstrip() + f", '{ref}': '{D.NAME}' " + h[e:]; open(R + f, 'w', encoding='utf-8').write(h)
print('ok', ref, len(keys), 'שלבים')
