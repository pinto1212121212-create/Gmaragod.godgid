# מאותיות מצולמות לקווי מתאר: ממוצע של כל הדוגמאות של אות (בלי החריגות), החלקה, ומעקב אחרי הגבול
import numpy as np
from PIL import Image, ImageFilter

def average(samples, S=8, keep=0.6):
    H = int(round(np.median([s['top'] - s['bot'] for s in samples])))
    W = int(round(np.median([s['w'] for s in samples])))
    arr = [np.array(Image.fromarray(s['img'].clip(0, 255).astype('uint8')).resize((W * S, H * S), Image.BILINEAR)).astype(float) for s in samples]
    def corr(a, b):
        a1 = a - a.mean(); b1 = b - b.mean(); return (a1 * b1).sum() / (np.sqrt((a1 ** 2).sum() * (b1 ** 2).sum()) + 1e-9)
    def shift(a, dx, dy):
        o = np.zeros_like(a); h, w = a.shape
        ys, yd = (slice(0, h - dy), slice(dy, h)) if dy >= 0 else (slice(-dy, h), slice(0, h + dy))
        xs, xd = (slice(0, w - dx), slice(dx, w)) if dx >= 0 else (slice(-dx, w), slice(0, w + dx))
        o[yd, xd] = a[ys, xs]; return o
    m = np.mean(arr, 0)
    for rnd in range(3):   # יישור: כל דוגמה מוזזת עד שהיא חופפת לממוצע (אחרת הממוצע מטושטש), ואז בלי הדוגמאות הרחוקות
        R = S * 2
        al = []
        for a in arr:
            best = max(((corr(shift(a, dx, dy), m), dx, dy) for dx in range(-R, R + 1, 2) for dy in range(-R, R + 1, 2)))
            al.append((best[0], shift(a, best[1], best[2])))
        al.sort(key=lambda t: -t[0])
        k = len(al) if len(al) <= 2 else max(2, int(round(len(al) * keep)))
        m = np.mean([a for c, a in al[:k]], 0)
    top = float(np.median([s['top'] for s in samples])); bot = float(np.median([s['bot'] for s in samples]))
    return m, W, H, top, bot

def shape(m, S=8, blur=0.28, thr=0.5):
    im = Image.fromarray(m.clip(0, 255).astype('uint8'))
    pad = S * 2
    big = Image.new('L', (im.width + 2 * pad, im.height + 2 * pad), 0); big.paste(im, (pad, pad))
    big = big.filter(ImageFilter.GaussianBlur(S * blur))
    a = np.array(big).astype(float)
    return a > thr * a.max(), pad

def trace(b):
    H, W = b.shape; E = {}
    def add(p, q): E.setdefault(p, []).append(q)
    ys, xs = np.nonzero(b)
    for y, x in zip(ys, xs):
        if y == 0 or not b[y - 1, x]: add((x + 1, y), (x, y))
        if y == H - 1 or not b[y + 1, x]: add((x, y + 1), (x + 1, y + 1))
        if x == 0 or not b[y, x - 1]: add((x, y), (x, y + 1))
        if x == W - 1 or not b[y, x + 1]: add((x + 1, y + 1), (x + 1, y))
    loops = []
    while E:
        s = next(iter(E)); loop = [s]; p = s; prev = None
        while True:
            qs = E[p]
            if len(qs) > 1 and prev is not None:   # צומת: פונים ימינה בעקביות
                d0 = (p[0] - prev[0], p[1] - prev[1])
                def rank(q):
                    d = (q[0] - p[0], q[1] - p[1]); cr = d0[0] * d[1] - d0[1] * d[0]; return -cr
                qs.sort(key=rank)
            q = qs.pop(0)
            if not qs: del E[p]
            prev, p = p, q
            if p == s: break
            loop.append(p)
        if len(loop) >= 8: loops.append(loop)
    return loops

def rdp(pts, eps):
    if len(pts) < 3: return pts
    a, b = np.array(pts[0], float), np.array(pts[-1], float); d = b - a; L = np.hypot(*d)
    P = np.array(pts, float)
    Q = P - a; dist = np.abs(d[0] * Q[:, 1] - d[1] * Q[:, 0]) / L if L else np.hypot(Q[:, 0], Q[:, 1])
    i = int(np.argmax(dist))
    if dist[i] > eps: return rdp(pts[:i + 1], eps)[:-1] + rdp(pts[i:], eps)
    return [pts[0], pts[-1]]

def smooth_loop(loop, eps=0.9, it=2):
    n = len(loop); i0 = 0
    pts = loop[i0:] + loop[:i0 + 1]
    k = len(pts) // 2
    p = rdp(pts[:k + 1], eps)[:-1] + rdp(pts[k:], eps)[:-1]
    p = [tuple(map(float, q)) for q in p]
    for _ in range(it):   # Chaikin
        q = []
        for i in range(len(p)):
            a, b = p[i], p[(i + 1) % len(p)]
            q += [(.75 * a[0] + .25 * b[0], .75 * a[1] + .25 * b[1]), (.25 * a[0] + .75 * b[0], .25 * a[1] + .75 * b[1])]
        p = q
    return p

def area(c): return 0.5 * sum(c[i][0] * c[(i + 1) % len(c)][1] - c[(i + 1) % len(c)][0] * c[i][1] for i in range(len(c)))

def to_font(m, W, H, top, bot, u, lsb, S=8, **kw):
    b, pad = shape(m, S, **kw)
    loops = trace(b)
    out = []
    for lp in loops:
        p = smooth_loop(lp)
        c = []
        for x, y in p:
            fx = lsb + (x - pad) / S * u
            fy = (top - (y - pad) / S * (top - bot) / H) * u
            c.append((int(round(fx)), int(round(fy))))
        cc = [c[0]] + [q for i, q in enumerate(c[1:]) if q != c[i]]
        if len(cc) >= 3 and abs(area(cc)) > 20: out.append(cc)
    # TrueType: חיצוני עם כיוון השעון (y למעלה). כל הלולאות כבר בכיוון עקבי — מכוונים לפי הגדולה ביותר
    if out:
        big = max(out, key=lambda c: abs(area(c)))
        if area(big) > 0: out = [c[::-1] for c in out]
    return out
