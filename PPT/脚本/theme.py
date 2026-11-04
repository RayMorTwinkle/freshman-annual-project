# -*- coding: utf-8 -*-
"""设计系统：配色、字体、排版工具。所有页面共用。"""
import os
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import ImageFont

# ---------- 画布 ----------
W, H = 13.3333, 7.5

# ---------- 配色 ----------
INK      = RGBColor(0x14, 0x1A, 0x22)   # 主文字
INK2     = RGBColor(0x3D, 0x46, 0x52)   # 次文字
MUTED    = RGBColor(0x77, 0x81, 0x8E)   # 说明
FAINT    = RGBColor(0xA8, 0xB1, 0xBC)
BLUE     = RGBColor(0x00, 0x42, 0x98)   # 哈工大蓝
BLUE_L   = RGBColor(0x2F, 0x6D, 0xBE)   # 浅一档
BLUE_T   = RGBColor(0xE8, 0xEE, 0xF7)   # 极浅填充
PAPER    = RGBColor(0xFA, 0xFA, 0xF7)   # 页面底色
CARD     = RGBColor(0xFF, 0xFF, 0xFF)
LINE     = RGBColor(0xD5, 0xDA, 0xE1)   # 细线
LINE2    = RGBColor(0xE6, 0xE9, 0xEE)
RED      = RGBColor(0xC0, 0x3A, 0x2B)   # 失败 / 警示
RED_T    = RGBColor(0xFA, 0xEC, 0xE9)
TEAL     = RGBColor(0x0B, 0x6B, 0x74)   # 数据
TEAL_T   = RGBColor(0xE6, 0xF1, 0xF1)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)

FONT = "微软雅黑"

# ---------- 版心 ----------
MX      = 0.78            # 左右页边
CW      = W - 2 * MX      # 版心宽 11.77
TOP     = 0.62            # 页眉起点
FOOT_Y  = 7.02


# ---------- 文本度量 ----------
_HEI = "/System/Library/Fonts/Hiragino Sans GB.ttc"
_cache = {}


def _font(size):
    k = int(size * 4)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(_HEI, k, index=2)  # W6
    return _cache[k]


def tw(s, size):
    """文本宽度（磅），size 为磅值。"""
    if not s:
        return 0.0
    return _font(size).getlength(s) / 4.0


def wrap(runs, size, width_pt):
    """runs: [(text, bold)] -> 行列表（每行为字符串）。按 CJK / 拉丁词切分。"""
    text = "".join(r[0] for r in runs)
    toks, buf = [], ""
    for ch in text:
        if ch == "\n":
            if buf:
                toks.append(buf); buf = ""
            toks.append("\n")
        elif ord(ch) < 128 and not ch.isspace():
            buf += ch
        elif ch.isspace():
            if buf: toks.append(buf); buf = ""
            toks.append(" ")
        else:
            if buf: toks.append(buf); buf = ""
            toks.append(ch)
    if buf:
        toks.append(buf)

    lines, cur = [], ""
    for t in toks:
        if t == "\n":
            lines.append(cur); cur = ""
            continue
        cand = cur + t
        if tw(cand.rstrip(), size) > width_pt and cur.strip():
            lines.append(cur.rstrip())
            cur = "" if t == " " else t
        else:
            cur = cand
    lines.append(cur.rstrip())
    return lines


def fit(runs, width_in, height_in, max_size, min_size=8.0, ls=1.12, max_lines=None):
    """二分找到能放进框内的最大字号。runs 可为 [(text,bold)] 或段落列表。"""
    if runs and isinstance(runs[0], list):
        paras = runs
    else:
        paras = [runs]
    width_pt = width_in * 72.0
    height_pt = height_in * 72.0
    size = float(max_size)
    while size >= min_size:
        total = sum(len(wrap(p, size, width_pt)) for p in paras)
        if (max_lines is None or total <= max_lines) and total * size * ls * 1.2 <= height_pt:
            return size, None
        size -= 0.5
    return float(min_size), None


# ---------- 基础构件 ----------
def set_font(run, size, color=INK, bold=False, italic=False, font=FONT):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = color
    f.name = font
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = rPr.makeelement(qn(tag), {})
            rPr.append(el)
        el.set("typeface", font)


def textbox(slide, x, y, w, h):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return tb


def para(tf, first=False, align=PP_ALIGN.LEFT, ls=1.12, space_after=0, space_before=0):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.line_spacing = ls
    p.space_after = Pt(space_after)
    p.space_before = Pt(space_before)
    return p


def add_run(p, text, size, color=INK, bold=False, font=FONT, italic=False):
    r = p.add_run()
    r.text = text
    set_font(r, size, color, bold, italic, font)
    return r


def T(slide, x, y, w, h, content, size=14, color=INK, bold=False,
      align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, ls=1.12, autofit=True,
      max_lines=None, min_size=8.0):
    """文本块。content: str（可用 \n 分段）或 [(text, bold), ...]。自动缩字。"""
    if isinstance(content, str):
        paras = [[(seg, bold)] for seg in content.split("\n")]
    else:
        paras = [[]]
        for t, b in content:
            parts = t.split("\n")
            for i, part in enumerate(parts):
                if i > 0:
                    paras.append([])
                if part:
                    paras[-1].append((part, b))
    if autofit:
        size, _ = fit(paras, w, h, size, min_size, ls, max_lines)
    tb = textbox(slide, x, y, w, h)
    tf = tb.text_frame
    tf.vertical_anchor = anchor
    for i, runs in enumerate(paras):
        p = para(tf, first=(i == 0), align=align, ls=ls)
        for t, b in runs:
            add_run(p, t, size, color, b)
    return tb


def rect(slide, x, y, w, h, fill=None, line=None, lw=1.0, shape=MSO_SHAPE.RECTANGLE,
         dash=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.shadow.inherit = False
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(lw)
        if dash:
            s.line.dash_style = dash
    s.text_frame.word_wrap = True
    return s


def hline(slide, x, y, w, color=LINE, lw=0.9):
    from pptx.enum.shapes import MSO_CONNECTOR
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y),
                                   Inches(x + w), Inches(y))
    c.line.color.rgb = color
    c.line.width = Pt(lw)
    return c


def vline(slide, x, y, h, color=LINE, lw=0.9):
    from pptx.enum.shapes import MSO_CONNECTOR
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y),
                                   Inches(x), Inches(y + h))
    c.line.color.rgb = color
    c.line.width = Pt(lw)
    return c


# ---------- 图片 ----------
def pic_fit(slide, path, x, y, w, h, align="center", valign="middle"):
    """等比缩放到框内（留白），返回实际放置矩形。"""
    from PIL import Image
    iw, ih = Image.open(path).size
    r = min(w / iw, h / ih)
    pw, ph = iw * r, ih * r
    px = x + (w - pw) / 2 if align == "center" else (x if align == "left" else x + w - pw)
    py = y + (h - ph) / 2 if valign == "middle" else (y if valign == "top" else y + h - ph)
    slide.shapes.add_picture(path, Inches(px), Inches(py), Inches(pw), Inches(ph))
    return px, py, pw, ph


def pic_cover(slide, path, x, y, w, h, fx=0.5, fy=0.5):
    """等比裁切填满框。fx/fy 为裁切焦点。"""
    from PIL import Image
    iw, ih = Image.open(path).size
    target = w / h
    src = iw / ih
    if src > target:      # 太宽，裁左右
        cw = ih * target
        cl = (iw - cw) * fx
        ct, cb, cl_, cr = 0, 0, cl / iw, (iw - cw - cl) / iw
    else:                 # 太高，裁上下
        chh = iw / target
        ct_ = (ih - chh) * fy
        cl_, cr = 0, 0
        ct, cb = ct_ / ih, (ih - chh - ct_) / ih
    p = slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
    p.crop_left, p.crop_right = cl_, cr
    p.crop_top, p.crop_bottom = ct, cb
    return p


# ---------- 页面骨架 ----------
def bg(slide, color=PAPER):
    rect(slide, 0, 0, W, H, fill=color)


def head(slide, kicker, title, kicker_color=BLUE, title_size=27, y=0.62,
         sub=None, wide=CW):
    """眉标 + 结论式标题。返回标题底边 y。"""
    T(slide, MX, y, wide, 0.24, kicker, size=10.5, color=kicker_color, bold=True)
    ty = y + 0.30
    size, _ = fit(title, wide, 1.55, title_size, 15, ls=1.16, max_lines=2)
    lines = wrap(title, size, wide * 72.0)
    tb = textbox(slide, MX, ty, wide, 0.05 + len(lines) * size * 1.16 * 1.2 / 72)
    tf = tb.text_frame
    p = para(tf, first=True, ls=1.16)
    for t, b in title:
        add_run(p, t, size, INK, True)
    bottom = ty + len(lines) * size * 1.16 * 1.2 / 72
    return bottom


def footer(slide, n, left="RoboTwin 2.0 × SmolVLA ｜ 大一年度项目结题答辩"):
    hline(slide, MX, FOOT_Y - 0.13, CW, LINE2, 0.75)
    T(slide, MX, FOOT_Y - 0.02, 8.0, 0.22, left, size=8.5, color=FAINT)
    T(slide, W - MX - 0.9, FOOT_Y - 0.02, 0.9, 0.22, f"{n:02d}", size=9,
      color=FAINT, align=PP_ALIGN.RIGHT)


def caption(slide, x, y, w, text, color=MUTED, size=9.5, align=PP_ALIGN.LEFT):
    return T(slide, x, y, w, 0.4, text, size=size, color=color, align=align, ls=1.15)


def tag(slide, x, y, text, color=BLUE, size=8.5, fill=BLUE_T, pad=(0.10, 0.03)):
    """小标签胶囊（方角）。"""
    tw_ = tw(text, size) / 72.0
    w = tw_ + pad[0] * 2
    h = size * 1.45 / 72 + pad[1] * 2
    rect(slide, x, y, w, h, fill=fill)
    T(slide, x, y + pad[1] * 0.6, w, h, text, size=size, color=color,
      bold=True, align=PP_ALIGN.CENTER, autofit=False)
    return w, h
