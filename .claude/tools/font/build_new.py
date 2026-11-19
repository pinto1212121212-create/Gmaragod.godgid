# ״מרובע שלנו״ — גופן עברי מצויר מאפס (צורות שלנו, לא מגופן קיים): כל אות בנויה מקווים עבים/דקים, ונמסרת ל־glyphs.to_font
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw
import glyphs as G
from ttf import build

P = dict(T=19, t=8, flag=7, round=10, wx=1.0, slant=0.0)
P.update(json.loads(os.environ.get('NF', '{}')))
S = 4                                     # פיקסלים ליחידה
H = 100                                   # גובה אות: 0 (למעלה) .. 100 (קו בסיס); ירידה עד 165, עלייה עד -45

def canvas(w):
    im = Image.new('L', (int(w * S), int((165 + 45) * S)), 0); return im, ImageDraw.Draw(im)
def R(d, x0, y0, x1, y1, r=0):
    box = [x0 * S, (y0 + 45) * S, x1 * S, (y1 + 45) * S]
    if r: d.rounded_rectangle(box, radius=r * S, fill=255)
    else: d.rectangle(box, fill=255)
def PL(d, pts): d.polygon([(x * S, (y + 45) * S) for x, y in pts], fill=255)
def ARC(d, cx, cy, rx, ry, a0, a1, w):
    for a in np.linspace(a0, a1, 60):
        x = cx + rx * np.cos(np.radians(a)); y = cy + ry * np.sin(np.radians(a))
        d.ellipse([(x - w / 2) * S, (y - w / 2 + 45) * S, (x + w / 2) * S, (y + w / 2 + 45) * S], fill=255)

T, t, F, RD = P['T'], P['t'], P['flag'], P['round']
def roof(d, x0, x1, flag=True):           # גג עבה, ודגל קטן בצד שמאל (כמו קוצו של יוד)
    R(d, x0, 0, x1, T, r=2)
    if flag: PL(d, [(x0, 0), (x0 + F * 1.6, 0), (x0, T + F)])
def base(d, x0, x1): R(d, x0, H - T, x1, H, r=2)
def stem(d, x, y0, y1, w=None): R(d, x - (w or t), y0, x, y1)

L = {}
def g(ch, w):
    def deco(f): L[ch] = (w, f); return f
    return deco

@g('ב', 72)
def _(d): roof(d, 4, 60); stem(d, 60, 2, H - T + 2); base(d, 2, 70); R(d, 52, 0, 60, T + RD, r=RD)
@g('ג', 46)
def _(d): roof(d, 6, 36); stem(d, 36, 2, H - 12); PL(d, [(36, H - 30), (40, H), (8, H), (4, H - 10)])
@g('ד', 70)
def _(d): roof(d, 2, 68); stem(d, 56, 2, H)
@g('ה', 72)
def _(d): roof(d, 2, 70); stem(d, 66, 2, H); stem(d, 16, 36, H)
@g('ו', 28)
def _(d): roof(d, 4, 24); stem(d, 24, 2, H)
@g('ז', 40)
def _(d): roof(d, 4, 36); stem(d, 24, 2, H)
@g('ח', 72)
def _(d): roof(d, 2, 70); stem(d, 68, 2, H); stem(d, 12, 6, H)
@g('ט', 72)
def _(d):
    stem(d, 70, 0, H - 24); base(d, 18, 54); ARC(d, 52, H - 24, 17, 15, 0, 90, T * .85)
    stem(d, 4 + t, 24, H - 22); ARC(d, 22, H - 22, 14, 13, 90, 180, T * .85)
    ARC(d, 24, 26, 13, 14, 180, 330, t * 1.4); R(d, 30, 14, 40, 30, r=3)
@g('י', 26)
def _(d): roof(d, 3, 24); stem(d, 24, 2, 46)
@g('כ', 64)
def _(d): roof(d, 4, 46); base(d, 4, 46); ARC(d, 46, H / 2, 16, H / 2 - T / 2, -90, 90, T * .62)
@g('ך', 62)
def _(d): roof(d, 2, 58); R(d, 52, 0, 60, T + RD, r=RD); stem(d, 60, 4, 165)
@g('ל', 64)
def _(d):
    stem(d, 14, -45, T, w=t + 2); R(d, 4, -45, 18, -38, r=2); R(d, 4, 0, 62, T, r=2)
    stem(d, 62, 2, H - 34); ARC(d, 44, H - 34, 18, 22, 0, 120, T * .8)
@g('ם', 66)
def _(d): roof(d, 2, 64); base(d, 2, 64); stem(d, 64, 2, H); stem(d, 4 + t, 2, H)
@g('מ', 72)
def _(d): roof(d, 2, 68); stem(d, 68, 2, H); base(d, 30, 70); PL(d, [(2, 10), (12, 4), (20, H - 10), (10, H - 6)])
@g('נ', 44)
def _(d): roof(d, 6, 32); stem(d, 32, 2, H - T + 2); base(d, 2, 40)
@g('ן', 28)
def _(d): roof(d, 4, 24); stem(d, 24, 2, 165)
@g('ס', 70)
def _(d): R(d, 2, 0, 68, H, r=26); R(d, 2 + t + 2, T, 68 - t - 2, H - T, r=14) if False else None; _ring(d, 2, 0, 68, H)
def _ring(d, x0, y0, x1, y1):
    im = d._image; m = Image.new('L', im.size, 0); dd = ImageDraw.Draw(m)
    dd.rounded_rectangle([x0 * S, (y0 + 45) * S, x1 * S, (y1 + 45) * S], radius=24 * S, fill=255)
    dd.rounded_rectangle([(x0 + t + 1) * S, (y0 + T + 45) * S, (x1 - t - 1) * S, (y1 - T + 45) * S], radius=12 * S, fill=0)
    im.paste(255, mask=m)
    # מחיקת הפנים
    hole = Image.new('L', im.size, 0); hd = ImageDraw.Draw(hole)
    hd.rounded_rectangle([(x0 + t + 1) * S, (y0 + T + 45) * S, (x1 - t - 1) * S, (y1 - T + 45) * S], radius=12 * S, fill=255)
    im.paste(0, mask=hole)
@g('ע', 72)
def _(d): stem(d, 70, 0, H - 26); PL(d, [(62, H - 30), (70, H - 26), (40, H), (4, H), (4, H - T)]); PL(d, [(6, 0), (18, 0), (52, H - 20), (40, H - 14)]); R(d, 4, 0, 20, 8, r=2)
@g('פ', 66)
def _(d): roof(d, 4, 46); base(d, 4, 46); ARC(d, 46, H / 2, 16, H / 2 - T / 2, -90, 90, T * .62); stem(d, 14 + t, 2, 40); R(d, 14, 32, 30, 42, r=3)
@g('ף', 62)
def _(d): roof(d, 2, 58); R(d, 52, 0, 60, T + RD, r=RD); stem(d, 60, 4, 165); stem(d, 12 + t, 2, 42); R(d, 12, 34, 28, 44, r=3)
@g('צ', 66)
def _(d): base(d, 4, 64); PL(d, [(4, 0), (18, 0), (64, H - T), (48, H - T)]); stem(d, 64, 0, 44); PL(d, [(56, 40), (64, 44), (44, 60), (40, 54)])
@g('ץ', 56)
def _(d): stem(d, 14, 0, 165, w=t + 1); R(d, 4, 0, 20, T, r=2); stem(d, 52, 0, 34); PL(d, [(52, 26), (52, 36), (18, 58), (14, 50)])
@g('ק', 70)
def _(d): roof(d, 2, 66); stem(d, 66, 2, H - 26); ARC(d, 52, H - 28, 14, 18, 0, 100, T * .7); stem(d, 12 + t, 36, 165)
@g('ר', 64)
def _(d): roof(d, 2, 50); R(d, 44, 0, 62, T + RD + 4, r=RD + 2); stem(d, 62, 6, H)
@g('ש', 80)
def _(d): stem(d, 78, 0, H - T); base(d, 8, 78); PL(d, [(4, 0), (16, 0), (24, H - T), (12, H)]); PL(d, [(36, 0), (48, 0), (54, 52), (44, 56)]); R(d, 32, 0, 50, 8, r=2); R(d, 66, 0, 80, 8, r=2)
@g('ת', 74)
def _(d): roof(d, 2, 72); stem(d, 70, 2, H); stem(d, 22, 8, H - 6); PL(d, [(22, H - 14), (22, H), (2, H), (6, H - 6)])
@g('א', 72)
def _(d): PL(d, [(4, 0), (20, 0), (70, H), (54, H)]); stem(d, 66, 0, 46); R(d, 56, 0, 72, 8, r=2); PL(d, [(58, 40), (66, 46), (52, 54), (48, 48)]); stem(d, 18, 52, H); R(d, 4, H - 10, 22, H, r=2); PL(d, [(14, 52), (30, 44), (34, 50), (18, 58)])
@g('׳', 22)
def _(d): PL(d, [(10, 0), (22, 0), (8, 34), (2, 34)])

# בנייה
u = 560 / H; GAP = 7 * u
glyphs = [('.notdef', [], 500, []), ('space', [0x20, 0xA0], int(26 * u), [])]
for ch, (w, f) in L.items():
    w2 = w * P['wx']
    im, d = canvas(w2 + 8)
    f(d)
    if P['wx'] != 1.0: im = im.resize((int((w2 + 8) * S), im.height))
    m = np.array(im).astype(float)
    if P['slant']:
        sh = Image.fromarray(m.astype('uint8')).transform(im.size, Image.AFFINE, (1, P['slant'], -P['slant'] * im.height * .6, 0, 1, 0)); m = np.array(sh).astype(float)
    top = 45 + 0; Hpx = 210
    G.STYLE.update({'blur': .5})
    cont = G.to_font(m, im.width / S, Hpx, top + 0, top - Hpx, u, GAP, S=S, thr=.5)
    # to_font: y_font = (top - y/S*(top-bot)/H)*u → נותן y=0 בשורת הבסיס? מתקנים: הבסיס בפיקסל 145 (=100+45)
    cont = [[(x, y - int((top - 145 * (top - (top - Hpx)) / Hpx) * u), o) for x, y, o in c] for c in cont]
    adv = int(round((w2 + 4) * u + 2 * GAP))
    cps = [ord(ch)] + ([0x27] if ch == '׳' else [])
    glyphs.append(('u%04X' % ord(ch), cps, adv, cont))
    if ch == '׳':
        sh = adv - int(GAP); glyphs.append(('u05F4', [0x5F4, 0x22], adv + sh, cont + [[(x + sh, y, o) for x, y, o in c] for c in cont]))
dsz = int(14 * u)
def dot(cx, cy): return [(cx, cy + dsz // 2, 1), (cx - dsz // 2, cy, 1), (cx, cy - dsz // 2, 1), (cx + dsz // 2, cy, 1)]
glyphs.append(('period', [0x2E], dsz + int(2 * GAP), [dot(int(GAP) + dsz // 2, dsz // 2)]))
glyphs.append(('colon', [0x3A], dsz + int(2 * GAP), [dot(int(GAP) + dsz // 2, dsz // 2), dot(int(GAP) + dsz // 2, int(H * u * .55))]))
build(sys.argv[1], 'Merubaa Shelanu', glyphs)
print('ok', len(glyphs))
