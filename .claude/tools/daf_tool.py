#!/usr/bin/env python3
"""
כלי עבודה לדפי גמרא באתר. הרצה מתיקיית הריפו:  python3 .claude/tools/daf_tool.py <פקודה> ...

פקודות:
  ruler   <img> <x0> <x1> <y0> <y1> <out.png> [scale]   סרגל אדום/כחול על אזור בצילום, לקריאת קואורדינטות
  columns <img> <y0> <y1>                                 מוצא את גבולות טורי הטקסט (הרווחים הלבנים) בשורות y0..y1
  zoom    <img> <x0> <y0> <x1> <y1> <out.png> [scale]     חיתוך מוגדל וחד — לקריאת טקסט קטן (רש״י, תוספות)
  crop    <ref> [i,i,...]                                 חותך את צילומי הקטעים לפי .claude/data, מעדכן DAF_SRC ו־DAF_LINES
  extend  <ref> <i> <up> <down>                           מרחיב צילום קטע בשורות למעלה/למטה, ומזיז את BEAT_SPAN בהתאם
  audit   <ref> [i,i,...]                                 מצייר מספור מילים + ההדגשות של כל שלב → .claude/out/audit-*.png
  slots   <ref> <i>                                       מדפיס כמה מילים בכל שורה של צילום הקטע (לחישוב BEAT_SPAN)
  setspan '<json>'                                        {"4b:3:0":[3,16], ...} — קובע טווח מילים מדויק לשלבים
  marks                                                   מייצר מחדש את daf-marks.js (לעץ הסוגיה) מתוך taanit.html
  report                                                  דוח כיסוי: לכל שלב — יש מיקום? מילה במילה? פיסוק? בתכלס?

מקור הצילומים: .claude/data/sources.json  {"4b": "taanit-img/4b-full.jpg", ...}
(הצילום המלא של כל עמוד נשמר ב־taanit-img/<ref>-full.jpg; צילום חדש — שומרים קודם לשם.)
"""
import sys, os, re, json
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageFont

ROOT = os.getcwd()
DATA = os.path.join(ROOT, '.claude', 'data')
OUT = os.path.join(ROOT, '.claude', 'out')
IMG = os.path.join(ROOT, 'taanit-img')
HTML = os.path.join(ROOT, 'taanit.html')
os.makedirs(OUT, exist_ok=True)

def jload(name, default=None):
    p = os.path.join(DATA, name)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else default
def jsave(name, obj):
    json.dump(obj, open(os.path.join(DATA, name), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def font(sz):
    for f in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()

def html_get(name):
    s = open(HTML, encoding='utf-8').read()
    m = re.search(r'const %s = (\{.*?\});\n' % name, s, flags=re.S)
    return json.loads(m.group(1)) if m else {}
def html_set(name, obj):
    s = open(HTML, encoding='utf-8').read()
    new = 'const %s = %s;\n' % (name, json.dumps(obj, ensure_ascii=False))
    s, n = re.subn(r'const %s = \{.*?\};\n' % name, lambda m: new, s, count=1, flags=re.S)
    if not n: raise SystemExit(f'{name} לא נמצא ב-taanit.html')
    open(HTML, 'w', encoding='utf-8').write(s)
def src_path(ref):
    m = jload('sources.json', {})
    return os.path.join(ROOT, m.get(ref, f'taanit-img/{ref}-full.jpg'))

# ---------- זיהוי שורות ומילים בצילום קטע ----------
def detect_lines(path):
    a = np.asarray(Image.open(path).convert('L')).astype(float); H, W = a.shape; med = np.median(a)
    reg = a[:, int(W * .08):int(W * .92)]; ink = (reg < med - 60).mean(axis=1); sm = np.convolve(ink, np.ones(7) / 7, 'same')
    mins = [0]
    for y in range(10, H - 10):
        w = sm[max(0, y - 13):y + 14]
        if sm[y] == w.min() and sm[y] < np.max(sm) * .45 and y - mins[-1] >= 22: mins.append(y)
    if H - mins[-1] < 14: mins[-1] = H
    else: mins.append(H)
    out = []
    for k in range(len(mins) - 1):
        b0, b1 = mins[k], mins[k + 1]
        if sm[b0:b1].max() <= np.max(sm) * .3: continue
        col = (a[b0:b1] < med - 60).mean(axis=0); cs = np.convolve(col, np.ones(9) / 9, 'same')
        idx = np.where(cs > .04)[0]; xl, xr = (idx[0] / W, idx[-1] / W) if len(idx) else (0, 1)
        bh = b1 - b0; inkm = (a[b0:b1] < med - 60); rows = inkm.mean(axis=1); r = np.where(rows > .05)[0]
        t0 = (b0 + r[0]) / H if len(r) else b0 / H; t1 = (b0 + r[-1] + 1) / H if len(r) else b1 / H
        core = inkm[int(bh * .2):int(bh * .85)].sum(axis=0)
        gaps = []; st = None
        for x in range(W):
            if core[x] <= 1:
                if st is None: st = x
            else:
                if st is not None and x - st >= 6: gaps.append(round((st + x) / 2 / W, 4))
                st = None
        # חיתוך טקסט שוליים (רש״י/תוספות) שנכנס מצד שמאל
        st = None; best = None
        for x in range(int(W * .02), int(W * .5)):
            if core[x] <= 1:
                if st is None: st = x
            else:
                if st is not None and x - st >= max(22, W * .035) and (best is None or x > best[1]): best = (st, x)
                st = None
        if best: xl = best[1] / W; gaps = [g for g in gaps if g > xl]
        out.append([round(b0 / H, 4), round(b1 / H, 4), round(float(xl), 4), round(float(xr), 4), round(float(t0), 4), round(float(t1), 4), gaps])
    return out
def slots(lines):
    out = []
    for li, ln in enumerate(lines):
        y0, y1, xl, xr, t0, t1, gaps = ln
        bs = [xr] + sorted([g for g in gaps if xl + 0.01 < g < xr - 0.01], reverse=True) + [xl]
        for wi in range(len(bs) - 1): out.append((li, bs[wi], bs[wi + 1]))
    return out

# ---------- חיתוך ----------
def snap(a, prof_fn, y, d):
    best = None
    for k in range(0, 9):
        for yy in ([y - k, y + k] if d < 0 else [y + k, y - k]):
            if 0 <= yy < a.shape[0]:
                v = prof_fn(yy)
                if best is None or v < best[0] - 0.004: best = (v, yy)
    return best[1]
def do_crop(ref, only=None):
    P = jload('pages.json'); R = jload('ranges.json')
    thr, nb, wb = P[ref][1], P[ref][2], P[ref][3]
    im = Image.open(src_path(ref)).convert('RGB'); a = np.asarray(im.convert('L')).astype(float); Hh, Ww = a.shape
    def prof(x0, x1): reg = a[:, x0:x1]; return (reg < np.median(reg) - 45).mean(axis=1)
    pn, pw = prof(*nb), prof(*wb)
    pr = lambda yy: pn[yy] if yy < thr else pw[yy]
    bands = P[ref][4] if len(P[ref]) > 4 else None
    D = html_get('DAF_SRC'); L = html_get('DAF_LINES')
    D.setdefault(ref, {})
    for i, (y0, y1) in R[ref].items():
        if only and i not in only: continue
        y0 = snap(a, pr, y0, -1); y1 = snap(a, pr, y1, 1); R[ref][i] = [y0, y1]
        if bands:  # כמה רוחבים (P[ref][4] = [[y_from, x0, x1], ...]): תופרים כל רצועה ברוחב שלה
            parts = [(max(y0, b[0]), min(y1, bands[k + 1][0] if k + 1 < len(bands) else Hh), b[1], b[2]) for k, b in enumerate(bands)]
            parts = [q for q in parts if q[1] > q[0]]
            x0 = min(q[2] for q in parts); x1 = max(q[3] for q in parts)
            c = Image.new('RGB', (x1 - x0, y1 - y0), (240, 236, 226))
            for (a0, a1, b0, b1) in parts: c.paste(im.crop((b0, a0, b1, a1)), (b0 - x0, a0 - y0))
        elif y1 <= thr: c = im.crop((nb[0], y0, nb[1], y1)); x0, x1 = nb
        elif y0 >= thr: c = im.crop((wb[0], y0, wb[1], y1)); x0, x1 = wb
        else:
            x0 = min(nb[0], wb[0]); x1 = max(nb[1], wb[1])
            A = im.crop((nb[0], y0, nb[1], thr)); B = im.crop((wb[0], thr, wb[1], y1))
            c = Image.new('RGB', (x1 - x0, A.height + B.height), (240, 236, 226)); c.paste(A, (nb[0] - x0, 0)); c.paste(B, (wb[0] - x0, A.height))
        c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
        out = os.path.join(IMG, f'{ref}-{i}.jpg')
        ImageOps.autocontrast(c, cutoff=1).filter(ImageFilter.UnsharpMask(1.5, 120, 3)).save(out, quality=82)
        D[ref][i] = [round(x0 / Ww * 100, 2), round(y0 / Hh * 100, 2), round((x1 - x0) / Ww * 100, 2), round((y1 - y0) / Hh * 100, 2)]
        L[f'{ref}-{i}'] = detect_lines(out)
        print(f'{ref}-{i}: y {y0}-{y1}, {len(L[ref + "-" + i])} שורות, {len(slots(L[ref + "-" + i]))} מילים')
    jsave('ranges.json', R)
    s = open(HTML, encoding='utf-8').read()
    s = re.sub(r'const DAF_SRC = \{.*?\};', lambda m: 'const DAF_SRC = ' + json.dumps(D) + ';', s, count=1, flags=re.S)
    open(HTML, 'w', encoding='utf-8').write(s)
    html_set('DAF_LINES', L)

def do_extend(ref, i, up, down):
    R = jload('ranges.json'); L = html_get('DAF_LINES'); SP = html_get('BEAT_SPAN')
    old = L.get(f'{ref}-{i}', [])
    y0, y1 = R[ref][i]; LINE = round((y1 - y0) / max(1, len(old))) if old else 17
    R[ref][i] = [y0 - LINE * up, y1 + LINE * down]; jsave('ranges.json', R)
    do_crop(ref, [i])
    L = html_get('DAF_LINES'); new = L[f'{ref}-{i}']
    off = sum(len([g for g in ln[6] if ln[2] + .01 < g < ln[3] - .01]) + 1 for ln in new[:up]) if up else 0
    if ref in SP and i in SP[ref]:
        for bi in SP[ref][i]: SP[ref][i][bi] = [SP[ref][i][bi][0] + off, SP[ref][i][bi][1] + off]
        html_set('BEAT_SPAN', SP)
    print(f'הוזזו טווחי המילים ב־{off}. הרץ audit {ref} {i} ובדוק!')

def do_audit(ref, only=None):
    L = html_get('DAF_LINES'); SP = html_get('BEAT_SPAN'); SRC = html_get('DAF_SRC')
    f13, f20 = font(13), font(20); tiles = []
    for i in sorted({k.split('-')[1] for k in L if k.startswith(ref + '-')}, key=int):
        if only and i not in only: continue
        crop = f'{ref}-{i}'; im = Image.open(os.path.join(IMG, crop + '.jpg')).convert('RGB'); W, H = im.size; sl = slots(L[crop])
        base = im.copy(); d = ImageDraw.Draw(base)
        for k, (li, xa, xb) in enumerate(sl):
            t0, t1 = L[crop][li][4], L[crop][li][5]
            d.rectangle([xb * W, t0 * H, xa * W, t1 * H], outline=(0, 0, 255)); d.text(((xa + xb) / 2 * W - 6, t1 * H - 14), str(k), fill=(220, 0, 0), font=f13)
        beats = (SP.get(ref, {}).get(i) or {'-': None})
        for bi, span in sorted(beats.items(), key=lambda x: (x[0] == '-', x[0].zfill(3))):
            t = base.copy(); dd = ImageDraw.Draw(t, 'RGBA')
            if span:
                for k in range(span[0], min(span[1], len(sl) - 1) + 1):
                    li, xa, xb = sl[k]; t0, t1 = L[crop][li][4], L[crop][li][5]
                    dd.rectangle([xb * W, t0 * H, xa * W, t1 * H], fill=(255, 180, 0, 90))
            lab = Image.new('RGB', (W, 26), (30, 30, 30)); ImageDraw.Draw(lab).text((6, 2), f'{ref}:{i}:{bi}  {span}', fill=(255, 255, 0), font=f20)
            tile = Image.new('RGB', (W, H + 26)); tile.paste(lab, (0, 0)); tile.paste(t, (0, 26)); tiles.append(tile)
    files = []
    for m in range(0, len(tiles), 6):
        g = tiles[m:m + 6]; Wm = max(t.width for t in g); Hm = sum(t.height + 6 for t in g)
        M = Image.new('RGB', (Wm, Hm), (80, 0, 0)); y = 0
        for t in g: M.paste(t, (Wm - t.width, y)); y += t.height + 6
        M.thumbnail((900, 3600)); fn = os.path.join(OUT, f'audit-{ref}-{m // 6:02d}.png'); M.save(fn); files.append(fn)
    print('\n'.join(files))

def do_slots(ref, i):
    L = html_get('DAF_LINES'); n = 0
    for li, ln in enumerate(L[f'{ref}-{i}']):
        k = len([g for g in ln[6] if ln[2] + .01 < g < ln[3] - .01]) + 1
        print(f'שורה {li}: מילים {n}–{n + k - 1}'); n += k

def do_setspan(js):
    upd = json.loads(js); SP = html_get('BEAT_SPAN')
    for k, v in upd.items():
        r, i, j = k.split(':'); SP.setdefault(r, {}).setdefault(i, {})[j] = v
    html_set('BEAT_SPAN', SP); print('עודכנו', len(upd))

def do_marks():
    s = open(HTML, encoding='utf-8').read()
    L = html_get('DAF_LINES'); SP = html_get('BEAT_SPAN'); SRC = html_get('DAF_SRC')
    W = dict(re.findall(r"'(\d+[ab]:\d+:\d+)': '(.*?)',?\n", s[s.index('const WBW = {'):s.index('const WDICT')]))
    words = {k: ' '.join(p.split('=')[0].strip() for p in v.split('|')) for k, v in W.items()}
    out = '// נוצר אוטומטית מתוך taanit.html (python3 .claude/tools/daf_tool.py marks) — לא לערוך ביד\n'
    out += 'const DAF_LINES = ' + json.dumps(L) + ';\nconst BEAT_SPAN = ' + json.dumps(SP) + ';\nconst BEAT_WORDS = ' + json.dumps(words, ensure_ascii=False) + ';\nconst DAF_SRC = ' + json.dumps(SRC) + ';\n'
    # תוכן ההסבר לעץ (מילה במילה, פיסוק, בתכלס, מילון, מונחים) — כדי שהחלונית בעץ תציג כל מה שיש בדף ההסבר
    def kv(name):
        a = s.index('const %s = {' % name); b = s.index('\n};', a)
        return dict(re.findall(r"^'(\d+[ab]:\d+:\d+)': '(.*?)',?$", s[a:b], flags=re.M))
    a = s.index('const KEY_TERMS = ['); b = s.index('\n];', a)
    terms = re.findall(r"\['(.*?)', '(.*?)'\]", s[a:b])
    TX = {'WBW': W, 'PUNCT': kv('PUNCT'), 'TAKHLES': kv('TAKHLES'), 'WDICT': html_get('WDICT'), 'KEY_TERMS': terms}
    out += 'const TX = ' + json.dumps(TX, ensure_ascii=False) + ';\n'
    open(os.path.join(ROOT, 'daf-marks.js'), 'w', encoding='utf-8').write(out); print('daf-marks.js עודכן')

def do_report():
    s = open(HTML, encoding='utf-8').read()
    LOC = html_get('BEAT_LOC'); SP = html_get('BEAT_SPAN')
    sec = lambda name: set(re.findall(r"'(\d+[ab]:\d+:\d+)':", s[s.index(f'const {name} = {{'):]))
    W, P, T = sec('WBW'), sec('PUNCT'), sec('TAKHLES')
    bad = 0
    for ref, scs in LOC.items():
        for si, arr in scs.items():
            for bi, loc in enumerate(arr):
                k = f'{ref}:{si}:{bi}'; miss = []
                if k not in T: miss.append('בתכלס')
                if loc:
                    if not (SP.get(ref, {}).get(si, {}).get(str(bi))): miss.append('BEAT_SPAN')
                    if k not in W: miss.append('מילה במילה')
                    if k not in P: miss.append('פיסוק')
                if miss: bad += 1; print(k, 'חסר:', ', '.join(miss))
    print('סה״כ שלבים עם חוסר:', bad)

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit()
    c = a[0]
    if c == 'ruler':
        f, x0, x1, y0, y1, out = a[1], *map(int, a[2:6]), a[6]; sc = float(a[7]) if len(a) > 7 else 1.6
        im = Image.open(f).convert('L').crop((x0, y0, x1, y1)); im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
        im = ImageOps.autocontrast(im).convert('RGB'); o = Image.new('RGB', (im.width + 50, im.height), 'white'); o.paste(im, (50, 0)); d = ImageDraw.Draw(o)
        for y in range(y0 - y0 % 10 + 10, y1, 10):
            yy = int((y - y0) * sc); d.line([(38, yy), (50, yy)], fill='red')
            if y % 20 == 0: d.text((2, yy - 6), str(y), fill='red')
        for x in range(x0 - x0 % 50 + 50, x1, 50):
            xx = 50 + int((x - x0) * sc); d.line([(xx, 0), (xx, 10)], fill='blue'); d.text((xx + 2, 0), str(x), fill='blue')
        o.save(out); print(out)
    elif c == 'columns':
        f, y0, y1 = a[1], int(a[2]), int(a[3]); arr = np.asarray(Image.open(f).convert('L')).astype(float)
        reg = arr[y0:y1, :]; ink = (reg < np.median(reg, axis=1, keepdims=True) - 50).mean(axis=0); sm = np.convolve(ink, np.ones(7) / 7, 'same')
        low = sm < 0.25 * np.median(sm); gaps = []; st = None
        for i, v in enumerate(low):
            if v and st is None: st = i
            if not v and st is not None:
                if i - st >= 3: gaps.append((st, i))
                st = None
        print('רווחים בין טורים (x מ־עד):', gaps)
    elif c == 'zoom':
        f, x0, y0, x1, y1, out = a[1], *map(int, a[2:6]), a[6]; sc = int(a[7]) if len(a) > 7 else 3
        im = Image.open(f).convert('L').crop((x0, y0, x1, y1)); im = im.resize((im.width * sc, im.height * sc), Image.LANCZOS)
        ImageOps.autocontrast(im).filter(ImageFilter.SHARPEN).save(out); print(out)
    elif c == 'crop': do_crop(a[1], a[2].split(',') if len(a) > 2 else None)
    elif c == 'extend': do_extend(a[1], a[2], int(a[3]), int(a[4]))
    elif c == 'audit': do_audit(a[1], a[2].split(',') if len(a) > 2 else None)
    elif c == 'slots': do_slots(a[1], a[2])
    elif c == 'setspan': do_setspan(a[1])
    elif c == 'marks': do_marks()
    elif c == 'report': do_report()
    else: print(__doc__)
