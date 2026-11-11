"""Rasterise deck_v1.pptx slide by slide with PIL, straight from the shapes' coordinates (no PowerPoint needed).

It is a layout check, not a pixel-exact render: boxes, fills, lines, arrows, pictures and tables are drawn where the
file puts them, and text is wrapped with the real Arial metrics. It cannot show PowerPoint's own line breaking, so it is
deliberately a little conservative.
    python src/preview.py <out_dir> [slide numbers...]
"""
import os, re, sys
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE

EMU = 914400
SC = 150  # pixels per inch -> 1999 x 1125
AR = '/System/Library/Fonts/Supplemental/Arial.ttf'
AB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
_f = {}


def font(pt, bold):
    k = (round(pt * SC / 72), bold)
    if k not in _f:
        _f[k] = ImageFont.truetype(AB if bold else AR, k[0])
    return _f[k]


def col(rgbobj, default=None):
    try:
        return '#' + str(rgbobj)
    except Exception:
        return default


def fill_of(shape):
    try:
        if shape.fill.type == 1:
            return col(shape.fill.fore_color.rgb)
    except Exception:
        pass
    return None


def line_of(shape):
    try:
        if shape.line.fill.type == 1:
            return col(shape.line.color.rgb), max(1, int(shape.line.width / 12700 * SC / 72))
    except Exception:
        pass
    return None, 0


def draw_text(dr, tf, x, y, w, h, anchor, default_color='#1F2A37'):
    lines = []   # (list of (text, font, color)), line_height, align
    for p in tf.paragraphs:
        runs = [(r.text, r.font.size.pt if r.font.size else 14, bool(r.font.bold),
                 col(r.font.color.rgb) if r.font.color and r.font.color.type else default_color) for r in p.runs]
        if not runs:
            continue
        pt = max(r[1] for r in runs)
        indent = 0
        pPr = p._p.pPr
        if pPr is not None and pPr.get('marL'):
            indent = int(pPr.get('marL')) / EMU * SC
        bullet = pPr is not None and pPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}buChar') is not None
        ls = p.line_spacing or 1.0
        words = []
        for t, ptt, b, c in runs:
            for wd in re.findall(r'\s*\S+\s*', t):
                words.append((wd, font(ptt, b), c))
        maxw = w - indent
        cur, curw, out = [], 0, []
        for wd, f, c in words:
            wl = f.getlength(wd.rstrip()); full = f.getlength(wd)
            if cur and curw + wl > maxw:
                out.append(cur); cur, curw = [], 0
            cur.append((wd, f, c)); curw += full
        if cur:
            out.append(cur)
        sa = (p.space_after.pt * SC / 72) if p.space_after else 0
        for i, ln in enumerate(out):
            lines.append((ln, pt * SC / 72 * 1.15 * ls, p.alignment, indent, bullet and i == 0, sa if i == len(out) - 1 else 0))
    total = sum(l[1] + l[5] for l in lines)
    yy = y if anchor != 'middle' else y + (h - total) / 2
    if anchor == 'bottom':
        yy = y + h - total
    for ln, lh, al, indent, bul, sa in lines:
        wsum = sum(f.getlength(t.rstrip() if k == len(ln) - 1 else t) for k, (t, f, c) in enumerate(ln))
        xx = x + indent
        if al == 2:     # center
            xx = x + indent + ((w - indent) - wsum) / 2
        elif al == 3:   # right
            xx = x + w - wsum
        if bul:
            dr.text((x + indent - 0.2 * SC, yy), '•', font=ln[0][1], fill='#2A78D6')
        for k, (t, f, c) in enumerate(ln):
            dr.text((xx, yy), t, font=f, fill=c)
            xx += f.getlength(t)
        yy += lh + sa
    return yy - y, h


def render(slide, path, overflow_log, idx):
    W, H = int(13.333 * SC), int(7.5 * SC)
    bg = '#FFFFFF'
    try:
        if slide.background.fill.type == 1:
            bg = col(slide.background.fill.fore_color.rgb)
    except Exception:
        pass
    im = Image.new('RGB', (W, H), bg)
    dr = ImageDraw.Draw(im)
    for sh in slide.shapes:
        x, y, w, h = [v / EMU * SC for v in (sh.left, sh.top, sh.width, sh.height)]
        if sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
            pic = Image.open(sh.image.blob if False else __import__('io').BytesIO(sh.image.blob)).convert('RGB')
            pic = pic.resize((max(1, int(w)), max(1, int(h))), Image.LANCZOS)
            im.paste(pic, (int(x), int(y)))
        elif sh.shape_type == MSO_SHAPE_TYPE.LINE or sh.__class__.__name__ == 'Connector':
            c, lw = line_of(sh)
            bx, by, ex, ey = [v / EMU * SC for v in (sh.begin_x, sh.begin_y, sh.end_x, sh.end_y)]
            dash = sh.line.dash_style is not None
            if dash:
                import math
                L = math.hypot(ex - bx, ey - by); n = int(L / 14)
                for i in range(0, n, 2):
                    a, b = i / max(n, 1), min((i + 1) / max(n, 1), 1)
                    dr.line([(bx + (ex - bx) * a, by + (ey - by) * a), (bx + (ex - bx) * b, by + (ey - by) * b)], fill=c or '#888', width=max(lw, 2))
            else:
                dr.line([(bx, by), (ex, ey)], fill=c or '#888', width=max(lw, 2))
            if sh.line._get_or_add_ln().find('{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd') is not None:
                import math
                ang = math.atan2(ey - by, ex - bx)
                for da in (2.6, -2.6):
                    dr.line([(ex, ey), (ex + 16 * math.cos(ang + da), ey + 16 * math.sin(ang + da))], fill=c or '#888', width=max(lw, 2))
        elif sh.has_table if hasattr(sh, 'has_table') else False:
            tbl = sh.table
            yy = y
            for r in tbl.rows:
                rh = r.height / EMU * SC
                xx = x
                for ci, cell in enumerate(tbl.columns):
                    cw = cell.width / EMU * SC
                    c = r.cells[ci]
                    if c.is_spanned:
                        xx += cw; continue
                    span_w = sum(tbl.columns[k].width for k in range(ci, ci + (c.span_width if c.is_merge_origin else 1))) / EMU * SC
                    try:
                        if c.fill.type == 1:
                            dr.rectangle([xx, yy, xx + span_w, yy + rh], fill=col(c.fill.fore_color.rgb))
                    except Exception:
                        pass
                    dr.line([(xx, yy + rh), (xx + span_w, yy + rh)], fill='#D9DCE1', width=1)
                    used, avail = draw_text(dr, c.text_frame, xx + 0.1 * SC, yy + 0.07 * SC, span_w - 0.2 * SC, rh - 0.14 * SC, 'middle')
                    if used > avail + 3:
                        overflow_log.append('slide %d table cell overflows' % idx)
                    xx += cw
                yy += rh
        elif sh.has_text_frame or sh.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
            f = fill_of(sh)
            lc, lw = line_of(sh)
            try:
                rounded = 'ROUNDED' in str(sh.auto_shape_type)
            except Exception:
                rounded = False
            box = [x, y, x + w, y + h]
            if f or lc:
                if rounded:
                    try:
                        rad = sh.adjustments[0] * min(w, h)
                    except Exception:
                        rad = min(w, h) * 0.1
                    dr.rounded_rectangle(box, radius=rad, fill=f, outline=lc, width=lw or 1)
                else:
                    dr.rectangle(box, fill=f, outline=lc, width=lw or 1)
            if sh.has_text_frame and sh.text_frame.text.strip():
                tf = sh.text_frame
                anch = {1: 'top', 3: 'middle', 4: 'bottom'}.get(int(tf.vertical_anchor) if tf.vertical_anchor else 1, 'top')
                used, avail = draw_text(dr, tf, x + 0.05 * SC, y + 0.03 * SC, w - 0.1 * SC, h - 0.06 * SC, anch)
                if used > avail + 4:
                    overflow_log.append('slide %d: text overflows its box (%.2f in used, %.2f in box): %s' % (idx, used / SC, avail / SC, tf.text[:50].replace('\n', ' ')))
    im.save(path)


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.abspath(sys.argv[1]); os.makedirs(out, exist_ok=True)
    only = [int(a) for a in sys.argv[2:]]
    prs = Presentation(os.path.join(here, '..', 'deck_v1.pptx'))
    log = []
    for i, s in enumerate(prs.slides, 1):
        if only and i not in only:
            continue
        render(s, os.path.join(out, 's%02d.png' % i), log, i)
    print('rendered; overflow notes:', len(log))
    for l in log:
        print('  ', l)
