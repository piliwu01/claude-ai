import warnings
warnings.filterwarnings("ignore")

import os
import json
import threading
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "slide_state.json")
SLIDES_DIR = ""

HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>霹靂簡報</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #000; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
  img { max-width: 100vw; max-height: 100vh; object-fit: contain; transition: opacity 0.15s; }
  #info {
    position: fixed; bottom: 12px; right: 16px;
    color: rgba(255,255,255,0.45); font-family: monospace; font-size: 13px;
    background: rgba(0,0,0,0.4); padding: 4px 10px; border-radius: 6px;
  }
</style>
</head>
<body>
<img id="slide" src="/slides/slide_001.png">
<div id="info">第 <span id="cur">1</span> / <span id="tot">?</span> 頁</div>
<script>
let lastSlide = 0;
async function poll() {
  try {
    const res = await fetch('/state?' + Date.now());
    if (!res.ok) return;
    const data = await res.json();
    document.getElementById('cur').textContent = data.current;
    document.getElementById('tot').textContent = data.total;
    if (data.current !== lastSlide) {
      lastSlide = data.current;
      const num = String(data.current).padStart(3, '0');
      const img = document.getElementById('slide');
      img.style.opacity = '0.5';
      img.onload = () => { img.style.opacity = '1'; };
      img.src = '/slides/slide_' + num + '.png?' + Date.now();
    }
  } catch(e) {}
}
setInterval(poll, 500);
poll();
</script>
</body>
</html>"""


def read_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"current": 1, "total": 0}


def write_state(data):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


class SlideHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        if path in ("/", "/index.html"):
            body = HTML_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif path == "/state":
            state = read_state()
            body = json.dumps(state, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif path.startswith("/slides/"):
            filename = path[8:]
            filepath = os.path.join(SLIDES_DIR, filename)
            if os.path.isfile(filepath):
                with open(filepath, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("霹靂簡報控制器 v1.0")
        self.resizable(False, False)
        self.configure(bg="#f0f4f8")
        self.geometry("540x600")

        self.pptx_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="⚡ 霹靂簡報控制器",
                 font=("微軟正黑體", 18, "bold"),
                 bg="#f0f4f8", fg="#1e293b").pack(pady=(20, 2))
        tk.Label(self, text="讓霹靂掌控您的 PowerPoint 投影片",
                 font=("微軟正黑體", 10),
                 bg="#f0f4f8", fg="#64748b").pack(pady=(0, 15))

        # Card 1: PPTX
        card1 = tk.LabelFrame(self, text="  選擇 PowerPoint 檔案  ",
                               font=("微軟正黑體", 10, "bold"),
                               bg="#ffffff", fg="#334155",
                               relief="groove", bd=1, padx=10, pady=8)
        card1.pack(fill="x", padx=20, pady=5)
        row1 = tk.Frame(card1, bg="#ffffff")
        row1.pack(fill="x")
        tk.Entry(row1, textvariable=self.pptx_path,
                 font=("微軟正黑體", 10), relief="solid", bd=1,
                 width=42).pack(side="left", padx=(0, 8), ipady=4)
        tk.Button(row1, text="瀏覽", bg="#2563eb", fg="white",
                  font=("微軟正黑體", 10, "bold"),
                  relief="flat", padx=10, cursor="hand2",
                  command=self._pick_pptx).pack(side="left")

        # Card 2: Output dir
        card2 = tk.LabelFrame(self, text="  投影片圖片輸出資料夾  ",
                               font=("微軟正黑體", 10, "bold"),
                               bg="#ffffff", fg="#334155",
                               relief="groove", bd=1, padx=10, pady=8)
        card2.pack(fill="x", padx=20, pady=5)
        row2 = tk.Frame(card2, bg="#ffffff")
        row2.pack(fill="x")
        tk.Entry(row2, textvariable=self.output_dir,
                 font=("微軟正黑體", 10), relief="solid", bd=1,
                 width=42).pack(side="left", padx=(0, 8), ipady=4)
        tk.Button(row2, text="瀏覽", bg="#2563eb", fg="white",
                  font=("微軟正黑體", 10, "bold"),
                  relief="flat", padx=10, cursor="hand2",
                  command=self._pick_dir).pack(side="left")

        tk.Label(card2,
                 text="※ 未選擇時，預設建立於 PPTX 同資料夾的 pili_slides 子資料夾",
                 font=("微軟正黑體", 8), bg="#ffffff", fg="#94a3b8").pack(anchor="w")

        # Start button
        self.start_btn = tk.Button(self, text="⚡ 啟動霹靂控制器",
                                   bg="#16a34a", fg="white",
                                   font=("微軟正黑體", 13, "bold"),
                                   relief="flat", padx=30, pady=10,
                                   cursor="hand2",
                                   command=self._start)
        self.start_btn.pack(pady=15)

        # Progress bar
        self.progress = ttk.Progressbar(self, mode="determinate", length=480)
        self.progress.pack(padx=20)

        # Log area
        log_frame = tk.LabelFrame(self, text="  執行記錄  ",
                                   font=("微軟正黑體", 10, "bold"),
                                   bg="#ffffff", fg="#334155",
                                   relief="groove", bd=1, padx=5, pady=5)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.log_box = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            bg="#1e293b", fg="#94a3b8",
            relief="flat", bd=0,
            height=10, state="disabled")
        self.log_box.pack(fill="both", expand=True)
        self.log_box.tag_config("ok", foreground="#4ade80")
        self.log_box.tag_config("err", foreground="#f87171")
        self.log_box.tag_config("sep", foreground="#475569")

    def _pick_pptx(self):
        path = filedialog.askopenfilename(
            title="選擇 PowerPoint 檔案",
            filetypes=[("PowerPoint 檔案", "*.pptx *.ppt")])
        if path:
            self.pptx_path.set(path)
            if not self.output_dir.get():
                self.output_dir.set(
                    os.path.join(os.path.dirname(path), "pili_slides"))

    def _pick_dir(self):
        d = filedialog.askdirectory(title="選擇輸出資料夾")
        if d:
            self.output_dir.set(d)

    def _log(self, msg, tag=None):
        self.log_box.config(state="normal")
        self.log_box.insert("end", msg + "\n", tag or "")
        self.log_box.see("end")
        self.log_box.config(state="disabled")
        self.update_idletasks()

    def _start(self):
        if not self.pptx_path.get():
            self._log("❌ 請先選擇 PPTX 檔案", "err")
            return
        self.start_btn.config(state="disabled", text="執行中…")
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        global SLIDES_DIR
        pptx = self.pptx_path.get()
        outdir = self.output_dir.get() or os.path.join(
            os.path.dirname(pptx), "pili_slides")

        os.makedirs(outdir, exist_ok=True)
        SLIDES_DIR = outdir

        self._log("=== 霹靂簡報控制器啟動 ===", "sep")
        self._log(f"📄 PPTX：{os.path.basename(pptx)}")
        self._log(f"📁 輸出：{outdir}")

        # Export via PowerPoint COM
        try:
            import win32com.client
        except ImportError:
            self._log("❌ 缺少 pywin32，請執行：pip install pywin32", "err")
            self.start_btn.config(state="normal", text="⚡ 啟動霹靂控制器")
            return

        try:
            self._log("⚡ 正在透過 PowerPoint 匯出投影片圖片…")
            ppt_app = win32com.client.Dispatch("PowerPoint.Application")
            ppt_app.Visible = True
            abs_pptx = os.path.abspath(pptx)
            presentation = ppt_app.Presentations.Open(abs_pptx)
            total = presentation.Slides.Count

            self.progress["maximum"] = total
            self.progress["value"] = 0

            for i in range(1, total + 1):
                img_path = os.path.abspath(
                    os.path.join(outdir, f"slide_{i:03d}.png"))
                presentation.Slides(i).Export(img_path, "PNG", 1920, 1080)
                self.progress["value"] = i
                self._log(f"  ✅ 第 {i}/{total} 頁匯出完成", "ok")

            presentation.Close()
            ppt_app.Quit()

            write_state({"current": 1, "total": total})
            self._log(f"✅ 共 {total} 頁匯出完成，伺服器即將啟動…", "ok")

        except Exception as e:
            self._log(f"❌ 匯出失敗：{e}", "err")
            self.start_btn.config(state="normal", text="⚡ 啟動霹靂控制器")
            return

        # Start HTTP server
        try:
            httpd = HTTPServer(("localhost", 3000), SlideHandler)
            self._log("=== 伺服器已啟動 ===", "sep")
            self._log("✅ http://localhost:3000  （瀏覽器已自動開啟）", "ok")
            self._log("✅ 告訴霹靂「下一頁」即可控制投影片", "ok")
            webbrowser.open("http://localhost:3000")
            httpd.serve_forever()
        except OSError as e:
            self._log(f"❌ 伺服器錯誤（port 3000 可能已被占用）：{e}", "err")
            self.start_btn.config(state="normal", text="⚡ 啟動霹靂控制器")


if __name__ == "__main__":
    App().mainloop()
