import threading
import sys
import os
import subprocess
import time
import tkinter as tk
from tkinter import font as tkfont
import webbrowser
import tempfile

CREATE_NO_WINDOW = 0x08000000

try:
    import yt_dlp
    import sounddevice as sd
    import numpy as np
except ImportError:
    subprocess.run(
        [sys.executable, '-m', 'pip', 'install', 'yt-dlp', 'sounddevice', 'numpy', '--quiet'],
        creationflags=CREATE_NO_WINDOW
    )
    import yt_dlp
    import sounddevice as sd
    import numpy as np

URL = "https://www.youtube.com/watch?v=jfKfPfyJRdk"
SAMPLERATE = 44100
CHANNELS = 2

BG           = "#0e0e12"
ACCENT       = "#c9a96e"
ACCENT2      = "#e8c88a"
DIM          = "#2a2a3a"
TEXT         = "#e8e0d0"
SUBTEXT      = "#5a5470"
BTN_BG       = "#1a1a24"
BTN_HOV      = "#2a2a38"
TITLEBAR_BG  = "#09090d"

class State:
    playing   = False
    stop_flag = False
    volume    = 0.8
    thread    = None
    proc      = None
    start_time = None

state = State()

# ── Audio ──────────────────────────────────────────────────────────────────
def stream_audio():
    state.stop_flag = False
    try:
        with yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True}) as ydl:
            info = ydl.extract_info(URL, download=False)
            stream_url   = info['url']
            http_headers = info.get('http_headers', {})

        header_args = []
        for k, v in http_headers.items():
            header_args += ['-headers', f'{k}: {v}\r\n']

        ffmpeg_cmd = ['ffmpeg', '-loglevel', 'quiet'] + header_args + [
            '-i', stream_url, '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', str(SAMPLERATE), '-ac', str(CHANNELS),
            '-f', 's16le', 'pipe:1'
        ]

        state.proc = subprocess.Popen(
            ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            bufsize=SAMPLERATE * CHANNELS * 2 * 5,
            creationflags=CREATE_NO_WINDOW
        )

        chunk_size = SAMPLERATE * CHANNELS * 2 // 10
        with sd.RawOutputStream(samplerate=SAMPLERATE, channels=CHANNELS, dtype='int16') as stream:
            while not state.stop_flag:
                data = state.proc.stdout.read(chunk_size)
                if not data:
                    break
                arr = np.frombuffer(data, dtype=np.int16).copy()
                arr = (arr * state.volume).astype(np.int16)
                stream.write(arr.tobytes())

        state.proc.terminate()
        state.proc.wait()
    except Exception:
        pass
    finally:
        state.playing = False

def do_start():
    if state.thread and state.thread.is_alive():
        return
    if state.start_time is None:
        state.start_time = time.time()
    state.playing = True
    state.thread  = threading.Thread(target=stream_audio, daemon=True)
    state.thread.start()

def do_stop():
    state.stop_flag = True
    state.playing   = False
    if state.proc:
        try:
            state.proc.terminate()
        except Exception:
            pass

# ── Icon (Pillow optional) ─────────────────────────────────────────────────
def make_icon_file():
    """Returns (png_path, ico_path) or (None, None). Builds ICO manually for multi-size support."""
    try:
        import io, struct
        from PIL import Image, ImageDraw

        def draw_girl(size):
            img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            S = size / 64.0
            def s(x): return int(x * S)
            sk   = (232, 196, 154, 255)
            hair = (26,  8,   8,   255)
            ac   = (201, 169, 110, 255)
            hood = (30,  30,  46,  255)
            hood2= (22,  22,  42,  255)
            book = (201, 160, 80,  255)
            bg_c = (14,  14,  18,  255)
            dark = (14,  14,  18,  240)
            d.ellipse([s(1),s(1),s(63),s(63)], fill=dark)
            for r in range(s(26), 0, -2):
                a = int(35*(1-r/s(26)))
                d.ellipse([s(32)-r,s(32)-r,s(32)+r,s(32)+r], fill=(*ac[:3],a))
            d.rectangle([s(8),s(42),s(56),s(64)], fill=hood)
            d.rectangle([s(12),s(42),s(52),s(52)], fill=hood2)
            d.rectangle([s(25),s(36),s(39),s(44)], fill=sk)
            d.ellipse([s(8),s(4),s(56),s(48)], fill=hair)
            d.ellipse([s(13),s(10),s(51),s(42)], fill=sk)
            d.polygon([s(13),s(12),s(7),s(26),s(14),s(21),s(12),s(30),s(22),s(18),s(32),s(12)], fill=hair)
            lw = max(1, int(size/32))
            d.rectangle([s(14),s(20),s(27),s(29)], outline=ac[:3], width=lw)
            d.rectangle([s(33),s(20),s(46),s(29)], outline=ac[:3], width=lw)
            d.line([s(27),s(24),s(33),s(24)], fill=ac, width=lw)
            d.line([s(17),s(24),s(25),s(24)], fill=hair, width=lw)
            d.line([s(35),s(24),s(43),s(24)], fill=hair, width=lw)
            d.arc([s(24),s(29),s(40),s(38)], start=200, end=340, fill=hair, width=lw)
            d.arc([s(6),s(5),s(20),s(30)],  start=90,  end=270, fill=ac, width=max(2,lw*2))
            d.arc([s(44),s(5),s(58),s(30)], start=270, end=90,  fill=ac, width=max(2,lw*2))
            d.ellipse([s(3),s(13),s(12),s(24)], fill=ac)
            d.ellipse([s(52),s(13),s(61),s(24)], fill=ac)
            d.rectangle([s(7),s(49),s(57),s(62)], fill=book)
            d.line([s(32),s(49),s(32),s(62)], fill=bg_c, width=lw)
            d.line([s(10),s(54),s(30),s(54)], fill=bg_c, width=lw)
            d.line([s(10),s(58),s(30),s(58)], fill=bg_c, width=lw)
            d.line([s(34),s(54),s(54),s(54)], fill=bg_c, width=lw)
            return img

        sizes   = [16, 32, 48, 64, 128, 256]
        images  = [draw_girl(sz) for sz in sizes]
        png_datas = []
        for img in images:
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            png_datas.append(buf.getvalue())

        n = len(sizes)
        header = struct.pack("<HHH", 0, 1, n)
        data_offset = 6 + n * 16
        entries = b""
        for png in png_datas:
            entries += struct.pack("<BBBBHHII", 0, 0, 0, 0, 1, 32, len(png), data_offset)
            data_offset += len(png)

        ico_tmp = tempfile.NamedTemporaryFile(suffix=".ico", delete=False)
        ico_tmp.write(header + entries + b"".join(png_datas))
        ico_tmp.close()

        png_tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        images[-1].save(png_tmp.name)
        png_tmp.close()

        return png_tmp.name, ico_tmp.name
    except Exception:
        return None, None

# ── App ────────────────────────────────────────────────────────────────────
class LofiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LofiGurl")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)   # remove native titlebar

        W, H = 370, 162
        sw   = root.winfo_screenwidth()
        sh   = root.winfo_screenheight()
        root.geometry(f"{W}x{H}+{(sw-W)//2}+{sh-H-70}")

        # icon — use .ico for taskbar/desktop via wm_iconbitmap (works with overrideredirect)
        png_path, ico_path = make_icon_file()
        if ico_path:
            try:
                self.root.wm_iconbitmap(ico_path)
            except Exception:
                pass
        if png_path:
            try:
                from PIL import ImageTk, Image
                _img       = Image.open(png_path)
                self._icon = ImageTk.PhotoImage(_img)
                self.root.iconphoto(True, self._icon)
            except Exception:
                pass
        self._ico_path = ico_path

        self._drag_x = self._drag_y = 0
        self._build_ui()
        self._tick()
        do_start()

    # ── Drag ──────────────────────────────────────────────────────────────
    def _drag_start(self, e):
        self._drag_x = e.x_root - self.root.winfo_x()
        self._drag_y = e.y_root - self.root.winfo_y()

    def _drag_motion(self, e):
        self.root.geometry(f"+{e.x_root - self._drag_x}+{e.y_root - self._drag_y}")

    # ── UI ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Titlebar ─────────────────────────────────────────────────────
        tb = tk.Frame(self.root, bg=TITLEBAR_BG, height=30)
        tb.pack(fill="x")
        tb.pack_propagate(False)
        tb.bind("<ButtonPress-1>", self._drag_start)
        tb.bind("<B1-Motion>",     self._drag_motion)

        # accent bottom line
        tk.Frame(self.root, bg=ACCENT, height=1).pack(fill="x")

        # dot
        dot = tk.Canvas(tb, width=8, height=8, bg=TITLEBAR_BG, highlightthickness=0)
        dot.pack(side="left", padx=(10, 4), pady=11)
        dot.create_oval(0, 0, 8, 8, fill=ACCENT, outline="")

        lbl_f = tkfont.Font(family="Georgia", size=9, slant="italic")
        lbl   = tk.Label(tb, text="lofi girl radio", font=lbl_f, bg=TITLEBAR_BG, fg=ACCENT)
        lbl.pack(side="left")
        lbl.bind("<ButtonPress-1>", self._drag_start)
        lbl.bind("<B1-Motion>",     self._drag_motion)

        # Minimize & Close buttons
        def _make_tb_btn(text, click_cmd, hover_fg, hover_bg):
            b = tk.Label(tb, text=text,
                         font=tkfont.Font(size=9), bg=TITLEBAR_BG,
                         fg="#444455", padx=9, pady=2, cursor="hand2")
            b.pack(side="right", padx=(0, 2))
            b.bind("<Enter>",    lambda e: b.config(fg=hover_fg, bg=hover_bg))
            b.bind("<Leave>",    lambda e: b.config(fg="#444455", bg=TITLEBAR_BG))
            b.bind("<Button-1>", lambda e: click_cmd())
            return b

        _make_tb_btn("✕", self._quit,     "#ff6b6b", "#2a0e0e")
        _make_tb_btn("─", self._minimize, ACCENT,    "#1a1a28")

        # ── Content ───────────────────────────────────────────────────────
        outer = tk.Frame(self.root, bg=BG, padx=12, pady=8)
        outer.pack(fill="both", expand=True)

        # Left — lofi girl
        left = tk.Frame(outer, bg=BG)
        left.pack(side="left", padx=(0, 12))
        gc = tk.Canvas(left, width=62, height=88, bg=BG, highlightthickness=0)
        gc.pack()
        self._draw_girl(gc)

        # Mid — controls
        mid = tk.Frame(outer, bg=BG)
        mid.pack(side="left", fill="both", expand=True)

        tf = tkfont.Font(family="Georgia", size=10, weight="bold", slant="italic")
        tk.Label(mid, text="lofi girl radio", font=tf, bg=BG, fg=ACCENT).pack(anchor="w")

        mono = tkfont.Font(family="Courier New", size=8)

        self.timer_var = tk.StringVar(value="00:00")
        tk.Label(mid, textvariable=self.timer_var, font=mono, bg=BG, fg=SUBTEXT).pack(anchor="w")

        vf = tk.Frame(mid, bg=BG)
        vf.pack(anchor="w", pady=(4, 0))
        tk.Label(vf, text="vol", font=mono, bg=BG, fg=SUBTEXT).pack(side="left")
        self.vol_bar = tk.Canvas(vf, width=80, height=5, bg=DIM,
                                  highlightthickness=0, bd=0, cursor="hand2")
        self.vol_bar.pack(side="left", padx=(5, 0))
        self.vol_bar.bind("<Button-1>",  self._click_vol)
        self.vol_bar.bind("<B1-Motion>", self._click_vol)
        self._draw_vol_bar()
        self.vol_lbl = tk.Label(vf, text=f"{int(state.volume*100)}%",
                                 font=mono, bg=BG, fg=SUBTEXT, width=4)
        self.vol_lbl.pack(side="left", padx=(4, 0))

        bf = tk.Frame(mid, bg=BG)
        bf.pack(anchor="w", pady=(7, 0))

        self.pp_btn = tk.Button(bf, text="⏸",
                                 font=tkfont.Font(size=13),
                                 bg=BTN_BG, fg=ACCENT,
                                 activebackground=BTN_HOV, activeforeground=ACCENT,
                                 relief="flat", bd=0, cursor="hand2",
                                 command=self._toggle, width=2, padx=2)
        self.pp_btn.pack(side="left", padx=(0, 4))

        sf = tkfont.Font(family="Courier New", size=12, weight="bold")
        for sym, cmd in [("−", self._vol_down), ("+", self._vol_up)]:
            tk.Button(bf, text=sym, font=sf,
                      bg=BTN_BG, fg=TEXT,
                      activebackground=BTN_HOV, activeforeground=ACCENT,
                      relief="flat", bd=0, cursor="hand2",
                      command=cmd, width=2).pack(side="left", padx=2)

        # Right — notes
        right = tk.Frame(outer, bg=BG)
        right.pack(side="right", padx=(10, 0))
        rc = tk.Canvas(right, width=28, height=88, bg=BG, highlightthickness=0)
        rc.pack()
        self._draw_deco(rc)

        # ── Bottom bar ────────────────────────────────────────────────────
        tk.Frame(self.root, bg=DIM, height=1).pack(fill="x")
        bot = tk.Frame(self.root, bg=TITLEBAR_BG)
        bot.pack(fill="x")

        self.status_var = tk.StringVar(value="● playing")
        tk.Label(bot, textvariable=self.status_var,
                 font=tkfont.Font(family="Courier New", size=9),
                 bg=TITLEBAR_BG, fg=SUBTEXT).pack(side="left", padx=(10, 0), pady=3)

        # "made by corazonthedev" — sub-frame so order is correct
        right_bot = tk.Frame(bot, bg=TITLEBAR_BG)
        right_bot.pack(side="right", padx=(0, 10), pady=3)

        tk.Label(right_bot, text="made by ",
                 font=tkfont.Font(family="Courier New", size=7),
                 bg=TITLEBAR_BG, fg=SUBTEXT).pack(side="left")

        dev = tk.Label(right_bot, text="corazonthedev",
                       font=tkfont.Font(family="Courier New", size=7, underline=True),
                       bg=TITLEBAR_BG, fg=ACCENT, cursor="hand2")
        dev.pack(side="left")
        dev.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/corazonthedev"))
        dev.bind("<Enter>",    lambda e: dev.config(fg=ACCENT2))
        dev.bind("<Leave>",    lambda e: dev.config(fg=ACCENT))

    # ── Drawing ───────────────────────────────────────────────────────────
    def _draw_girl(self, c):
        h  = "#1a0808"
        sk = "#e8c49a"
        ac = ACCENT

        c.create_rectangle(8, 46, 54, 86, fill="#1e1e2e", outline="")
        c.create_rectangle(12, 46, 50, 60, fill="#16162a", outline="")
        c.create_rectangle(25, 38, 37, 48, fill=sk, outline="")
        c.create_oval(8, 6, 54, 50, fill=h, outline="")
        c.create_oval(14, 12, 48, 44, fill=sk, outline="")
        c.create_polygon(14,14, 10,26, 16,22, 14,30, 22,20, 30,15, fill=h, outline="")
        c.create_rectangle(16, 22, 27, 30, outline=ac, width=1)
        c.create_rectangle(33, 22, 44, 30, outline=ac, width=1)
        c.create_line(27, 26, 33, 26, fill=ac, width=1)
        c.create_line(19, 26, 25, 26, fill=h, width=1)
        c.create_line(35, 26, 41, 26, fill=h, width=1)
        c.create_arc(24, 30, 38, 40, start=200, extent=140, style="arc", outline=h, width=1)
        c.create_arc( 8,  8, 22, 32, start= 90, extent=180, outline=ac, width=2, style="arc")
        c.create_arc(40,  8, 54, 32, start=270, extent=180, outline=ac, width=2, style="arc")
        c.create_oval( 6, 16, 14, 25, fill=ac, outline="")
        c.create_oval(48, 16, 56, 25, fill=ac, outline="")
        c.create_rectangle(7, 62, 55, 82, fill="#c9a050", outline="")
        c.create_line(31, 62, 31, 82, fill=BG, width=1)
        c.create_line(10, 69, 29, 69, fill=BG, width=1)
        c.create_line(10, 74, 29, 74, fill=BG, width=1)
        c.create_line(33, 69, 52, 69, fill=BG, width=1)

    def _draw_deco(self, c):
        nf     = tkfont.Font(size=9)
        notes  = ["♪", "♫", "♩", "♬"]
        colors = [ACCENT, DIM, ACCENT, DIM]
        for i, (n, col) in enumerate(zip(notes, colors)):
            c.create_text(14, 12 + i * 20, text=n, fill=col, font=nf)

    # ── Controls ──────────────────────────────────────────────────────────
    def _draw_vol_bar(self):
        self.vol_bar.delete("all")
        w = int(80 * state.volume)
        self.vol_bar.create_rectangle(0, 0, 80, 5, fill=DIM,   outline="")
        self.vol_bar.create_rectangle(0, 0,  w, 5, fill=ACCENT, outline="")

    def _click_vol(self, e):
        state.volume = max(0.0, min(1.0, e.x / 80))
        self._draw_vol_bar()
        self.vol_lbl.config(text=f"{int(state.volume*100)}%")

    def _toggle(self):
        if state.playing:
            do_stop()
            self.pp_btn.config(text="▶")
            self.status_var.set("⏸  paused")
        else:
            do_start()
            self.pp_btn.config(text="⏸")
            self.status_var.set("● playing")

    def _vol_up(self):
        state.volume = min(1.0, state.volume + 0.1)
        self._draw_vol_bar()
        self.vol_lbl.config(text=f"{int(state.volume*100)}%")

    def _vol_down(self):
        state.volume = max(0.0, state.volume - 0.1)
        self._draw_vol_bar()
        self.vol_lbl.config(text=f"{int(state.volume*100)}%")

    def _quit(self):
        do_stop()
        self.root.destroy()

    def _minimize(self):
        # Hide completely — appears in system tray/hidden icons, not as a floating window
        self.root.withdraw()
        self._setup_tray()

    def _setup_tray(self):
        try:
            import pystray
            from PIL import Image
            _, icon_path = make_icon_file()
            png_path, _ = make_icon_file()
            if png_path:
                img = Image.open(png_path)
            else:
                img = Image.new("RGB", (64, 64), (14, 14, 18))
            menu = pystray.Menu(
                pystray.MenuItem("Show", lambda: self.root.after(0, self._restore)),
                pystray.MenuItem("Quit", lambda: self.root.after(0, self._quit)),
            )
            self._tray_icon = pystray.Icon("lofi radio", img, "lofi girl radio", menu)
            import threading
            threading.Thread(target=self._tray_icon.run, daemon=True).start()
        except Exception:
            # pystray not available: just restore after short delay
            self.root.after(3000, self._restore)

    def _restore(self):
        try:
            self._tray_icon.stop()
        except Exception:
            pass
        self.root.deiconify()

    def _tick(self):
        if state.start_time:
            elapsed = int(time.time() - state.start_time)
            m, s    = divmod(elapsed, 60)
            self.timer_var.set(f"{m:02d}:{s:02d}")
        self.root.after(1000, self._tick)


def main():
    root = tk.Tk()
    LofiApp(root)
    root.mainloop()
    do_stop()

if __name__ == '__main__':
    main()
