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

# סגנון: ex = כמה להצר קווים אנכיים, dy = כמה לעבות קווים אופקיים (ניגודיות ״מודרנית״), בפיקסלים של S
STYLE = {'ex': 0, 'dy': 0}
def _morph(b):
    ex, dy = STYLE.get('ex', 0), STYLE.get('dy', 0)
    if ex:
        o = b.copy()
        for i in range(1, ex + 1): o &= np.roll(b, i, 1) & np.roll(b, -i, 1)
        b = o
    if dy:
        o = b.copy()
        for i in range(1, dy + 1): o |= np.roll(b, i, 0) | np.roll(b, -i, 0)
        b = o
    return b

def shape(m, S=8, blur=0.28, thr=0.5):
    im = Image.fromarray(m.clip(0, 255).astype('uint8'))
    pad = S * 2
    big = Image.new('L', (im.width + 2 * pad, im.height + 2 * pad), 0); big.paste(im, (pad, pad))
    big = big.filter(ImageFilter.GaussianBlur(S * blur))
    a = np.array(big).astype(float)
    return _morph(a > thr * a.max()), pad

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

def _ang(a, b, c):
    v1 = (a[0] - b[0], a[1] - b[1]); v2 = (c[0] - b[0], c[1] - b[1])
    n1 = np.hypot(*v1); n2 = np.hypot(*v2)
    if n1 == 0 or n2 == 0: return 180.0
    return float(np.degrees(np.arccos(max(-1, min(1, (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2))))))

def _gauss(P, sig, circular=True):
    if sig <= 0 or len(P) < 3: return P.copy()
    r = int(3 * sig); k = np.exp(-np.arange(-r, r + 1) ** 2 / (2 * sig * sig)); k /= k.sum()
    if circular:
        Q = np.concatenate([P[-r:], P, P[:r]]) if r < len(P) else np.tile(P, (3, 1))[len(P) - r:2 * len(P) + r]
    else:
        Q = np.concatenate([np.repeat(P[:1], r, 0), P, np.repeat(P[-1:], r, 0)])
    return np.stack([np.convolve(Q[:, 0], k, 'valid'), np.convolve(Q[:, 1], k, 'valid')], 1)

def smooth_loop(loop, S=8, corner=140, snap=8):
    """שיפור כמו במהדורות החדשות: מוצאים את הפינות האמיתיות (נשארות חדות), מחליקים רק ביניהן,
    קטע כמעט ישר — ישר לגמרי (ואנכי/אופקי אם הוא קרוב לזה). מחזיר [(x, y, 1)]"""
    P = np.array(loop, float); N = len(P)
    if N < 12: return [(x, y, 1) for x, y in P]
    Ps = _gauss(P, S * .5)
    k = max(3, int(S * 1.6))
    def ang(i):
        a, b, c = Ps[(i - k) % N], Ps[i], Ps[(i + k) % N]
        v1, v2 = a - b, c - b; n = np.hypot(*v1) * np.hypot(*v2)
        return 180.0 if n == 0 else float(np.degrees(np.arccos(np.clip((v1 @ v2) / n, -1, 1))))
    A = np.array([ang(i) for i in range(N)])
    cs = [i for i in range(N) if A[i] < corner and A[i] == min(A[(i + j) % N] for j in range(-k, k + 1))]
    ded = []
    for i in cs:
        if not ded or i - ded[-1] > k: ded.append(i)
    if len(ded) >= 2 and (ded[0] + N - ded[-1]) <= k: ded.pop()
    out = []
    if not ded:   # לולאה עגולה בלי פינות
        Q = _gauss(P, S * 1.1)
        return [(x, y, 1) for x, y in rdp(list(map(tuple, Q)) + [tuple(Q[0])], S * .1)[:-1]]
    for j, i0 in enumerate(ded):
        i1 = ded[(j + 1) % len(ded)]
        span = (i1 - i0) % N or N
        idx = [(i0 + t) % N for t in range(span + 1)]
        seg = P[idx]
        a, b2 = seg[0], seg[-1]; ch = b2 - a; L = np.hypot(*ch)
        dev = np.abs(ch[0] * (seg[:, 1] - a[1]) - ch[1] * (seg[:, 0] - a[0])) / L if L else np.zeros(len(seg))
        if L > S and dev.max() < S * .45:     # קו ישר
            an = np.degrees(np.arctan2(abs(ch[1]), abs(ch[0])))
            out.append(('L', a.copy(), b2.copy(), an)); continue
        sm = _gauss(seg, S * 1.1, circular=False)
        sm[0], sm[-1] = a, b2
        pts = rdp(list(map(tuple, sm)), S * .1)
        out.append(('C', pts))
    # בונים את הלולאה, ומיישרים קווים כמעט אנכיים/אופקיים
    res = []
    for seg in out:
        if seg[0] == 'L':
            _, a, b2, an = seg
            if an > 90 - snap: mx = (a[0] + b2[0]) / 2; a[0] = b2[0] = mx
            elif an < snap: my = (a[1] + b2[1]) / 2; a[1] = b2[1] = my
            res += [tuple(a), tuple(b2)]
        else: res += seg[1]
    clean = [res[0]]
    for q in res[1:]:
        if np.hypot(q[0] - clean[-1][0], q[1] - clean[-1][1]) > S * .05: clean.append(q)
    return [(x, y, 1) for x, y in clean]

def area(c): return 0.5 * sum(c[i][0] * c[(i + 1) % len(c)][1] - c[(i + 1) % len(c)][0] * c[i][1] for i in range(len(c)))

def sides(b, pad, S):
    # ריווח אופטי: כמה ״אוויר״ יש בממוצע בין קצה האות לדיו, בכל צד (בפיקסלים של המקור)
    ys = [y for y in range(b.shape[0]) if b[y].any()]
    if not ys: return 0.0, 0.0
    xs = np.nonzero(b.any(0))[0]; x0, x1 = xs.min(), xs.max()
    L = [np.nonzero(b[y])[0].min() - x0 for y in ys]; R = [x1 - np.nonzero(b[y])[0].max() for y in ys]
    return float(np.mean(L)) / S, float(np.mean(R)) / S

def stem(m, S=8, thr=0.5):
    b, pad = shape(m, S, thr=thr); h = b.shape[0]
    runs = []
    for y in range(int(h * .35), int(h * .65), 2):
        r = b[y]; x = 0
        while x < len(r):
            if r[x]:
                x0 = x
                while x < len(r) and r[x]: x += 1
                runs.append(x - x0)
            x += 1
    return float(np.median(runs)) if runs else 0.0

def thr_for(m, target, S=8):
    lo, hi = .32, .68
    for _ in range(8):
        t = (lo + hi) / 2; w = stem(m, S, t)
        if w > target: lo = t
        else: hi = t
    return (lo + hi) / 2

def to_font(m, W, H, top, bot, u, lsb, S=8, **kw):
    b, pad = shape(m, S, **kw)
    loops = trace(b)
    out = []
    for lp in loops:
        p = smooth_loop(lp, S=S)
        c = []
        for x, y, o in p:
            fx = lsb + (x - pad) / S * u
            fy = (top - (y - pad) / S * (top - bot) / H) * u
            c.append((int(round(fx)), int(round(fy)), o))
        cc = [c[0]] + [q for i, q in enumerate(c[1:]) if q[:2] != c[i][:2]]
        if len(cc) >= 3 and abs(area(cc)) > 20: out.append(cc)
    # TrueType: חיצוני עם כיוון השעון (y למעלה). כל הלולאות כבר בכיוון עקבי — מכוונים לפי הגדולה ביותר
    if out:
        big = max(out, key=lambda c: abs(area(c)))
        if area(big) > 0: out = [c[::-1] for c in out]
    to_font.sides = sides(b, pad, S)
    return out
