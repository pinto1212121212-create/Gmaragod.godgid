# כותב קובץ TrueType פשוט (בלי ספריות חיצוניות): קווי מתאר ישרים בלבד (on-curve), מספיק לגופן מדויק ברזולוציה גבוהה
import struct, time

def _cs(data):
    data += b'\0' * ((4 - len(data) % 4) % 4)
    return sum(struct.unpack('>%dI' % (len(data) // 4), data)) & 0xFFFFFFFF

def _glyf(contours):
    # contours: [[(x,y),...], ...] integers
    if not contours: return b''
    xs = [p[0] for c in contours for p in c]; ys = [p[1] for c in contours for p in c]
    out = struct.pack('>hhhhh', len(contours), min(xs), min(ys), max(xs), max(ys))
    ends, n = [], -1
    for c in contours: n += len(c); ends.append(n)
    out += struct.pack('>%dH' % len(ends), *ends) + struct.pack('>H', 0)
    flags, dx, dy = [], [], []
    px = py = 0
    for c in contours:
        for pt in c:
            x, y = pt[0], pt[1]; on = pt[2] if len(pt) > 2 else 1
            ddx, ddy = x - px, y - py; px, py = x, y
            f = 1 if on else 0
            if ddx == 0: f |= 0x10
            elif -255 <= ddx <= 255: f |= 0x02 | (0x10 if ddx > 0 else 0); dx.append(struct.pack('>B', abs(ddx)))
            else: dx.append(struct.pack('>h', ddx))
            if ddy == 0: f |= 0x20
            elif -255 <= ddy <= 255: f |= 0x04 | (0x20 if ddy > 0 else 0); dy.append(struct.pack('>B', abs(ddy)))
            else: dy.append(struct.pack('>h', ddy))
            flags.append(f)
    out += bytes(flags) + b''.join(dx) + b''.join(dy)
    out += b'\0' * ((4 - len(out) % 4) % 4)
    return out

def build(path, family, glyphs, upm=1000, asc=850, desc=-300, version='1.0'):
    """glyphs: list of (name, codepoints[list], advance, contours). glyph 0 must be .notdef"""
    n = len(glyphs)
    glyf, loca = b'', [0]
    bbox = [0, 0, 0, 0]; maxpts = maxc = 0
    lsbs = []
    for name, cps, adv, cont in glyphs:
        g = _glyf(cont); glyf += g; loca.append(len(glyf))
        if cont:
            xs = [p[0] for c in cont for p in c]; ys = [p[1] for c in cont for p in c]
            bbox = [min(bbox[0], min(xs)), min(bbox[1], min(ys)), max(bbox[2], max(xs)), max(bbox[3], max(ys))]
            maxpts = max(maxpts, sum(len(c) for c in cont)); maxc = max(maxc, len(cont)); lsbs.append(min(xs))
        else: lsbs.append(0)
    T = {}
    T['glyf'] = glyf
    T['loca'] = struct.pack('>%dI' % len(loca), *loca)
    now = int(time.time()) + 2082844800
    T['head'] = struct.pack('>IIIIHHqqhhhhHHhhh', 0x00010000, 0x00010000, 0, 0x5F0F3CF5, 0x000B, upm, now, now,
                            bbox[0], bbox[1], bbox[2], bbox[3], 0, 8, 2, 1, 0)
    advs = [g[2] for g in glyphs]
    T['hhea'] = struct.pack('>IhhhHhhhhhhhhhhhH', 0x00010000, asc, desc, 0, max(advs), min(lsbs), 0, bbox[2], 1, 0, 0, 0, 0, 0, 0, 0, n)
    T['hmtx'] = b''.join(struct.pack('>Hh', a, l) for a, l in zip(advs, lsbs))
    T['maxp'] = struct.pack('>IHHHHHHHHHHHHHH', 0x00010000, n, maxpts, maxc, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0)
    # cmap format 4
    m = sorted((cp, i) for i, g in enumerate(glyphs) for cp in g[1])
    segs = [(cp, cp, gi) for cp, gi in m]
    segs.append((0xFFFF, 0xFFFF, 0))
    sc = len(segs)
    ends = b''.join(struct.pack('>H', s[1]) for s in segs)
    starts = b''.join(struct.pack('>H', s[0]) for s in segs)
    deltas = b''.join(struct.pack('>H', (s[2] - s[0]) & 0xFFFF) for s in segs)
    ro = b'\0\0' * sc
    import math
    sr = 2 * 2 ** int(math.log2(sc)); es = int(math.log2(sr // 2)); rs = 2 * sc - sr
    sub = struct.pack('>HHHHHHH', 4, 0, 0, 2 * sc, sr, es, rs) + ends + b'\0\0' + starts + deltas + ro
    sub = sub[:2] + struct.pack('>H', len(sub)) + sub[4:]
    T['cmap'] = struct.pack('>HHHHI', 0, 1, 3, 1, 12) + sub
    # name
    recs = [(1, family), (2, 'Regular'), (3, family + ' ' + version), (4, family), (5, 'Version ' + version), (6, family.replace(' ', ''))]
    strs = b''; rr = b''
    for nid, s in recs:
        e = s.encode('utf-16-be'); rr += struct.pack('>HHHHHH', 3, 1, 0x409, nid, len(e), len(strs)); strs += e
    T['name'] = struct.pack('>HHH', 0, len(recs), 6 + 12 * len(recs)) + rr + strs
    T['OS/2'] = struct.pack('>HhHHHhhhhhhhhhhh10sIIII4sHHHhhhHHII', 1, 500, 400, 5, 0, 650, 700, 0, 140, 650, 700, 0, 480, 50, 300, 0,
                            b'\x02\x00\x05\x03\x00\x00\x00\x00\x00\x00', 0x800, 0, 0, 0, b'GMRA',
                            0x40, min(cp for cp, _ in m), max(cp for cp, _ in m), asc, desc, 0, asc, -desc, 0x20, 0)
    T['post'] = struct.pack('>IIhhIIIII', 0x00030000, 0, -100, 50, 0, 0, 0, 0, 0)
    tags = sorted(T)
    nt = len(tags); sr = 16 * 2 ** int(math.log2(nt)); es = int(math.log2(sr // 16)); rs = nt * 16 - sr
    head = struct.pack('>IHHHH', 0x00010000, nt, sr, es, rs)
    off = 12 + 16 * nt; dirs = b''; body = b''
    for t in tags:
        d = T[t]; dirs += struct.pack('>4sIII', t.encode(), _cs(d), off + len(body), len(d))
        body += d + b'\0' * ((4 - len(d) % 4) % 4)
    font = bytearray(head + dirs + body)
    # checkSumAdjustment
    hi = tags.index('head'); hoff = struct.unpack('>I', font[12 + 16 * hi + 8:12 + 16 * hi + 12])[0]
    adj = (0xB1B0AFBA - _cs(bytes(font))) & 0xFFFFFFFF
    font[hoff + 8:hoff + 12] = struct.pack('>I', adj)
    open(path, 'wb').write(bytes(font))
