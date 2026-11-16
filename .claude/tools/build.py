#!/usr/bin/env python3
"""בונה את האתר מהמקור: .claude/src/taanit.src.html  →  taanit.html (קוד) + taanit-data/<ref>.js (תוכן לכל דף).

למה: taanit.html עבר 1MB, והטלפון הוריד את כל הדפים בכל פתיחה. עכשיו נטען רק הדף שנכנסים אליו
(והשכנים שלו ברקע). המקור נשאר קובץ אחד — כל הכלים (daf_tool, split_beat) עובדים עליו כמו קודם.

  python3 .claude/tools/build.py        ← אחרי כל שינוי במקור (daf_tool מריץ את זה לבד)

**לא עורכים את taanit.html או את taanit-data/ ביד** — הם נדרסים בכל build.
מה עובר לקובץ של כל דף: amudim[ref].translation/rashi/tosafot/scenes, השורות של הדף ב־WBW/PUNCT/TAKHLES,
DAF_LINES ו־CONTEXT (מ־context-data.js) של הדף, וההגדרות של ״זה מול זה״ (pair) של הקטעים שלו. כל השאר (קוד, MISHNA/PAIRS, BEAT_SPAN,
BEAT_LOC, DAF_SRC, WDICT, KEY_TERMS) נשאר ב־taanit.html.
"""
import hashlib, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, '.claude', 'src', 'taanit.src.html')
OUT = os.path.join(ROOT, 'taanit.html')
DDIR = os.path.join(ROOT, 'taanit-data')


def scan_expr_end(s, i):
    """i = תחילת ביטוי JS (אחרי '= '). מחזיר את האינדקס אחרי ה־';' שסוגר אותו (מתחשב במחרוזות, תבניות ${} והערות)."""
    depth, n = 0, len(s)
    while i < n:
        c = s[i]
        if c in '\'"`':
            i = scan_expr_end_str(s, i); continue
        if s.startswith('//', i):
            i = s.index('\n', i); continue
        if s.startswith('/*', i):
            i = s.index('*/', i) + 2; continue
        if c in '([{': depth += 1
        elif c in ')]}': depth -= 1
        elif c == ';' and depth == 0:
            return i + 1
        i += 1
    raise SystemExit('לא נמצא סוף לביטוי')


def scan_expr_end_str(s, i):
    """i על ' " או ` — מחזיר את האינדקס אחרי סוף המחרוזת"""
    q = s[i]
    if q != '`':
        i += 1
        while s[i] != q:
            i += 2 if s[i] == '\\' else 1
        return i + 1
    i += 1
    while True:
        if s[i] == '\\': i += 2; continue
        if s[i] == '`': return i + 1
        if s.startswith('${', i):
            d = 1; i += 2
            while d:
                if s[i] in '\'"`': i = scan_expr_end_str(s, i); continue
                if s[i] in '([{': d += 1
                elif s[i] in ')]}': d -= 1
                i += 1
            continue
        i += 1


def obj_block(s, name):
    a = f'const {name} = {{\n'
    i = s.index(a) + len(a); j = s.index('\n};', i)
    return i, j


def main():
    s = open(SRC, encoding='utf-8').read()
    bi = s.index('const BEAT_LOC = ') + len('const BEAT_LOC = ')
    refs = list(json.loads(s[bi:s.index(';\n', bi)]).keys())
    parts = {r: [] for r in refs}

    # 1. amudim['ref'].X = ...;
    for r in refs:
        for fld in ['translation', 'rashi', 'tosafot', 'scenes']:
            a = f"amudim['{r}'].{fld} = "
            while a in s:
                i = s.index(a); j = scan_expr_end(s, i + len(a))
                parts[r].append(s[i:j])
                s = s[:i] + s[j:].lstrip('\n') if s[j:j + 1] == '\n' else s[:i] + s[j:]

    # 2. הגדרות ״זה מול זה״ מיוחדות ל־4b, והלולאה הכללית
    m = re.search(r"for \(const \[i, cfg\] of \[\[.*?\]\]\) Object\.assign\(amudim\['(\w+)'\]\.scenes\[i\], cfg\);\n", s, re.S)
    if m:
        parts[m.group(1)].append(m.group(0).rstrip('\n')); s = s[:m.start()] + s[m.end():]
    a = "for (const [ref, i, cfg] of [\n"; i = s.index(a) + len(a); j = s.index("]) Object.assign(amudim[ref].scenes[i], cfg);", i)
    keep, per = [], {}
    for ln in s[i:j].split('\n'):
        mm = re.match(r"^\s*\['(\w+)', (\d+), (\{.*\})\],?\s*$", ln)
        if mm and mm.group(1) in parts:
            per.setdefault(mm.group(1), []).append(f"[{mm.group(2)}, {mm.group(3)}]")
        elif ln.strip():
            keep.append(ln)
    s = s[:i] + '\n'.join(keep) + ('\n' if keep else '') + s[j:]
    for r, rows in per.items():
        parts[r].append("for (const [i, cfg] of [\n  " + ',\n  '.join(rows) + "\n]) Object.assign(amudim['" + r + "'].scenes[i], cfg);")

    # 3. WBW / PUNCT / TAKHLES — שורה לכל שלב
    for name in ['WBW', 'PUNCT', 'TAKHLES']:
        i, j = obj_block(s, name)
        keep, per = [], {}
        for ln in s[i:j].split('\n'):
            mm = re.match(r"^\s*'(\w+):\d+:\d+':", ln)
            if mm and mm.group(1) in parts:
                per.setdefault(mm.group(1), []).append(ln.strip().rstrip(','))
            else:
                keep.append(ln)
        s = s[:i] + '\n'.join(keep) + s[j:]
        for r, rows in per.items():
            parts[r].append(f"Object.assign({name}, {{\n" + ',\n'.join(rows) + "\n});")

    # 4. DAF_LINES
    a = 'const DAF_LINES = '; i = s.index(a) + len(a); j = s.index(';\n', i)
    DL = json.loads(s[i:j]); keep = {}
    per = {}
    for k, v in DL.items():
        r = k.rsplit('-', 1)[0]
        (per.setdefault(r, {}) if r in parts else keep)[k] = v
    s = s[:i] + json.dumps(keep, ensure_ascii=False) + s[j:]
    for r, d in per.items():
        parts[r].append('Object.assign(DAF_LINES, ' + json.dumps(d, ensure_ascii=False) + ');')

    # 4ב. CONTEXT (ההסבר הארוך) — גם הוא לפי דף. tree.html ממשיך לטעון את context-data.js כולו
    C = open(os.path.join(ROOT, 'context-data.js'), encoding='utf-8').read()
    per = {}
    for ln in C.split('\n'):
        mm = re.match(r"^'(\w+):\d+:\d+':", ln)
        if mm and mm.group(1) in parts: per.setdefault(mm.group(1), []).append(ln.strip().rstrip(','))
    for r, rows in per.items():
        parts[r].append("Object.assign(CONTEXT, {\n" + ',\n'.join(rows) + "\n});")
    tag = '<script src="context-data.js"></script>'
    if tag not in s: raise SystemExit('לא נמצא ' + tag)
    s = s.replace(tag, '<script>const CONTEXT = {};   /* ההסבר הארוך נטען עם כל דף (taanit-data) */</script>')

    # 5. כתיבה
    os.makedirs(DDIR, exist_ok=True)
    ver = {}
    for r in refs:
        body = (f"// ✳️ נוצר אוטומטית ע״י .claude/tools/build.py מתוך .claude/src/taanit.src.html — לא לערוך ביד.\n"
                f"// התוכן של דף {r}: נטען רק כשנכנסים לדף (loadPage ב־taanit.html).\n"
                + '\n\n'.join(parts[r]) + f"\n\npageLoaded('{r}');\n")
        open(os.path.join(DDIR, f'{r}.js'), 'w', encoding='utf-8').write(body)
        ver[r] = hashlib.md5(body.encode()).hexdigest()[:8]
    for f in os.listdir(DDIR):
        if f.endswith('.js') and f[:-3] not in ver: os.remove(os.path.join(DDIR, f))
    a = 'const DATA_V = {};'
    if a not in s: raise SystemExit('חסר "const DATA_V = {};" במקור')
    s = s.replace(a, 'const DATA_V = ' + json.dumps(ver) + ';')
    s = s.replace('<!-- ✳️ BUILD NOTE -->', '<!-- ✳️ הקובץ נוצר אוטומטית (.claude/tools/build.py). עורכים רק את המקור. -->')
    open(OUT, 'w', encoding='utf-8').write(s)
    tot = sum(os.path.getsize(os.path.join(DDIR, f'{r}.js')) for r in refs)
    print(f'taanit.html {len(s.encode()) // 1024}KB · taanit-data: {len(refs)} דפים, {tot // 1024}KB')


if __name__ == '__main__':
    main()
