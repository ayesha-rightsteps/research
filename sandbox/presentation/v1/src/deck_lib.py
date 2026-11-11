"""Small layout helpers on top of python-pptx for deck v1.

One `Deck` object builds three things from the same calls, so they cannot drift apart:
  * the .pptx (native shapes, tables, pictures, speaker notes),
  * deck_v1.md (every slide's on-slide text, picture names and speaker notes),
  * a text-fit report (every text box and table row is measured with the real Arial metrics; anything that would
    overflow its box is listed, because there is no PowerPoint here to look at).
"""
import os, re
from lxml import etree
from PIL import Image, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE
from pptx.oxml.ns import qn

# ------------------------------------------------------------------ design tokens
INK, BLUE, DBLUE = '1F2A37', '2A78D6', '1B4F96'
LBLUE, GREY_T, GREY_BG = 'EAF2FC', '5B6470', 'F3F4F6'
ORANGE, ORANGE_BG, BORDER, WHITE, NAVY = 'EC6A36', 'FDEEE7', 'D9DCE1', 'FFFFFF', '14233A'
FONT = 'Arial'
SW, SH = 13.333, 7.5
LM, RM = 0.55, 0.55
CW = SW - LM - RM

_AR = '/System/Library/Fonts/Supplemental/Arial.ttf'
_AB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
_fonts = {}


def _font(bold, pt):
    k = (bold, pt)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(_AB if bold else _AR, int(round(pt * 10)))
    return _fonts[k]


def rgb(h):
    return RGBColor.from_string(h)


def parse_runs(text):
    """'a **b** c' -> [('a ', False), ('b', True), (' c', False)]"""
    out, bold = [], False
    for part in re.split(r'(\*\*)', text):
        if part == '**':
            bold = not bold
        elif part:
            out.append((part, bold))
    return out


def plain(text):
    return text.replace('**', '')


def wrap_lines(text, pt, width_in, bold=False):
    """Number of wrapped lines for one paragraph (bold segments measured bold)."""
    width = width_in * 72 * 10
    words = []
    for seg, b in parse_runs(text):
        for w in re.findall(r'\s*\S+\s*', seg):
            words.append((w, b or bold))
    lines, cur = 1, 0.0
    for w, b in words:
        wl = _font(b, pt).getlength(w.rstrip())
        full = _font(b, pt).getlength(w)
        if cur > 0 and cur + wl > width:
            lines += 1
            cur = 0.0
        cur += full
    return lines


def text_height_in(paras, pt, width_in, bold=False, spacing=1.15, space_after_pt=0):
    n = sum(wrap_lines(p, pt, width_in, bold) for p in paras)
    return (n * pt * spacing + max(len(paras) - 1, 0) * space_after_pt) / 72.0


class Deck:
    def __init__(self, total_hint=None):
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = Inches(SW), Inches(SH)
        self.blank = self.prs.slide_layouts[6]
        self.warnings = []
        self.md = []
        self.n = 0
        self.cur = None
        self.total = total_hint

    # ---------------------------------------------------------------- slide lifecycle
    def new_slide(self, key, title, section, dark=False, number=True):
        self.n += 1
        self.cur = dict(key=key, title=title, section=section, items=[], notes='')
        s = self.prs.slides.add_slide(self.blank)
        self.s = s
        self.key = key
        if dark:
            bg = s.background.fill
            bg.solid()
            bg.fore_color.rgb = rgb(NAVY)
        if not dark and title:
            self._title(title, section)
        if number and not dark:
            self._footer()
        self.md.append(self.cur)
        return s

    def _title(self, title, section):
        bar = self.s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(LM), Inches(0.46), Inches(0.09), Inches(0.9))
        self._flat(bar, BLUE)
        self._text(LM + 0.25, 0.38, CW - 0.25, 1.06, [title], 27, bold=True, color=INK, anchor='middle',
                   check='title', spacing=1.1)
        self._text(SW - RM - 4.5, 0.12, 4.5, 0.26, [section.upper()], 9.5, color=GREY_T, align='right',
                   check=None, bold=True)

    def _footer(self):
        ln = self.s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(LM), Inches(7.02), Inches(SW - RM), Inches(7.02))
        ln.line.color.rgb = rgb(BORDER); ln.line.width = Pt(0.75)
        self._text(LM, 7.07, 8, 0.3, ['Priority Arbitration Head (PAH) · MS thesis · Ayesha Khalil'], 10, color=GREY_T, check=None)
        self._text(SW - RM - 2, 7.07, 2, 0.3, [str(self.n)], 10, color=GREY_T, align='right', check=None)

    def notes(self, text):
        self.cur['notes'] = text.strip()
        self.s.notes_slide.notes_text_frame.text = text.strip()

    # ---------------------------------------------------------------- primitives
    def _flat(self, shape, fill=None, line=None, line_w=0.75):
        shape.shadow.inherit = False
        if fill:
            shape.fill.solid(); shape.fill.fore_color.rgb = rgb(fill)
        else:
            shape.fill.background()
        if line:
            shape.line.color.rgb = rgb(line); shape.line.width = Pt(line_w)
        else:
            shape.line.fill.background()

    def _fill_tf(self, tf, paras, pt, bold, color, align, spacing, space_after, bullet=False):
        tf.word_wrap = True
        for i, p in enumerate(paras):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = {'left': PP_ALIGN.LEFT, 'center': PP_ALIGN.CENTER, 'right': PP_ALIGN.RIGHT}[align]
            para.line_spacing = spacing
            para.space_after = Pt(space_after)
            if bullet:
                pPr = para._p.get_or_add_pPr()
                pPr.set('marL', str(int(0.26 * 914400))); pPr.set('indent', str(int(-0.26 * 914400)))
                bu = etree.SubElement(pPr, qn('a:buClr')); c = etree.SubElement(bu, qn('a:srgbClr')); c.set('val', BLUE)
                bf = etree.SubElement(pPr, qn('a:buFont')); bf.set('typeface', 'Arial')
                bc = etree.SubElement(pPr, qn('a:buChar')); bc.set('char', '•')
            for seg, b in parse_runs(p):
                r = para.add_run(); r.text = seg
                f = r.font; f.name = FONT; f.size = Pt(pt); f.bold = bool(b or bold); f.color.rgb = rgb(color)

    def _text(self, x, y, w, h, paras, pt, bold=False, color=INK, align='left', anchor='top', bullet=False,
              spacing=1.1, space_after=0, check='box', inset=0.05):
        tb = self.s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.margin_left = tf.margin_right = Inches(inset); tf.margin_top = tf.margin_bottom = Inches(0.03)
        tf.vertical_anchor = {'top': MSO_ANCHOR.TOP, 'middle': MSO_ANCHOR.MIDDLE, 'bottom': MSO_ANCHOR.BOTTOM}[anchor]
        self._fill_tf(tf, paras, pt, bold, color, align, spacing, space_after, bullet)
        if check:
            avail = w - 2 * inset - (0.26 if bullet else 0)
            need = text_height_in(paras, pt, avail, bold, spacing * 1.17, space_after) + 0.06
            if need > h + 0.02:
                self.warnings.append('slide %d [%s] %s: text needs %.2f in, box has %.2f in: %s'
                                     % (self.n, self.key, check, need, h, plain(paras[0])[:60]))
        return tb

    def _log(self, kind, content):
        self.cur['items'].append((kind, content))

    # ---------------------------------------------------------------- content blocks
    def text(self, x, y, w, h, paras, pt=18, bold=False, color=INK, align='left', anchor='top', bullet=False,
             space_after=6, log=True):
        if isinstance(paras, str):
            paras = [paras]
        self._text(x, y, w, h, paras, pt, bold, color, align, anchor, bullet, space_after=space_after, check='text')
        if log:
            self._log('bullets' if bullet else 'text', paras)

    def card(self, x, y, w, h, head, body, fill=GREY_BG, head_color=DBLUE, head_pt=16, body_pt=14, accent=BLUE,
             line=None, body_color=INK, body_space=3):
        shp = self.s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        shp.adjustments[0] = min(0.2, 0.14 / min(w, h))
        self._flat(shp, fill, line)
        if accent:
            bar = self.s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y + 0.12), Inches(0.07), Inches(h - 0.24))
            self._flat(bar, accent)
        hh = text_height_in([head], head_pt, w - 0.4, True, 1.2) + 0.04
        self._text(x + 0.2, y + 0.1, w - 0.35, hh + 0.02, [head], head_pt, bold=True, color=head_color,
                   check='card-head', spacing=1.05)
        paras = body if isinstance(body, list) else [body]
        self._text(x + 0.2, y + 0.1 + hh + 0.04, w - 0.35, h - hh - 0.2, paras, body_pt, color=body_color,
                   check='card-body', space_after=body_space, spacing=1.05)
        self._log('card', (plain(head), [plain(p) for p in paras]))

    def callout(self, x, y, w, h, text, kind='blue', pt=16, align='left'):
        fill, bar = (LBLUE, BLUE) if kind == 'blue' else (ORANGE_BG, ORANGE)
        shp = self.s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        shp.adjustments[0] = min(0.2, 0.12 / min(w, h))
        self._flat(shp, fill)
        b = self.s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y + 0.1), Inches(0.07), Inches(h - 0.2))
        self._flat(b, bar)
        paras = text if isinstance(text, list) else [text]
        self._text(x + 0.2, y, w - 0.3, h, paras, pt, anchor='middle', check='callout', align=align, spacing=1.05,
                   space_after=2)
        self._log('callout', [plain(p) for p in paras])

    def chip(self, x, y, w, h, big, small, fill=LBLUE, big_color=DBLUE, big_pt=22, small_pt=12):
        shp = self.s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        shp.adjustments[0] = 0.1
        self._flat(shp, fill)
        bh = big_pt * 1.45 / 72
        self._text(x + 0.1, y + 0.08, w - 0.2, bh, [big], big_pt, bold=True, color=big_color, align='center', check='chip-big')
        self._text(x + 0.1, y + 0.1 + bh, w - 0.2, h - bh - 0.14, [small], small_pt, color=INK, align='center',
                   check='chip-small', spacing=1.05)
        self._log('chip', (plain(big), plain(small)))

    def box(self, x, y, w, h, text, fill=GREY_BG, line=None, color=INK, pt=14, bold=False, dashed=False, round_=0.1,
            anchor='middle', align='center', log=True):
        shp = self.s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        shp.adjustments[0] = round_
        self._flat(shp, fill, line, 1.25)
        if dashed:
            shp.line.dash_style = MSO_LINE.DASH
        paras = text if isinstance(text, list) else [text]
        if paras:
            self._text(x + 0.05, y, w - 0.1, h, paras, pt, bold=bold, color=color, align=align, anchor=anchor,
                       check='box', spacing=1.05, space_after=1)
        if log:
            self._log('box', [plain(p) for p in paras])
        return shp

    def arrow(self, x1, y1, x2, y2, color=GREY_T, width=1.75, dashed=False):
        c = self.s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        c.line.color.rgb = rgb(color); c.line.width = Pt(width)
        if dashed:
            c.line.dash_style = MSO_LINE.DASH
        ln = c.line._get_or_add_ln()
        t = etree.SubElement(ln, qn('a:tailEnd')); t.set('type', 'triangle'); t.set('w', 'med'); t.set('len', 'med')

    def image(self, path, x, y, w, h, caption=None, align='center', valign='center'):
        """Fit the picture inside (x, y, w, h) keeping its aspect ratio."""
        with Image.open(path) as im:
            iw, ih = im.size
        sc = min(w / iw, h / ih)
        pw, ph = iw * sc, ih * sc
        px = x + (w - pw) / 2 if align == 'center' else x
        py = y + (h - ph) / 2 if valign == 'center' else y
        self.s.shapes.add_picture(path, Inches(px), Inches(py), Inches(pw), Inches(ph))
        self._log('image', os.path.basename(path))
        return px, py, pw, ph

    def table(self, x, y, col_w, rows, pt=13, head_pt=None, max_h=None, header=True, zebra=False, bold_first_col=False,
              highlight_rows=(), sub_rows=(), align=None, pad=0.07, min_row=0.0):
        """rows: list of lists of strings. sub_rows: row indexes drawn as a merged group label."""
        head_pt = head_pt or pt
        nr, nc = len(rows), len(col_w)
        heights = []
        for ri, r in enumerate(rows):
            h = 0
            if ri in sub_rows:
                h = text_height_in([r[0]], pt - 1, sum(col_w) - 0.2, True, 1.2) + 2 * pad
            else:
                for ci, cell in enumerate(r):
                    p = head_pt if (header and ri == 0) else pt
                    b = (header and ri == 0) or (bold_first_col and ci == 0)
                    h = max(h, text_height_in(cell.split('\n'), p, col_w[ci] - 0.2, b, 1.2) + 2 * pad)
            heights.append(max(h, min_row))
        total = sum(heights)
        if max_h and total > max_h + 0.01:
            self.warnings.append('slide %d [%s] table: needs %.2f in, allowed %.2f in' % (self.n, self.key, total, max_h))
        gf = self.s.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(sum(col_w)), Inches(total))
        tbl = gf.table
        tblPr = tbl._tbl.tblPr
        sid = tblPr.find(qn('a:tableStyleId'))
        if sid is not None:
            sid.text = '{2D5ABB26-0587-4C30-8999-92F81FD0307C}'
        tbl.first_row = False; tbl.horz_banding = False
        for ci, w in enumerate(col_w):
            tbl.columns[ci].width = Inches(w)
        for ri, r in enumerate(rows):
            tbl.rows[ri].height = Inches(heights[ri])
            is_head = header and ri == 0
            is_sub = ri in sub_rows
            is_hi = ri in highlight_rows
            if is_sub:
                tbl.cell(ri, 0).merge(tbl.cell(ri, nc - 1))
            for ci in range(nc):
                cell = tbl.cell(ri, ci)
                if is_sub and ci > 0:
                    continue
                txt = r[ci] if ci < len(r) else ''
                cell.margin_left = cell.margin_right = Inches(0.1)
                cell.margin_top = cell.margin_bottom = Inches(pad)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                tcPr = cell._tc.get_or_add_tcPr()
                lnB = etree.SubElement(tcPr, qn('a:lnB')); lnB.set('w', '9525')
                sf = etree.SubElement(lnB, qn('a:solidFill')); cc = etree.SubElement(sf, qn('a:srgbClr'))
                cc.set('val', INK if is_head else BORDER)
                fill = None
                if is_head:
                    fill = WHITE
                elif is_sub:
                    fill = GREY_BG
                elif is_hi:
                    fill = LBLUE
                elif zebra and ri % 2 == 0:
                    fill = 'FAFAFA'
                if fill:
                    cell.fill.solid(); cell.fill.fore_color.rgb = rgb(fill)
                else:
                    cell.fill.background()
                tf = cell.text_frame
                tf.word_wrap = True
                paras = txt.split('\n')
                al = (align[ci] if align else 'left')
                p_pt = head_pt if is_head else (pt - 1 if is_sub else pt)
                col = INK if not is_sub else GREY_T
                self._fill_tf(tf, paras, p_pt, bold=(is_head or is_sub or is_hi or (bold_first_col and ci == 0)),
                              color=col, align=al, spacing=1.05, space_after=0)
        self._log('table', [[plain(c) for c in r] for r in rows])
        return total

    # ---------------------------------------------------------------- output
    def save(self, pptx_path, meta):
        cp = self.prs.core_properties
        cp.title, cp.author, cp.subject = meta['title'], meta['author'], meta['subject']
        self.prs.save(pptx_path)

    def write_md(self, md_path, head, tail=''):
        out = [head]
        for i, sl in enumerate(self.md, 1):
            out.append('\n---\n\n## %s%s\n' % ('Slide %d — ' % i if not sl['key'].startswith('app') else '', sl['title'] or sl['key']))
            out.append('*Section: %s*\n' % sl['section'])
            imgs = [c for k, c in sl['items'] if k == 'image']
            body = []
            for kind, c in sl['items']:
                if kind == 'text':
                    body.extend(c)
                elif kind == 'bullets':
                    body.extend('- ' + x for x in c)
                elif kind == 'card':
                    body.append('- **%s** — %s' % (c[0], ' '.join(c[1])))
                elif kind == 'callout':
                    body.append('> ' + ' '.join(c))
                elif kind == 'chip':
                    body.append('- **%s** — %s' % c)
                elif kind == 'box':
                    body.append('- [box] ' + ' / '.join(c))
                elif kind == 'table':
                    rows = c
                    body.append('')
                    body.append('| ' + ' | '.join(x.replace('\n', ' ') for x in rows[0]) + ' |')
                    body.append('|' + '---|' * len(rows[0]))
                    for r in rows[1:]:
                        body.append('| ' + ' | '.join(x.replace('\n', ' ') for x in r) + ' |')
                    body.append('')
            if body:
                out.append('**On slide:**\n')
                out.append('\n'.join(body) + '\n')
            for im in imgs:
                out.append('**Image:** `images/%s`\n' % im)
            if sl['notes']:
                out.append('**Say:** %s\n' % sl['notes'].replace('\n\n', '\n\n> '))
        out.append(tail)
        open(md_path, 'w').write('\n'.join(out))
