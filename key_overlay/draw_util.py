#  Original code under MIT License
#
#  Copyright (c) 2026 Oleksii Sylichenko
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

from key_overlay import config


# ──────────────────────────────────────────────
# Утиліти: намалювати заокруглений прямокутник на Canvas
# ──────────────────────────────────────────────

def _rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    pts = [
        x1 + r, y1, x2 - r, y1,
        x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2,
        x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r,
        x1, y1 + r, x1, y1,
        x1 + r, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kwargs)


def _draw_key(canvas, x, y, label_top, label_bot, pressed=False, release_t=0.0):
    face = config.KEY_FACE_PRESSED if pressed else config.KEY_FACE_IDLE
    shadow = config.KEY_SHADOW_PRESSED if pressed else config.KEY_SHADOW_IDLE

    text = "#111111" if pressed else "#333333"

    _rounded_rect(canvas,
                  x, y + config.KEY_OFFSET,
                  x + config.KEY_W, y + config.KEY_H + config.KEY_OFFSET,
                  config.KEY_RADIUS, fill=shadow, outline="")
    _rounded_rect(canvas,
                  x, y,
                  x + config.KEY_W, y + config.KEY_H,
                  config.KEY_RADIUS, fill=face, outline="")

    cx = x + config.KEY_W // 2
    canvas.create_text(cx, y + 14, text=label_top,
                       font=(config.FONT_FAMILY, config.FONT_SIZE_TOP),
                       fill=text)
    canvas.create_text(cx, y + 34, text=label_bot,
                       font=(config.FONT_FAMILY, config.FONT_SIZE_BOT, "bold"),
                       fill=text)
