# בונה את ״וילנא שלנו — גמרא״ (fonts/gm.ttf) מהדוגמאות שנחתכו מש״ס וילנא הישן (ראם, תרמ״א) — ראו .claude/vilna-src
import sys, pickle, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from glyphs import average, to_font, stem, thr_for
from ttf import build

samples = pickle.load(open(sys.argv[1], 'rb')); out = sys.argv[2]
XH = float(np.median([s['xh'] for v in samples.values() for s in v]))
u = 560 / XH                    # גובה האות הרגילה (מ, ב, ר) = 560 יחידות
GAP = 1.6 * u                    # רווח בין אותיות (חצי מכל צד)
glyphs = [('.notdef', [], 500, []), ('space', [0x20, 0xA0], int(0.32 * XH * u), [])]
AV = {ch: average(samples[ch]) for ch in samples}
# משקל אחיד: עובי הקו האנכי של כל אות קרוב לחציון של האותיות עם קו אנכי ברור
STEMS = [stem(AV[c][0]) for c in 'דהוזחכנןרתגק' if c in AV]
TGT = float(np.median(STEMS))
# גבהים אחידים: ראש האות בגובה אחד, בסיס על קו אחד, ירידות ועליות באורך אחד
DESC_L = 'ךןףץק'; ASC = float(np.median([s['top'] for s in samples.get('ל', [])])) if 'ל' in samples else XH * 1.4
DSC = float(np.median([AV[c][4] for c in 'ןךף' if c in AV]))
def snap(ch, top, bot):
    if ch == 'ל': top = ASC
    elif abs(top - XH) < XH * .15: top = XH
    if ch in DESC_L: bot = DSC if ch != 'ק' else DSC * .9
    elif abs(bot) < XH * .15: bot = 0.0
    return top, bot
for ch in sorted(samples):
    m, W, H, top, bot = AV[ch]
    top, bot = snap(ch, top, bot)
    t = thr_for(m, TGT) if ch not in '׳י' else 0.5
    t = min(.6, max(.4, t))
    cont = to_font(m, W, H, top, bot, u, GAP, thr=t)
    L, R = to_font.sides                       # ריווח אופטי: מקזזים 40% מה״אוויר״ שבצדי האות (ר, ו, ל, י...)
    k = .4; dl, dr = k * L * u, k * R * u
    cont = [[(x - int(round(dl)), y, o) for x, y, o in c] for c in cont]
    adv = int(round(W * u + 2 * GAP - dl - dr))
    glyphs.append(('u%04X' % ord(ch), [ord(ch)] + ([0x27] if ch == '׳' else []), adv, cont))
    if ch == '׳':   # ״ = שני גרשים
        sh = adv - int(GAP)
        glyphs.append(('u05F4', [0x5F4, 0x22], adv + sh, cont + [[(x + sh, y, o) for x, y, o in c] for c in cont]))
# ץ לא הופיעה בצילום: ן (הרגל הארוכה) + ראש של י בצד ימין למעלה — שתיהן מאותו דפוס
if 'ץ' not in samples and 'ן' in samples and 'י' in samples:
    Sx = 8
    mn, Wn, Hn, tn, bn = AV['ן']; my, Wy, Hy, ty, by = AV['י']; tn, bn = snap('ן', tn, bn)
    scale = (Hn * Sx) / (tn - bn) / Sx          # שורות לפיקסל
    off = int(Wy * Sx * .55)                    # כמה הי בולטת ימינה מעבר לן
    W2 = mn.shape[1] + off; m = np.zeros((mn.shape[0], W2)); m[:, :mn.shape[1]] = mn
    yy = int((tn - ty) * Sx * Hn / (tn - bn)); x0 = W2 - my.shape[1]
    h = min(my.shape[0], m.shape[0] - yy)
    m[yy:yy + h, x0:x0 + my.shape[1]] = np.maximum(m[yy:yy + h, x0:x0 + my.shape[1]], my[:h])
    W2px = W2 / Sx
    cont = to_font(m, int(round(W2px)), Hn, tn, bn, u, GAP)
    glyphs.append(('u05E5', [0x5E5], int(round(W2px * u + 2 * GAP)), cont))
# נקודה ונקודתיים: מעוין קטן מעוגל, בגובה הנכון
d = int(0.16 * XH * u); g = int(GAP)
def dot(cx, cy): return [(cx, cy + d // 2), (cx + d // 2, cy), (cx, cy - d // 2), (cx - d // 2, cy)][::-1]
glyphs.append(('period', [0x2E], d + 2 * g, [dot(g + d // 2, d // 2)]))
glyphs.append(('colon', [0x3A], d + 2 * g, [dot(g + d // 2, d // 2), dot(g + d // 2, int(XH * u * .55))]))
build(out, 'Vilna Shelanu GM', glyphs)
print('glyphs', len(glyphs), 'XH', round(XH, 1))
