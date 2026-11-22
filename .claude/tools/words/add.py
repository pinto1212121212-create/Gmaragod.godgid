"""מוסיף ״מילה קשה״ לסוף ה־CONTEXT של שלבים. שימוש: python3 .claude/tools/words/add.py <ref>
הנתונים: .claude/tools/words/<ref>.py — W = {'ref:s:b': [('מילה', 'הסבר'), ...]}. מילה שכבר קיימת בשלב — לא מתווספת שוב."""
import sys, re, os, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
ref = sys.argv[1]
spec = importlib.util.spec_from_file_location('w', os.path.join(here, ref + '.py')); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
p = os.path.join(here, '..', '..', 'src', 'context-data.js'); s = open(p, encoding='utf-8').read()
cnt, miss = 0, []
for k, items in m.W.items():
    mm = re.search(r"^'%s': '(.*)',\s*$" % re.escape(k), s, re.M)
    if not mm: miss.append(k); continue
    cur = mm.group(1)
    add = ''.join(f"<br><b>מילה קשה — {t}:</b> {d}" for t, d in items if f"מילה קשה — {t}:" not in cur.replace("\\'", "'"))
    if not add: continue
    s = s[:mm.end(1)] + add.replace("'", "\\'") + s[mm.end(1):]; cnt += 1
open(p, 'w', encoding='utf-8').write(s)
print(ref, 'שלבים שעודכנו:', cnt, '| חסר מפתח:', miss)
