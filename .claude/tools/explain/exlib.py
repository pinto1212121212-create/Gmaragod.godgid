CSS = open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'raw', 'rabba-4b.html'), encoding='utf-8').read().split('<style>')[1].split('</style>')[0]
CSS += """
.on.gr{background:#6fd35c} .on.rd{background:#ff7d8c} .on.pu{background:#c4a7ff} .on.gd{background:#f2b84b} .on.bl{background:#5fb2ff}
.step.q{border-color:rgba(255,93,114,.45)} .step.q .num{background:#ff5d72}
.step.a .num{background:#6fd35c} .step.a{border-color:rgba(111,211,92,.4)}
.step.x .num{background:#ff9f43} .step.x{border-color:rgba(255,159,67,.45)}
.step.s .num{background:#5fb2ff} .step.s{border-color:rgba(95,178,255,.4)}
.chain{display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:12px}
.node{background:rgba(236,233,226,.07);border:2px solid rgba(200,168,90,.45);border-radius:16px;padding:10px 14px;text-align:center;font-size:20px;line-height:1.45;color:var(--p);min-width:150px}
.node small{display:block;font-size:16px;color:var(--soft)}
.node.gd{border-color:var(--gold);background:rgba(200,168,90,.16)} .node.gr{border-color:#6fd35c;background:rgba(111,211,92,.12)} .node.rd{border-color:#ff5d72;background:rgba(255,93,114,.12)} .node.bl{border-color:#5fb2ff;background:rgba(95,178,255,.12)}
.arr{font-size:30px;color:var(--gold);font-weight:900}
table.t{width:100%;border-collapse:separate;border-spacing:6px;margin-top:12px;font-size:20px}
table.t th{color:var(--gb);font-size:18px;padding:6px;background:rgba(200,168,90,.12);border-radius:10px}
table.t td{background:rgba(236,233,226,.06);border-radius:10px;padding:8px;text-align:center;color:var(--p);line-height:1.4}
table.t td.ok{background:rgba(111,211,92,.18);color:#bff3b3;font-weight:800} table.t td.no{background:rgba(255,93,114,.18);color:#ffc2ca;font-weight:800}
table.t td.n{color:var(--gb);font-weight:900}
.lst{margin-top:10px;font-size:22px;line-height:1.7;color:var(--soft);padding-right:4px}
.lst div{margin:4px 0} .lst b{color:var(--p)}
.vq{font-family:'Frank Ruhl Libre','David',serif;font-size:24px;color:#ffe6b0}
"""
CSS += "\n/* ===================== 🎨 עיצוב משודרג (נוב׳ 2026) ===================== */\n:root{--ink:#0a0a0a;--card:#141414;--card2:#1a1a1a}\nbody{background:#0a0a0a;width:900px;padding:0 0 30px;font-family:'DejaVu Sans','Heebo','Noto Sans Hebrew',Arial,sans-serif;\n  background-image:radial-gradient(900px 500px at 85% -10%,rgba(200,168,90,.16),transparent 60%),radial-gradient(700px 600px at -10% 40%,rgba(95,178,255,.07),transparent 60%)}\n.hero{position:relative;margin:0 0 30px;padding:40px 40px 34px;text-align:center;overflow:hidden;\n  background:linear-gradient(160deg,#1c1c1c 0%,#141414 55%,#0a0a0a 100%);border-bottom:3px solid rgba(200,168,90,.55)}\n.hero:before{content:'';position:absolute;inset:0;opacity:.18;\n  background-image:repeating-linear-gradient(45deg,rgba(200,168,90,.5) 0 2px,transparent 2px 22px),repeating-linear-gradient(-45deg,rgba(200,168,90,.35) 0 2px,transparent 2px 22px);\n  -webkit-mask-image:radial-gradient(ellipse at center,#000 0%,transparent 70%)}\n.hero .ic{position:relative;display:inline-flex;align-items:center;justify-content:center;width:104px;height:104px;border-radius:50%;font-size:56px;\n  background:radial-gradient(circle at 35% 30%,#4a4334,#161616);border:3px solid var(--gold);box-shadow:0 0 0 8px rgba(200,168,90,.12),0 12px 30px rgba(0,0,0,.45);margin-bottom:14px}\n.hero h1{position:relative;font-size:46px;letter-spacing:-.5px;text-shadow:0 3px 18px rgba(200,168,90,.25)}\n.hero .sub{position:relative;margin:10px auto 0;max-width:760px;font-size:22px;color:#c9c3b8}\n.hero .daf{position:relative;display:inline-block;margin-top:14px;padding:5px 18px;border-radius:30px;background:rgba(200,168,90,.16);border:1px solid rgba(200,168,90,.55);color:var(--gb);font-weight:800;font-size:18px}\n.flow{position:relative;margin:0 34px;padding-right:62px}\n.flow:before{content:'';position:absolute;right:23px;top:18px;bottom:30px;width:4px;border-radius:4px;background:linear-gradient(180deg,var(--gold),rgba(95,178,255,.55) 60%,rgba(200,168,90,.15))}\n.step{background:linear-gradient(180deg,var(--card2),var(--card));border:1px solid rgba(255,255,255,.07);border-radius:22px;padding:20px 24px 22px;margin-bottom:26px;\n  box-shadow:0 10px 26px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.05)}\n.step:after{content:'';position:absolute;right:-1px;top:18px;bottom:18px;width:5px;border-radius:5px;background:var(--rc,var(--gold))}\n.step .num{top:14px;right:-58px;width:46px;height:46px;padding:0;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:21px;\n  background:var(--rc,var(--gold));color:#0a0a0a;border:4px solid #0a0a0a;box-shadow:0 0 0 3px var(--rc,var(--gold)),0 6px 14px rgba(0,0,0,.5)}\n.step .role{display:inline-flex;align-items:center;gap:6px;font-size:16px;font-weight:900;padding:3px 12px;border-radius:20px;\n  color:var(--rc,var(--gold));background:color-mix(in srgb,var(--rc,var(--gold)) 16%,transparent);border:1px solid color-mix(in srgb,var(--rc,var(--gold)) 50%,transparent)}\n.step h2{font-size:29px;margin:8px 0 12px;line-height:1.3}\n.step.q{--rc:#ff5d72;border-color:rgba(255,93,114,.25)} .step.a{--rc:#6fd35c;border-color:rgba(111,211,92,.22)} .step.x{--rc:#ff9f43;border-color:rgba(255,159,67,.25)}\n.step.s{--rc:#5fb2ff;border-color:rgba(95,178,255,.22)} .step.k{--rc:#c4a7ff;border-color:rgba(196,167,255,.22)} .step.n{--rc:#2dd4bf;border-color:rgba(45,212,191,.22)}\n.step.sum{--rc:var(--gold);background:linear-gradient(135deg,rgba(200,168,90,.28),rgba(200,168,90,.07) 60%,rgba(16,16,16,.9));border:2px solid var(--gold);\n  box-shadow:0 0 0 6px rgba(200,168,90,.08),0 14px 34px rgba(0,0,0,.45)}\n.step.sum h2{font-size:30px} .step.sum p{font-size:25px;color:var(--p);line-height:1.6}\n.node{border-radius:18px;padding:12px 16px;min-width:160px;box-shadow:0 6px 16px rgba(0,0,0,.3);background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,.02))}\n.node.gd{background:linear-gradient(180deg,rgba(200,168,90,.26),rgba(200,168,90,.08))} .node.gr{background:linear-gradient(180deg,rgba(111,211,92,.22),rgba(111,211,92,.06))}\n.node.rd{background:linear-gradient(180deg,rgba(255,93,114,.22),rgba(255,93,114,.06))} .node.bl{background:linear-gradient(180deg,rgba(95,178,255,.22),rgba(95,178,255,.06))}\n.node.pu{border-color:#c4a7ff;background:linear-gradient(180deg,rgba(196,167,255,.22),rgba(196,167,255,.06))}\n.chain{gap:6px}\n.arr{display:inline-flex;align-items:center;justify-content:center;min-width:44px;height:44px;border-radius:50%;font-size:24px;background:rgba(200,168,90,.14);border:1px solid rgba(200,168,90,.45)}\n.chain>.node+.node{margin-right:4px}\n.mirror{position:relative;gap:46px}\n.mirror .box{background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,.02));border:1px solid rgba(255,255,255,.08);border-top:4px solid var(--gold);border-radius:18px;padding:14px 12px 16px;box-shadow:0 6px 16px rgba(0,0,0,.3)}\n.mirror .box:nth-child(2){border-top-color:#5fb2ff}\n.mirror:after{content:'⟷';position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;\n  background:#0a0a0a;border:2px solid var(--gold);color:var(--gold);font-size:22px;font-weight:900}\n.mirror h3{font-size:23px}\ntable.t{border-spacing:0 6px}\ntable.t th{background:linear-gradient(180deg,rgba(200,168,90,.3),rgba(200,168,90,.12));color:#ffe6b0;font-size:18px;padding:9px 8px;border-radius:0}\ntable.t th:first-child{border-radius:0 12px 12px 0} table.t th:last-child{border-radius:12px 0 0 12px}\ntable.t td{border-radius:0;background:rgba(255,255,255,.05);padding:10px 8px;border-top:1px solid rgba(255,255,255,.04)}\ntable.t tr:nth-child(odd) td{background:rgba(255,255,255,.08)}\ntable.t td:first-child{border-radius:0 12px 12px 0} table.t td:last-child{border-radius:12px 0 0 12px}\ntable.t tr td.n{color:#ffe6b0;background:rgba(200,168,90,.14)}\n.lst div{position:relative;padding:8px 14px 8px 10px;margin:8px 0;border-radius:12px;background:rgba(255,255,255,.05);border-right:4px solid var(--rc,var(--gold));line-height:1.55}\n.vq{display:inline-block;font-family:'FreeSerif','Frank Ruhl Libre','David',serif;font-size:27px;color:#3a2a14;background:linear-gradient(180deg,#f3e6c8,#e6d3a8);\n  padding:6px 16px;border-radius:10px;box-shadow:inset 0 0 0 1px rgba(122,90,42,.35),0 4px 10px rgba(0,0,0,.3);line-height:1.6}\n.gapnote{background:rgba(255,93,114,.1);border:1px dashed rgba(255,93,114,.5);border-radius:12px;padding:8px}\n.foot{margin:6px 34px 0;text-align:center;color:#7d776a;font-size:16px;font-weight:700;letter-spacing:.5px}\n.foot b{color:#a99a7c}\n.bar{border-radius:10px;box-shadow:inset 0 -3px 0 rgba(0,0,0,.18)}\n"
import re as _re
ROLE_LBL = {"q": "❓ שאלה", "a": "✅ תשובה", "x": "⚡ דחייה", "s": "📜 מקור", "k": "💡 הסבר", "n": "📖 מעשה / ראיה"}
def page(title, sub, body):
    if title.startswith('<svg'):   # דמות עם כיפה בתחילת הכותרת
        k = title.index('</svg>') + 6; ic, t = _re.sub(r'width="[^"]*" height="[^"]*"', 'width="1.45em" height="1.45em"', title[:k]), title[k:].strip()
    else:
        m = _re.match(r'^\s*([^\w\s״"׳<]{1,3})\s*(.*)$', title)   # האמוג׳י בתחילת הכותרת → סמל גדול
        ic, t = (m.group(1), m.group(2)) if m else ('📜', title)
    daf, _, rest = sub.partition(' · ')
    hero = f'<div class="hero"><div class="ic">{ic}</div><h1>{t}</h1><div class="sub">{rest or daf}</div>' + (f'<div class="daf">📖 {daf}</div>' if rest else '') + '</div>'
    foot = f'<div class="foot">גמרא בעיון · <b>{daf}</b></div>'
    return f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{hero}<div class="flow">{body}</div>{foot}</body></html>'
def step(n, h, inner, cls=''):
    role = f'<span class="role">{ROLE_LBL[cls]}</span>' if cls in ROLE_LBL else ''
    return f'<div class="step {cls}"><span class="num">{n}</span>{role}<h2>{h}</h2>{inner}</div>'
def P(t, st=''): return f'<p style="{st}">{t}</p>'
def chips(*c): return ''.join(f'<div class="legend"><span class="chip {k}">{t}</span></div>' for k, t in c)
def two(*ms): return '<div class="two">' + ''.join(f'<div class="m"><div class="w">📍 {w}</div>{t}</div>' for w, t in ms) + '</div>'
VS = '<div class="vs">⚡</div>'
def tl(labels, rows, namew=130, gap=False):
    cols = f'{namew}px ' + ' '.join('1fr' for _ in labels)
    o = f'<div class="tl"><div class="lab" style="grid-template-columns:{cols}"><span></span>' + ''.join(f'<span>{l}</span>' for l in labels) + '</div>'
    for name, color, cells, *g in rows:
        o += f'<div class="row{" gap" if g and g[0] else ""}" style="grid-template-columns:{cols};gap:4px"><span class="name" style="color:{color}">{name}</span>'
        for c in cells:
            k, t = c if isinstance(c, tuple) else (c, '')
            o += f'<div class="bar {"off" if k == "off" else "on " + k}">{t or ("✗" if k == "off" else "✔")}</div>'
        o += '</div>'
    return o + '</div>'
def mirror(*bs): return '<div class="mirror">' + ''.join(f'<div class="box"><h3>{h}</h3><p style="font-size:20px;text-align:center">{t}</p></div>' for h, t in bs) + '</div>'
def chain(*items):
    o = '<div class="chain">'
    for it in items:
        if isinstance(it, str): o += f'<span class="arr">{it}</span>'
        else: o += f'<div class="node {it[0]}">{it[1]}</div>'
    return o + '</div>'
def table(head, rows):
    o = '<table class="t"><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr>'
    for r in rows:
        o += '<tr>' + ''.join((f'<td class="{c[0]}">{c[1]}</td>' if isinstance(c, tuple) else f'<td>{c}</td>') for c in r) + '</tr>'
    return o + '</table>'
def lst(*xs): return '<div class="lst">' + ''.join(f'<div>{x}</div>' for x in xs) + '</div>'
def sumbox(t, n='🏁', h='בשורה אחת'): return f'<div class="step sum"><span class="num">{n}</span><h2>{h}</h2><p>{t}</p></div>'

def upgrade_raw(html):
    """איורים שנכתבו ביד (raw/*.html): אותו עיצוב משודרג — כותרת, קו זרימה ותגית תפקיד"""
    html = html.replace('</style>', CSS.split('/* ===================== 🎨 עיצוב משודרג')[1].split('*/', 1)[1] + '</style>', 1) if '🎨 עיצוב משודרג' in CSS else html
    m = _re.search(r'<h1>(.*?)</h1>\s*<div class="sub">(.*?)</div>', html, _re.S)
    if not m: return html
    t = m.group(1); mm = _re.match(r'^\s*([^\w\s״"׳<]{1,3})\s*(.*)$', t)
    ic, t = (mm.group(1), mm.group(2)) if mm else ('📜', t)
    daf, _, rest = m.group(2).partition(' · ')
    hero = f'<div class="hero"><div class="ic">{ic}</div><h1>{t}</h1><div class="sub">{rest or daf}</div>' + (f'<div class="daf">📖 {daf}</div>' if rest else '') + '</div><div class="flow">'
    html = html[:m.start()] + hero + html[m.end():]
    return html.replace('</body>', f'</div><div class="foot">גמרא בעיון · <b>{daf}</b></div></body>', 1)
