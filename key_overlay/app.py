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

# ──────────────────────────────────────────────
# Головний клас
# ──────────────────────────────────────────────

import tkinter as tk

from pynput import keyboard

from key_overlay import config
from key_overlay.draw_util import _rounded_rect, _draw_key
from key_overlay.key_labels import KEY_LABELS, KEYS_LAYOUT


class KeyOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "#010101")
        self.root.configure(bg="#010101")

        self.pressed: set[keyboard.Key] = set()
        self.canvas: tk.Canvas | None = None

        self._build_window()
        self._redraw()

        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release)
        self.listener.start()

    def _on_press(self, key):
        if key == keyboard.Key.esc:
            self.root.after(0, self.root.quit)
            return False
        if key in KEY_LABELS:
            self.pressed.add(key)
            self.root.after(0, self._redraw)

    def _on_release(self, key):
        if key in KEY_LABELS:
            self.pressed.discard(key)
            self.root.after(0, self._redraw)

    def _build_window(self):
        win_w = config.WINDOW_PAD_X * 2 + config.COLS * config.KEY_W + (config.COLS - 1) * config.GAP
        win_h = config.WINDOW_PAD_Y * 2 + config.ROWS * config.KEY_H + (
                config.ROWS - 1) * config.GAP + config.KEY_OFFSET

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        wx = sw - win_w - config.MARGIN_RIGHT
        wy = sh - win_h - config.MARGIN_BOTTOM

        self.root.geometry(f"{win_w}x{win_h}+{wx}+{wy}")

        self.canvas = tk.Canvas(self.root,
                                width=win_w, height=win_h,
                                bg="#010101", highlightthickness=0)
        self.canvas.pack()

    def _redraw(self):
        self.canvas.delete("all")

        win_w = config.WINDOW_PAD_X * 2 + config.COLS * config.KEY_W + (config.COLS - 1) * config.GAP
        win_h = config.WINDOW_PAD_Y * 2 + config.ROWS * config.KEY_H + (
                config.ROWS - 1) * config.GAP + config.KEY_OFFSET

        _rounded_rect(self.canvas, 0, 0, win_w, win_h,
                      config.BG_RADIUS, fill=config.BG_COLOR, outline="")

        for key, (col, row) in KEYS_LAYOUT.items():
            label_top, label_bot = KEY_LABELS[key]
            kx = config.WINDOW_PAD_X + col * (config.KEY_W + config.GAP)
            ky = config.WINDOW_PAD_Y + row * (config.KEY_H + config.GAP)
            _draw_key(self.canvas, kx, ky, label_top, label_bot,
                      pressed=(key in self.pressed))

        # підказка в порожній комірці (0, 0)
        cx = config.WINDOW_PAD_X + 0 * (config.KEY_W + config.GAP) + config.KEY_W // 2
        cy = config.WINDOW_PAD_Y + 0 * (config.KEY_H + config.GAP) + config.KEY_H // 2
        self.canvas.create_text(cx, cy,
                                text="Esc\nto exit",
                                font=(config.FONT_FAMILY, 9),
                                fill="#555555",
                                justify="center")

    def run(self):
        self.root.mainloop()
        self.listener.stop()


if __name__ == '__main__':
    print('Press "Esc" to exit')
    KeyOverlay().run()
