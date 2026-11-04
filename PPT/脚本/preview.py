# -*- coding: utf-8 -*-
"""把生成的 PPTX 还原成 PNG，用于人工目视检查版式。"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Emu

sys.path.insert(0, os.path.dirname(__file__))
from theme import tw

SCALE = 130.0  # px per inch
F_REG = "/System/Library/Fonts/Hiragino Sans GB.ttc"
_fc = {}


def F(pt, bold):
    k = (round(pt * SCALE / 72.0), bold)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(F_REG, max(1, k[0]), index=2 if bold else 0)
    return _fc[k]


def col(shape, attr):
    try:
        f = getattr(shape, attr)
        if f.type is None:
            return None
        return tuple(f.fore_color.rgb)
    except Exception:
        return None


def line_col(shape):
    try:
        if shape.line.fill.type is None or shape.line.fill.type == 5:
            return None, 0
    except Exception:
        return None, 0
    try:
        return tuple(shape.line.color.rgb), max(1, int(shape.line.width.pt * SCALE / 72))
    except Exception:
        return None, 0


def wrap_px(runs, px_w):
    """runs: [(text, font)] -> lines of [(text, font)]"""
    lines, cur, curw = [], [], 0.0
    for text, font in runs:
        buf = ""
        for ch in text:
            w = font.getlength(ch)
            if curw + w > px_w and (cur or buf):
                if buf:
                    cur.append((buf, font)); buf = ""
                lines.append(cur); cur = []; curw = 0.0
            buf += ch
            curw += w
        if buf:
            cur.append((buf, font))
    lines.append(cur)
    return lines


def draw_text(d, shape, y0, h0, w0, x0):
    tf = shape.text_frame
    anchor = tf.vertical_anchor
    blocks = []
    for p in tf.paragraphs:
        runs = []
        size = 12
        for r in p.runs:
            sz = r.font.size.pt if r.font.size else 12
            size = sz
            c = tuple(r.font.color.rgb) if r.font.color and r.font.color.type is not None else (0, 0, 0)
            runs.append((r.text, F(sz, bool(r.font.bold)), c))
        ls = p.line_spacing if isinstance(p.line_spacing, float) else 1.0
        sa = p.space_after.pt if p.space_after else 0
        blocks.append((runs, size, ls, sa, p.alignment))
    if not blocks:
        return
    # 预排版
    laid, total = [], 0.0
    for runs, size, ls, sa, align in blocks:
        rgb = [(t, f) for (t, f, c) in runs]
        cols_ = [c for (t, f, c) in runs]
        lines = wrap_px(rgb, w0)
        lh = size * SCALE / 72.0 * 1.2 * ls
        laid.append((lines, lh, align, cols_, sa))
        total += lh * len(lines) + sa * SCALE / 72.0
    y = y0
    if anchor == MSO_ANCHOR.MIDDLE:
        y = y0 + (h0 - total) / 2
    elif anchor == MSO_ANCHOR.BOTTOM:
        y = y0 + h0 - total
    for lines, lh, align, cols_, sa in laid:
        for ln in lines:
            lw = sum(f.getlength(t) for t, f in ln)
            x = x0
            if align == PP_ALIGN.CENTER:
                x = x0 + (w0 - lw) / 2
            elif align == PP_ALIGN.RIGHT:
                x = x0 + w0 - lw
            for i, (t, f) in enumerate(ln):
                d.text((x, y), t, font=f, fill=cols_[min(i, len(cols_) - 1)])
                x += f.getlength(t)
            y += lh
        y += sa * SCALE / 72.0


def render(path, outdir):
    prs = Presentation(path)
    os.makedirs(outdir, exist_ok=True)
    Wp = int(prs.slide_width / 914400 * SCALE)
    Hp = int(prs.slide_height / 914400 * SCALE)
    files = []
    for idx, s in enumerate(prs.slides, 1):
        img = Image.new("RGB", (Wp, Hp), (255, 255, 255))
        d = ImageDraw.Draw(img)
        for sh in s.shapes:
            try:
                x = sh.left / 914400 * SCALE
                y = sh.top / 914400 * SCALE
                w = sh.width / 914400 * SCALE
                h = sh.height / 914400 * SCALE
            except Exception:
                continue
            if sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
                try:
                    im = Image.open(sh.image.blob and __import__("io").BytesIO(sh.image.blob))
                except Exception:
                    continue
                iw, ih = im.size
                box = (int(iw * sh.crop_left), int(ih * sh.crop_top),
                       int(iw * (1 - sh.crop_right)), int(ih * (1 - sh.crop_bottom)))
                im = im.crop(box)
                tw_, th_ = max(1, int(w)), max(1, int(h))
                if im.mode == "RGBA":
                    im = im.resize((tw_, th_), Image.LANCZOS)
                    img.paste(im, (int(x), int(y)), im)
                else:
                    im = im.convert("RGB").resize((tw_, th_), Image.LANCZOS)
                    img.paste(im, (int(x), int(y)))
            elif sh.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
                fill = col(sh, "fill")
                lc, lw = line_col(sh)
                shape_id = sh.auto_shape_type
                if fill or lc:
                    if shape_id is not None and "OVAL" in str(shape_id):
                        d.ellipse([x, y, x + w, y + h], fill=fill, outline=lc, width=lw)
                    else:
                        d.rectangle([x, y, x + w, y + h], fill=fill, outline=lc, width=lw)
                if sh.has_text_frame and sh.text_frame.text.strip():
                    draw_text(d, sh, y, h, w, x)
            elif sh.shape_type == MSO_SHAPE_TYPE.LINE:
                lc, lw = line_col(sh)
                d.line([(x, y), (x + w, y + h)], fill=lc or (0, 0, 0), width=lw or 1)
            elif sh.has_text_frame and sh.text_frame.text.strip():
                draw_text(d, sh, y, h, w, x)
        f = os.path.join(outdir, f"slide{idx:02d}.png")
        img.save(f)
        files.append(f)
    print(f"rendered {len(files)} slides -> {outdir}")
    return files


if __name__ == "__main__":
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "输出/preview"
    render(src, out)
