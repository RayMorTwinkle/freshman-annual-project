# -*- coding: utf-8 -*-
"""通用图元：箭头、条形图、种子格、数值块。"""
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from theme import (INK, INK2, MUTED, FAINT, BLUE, BLUE_L, BLUE_T, LINE, LINE2,
                   RED, RED_T, TEAL, TEAL_T, WHITE, CARD, PAPER,
                   rect, T, tw, hline, vline)


def arrow(slide, x1, y1, x2, y2, color=FAINT, lw=1.0):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1),
                                   Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(lw)
    ln = c.line._get_or_add_ln()
    tail = ln.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'sm', 'len': 'med'})
    ln.append(tail)
    return c


def chip(slide, x, y, text, size=10, color=BLUE, fill=BLUE_T, h=None, pad=0.13):
    w = tw(text, size) / 72.0 + pad * 2
    hh = h or (size * 1.55 / 72)
    rect(slide, x, y, w, hh, fill=fill)
    T(slide, x, y, w, hh, text, size=size, color=color, bold=True,
      align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, autofit=False)
    return w


def chip_row(slide, x, y, items, w_gap=0.12, h=0.30, size=10,
             color=BLUE, fill=BLUE_T, max_w=None):
    cx = x
    for it in items:
        w = tw(it, size) / 72.0 + 0.26
        if max_w and cx + w > x + max_w:
            cx = x
            y += h + 0.10
        chip(slide, cx, y, it, size=size, color=color, fill=fill, h=h)
        cx += w + w_gap
    return y + h


def bignum(slide, x, y, w, num, label, sub=None, size=32, color=INK, label_size=10.5):
    T(slide, x, y, w, size * 1.35 / 72, num, size=size, color=color, bold=True, autofit=False)
    T(slide, x, y + size * 1.28 / 72, w, 0.26, label, size=label_size, color=MUTED)
    if sub:
        T(slide, x, y + size * 1.28 / 72 + 0.28, w, 0.30, sub, size=9.5, color=FAINT, ls=1.1)


def stat_block(slide, x, y, value, label, size=30, color=BLUE, gap=0.28, w=None):
    """返回占用宽度，便于按测量值横向排布。"""
    ww = w or max(tw(value, size) / 72.0, tw(label, 9) / 72.0)
    T(slide, x, y, ww + 0.1, size * 1.3 / 72, value, size=size, color=color,
      bold=True, autofit=False)
    T(slide, x, y + size * 1.24 / 72, ww + 0.1, 0.24, label, size=9, color=MUTED, autofit=False)
    return ww + gap


def bar_chart(slide, x, y, w, h, bars, maxv, axis_color=LINE):
    """bars: [(label, value, color, note)]  竖直柱状图，原生形状。"""
    base_y = y + h
    hline(slide, x, base_y, w, axis_color, 1.0)
    n = len(bars)
    slot = w / n
    bw = min(1.15, slot * 0.44)
    for i, (label, val, color, note) in enumerate(bars):
        cx = x + slot * (i + 0.5)
        bh = h * (val / maxv) * 0.80
        rect(slide, cx - bw / 2, base_y - bh, bw, bh, fill=color)
        T(slide, cx - bw / 2, base_y - bh - 0.48, bw, 0.36,
          note or str(val), size=19, color=color, bold=True,
          align=PP_ALIGN.CENTER, autofit=False)
        T(slide, cx - slot / 2, base_y + 0.10, slot, 0.26, label, size=10.5,
          color=INK2, align=PP_ALIGN.CENTER, autofit=False)


def seed_grid(slide, x, y, cw, ch, gap, rows, header=None,
              success_color=BLUE, fail_color=RED):
    """rows: [(row_label, [bool,...])]"""
    for c, h_ in enumerate(header or []):
        T(slide, x + 0.78 + c * (cw + gap), y - 0.30, cw, 0.24, h_, size=8.8,
          color=FAINT, align=PP_ALIGN.CENTER, autofit=False)
    for r, (label, cells) in enumerate(rows):
        ry = y + r * (ch + 0.38)
        T(slide, x, ry, 0.66, ch, label, size=9.5, color=MUTED,
          align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, autofit=False)
        for c, ok in enumerate(cells):
            cx = x + 0.78 + c * (cw + gap)
            if ok:
                rect(slide, cx, ry, cw, ch, fill=success_color)
                T(slide, cx, ry, cw, ch, "√", size=13, color=WHITE, bold=True,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, autofit=False)
            else:
                rect(slide, cx, ry, cw, ch, fill=RED_T, line=fail_color, lw=1.0)
                T(slide, cx, ry, cw, ch, "×", size=13, color=fail_color, bold=True,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, autofit=False)


def legend_sq(slide, x, y, color, label, filled=True, size=9):
    if filled:
        rect(slide, x, y + 0.07, 0.115, 0.115, fill=color)
    else:
        rect(slide, x, y + 0.07, 0.115, 0.115, fill=None, line=color, lw=1.0)
    T(slide, x + 0.20, y, 1.2, 0.24, label, size=size, color=MUTED, autofit=False)
    return 0.20 + tw(label, size) / 72.0 + 0.18


def note_card(slide, x, y, w, h, title, body, accent=RED, fill=None, title_size=10):
    rect(slide, x, y, w, h, fill=fill or RED_T)
    rect(slide, x, y, 0.05, h, fill=accent)
    T(slide, x + 0.26, y + 0.18, w - 0.46, 0.26, title, size=title_size,
      color=accent, bold=True, autofit=False)
    T(slide, x + 0.26, y + 0.50, w - 0.46, h - 0.62, body, size=10,
      color=INK2, ls=1.30)
