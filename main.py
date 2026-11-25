#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - Tuesday, 24 November 2026.

Draws one 1024x1024 PNG news summary to /output/entry.png using only
the Python standard library. Fonts are embedded as base64 subsets of
DejaVu Sans (regular + bold, ASCII only) and parsed from memory.
No file is read at runtime, no network is used, output is deterministic.
"""
import base64
import math
import os
import struct
import zlib

# Embedded subset fonts (DejaVu Sans, printable ASCII only), base64.
FONT_REG_B64 = "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"
FONT_BOLD_B64 = "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"

W = 1024
H = 1024


def u16(b, o):
    return struct.unpack_from(">H", b, o)[0]


def i16(b, o):
    return struct.unpack_from(">h", b, o)[0]


def u32(b, o):
    return struct.unpack_from(">I", b, o)[0]


class TTF:
    """Minimal TrueType reader: cmap format 4/12, hmtx, glyf simple outlines."""

    def __init__(self, data):
        self.data = data
        n = u16(data, 4)
        self.tabs = {}
        for i in range(n):
            o = 12 + 16 * i
            tag = data[o:o + 4].decode("latin1")
            self.tabs[tag] = (u32(data, o + 8), u32(data, o + 12))
        head = self.tab("head")
        self.upem = u16(head, 18)
        self.loc_fmt = i16(head, 50)
        self.nglyphs = u16(self.tab("maxp"), 4)
        hhea = self.tab("hhea")
        self.nmetrics = u16(hhea, 34)
        self.ascent = i16(hhea, 4)
        self.descent = i16(hhea, 6)
        self.hmtx = self.tab("hmtx")
        self.glyf = self.tab("glyf")
        loca = self.tab("loca")
        if self.loc_fmt == 0:
            self.loca = [u16(loca, 2 * i) * 2 for i in range(self.nglyphs + 1)]
        else:
            self.loca = [u32(loca, 4 * i) for i in range(self.nglyphs + 1)]
        self.cmap = {}
        self._parse_cmap()

    def tab(self, tag):
        off, ln = self.tabs[tag]
        return self.data[off:off + ln]

    def _parse_cmap(self):
        cmap = self.tab("cmap")
        nsub = u16(cmap, 2)
        for i in range(nsub):
            off = 4 + 8 * i
            sub = u32(cmap, off + 4)
            fmt = u16(cmap, sub)
            if fmt == 4:
                self._cmap4(cmap[sub:])
                return
            if fmt == 12:
                self._cmap12(cmap[sub:])
                return

    def _cmap4(self, t):
        seg = u16(t, 6) // 2
        ends = [u16(t, 14 + 2 * i) for i in range(seg)]
        starts = [u16(t, 16 + 2 * seg + 2 * i) for i in range(seg)]
        deltas = [i16(t, 16 + 4 * seg + 2 * i) for i in range(seg)]
        roffs = [u16(t, 16 + 6 * seg + 2 * i) for i in range(seg)]
        base = 16 + 6 * seg
        for s in range(seg):
            if starts[s] == 0xFFFF:
                break
            for cp in range(starts[s], ends[s] + 1):
                if roffs[s] == 0:
                    gid = (cp + deltas[s]) % 65536
                else:
                    ro = base + 2 * s + roffs[s] + 2 * (cp - starts[s])
                    gid = (u16(t, ro) + deltas[s]) % 65536
                self.cmap[cp] = gid

    def _cmap12(self, t):
        ngroups = u32(t, 12)
        for i in range(ngroups):
            o = 16 + 12 * i
            start, end, gid = u32(t, o), u32(t, o + 4), u32(t, o + 8)
            for cp in range(start, end + 1):
                self.cmap[cp] = gid + (cp - start)

    def gid(self, ch):
        return self.cmap.get(ord(ch), 0)

    def advance(self, gid):
        if gid >= self.nmetrics:
            gid = self.nmetrics - 1
        return u16(self.hmtx, 4 * gid)

    def outline(self, gid):
        """Simple-outline contours as lists of (x, y, on_curve). [] if empty/composite."""
        if gid >= self.nglyphs:
            return []
        start, end = self.loca[gid], self.loca[gid + 1]
        if end <= start:
            return []
        g = self.glyf[start:end]
        ncont = i16(g, 0)
        if ncont <= 0:
            return []
        endpts = [u16(g, 10 + 2 * i) for i in range(ncont)]
        npts = endpts[-1] + 1
        inslen = u16(g, 10 + 2 * ncont)
        p = 10 + 2 * ncont + 2 + inslen
        flags = []
        while len(flags) < npts:
            f = g[p]
            p += 1
            flags.append(f)
            if f & 0x08:
                rep = g[p]
                p += 1
                flags.extend([f] * rep)
        xs = []
        x = 0
        for f in flags:
            if f & 0x02:
                d = g[p]
                p += 1
                x += d if (f & 0x10) else -d
            elif not (f & 0x10):
                x += i16(g, p)
                p += 2
            xs.append(x)
        ys = []
        y = 0
        for f in flags:
            if f & 0x04:
                d = g[p]
                p += 1
                y += d if (f & 0x20) else -d
            elif not (f & 0x20):
                y += i16(g, p)
                p += 2
            ys.append(y)
        contours = []
        s = 0
        for e in endpts:
            contours.append([(xs[i], ys[i], bool(flags[i] & 0x01))
                             for i in range(s, e + 1)])
            s = e + 1
        return contours

SS = 3  # supersampling factor for glyph antialiasing


def _flatten(contour, scale, ox, oy):
    """Flatten one quadratic outline contour to a polyline in subpixel coords.

    oy is the subpixel y of the glyph top; font y grows upward.
    Returns a list of (x, y) subpixel points, closed implicitly.
    """
    pts = [(x * scale + ox, oy - y * scale) for (x, y, on) in contour]
    on = [p[2] for p in contour]
    n = len(pts)
    if n == 0:
        return []
    if n == 1:
        return [pts[0]]
    # start point: first on-curve point, else midpoint of last/first
    if on[0]:
        start = pts[0]
        idx = 1
    else:
        start = ((pts[-1][0] + pts[0][0]) / 2.0, (pts[-1][1] + pts[0][1]) / 2.0)
        idx = 0
    out = [start]
    cur = start
    i = idx
    while i < n:
        p = pts[i]
        if on[i]:
            out.append(p)
            cur = p
            i += 1
        else:
            # quadratic with control p; end is next on-curve or midpoint
            if i + 1 < n:
                q = pts[i + 1]
                if on[i + 1]:
                    end = q
                    nxt = i + 2
                else:
                    end = ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)
                    nxt = i + 1
            else:
                end = start
                nxt = n
            steps = max(2, int(math.hypot(end[0] - cur[0], end[1] - cur[1]) / 4.0) + 1)
            for s in range(1, steps + 1):
                t = s / float(steps)
                mt = 1.0 - t
                out.append((mt * mt * cur[0] + 2 * mt * t * p[0] + t * t * end[0],
                            mt * mt * cur[1] + 2 * mt * t * p[1] + t * t * end[1]))
            cur = end
            i = nxt
    return out


def _fill_poly_subpixels(polys, w, h):
    """Fill polygons (even-odd) into a coverage buffer w*h, values 0..SS*SS."""
    cov = bytearray(w * h)
    for py in range(h * SS):
        y = py + 0.5
        xs = []
        for poly in polys:
            m = len(poly)
            for i in range(m):
                x0, y0 = poly[i]
                x1, y1 = poly[(i + 1) % m]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
        if not xs:
            continue
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            a = int(math.ceil(xs[k]))
            b = int(math.floor(xs[k + 1]))
            if b < a:
                continue
            row = py // SS
            for px in range(max(0, a), min(w * SS, b + 1)):
                cov[row * w + px // SS] += 1
    return cov


class GlyphCache:
    def __init__(self, font):
        self.font = font
        self.cache = {}

    def bitmap(self, ch, size):
        """Return (w, h, cov_bytes, left_bearing_px, top_px) for one char."""
        key = (ch, size)
        hit = self.cache.get(key)
        if hit is not None:
            return hit
        font = self.font
        gid = font.gid(ch)
        scale = size / float(font.upem)
        contours = font.outline(gid)
        if not contours:
            res = (0, 0, b"", 0, 0)
            self.cache[key] = res
            return res
        xs = [p[0] for c in contours for p in c]
        ys = [p[1] for c in contours for p in c]
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        top = int(math.ceil(ymax * scale))
        bot = int(math.floor(ymin * scale))
        left = int(math.floor(xmin * scale))
        right = int(math.ceil(xmax * scale))
        w = max(1, right - left)
        h = max(1, top - bot)
        polys = []
        for c in contours:
            # scale is in subpixels here: outline coords * size/upem * SS
            poly = _flatten(c, scale * SS, -left * SS, top * SS)
            if len(poly) >= 2:
                polys.append(poly)
        cov = _fill_poly_subpixels(polys, w, h)
        # normalise coverage 0..255
        full = SS * SS
        cov = bytes(min(255, (v * 255) // full) for v in cov)
        res = (w, h, cov, left, top)
        self.cache[key] = res
        return res

    def text_width(self, text, size):
        font = self.font
        scale = size / float(font.upem)
        total = 0
        for ch in text:
            total += font.advance(font.gid(ch))
        return int(round(total * scale))

    def wrap(self, text, size, maxw):
        words = text.split(" ")
        lines = []
        cur = ""
        for wd in words:
            trial = wd if not cur else cur + " " + wd
            if self.text_width(trial, size) <= maxw or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg) * (w * h)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = (y * self.w + x) * 3
            self.px[o] = c[0]
            self.px[o + 1] = c[1]
            self.px[o + 2] = c[2]

    def rect(self, x, y, w, h, c):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            o = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                self.px[o] = c[0]
                self.px[o + 1] = c[1]
                self.px[o + 2] = c[2]
                o += 3

    def hline(self, x0, x1, y, c):
        if y < 0 or y >= self.h:
            return
        for x in range(max(0, x0), min(self.w, x1)):
            self.set(x, y, c)

    def vline(self, x, y0, y1, c):
        if x < 0 or x >= self.w:
            return
        for y in range(max(0, y0), min(self.h, y1)):
            self.set(x, y, c)

    def line(self, x0, y0, x1, y1, c):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            dy = yy - cy
            span = int(math.sqrt(max(0, r * r - dy * dy)))
            self.hline(cx - span, cx + span + 1, yy, c)

    def ellipse(self, cx, cy, rx, ry, c):
        for yy in range(cy - ry, cy + ry + 1):
            dy = (yy - cy) / float(ry)
            span = int(rx * math.sqrt(max(0.0, 1.0 - dy * dy)))
            self.hline(cx - span, cx + span + 1, yy, c)

    def poly(self, points, c):
        """Scanline fill of a polygon (even-odd)."""
        if len(points) < 3:
            return
        ys = [p[1] for p in points]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            m = len(points)
            for i in range(m):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % m]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0 + 0.5) * (x1 - x0) / float(y1 - y0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                self.hline(int(math.ceil(xs[k])), int(math.floor(xs[k + 1])) + 1, y, c)

    def rrect(self, x, y, w, h, r, c):
        self.rect(x + r, y, w - 2 * r, h, c)
        self.rect(x, y + r, w, h - 2 * r, c)
        for cx, cy in ((x + r, y + r), (x + w - r - 1, y + r),
                       (x + r, y + h - r - 1), (x + w - r - 1, y + h - r - 1)):
            self.circle(cx, cy, r, c)

    def ring(self, cx, cy, r, c, thick=2):
        for t in range(thick):
            rr = r - t
            for yy in range(cy - rr, cy + rr + 1):
                dy = yy - cy
                span = int(math.sqrt(max(0, rr * rr - dy * dy)))
                self.set(cx - span, yy, c)
                self.set(cx + span, yy, c)

    def blit_glyph(self, bmp, x, y, c):
        w, h, cov, left, top = bmp
        if w == 0 or h == 0:
            return
        x0 = x + left
        y0 = y - top
        for row in range(h):
            yy = y0 + row
            if yy < 0 or yy >= self.h:
                continue
            for col in range(w):
                a = cov[row * w + col]
                if a == 0:
                    continue
                xx = x0 + col
                if xx < 0 or xx >= self.w:
                    continue
                o = (yy * self.w + xx) * 3
                if a >= 255:
                    self.px[o] = c[0]
                    self.px[o + 1] = c[1]
                    self.px[o + 2] = c[2]
                else:
                    self.px[o] = (c[0] * a + self.px[o] * (255 - a)) // 255
                    self.px[o + 1] = (c[1] * a + self.px[o + 1] * (255 - a)) // 255
                    self.px[o + 2] = (c[2] * a + self.px[o + 2] * (255 - a)) // 255

    def text(self, gc, txt, size, x, y_top, c, align="left", maxw=None):
        """Draw text with top at y_top; returns width drawn."""
        if maxw is not None and align == "center":
            w = gc.text_width(txt, size)
            x = x + (maxw - w) // 2
        elif maxw is not None and align == "right":
            w = gc.text_width(txt, size)
            x = x + maxw - w
        scale = size / float(gc.font.upem)
        cx = x
        for ch in txt:
            gid = gc.font.gid(ch)
            bmp = gc.bitmap(ch, size)
            self.blit_glyph(bmp, cx, y_top + int(round(gc.font.ascent * scale)), c)
            cx += int(round(gc.font.advance(gid) * scale))
        return cx - x

    def text_lines(self, gc, lines, size, x, y_top, c, leading=None):
        if leading is None:
            leading = size + 3
        y = y_top
        for ln in lines:
            self.text(gc, ln, size, x, y, c)
            y += leading
        return y


def png_bytes(cv):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 6)

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", comp) + chunk(b"IEND", b""))

# ---------- palette ----------
PAPER = (246, 241, 231)
INK = (18, 28, 43)
NAVY = (14, 42, 71)
NAVY2 = (24, 62, 102)
GOLD = (232, 163, 61)
CREAM = (191, 211, 230)
WHITE = (255, 255, 255)
CARDLINE = (216, 210, 196)
MUTED = (90, 100, 114)
REGION_BG = {
    "USA": (31, 78, 121), "MIDEAST": (140, 59, 27), "EUROPE": (46, 107, 79),
    "ASIA": (138, 109, 27), "AFRICA": (107, 58, 122), "AMERICAS": (23, 94, 99),
    "SPORT": (39, 78, 19),
}
STATUS_BG = {
    "CONFIRMED": (30, 125, 50), "OFFICIAL": (21, 101, 192),
    "REPORTED": (141, 110, 0), "CLAIM": (179, 38, 30),
}
SCENE_BG = {
    "USA": (23, 58, 94), "MIDEAST": (94, 46, 30), "EUROPE": (30, 74, 88),
    "ASIA": (96, 74, 24), "AFRICA": (74, 48, 96), "AMERICAS": (24, 72, 76),
    "SPORT": (34, 66, 30),
}


def _waves(cv, x, y, w, h, c):
    for i in range(3):
        yy = y + h - 8 - i * 7
        for xx in range(x, x + w, 14):
            cv.line(xx, yy, xx + 7, yy - 3, c)
            cv.line(xx + 7, yy - 3, xx + 14, yy, c)


def _sun(cv, x, y, r=9):
    cv.circle(x, y, r, GOLD)
    for k in range(8):
        a = k * math.pi / 4.0
        cv.line(x + int((r + 2) * math.cos(a)), y + int((r + 2) * math.sin(a)),
                x + int((r + 6) * math.cos(a)), y + int((r + 6) * math.sin(a)), GOLD)


def scene_chip(cv, x, y, w, h):
    cv.rect(x, y, w, h, (16, 34, 56))
    cy = y + h // 2
    cv.rect(x + w // 2 - 22, cy - 16, 44, 32, (24, 90, 60))
    cv.rect(x + w // 2 - 15, cy - 10, 30, 20, (46, 160, 110))
    cv.rect(x + w // 2 - 6, cy - 4, 12, 8, (232, 163, 61))
    for k in range(4):
        px = x + w // 2 - 15 + k * 10
        cv.vline(px, y + 2, cy - 16, GOLD)
        cv.vline(px, cy + 16, y + h - 2, GOLD)
        py = cy - 8 + k * 6
        cv.hline(x + w // 2 - 30, x + w // 2 - 22, py, GOLD)
        cv.hline(x + w // 2 + 22, x + w // 2 + 30, py, GOLD)
    cv.line(x + 8, y + 8, x + 30, y + 8, (90, 140, 190))
    cv.line(x + 8, y + 8, x + 8, y + 26, (90, 140, 190))


def scene_tanker(cv, x, y, w, h):
    cv.rect(x, y, w, h, (18, 52, 84))
    _sun(cv, x + w - 26, y + 14)
    # hull
    cv.poly([(x + 18, y + h - 26), (x + w - 18, y + h - 26),
             (x + w - 34, y + h - 12), (x + 34, y + h - 12)], (120, 40, 28))
    cv.rect(x + 30, y + h - 44, 34, 18, (200, 120, 40))
    cv.rect(x + 74, y + h - 44, 34, 18, (40, 120, 90))
    cv.rect(x + 118, y + h - 44, 34, 18, (200, 120, 40))
    cv.rect(x + w - 60, y + h - 52, 8, 26, (220, 220, 220))
    cv.rect(x + w - 66, y + h - 58, 20, 8, (220, 220, 220))
    _waves(cv, x, y + h - 12, w, 12, (120, 190, 230))
    # mines
    for mx, my in ((x + w - 96, y + 16), (x + 26, y + 20)):
        cv.circle(mx, my, 5, (30, 30, 30))
        cv.line(mx - 8, my, mx + 8, my, (30, 30, 30))
        cv.line(mx, my - 8, mx, my + 8, (30, 30, 30))


def scene_tower(cv, x, y, w, h):
    cv.rect(x, y, w, h, (40, 26, 52))
    _sun(cv, x + 26, y + 14)
    bx = x + w // 2 - 22
    cv.rect(bx, y + 6, 44, h - 6, (70, 90, 130))
    for r in range(5):
        for c in range(3):
            cv.rect(bx + 6 + c * 13, y + 12 + r * 9, 8, 5, (250, 210, 90))
    cv.rect(bx - 8, y + h - 14, 60, 14, (50, 60, 80))
    # drone + flash
    dx, dy = x + w - 34, y + 16
    cv.line(dx - 10, dy - 6, dx + 10, dy + 6, (220, 220, 220))
    cv.line(dx - 10, dy + 6, dx + 10, dy - 6, (220, 220, 220))
    cv.circle(dx, dy, 3, (220, 60, 40))
    for k in range(6):
        a = k * math.pi / 3.0
        cv.line(dx + int(8 * math.cos(a)), dy + int(8 * math.sin(a)),
                dx + int(13 * math.cos(a)), dy + int(13 * math.sin(a)), GOLD)


def scene_warship(cv, x, y, w, h):
    cv.rect(x, y, w, h, (20, 60, 92))
    _sun(cv, x + w - 26, y + 14)
    cv.poly([(x + 16, y + h - 24), (x + w - 16, y + h - 24),
             (x + w - 40, y + h - 10), (x + 40, y + h - 10)], (90, 100, 110))
    cv.rect(x + w // 2 - 6, y + h - 46, 12, 22, (120, 130, 140))
    cv.line(x + w // 2 - 6, y + h - 46, x + w // 2 - 26, y + h - 52, (220, 220, 220))
    cv.circle(x + w // 2 - 26, y + h - 52, 2, (220, 60, 40))
    _waves(cv, x, y + h - 10, w, 10, (140, 200, 235))
    # drone above
    dx, dy = x + 34, y + 14
    cv.line(dx - 9, dy, dx + 9, dy, (230, 230, 230))
    cv.circle(dx, dy, 3, (230, 230, 230))


def scene_desert(cv, x, y, w, h):
    cv.rect(x, y, w, h, (150, 110, 60))
    _sun(cv, x + w - 26, y + 14)
    # dunes kept inside the band: low polygons along the bottom
    cv.poly([(x, y + h), (x, y + h - 12), (x + w // 2, y + h - 20),
             (x + w, y + h - 8), (x + w, y + h)], (190, 140, 70))
    cv.poly([(x, y + h), (x, y + h - 6), (x + w // 3, y + h - 12),
             (x + w // 2, y + h - 4), (x + w // 2, y + h)], (170, 120, 55))
    # road + convoy
    cv.poly([(x + 10, y + h - 6), (x + w - 10, y + h - 6),
             (x + w - 30, y + h - 22), (x + 30, y + h - 22)], (60, 50, 40))
    for tx in (x + 44, x + 84, x + 124):
        cv.rect(tx, y + h - 34, 26, 12, (40, 50, 60))
        cv.circle(tx + 7, y + h - 20, 3, (20, 20, 20))
        cv.circle(tx + 19, y + h - 20, 3, (20, 20, 20))


def scene_shop(cv, x, y, w, h):
    cv.rect(x, y, w, h, (96, 60, 90))
    # awning
    for i in range(6):
        c = (200, 60, 50) if i % 2 == 0 else (245, 240, 225)
        cv.rect(x + 14 + i * 16, y + 8, 16, 12, c)
    cv.rect(x + 14, y + 20, 96, 4, (60, 40, 30))
    cv.rect(x + 20, y + 24, 84, h - 24, (70, 90, 120))
    cv.rect(x + 30, y + 32, 26, h - 32, (180, 210, 230))
    cv.rect(x + 66, y + 32, 26, h - 32, (180, 210, 230))
    cv.rect(x + w - 34, y + 10, 22, 14, (232, 163, 61))
    cv.circle(x + w - 23, y + 17, 4, (179, 38, 30))


def scene_heli(cv, x, y, w, h):
    cv.rect(x, y, w, h, (52, 88, 120))
    cv.circle(x + w - 24, y + 14, 8, (240, 240, 220))
    cv.line(x + 20, y + 16, x + w - 20, y + 16, (230, 230, 230))
    cv.line(x + 30, y + 12, x + w - 30, y + 12, (230, 230, 230))
    cv.ellipse(x + w // 2, y + 30, 34, 12, (200, 60, 40))
    cv.rect(x + w // 2 - 30, y + 24, 60, 12, (200, 60, 40))
    cv.poly([(x + w // 2 + 28, y + 28), (x + w - 14, y + 24),
             (x + w - 14, y + 32), (x + w // 2 + 28, y + 34)], (180, 50, 35))
    cv.line(x + w // 2 - 8, y + 36, x + w // 2 - 14, y + h - 12, (40, 40, 40))
    cv.line(x + w // 2 + 8, y + 36, x + w // 2 + 14, y + h - 12, (40, 40, 40))
    cv.rect(x, y + h - 6, w, 6, (40, 90, 50))


def scene_blast(cv, x, y, w, h):
    cv.rect(x, y, w, h, (60, 40, 60))
    cv.rect(x + 16, y + 18, 44, h - 18, (90, 80, 100))
    cv.rect(x + 70, y + 26, 36, h - 26, (80, 70, 90))
    for r in range(3):
        for c in range(2):
            cv.rect(x + 22 + c * 16, y + 24 + r * 10, 9, 6, (250, 210, 90))
    # flame
    fx, fy = x + w // 2 + 18, y + 20
    cv.poly([(fx - 12, fy + 12), (fx, fy - 10), (fx + 12, fy + 12)], (240, 120, 30))
    cv.poly([(fx - 6, fy + 12), (fx, fy + 2), (fx + 6, fy + 12)], (250, 200, 60))
    cv.circle(fx - 18, fy - 4, 4, (120, 120, 120))
    cv.circle(fx + 22, fy - 8, 5, (120, 120, 120))


def scene_trophy(cv, x, y, w, h):
    cv.rect(x, y, w, h, (24, 90, 50))
    cx = x + w // 2
    cy = y + h // 2 + 2
    cv.poly([(cx - 16, cy - 16), (cx + 16, cy - 16), (cx + 10, cy + 6),
             (cx - 10, cy + 6)], GOLD)
    cv.rect(cx - 4, cy + 6, 8, 8, GOLD)
    cv.rect(cx - 12, cy + 14, 24, 5, GOLD)
    cv.line(cx - 16, cy - 12, cx - 26, cy - 2, GOLD)
    cv.line(cx + 16, cy - 12, cx + 26, cy - 2, GOLD)
    # ball
    cv.circle(x + 24, y + h - 14, 8, WHITE)
    cv.circle(x + w - 24, y + 14, 6, WHITE)
    for px, py, pc in ((x + 20, y + 12, (232, 163, 61)), (x + w - 30, y + h - 16, (232, 163, 61)),
                       (x + 30, y + h - 22, (255, 255, 255)), (x + w - 20, y + 26, (255, 255, 255))):
        cv.circle(px, py, 2, pc)


def scene_stadium(cv, x, y, w, h):
    cv.rect(x, y, w, h, (30, 70, 40))
    # pitch: flat strip inside the band, stands above it
    cv.rect(x, y + h - 14, w, 14, (60, 140, 70))
    cv.rect(x + w // 4, y + h - 10, w // 2, 6, (90, 180, 100))
    # stands
    cv.poly([(x + 10, y + h - 18), (x + w - 10, y + h - 18),
             (x + w - 26, y + 12), (x + 26, y + 12)], (120, 130, 140))
    for r in range(3):
        cv.hline(x + 30 + r * 6, x + w - 30 - r * 6, y + 18 + r * 10, (200, 210, 220))
    cv.circle(x + w // 2, y + h - 16, 8, WHITE)
    cv.circle(x + w // 2, y + h - 16, 3, (20, 20, 20))
    # flags
    for fx, fc in ((x + 16, (200, 60, 50)), (x + w - 22, (40, 90, 180))):
        cv.vline(fx + 3, y + 4, y + 22, (230, 230, 230))
        cv.poly([(fx + 3, y + 4), (fx + 14, y + 8), (fx + 3, y + 12)], fc)


def scene_rocket(cv, x, y, w, h):
    cv.rect(x, y, w, h, (12, 20, 44))
    for sx, sy in ((x + 16, y + 10), (x + w - 20, y + 18), (x + 30, y + h - 14),
                   (x + w - 34, y + h - 10), (x + w // 2 + 30, y + 8)):
        cv.circle(sx, sy, 2, WHITE)
    cx = x + w // 2
    cv.poly([(cx - 10, y + h - 22), (cx - 10, y + 18), (cx, y + 6),
             (cx + 10, y + 18), (cx + 10, y + h - 22)], (220, 225, 235))
    cv.poly([(cx - 10, y + h - 22), (cx - 20, y + h - 8), (cx - 10, y + h - 14)], (200, 60, 40))
    cv.poly([(cx + 10, y + h - 22), (cx + 20, y + h - 8), (cx + 10, y + h - 14)], (200, 60, 40))
    cv.circle(cx, y + 22, 4, (40, 120, 180))
    cv.poly([(cx - 5, y + h - 22), (cx, y + h - 4), (cx + 5, y + h - 22)], (250, 180, 40))
    cv.circle(x + 18, y + h - 16, 10, (200, 200, 190))


def scene_satellite(cv, x, y, w, h):
    cv.rect(x, y, w, h, (14, 26, 52))
    for sx, sy in ((x + 14, y + 10), (x + 40, y + 26), (x + w - 16, y + 12),
                   (x + w - 40, y + h - 12), (x + 20, y + h - 16)):
        cv.circle(sx, sy, 2, WHITE)
    cx, cy = x + w // 2, y + h // 2
    cv.ellipse(cx, cy, w // 2 - 6, h // 2 - 4, (40, 90, 160))
    cv.ellipse(cx, cy, w // 2 - 6, h // 2 - 4, (14, 26, 52))
    cv.rect(cx - 26, cy - 7, 18, 14, (40, 110, 190))
    cv.rect(cx + 8, cy - 7, 18, 14, (40, 110, 190))
    cv.rect(cx - 8, cy - 10, 16, 20, (200, 200, 210))
    cv.circle(cx, cy, 3, (232, 163, 61))
    cv.line(cx - 8, cy - 14, cx - 16, cy - 22, (200, 200, 210))


def scene_badge(cv, x, y, w, h):
    cv.rect(x, y, w, h, (56, 44, 30))
    cx, cy = x + w // 2 - 12, y + h // 2
    # star badge
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        r = 20 if k % 2 == 0 else 9
        pts.append((cx + int(r * math.cos(a)), cy + int(r * math.sin(a))))
    cv.poly(pts, GOLD)
    cv.circle(cx, cy, 6, (120, 40, 28))
    # handcuffs
    cv.ring(x + w - 30, y + h - 16, 8, (200, 200, 210), 2)
    cv.ring(x + w - 52, y + h - 16, 8, (200, 200, 210), 2)
    cv.line(x + w - 44, y + h - 16, x + w - 38, y + h - 16, (200, 200, 210))
    # road
    cv.poly([(x + 8, y + h - 6), (x + w - 8, y + h - 6),
             (x + w - 24, y + h - 18), (x + 24, y + h - 18)], (70, 60, 50))


SCENES = {
    "chip": scene_chip, "tanker": scene_tanker, "tower": scene_tower,
    "warship": scene_warship, "desert": scene_desert, "shop": scene_shop,
    "heli": scene_heli, "blast": scene_blast, "trophy": scene_trophy,
    "stadium": scene_stadium, "rocket": scene_rocket,
    "satellite": scene_satellite, "badge": scene_badge,
}

# ---------- data: all stories first reported 24 November 2026 ----------
LEAD = {
    "scene": "chip", "region": "USA", "status": "CONFIRMED", "source": "REUTERS",
    "stat": "10/12", "statlabel": "COUNTS",
    "headline": "Huawei found guilty in US trial, cleared of racketeering",
    "detail": "Jury convicts on 10 of 12 counts, incl. trade-secret theft and bank fraud; firm to appeal. Sentencing set for Sep 2027.",
}

CARDS = [
    {"scene": "tanker", "region": "MIDEAST", "status": "CLAIM", "source": "IRGC / JMIC",
     "stat": "4", "statlabel": "TANKERS",
     "headline": "Four tankers hit mines in Strait of Hormuz",
     "detail": "IRGC says a fourth tanker struck a mine after three caught fire; maritime centre says claims unconfirmed."},
    {"scene": "tower", "region": "MIDEAST", "status": "CONFIRMED", "source": "SAUDI TV",
     "stat": "11", "statlabel": "WOUNDED",
     "headline": "Drone hits PIF tower in Riyadh, 11 wounded",
     "detail": "Saudi civil defence says a tower in the King Abdullah Financial District was hit for a second time in a week."},
    {"scene": "warship", "region": "EUROPE", "status": "CONFIRMED", "source": "KYIV",
     "stat": "2", "statlabel": "SEAS",
     "headline": "Ukraine hits Russian ships in two seas",
     "detail": "Drone strike on cargo ship Sparta II in the Gulf of Finland; corvette claimed sunk off Libya."},
    {"scene": "desert", "region": "MIDEAST", "status": "REPORTED", "source": "YEMEN ARMY",
     "stat": "60 km", "statlabel": "FROM ADEN",
     "headline": "Houthis 60 km from Aden, ready to attack",
     "detail": "Yemen army says fighters closed in on the temporary capital and built a defence line north and west."},
    {"scene": "shop", "region": "AMERICAS", "status": "CONFIRMED", "source": "PRESIDENT",
     "stat": "25", "statlabel": "HOSTAGES",
     "headline": "25 hostages held at Cartagena supermarket",
     "detail": "Armed men seized a store in Colombia; five older women freed as troops deployed, airport briefly shut."},
    {"scene": "heli", "region": "EUROPE", "status": "CONFIRMED", "source": "DEFENCE MIN.",
     "stat": "5", "statlabel": "KILLED",
     "headline": "Turkish military helicopter crash kills five",
     "detail": "AS-532 went down after take-off from Eskisehir on a training flight; second crash in 12 days."},
    {"scene": "blast", "region": "ASIA", "status": "CONFIRMED", "source": "POLICE",
     "stat": "6", "statlabel": "KILLED",
     "headline": "Hanoi restaurant blast kills at least six",
     "detail": "Explosion at a hot pot eatery in Dong Da district injures a dozen; cooking gas leak suspected."},
    {"scene": "trophy", "region": "AFRICA", "status": "CONFIRMED", "source": "CAS",
     "stat": "1", "statlabel": "TITLE",
     "headline": "Senegal get Africa Cup title back on appeal",
     "detail": "Sports court upholds Senegal appeal, restoring the 2025 AFCON title stripped after the final."},
    {"scene": "stadium", "region": "SPORT", "status": "OFFICIAL", "source": "FIFA",
     "stat": "48", "statlabel": "TEAMS 2031",
     "headline": "FIFA names 2031 and 2035 Women's World Cup hosts",
     "detail": "USA, Mexico, Costa Rica and Jamaica to co-host 2031; England, Scotland, Wales and N. Ireland get 2035."},
    {"scene": "rocket", "region": "ASIA", "status": "OFFICIAL", "source": "CNSA",
     "stat": "3", "statlabel": "CREW",
     "headline": "China launches Shenzhou 24 with Pakistani astronaut",
     "detail": "Three crew head to the Tiangong station, the first foreign astronaut aboard China's space station."},
    {"scene": "satellite", "region": "EUROPE", "status": "REPORTED", "source": "NATO",
     "stat": "60", "statlabel": "DAYS",
     "headline": "NATO vows defence as space threat reports grow",
     "detail": "Rutte says alliance will defend in space after reports Russia may launch a nuclear-armed satellite."},
    {"scene": "badge", "region": "AMERICAS", "status": "CONFIRMED", "source": "MEXICO",
     "stat": "20", "statlabel": "DIED IN RAID",
     "headline": "US drone helped capture El Chapo Isidro",
     "detail": "Mexico says it will try the cartel leader at home despite a US extradition request; 20 died in the raid."},
]

TIMELINE = [
    ("00:00", "Iran: 4 tankers hit mines, Hormuz"),
    ("02:09", "El Chapo Isidro captured, Sinaloa"),
    ("04:14", "Russian jets near Ulleungdo; shelter order"),
    ("08:14", "Ukraine strikes Russian ships"),
    ("11:40", "Israel kills Hamas security chief, Gaza"),
    ("12:55", "UK sanctions Houthis"),
    ("14:27", "Riyadh PIF tower hit, 11 wounded"),
    ("20:41", "Huawei guilty verdict, New York"),
]

NUMBERS = [
    ("4", "tankers hit mines in Hormuz"),
    ("25", "hostages in Cartagena"),
    ("11", "wounded in Riyadh"),
    ("10/12", "Huawei counts, guilty"),
    ("60 km", "Houthis from Aden"),
    ("5", "killed in Turkiye crash"),
    ("6", "killed in Hanoi blast"),
    ("48", "teams, 2031 World Cup"),
]

ALSO_ON = ("ALSO ON 24 NOV: COP31 ends with no deal in Antalya  |  Sarkozy and Carla Bruni ordered to trial  |  "
            "WHO chief urges US to lift Cuba fuel blockade  |  Lukashenko offers joint flight to Moscow talks  |  "
            "China sentences spy official to death  |  Gaza meningitis alert: 272 cases in October")

LEGEND = ("LEGEND:  CONFIRMED = confirmed by officials or a court   OFFICIAL = announced by an institution   "
          "REPORTED = reported, not independently verified   CLAIM = one side's claim")
SOURCES = ("Sources: Reuters, AP, BBC, AFP, Al Jazeera, Daily Summary Of  |  All times UTC  |  "
           "THE WORLD IN ONE DAY - Tuesday, 24 November 2026")


def draw_chip(cv, gc, x, y, text, bg, size=10, bold=True):
    f = gc
    w = f.text_width(text, size) + 12
    cv.rrect(x, y, w, 15, 3, bg)
    f2 = gc
    cv.text(f2, text, size, x + 6, y + 2, WHITE)
    return w


def draw_card(cv, reg, bold, c, x, y, w, h):
    cv.rect(x, y, w, h, WHITE)
    cv.rect(x, y, w, 1, CARDLINE)
    cv.rect(x, y + h - 1, w, 1, CARDLINE)
    cv.rect(x, y, 1, h, CARDLINE)
    cv.rect(x + w - 1, y, 1, h, CARDLINE)
    scene = SCENES[c["scene"]]
    scene(cv, x + 1, y + 1, w - 2, 48)
    # stat badge on the scene, top right
    sw = bold.text_width(c["stat"], 15) + 12
    cv.rect(x + w - sw - 6, y + 6, sw, 20, (0, 0, 0))
    cv.text(bold, c["stat"], 15, x + w - sw, y + 8, GOLD)
    # chips row
    cx = x + 8
    cx += draw_chip(cv, bold, cx, y + 55, c["region"], REGION_BG[c["region"]], 9) + 5
    cx += draw_chip(cv, bold, cx, y + 55, c["status"], STATUS_BG[c["status"]], 9) + 5
    cv.text(reg, c["source"], 9, x + w - 8 - reg.text_width(c["source"], 9), y + 58, MUTED)
    # headline + detail
    lines = bold.wrap(c["headline"], 14, w - 16)
    cv.text_lines(bold, lines[:2], 14, x + 8, y + 74, INK, leading=17)
    dlines = reg.wrap(c["detail"], 10, w - 16)
    cv.text_lines(reg, dlines[:2], 10, x + 8, y + 108, (60, 68, 80), leading=12)


def build():
    reg = GlyphCache(TTF(base64.b64decode(FONT_REG_B64)))
    bold = GlyphCache(TTF(base64.b64decode(FONT_BOLD_B64)))
    cv = Canvas(W, H, PAPER)
    # ---------- header ----------
    cv.rect(10, 10, 1004, 104, NAVY)
    cv.rect(10, 10, 1004, 4, GOLD)
    cv.text(bold, "THE WORLD IN ONE DAY", 40, 26, 22, WHITE)
    cv.text(reg, "Tuesday, 24 November 2026  -  30 stories from 64 sources  -  All times UTC",
            15, 26, 68, CREAM)
    cx = 26
    cv.text(bold, "ACROSS:", 10, cx, 96, GOLD)
    cx += bold.text_width("ACROSS:", 10) + 8
    for rname in ("USA", "MIDEAST", "EUROPE", "ASIA", "AFRICA", "AMERICAS", "SPORT"):
        cx += draw_chip(cv, bold, cx, 93, rname, REGION_BG[rname], 9) + 5
    cv.text(reg, "13 STORIES  |  TOP 50 SHARE $100", 10, 830, 96, CREAM)
    # ---------- lead card ----------
    lx, ly, lw, lh = 10, 122, 1004, 118
    cv.rect(lx, ly, lw, lh, WHITE)
    cv.rect(lx, ly, lw, 1, CARDLINE)
    cv.rect(lx, ly + lh - 1, lw, 1, CARDLINE)
    cv.rect(lx, ly, 1, lh, CARDLINE)
    cv.rect(lx + lw - 1, ly, 1, lh, CARDLINE)
    SCENES[LEAD["scene"]](cv, lx + 1, ly + 1, 318, lh - 2)
    tx = lx + 334
    cx = tx
    cx += draw_chip(cv, bold, cx, ly + 10, LEAD["region"], REGION_BG[LEAD["region"]], 10) + 6
    cx += draw_chip(cv, bold, cx, ly + 10, LEAD["status"], STATUS_BG[LEAD["status"]], 10) + 6
    cv.text(reg, LEAD["source"], 10, cx, ly + 12, MUTED)
    lines = bold.wrap(LEAD["headline"], 21, 560)
    cv.text_lines(bold, lines[:2], 21, tx, ly + 32, INK, leading=24)
    dlines = reg.wrap(LEAD["detail"], 12, 560)
    cv.text_lines(reg, dlines[:2], 12, tx, ly + 82, (60, 68, 80), leading=15)
    sx = lx + lw - 150
    cv.rect(sx, ly + 14, 2, lh - 28, GOLD)
    cv.text(bold, LEAD["stat"], 34, sx + 16, ly + 26, NAVY)
    cv.text(bold, LEAD["statlabel"], 11, sx + 16, ly + 66, MUTED)
    cv.text(reg, "GUILTY", 11, sx + 16, ly + 84, (30, 125, 50))
    # ---------- grid of 12 cards ----------
    xs = [10, 347, 684]
    ws = [329, 329, 330]
    gy = 248
    for i, c in enumerate(CARDS):
        row, col = i // 3, i % 3
        draw_card(cv, reg, bold, c, xs[col], gy + row * 140, ws[col], 132)
    # ---------- timeline strip ----------
    ty = 808
    cv.rect(10, ty, 1004, 62, NAVY2)
    cv.text(bold, "THE DAY IN UTC", 12, 22, ty + 7, GOLD)
    cv.text(reg, "TUESDAY 24 NOVEMBER 2026", 10, 150, ty + 9, CREAM)
    colw = 1004 // 8
    for i, (t, label) in enumerate(TIMELINE):
        ex = 10 + i * colw + 12
        cv.circle(ex + 3, ty + 34, 3, GOLD)
        cv.text(bold, t, 12, ex, ty + 26, WHITE)
        lab = reg.wrap(label, 9, colw - 18)
        cv.text_lines(reg, lab[:2], 9, ex, ty + 42, CREAM, leading=11)
    # ---------- day in numbers ----------
    ny = 878
    cv.rect(10, ny, 1004, 64, WHITE)
    cv.rect(10, ny, 1004, 3, GOLD)
    cv.text(bold, "DAY IN NUMBERS", 12, 22, ny + 8, NAVY)
    for i, (num, label) in enumerate(NUMBERS):
        ex = 10 + i * colw + 12
        cv.text(bold, num, 20, ex, ny + 24, NAVY)
        lab = reg.wrap(label, 9, colw - 18)
        cv.text_lines(reg, lab[:2], 9, ex, ny + 44, MUTED, leading=10)
    # ---------- also on ----------
    ay = 950
    alines = reg.wrap(ALSO_ON, 11, 1004 - 20)
    cv.text_lines(reg, alines[:2], 11, 10, ay, INK, leading=14)
    # ---------- footer ----------
    fy = 980
    cv.text(reg, LEGEND, 10, 10, fy, MUTED)
    cv.text(reg, SOURCES, 10, 10, fy + 15, MUTED)
    cv.rect(10, fy + 30, 1004, 2, GOLD)
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    cv = build()
    data = png_bytes(cv)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
