"""כלי עזר לבניית ED_GEO שורה־שורה מצילום PDF (1080×2340).
  cols IMG Y0 Y1            — רווחים לבנים בין הטורים בגובה הזה
  rows IMG X0 X1 Y0 Y1      — שורות טקסט (מרכזים) בטור
  strip IMG X0 X1 Y0 P N OUT [K]  — רצועה מוגדלת עם מספר לכל שורה (לקריאה), N שורות מ־Y0 (מרכז) בקפיצות P
  grid IMG OUT Y0 Y1 [X0 X1 Y P N ...]  — מצייר קווים על הצילום לבדיקה
"""
import sys
from PIL import Image, ImageDraw, ImageOps
import numpy as np
a = sys.argv
im = Image.open(a[2]).convert('L'); A = np.array(im).astype(float)
if a[1] == 'cols':
    y0, y1 = int(a[3]), int(a[4]); p = (A[y0:y1] < 120).sum(0); out = []; inr = False
    for i, v in enumerate(p):
        if v > 0 and not inr: s = i; inr = True
        if v == 0 and inr: out.append((s, i)); inr = False
    print([(out[k][1], out[k + 1][0]) for k in range(len(out) - 1) if out[k + 1][0] - out[k][1] > 14])
elif a[1] == 'rows':
    x0, x1, y0, y1 = map(int, a[3:7]); p = (A[y0:y1, x0:x1] < 120).sum(1); out = []; inr = False
    for i, v in enumerate(p):
        if v > 4 and not inr: s = i; inr = True
        if v <= 4 and inr: out.append((y0 + s + y0 + i) // 2); inr = False
    print(out)
elif a[1] == 'strip':
    x0, x1 = int(a[3]), int(a[4]); y0, P, N = float(a[5]), float(a[6]), int(a[7]); K = float(a[9]) if len(a) > 9 else 3
    W = im.crop((x0, int(y0 - P / 2), x1, int(y0 + P * (N - .5))))
    W = ImageOps.autocontrast(W).resize((int(W.width * K), int(W.height * K)), Image.LANCZOS).convert('RGB'); d = ImageDraw.Draw(W)
    for k in range(N):
        yy = int((k + .5) * P * K); d.line((0, yy, 14, yy), fill=(255, 0, 0), width=3); d.text((16, yy - 8), str(k + 1), fill=(255, 0, 0))
    W.save(a[8])
elif a[1] == 'grid':
    out = a[3]; y0, y1 = int(a[4]), int(a[5]); R = im.convert('RGB'); d = ImageDraw.Draw(R); v = a[6:]
    cs = [(255, 0, 0), (0, 150, 0), (0, 0, 255), (200, 0, 200)]
    for j in range(0, len(v), 5):
        x0, x1, y, P, N = float(v[j]), float(v[j + 1]), float(v[j + 2]), float(v[j + 3]), int(v[j + 4])
        for k in range(N): d.line((x0, y + k * P, x1, y + k * P), fill=cs[(j // 5) % 4], width=1)
    R.crop((0, y0, R.width, y1)).save(out)
