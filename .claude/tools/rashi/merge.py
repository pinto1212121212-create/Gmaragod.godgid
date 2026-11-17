"""ממזג רש״י מלא של דף (rashi/<ref>.py: R = {key: [[dh, rashi, plain], ...]}) לתוך .claude/src/rashi-data.js.
מוחק את כל המפתחות הקיימים של הדף ומכניס את החדשים, לפי הסדר. שימוש: python3 .claude/tools/rashi/merge.py 6b"""
import sys, re, json, importlib.util, os
ref = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('m', os.path.join(here, ref + '.py')); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
p = os.path.join(here, '..', '..', 'src', 'rashi-data.js'); s = open(p, encoding='utf-8').read()
body = s[s.index('const RASHI_AT = {') + len('const RASHI_AT = {'): s.rindex('};')]
# מפצלים לבלוקים לפי מפתח
blocks = re.split(r"(?m)^(?=// =====|'\d+[ab]:\d+:\d+': \[)", body)
keep = [b for b in blocks if not b.startswith("'%s:" % ref) and not b.startswith('// ===== %s ' % m.NAME)]
order = lambda k: tuple(int(x) for x in k.split(':')[1:])
new = '// ===== %s ===== (רש״י מלא, נקרא מהצילום)\n' % m.NAME + ''.join(
  "'%s': [\n%s\n],\n" % (k, '\n'.join('  [%s, %s, %s],' % tuple(json.dumps(x, ensure_ascii=False) for x in (e + [''])[:3]) for e in v))
  for k, v in sorted(m.R.items(), key=lambda kv: order(kv[0])))
# מכניסים לפי סדר הדפים
REFS = ['2a','2b','3a','3b','4a','4b','5a','5b','6a','6b','7a','7b','8a','8b','9a','9b']
out, done = [], False
for b in keep:
    mm = re.match(r"'(\d+[ab]):", b) or re.match(r"// ===== (.+?) =====", b)
    NM = {'ב׳ ע״א':'2a','ב׳ ע״ב':'2b','ג׳ ע״א':'3a','ג׳ ע״ב':'3b','ד׳ ע״א':'4a','ד׳ ע״ב':'4b','ה׳ ע״א':'5a','ה׳ ע״ב':'5b','ו׳ ע״א':'6a','ו׳ ע״ב':'6b','ז׳ ע״א':'7a','ז׳ ע״ב':'7b','ח׳ ע״א':'8a','ח׳ ע״ב':'8b','ט׳ ע״א':'9a','ט׳ ע״ב':'9b'}
    r = mm and (mm.group(1) if mm.group(1) in REFS else NM.get(mm.group(1)))
    if not done and r and REFS.index(r) > REFS.index(ref): out.append(new); done = True
    out.append(b)
if not done: out.append(new)
s = s[:s.index('const RASHI_AT = {') + len('const RASHI_AT = {')] + ''.join(out) + s[s.rindex('};'):]
open(p, 'w', encoding='utf-8').write(s)
print(ref, sum(len(v) for v in m.R.values()), 'פירושים ב־', len(m.R), 'שלבים')
