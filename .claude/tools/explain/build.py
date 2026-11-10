# 🖼️ בונה את ההסברים המאוירים: python3 .claude/tools/explain/build.py [שם ...]
# spec.py: E['שם'] = page(...) (רכיבים ב־exlib.py). raw/*.html: איורים שנכתבו ביד (רבה, רב יוסף).
# פלט: explain/<שם>.jpg (רוחב 1200). אחר כך מוסיפים את השם ל־explain-data.js (EXPLAIN + EXPLAIN_TITLE).
import os, sys, glob, subprocess, json
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(H, '..', '..', '..'))
sys.path.insert(0, H)
from spec import E
OUT = os.path.join(ROOT, '.claude', 'out', 'explain'); os.makedirs(OUT, exist_ok=True)
pages = dict(E)
for f in glob.glob(os.path.join(H, 'raw', '*.html')): pages[os.path.basename(f)[:-5]] = open(f, encoding='utf-8').read()
names = sys.argv[1:] or list(pages)
for n in names: open(os.path.join(OUT, n + '.html'), 'w', encoding='utf-8').write(pages[n])
js = """const { chromium } = require('playwright'); const [D, ...names] = process.argv.slice(2);
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 900, height: 1000 }, deviceScaleFactor: 2 });
  for (const n of names) { await p.goto('file://' + D + '/' + n + '.html'); await p.waitForTimeout(300); await p.screenshot({ path: D + '/' + n + '.png', fullPage: true }); }
  await b.close(); })();"""
open(os.path.join(OUT, 'shot.js'), 'w').write(js)
subprocess.run(['node', os.path.join(OUT, 'shot.js'), OUT, *names], check=True, cwd=ROOT)
for n in names:
    im = Image.open(os.path.join(OUT, n + '.png')).convert('RGB'); im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
    im.save(os.path.join(ROOT, 'explain', n + '.jpg'), quality=84, optimize=True); print('explain/' + n + '.jpg', im.size)
