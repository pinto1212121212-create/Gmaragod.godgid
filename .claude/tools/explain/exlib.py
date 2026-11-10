CSS = open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'raw', 'rabba-4b.html'), encoding='utf-8').read().split('<style>')[1].split('</style>')[0]
CSS += """
.on.gr{background:#6fd35c} .on.rd{background:#ff7d8c} .on.pu{background:#c4a7ff} .on.gd{background:#f2b84b} .on.bl{background:#5fb2ff}
.step.q{border-color:rgba(255,93,114,.45)} .step.q .num{background:#ff5d72}
.step.a .num{background:#6fd35c} .step.a{border-color:rgba(111,211,92,.4)}
.step.x .num{background:#ff9f43} .step.x{border-color:rgba(255,159,67,.45)}
.step.s .num{background:#5fb2ff} .step.s{border-color:rgba(95,178,255,.4)}
.chain{display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:12px}
.node{background:rgba(236,233,226,.07);border:2px solid rgba(232,183,109,.45);border-radius:16px;padding:10px 14px;text-align:center;font-size:20px;line-height:1.45;color:var(--p);min-width:150px}
.node small{display:block;font-size:16px;color:var(--soft)}
.node.gd{border-color:var(--gold);background:rgba(232,183,109,.16)} .node.gr{border-color:#6fd35c;background:rgba(111,211,92,.12)} .node.rd{border-color:#ff5d72;background:rgba(255,93,114,.12)} .node.bl{border-color:#5fb2ff;background:rgba(95,178,255,.12)}
.arr{font-size:30px;color:var(--gold);font-weight:900}
table.t{width:100%;border-collapse:separate;border-spacing:6px;margin-top:12px;font-size:20px}
table.t th{color:var(--gb);font-size:18px;padding:6px;background:rgba(232,183,109,.12);border-radius:10px}
table.t td{background:rgba(236,233,226,.06);border-radius:10px;padding:8px;text-align:center;color:var(--p);line-height:1.4}
table.t td.ok{background:rgba(111,211,92,.18);color:#bff3b3;font-weight:800} table.t td.no{background:rgba(255,93,114,.18);color:#ffc2ca;font-weight:800}
table.t td.n{color:var(--gb);font-weight:900}
.lst{margin-top:10px;font-size:22px;line-height:1.7;color:var(--soft);padding-right:4px}
.lst div{margin:4px 0} .lst b{color:var(--p)}
.vq{font-family:'Frank Ruhl Libre','David',serif;font-size:24px;color:#ffe6b0}
"""
def page(title, sub, body):
    return f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>{CSS}</style></head><body><h1>{title}</h1><div class="sub">{sub}</div>{body}</body></html>'
def step(n, h, inner, cls=''):
    return f'<div class="step {cls}"><span class="num">{n}</span><h2>{h}</h2>{inner}</div>'
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
