def head(x, beard=None, long=False, kc='#1b2654'):
    b = ''
    if beard:
        b = (f'<path d="M{x-13} 25c0 {13 if long else 9} 6 {20 if long else 16} 13 {20 if long else 16}s13-{7 if long else 7} 13-{20 if long else 16}'
             f'c-3 5-8 7-13 7s-10-2-13-7z" fill="{beard}"/>')
    side = f'<path d="M{x-13} 22c-1 4 0 7 2 9M{x+13} 22c1 4 0 7-2 9" stroke="{beard or "#4a3423"}" stroke-width="3" fill="none" stroke-linecap="round"/>'
    smile = '' if beard else f'<path d="M{x-4} 31q4 3 8 0" stroke="#9a5a3a" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
    return (f'<circle cx="{x}" cy="25" r="13" fill="#f2c9a0"/>{side}{b}{smile}'
            f'<circle cx="{x-4.5}" cy="24" r="1.7" fill="#2a1d12"/><circle cx="{x+4.5}" cy="24" r="1.7" fill="#2a1d12"/>'
            f'<path d="M{x-11.5} 17.5a11.5 7.5 0 0 1 23 0z" fill="{kc}"/><path d="M{x-11.5} 17.5h23" stroke="#e8b76d" stroke-width="1.3"/>')
def svg(body, w=48):
    return (f'<svg class="kip" viewBox="0 0 {w} 48" width="{w/40:.2f}em" height="1.2em" style="vertical-align:-.25em" aria-hidden="true">{body}</svg>')
KIP = {
 'man': svg(head(24, '#5a3b22')),
 'elder': svg(head(24, '#ece7dc', long=True)),
 'young': svg(head(24)),
 'two': svg(head(25, '#5a3b22', kc='#3a2a5a') + head(55, '#6b4a2a'), 80),
}
