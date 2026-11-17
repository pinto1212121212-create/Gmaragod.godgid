#!/usr/bin/env python3
"""📖 ״הפסוק במקומו״: בונה את .claude/src/psuk-data.js
  1) refs.js מוצא בכל שלב את הפסוקים שבהפניות (״(הושע ו, ה)״ ב־PUNCT/WBW)
  2) data.py: V = הסבר לכל פרק/פסוק (מה קורה שם, מי אומר), MAN = שלבים בלי הפניה
  python3 .claude/tools/psuk/build.py   ← ואחר כך python3 .claude/tools/build.py
דף חדש: להוסיף ל־V כל פרק חדש שמופיע (הכלי מדפיס ״missing״), ול־MAN שלבים עם פסוק בלי הפניה."""
import json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(H, '..', '..', '..'))
subprocess.run(['node', os.path.join(H, 'refs.js')], check=True)
sys.path.insert(0, H); from data import V, MAN
R = json.load(open(os.path.join(H, 'refmap.json')))
chap = lambda i: i.split(',')[0].strip()
OF, miss = {}, set()
for k in sorted(set(R) | set(MAN)):
    ids = list(R.get(k, [])) + [m for m in MAN.get(k, []) if not any(chap(x) == m for x in R.get(k, []))]
    out = []
    for i in ids:
        key = i if i in V else chap(i) if chap(i) in V else None
        if not key: miss.add(i); continue
        if not any(o[1] == key for o in out): out.append([i, key])
    if out: OF[k] = out
print('שלבים עם פסוק:', len(OF), '· חסר הסבר ל:', sorted(miss) or 'אין')
js = "// ✳️ נוצר ע״י .claude/tools/psuk/build.py — עורכים את data.py.\n// 📖 PSUK[key] = [מי/איפה, מה קורה שם];  PSUK_OF['ref:s:b'] = [[הפניה, key], ...]\n"
js += "const PSUK = " + json.dumps({k: list(v) for k, v in V.items()}, ensure_ascii=False, indent=0) + ";\nconst PSUK_OF = " + json.dumps(OF, ensure_ascii=False) + ";\n"
open(os.path.join(ROOT, '.claude', 'src', 'psuk-data.js'), 'w', encoding='utf-8').write(js)
