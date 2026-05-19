import warnings
warnings.filterwarnings("ignore")

import os
import sys
import json
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

import parser as schedule_parser
import excel_writer

# ── 路徑設定 ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
CACHE_PATH = os.path.join(BASE_DIR, '課表快取.json')
OVERRIDES_PATH = os.path.join(BASE_DIR, 'overrides.json')

DEFAULT_PDF = r'C:\Users\北興\Desktop\520師課表.pdf'
DEFAULT_EXCEL = r'C:\Users\北興\Desktop\114學年代課.xlsx'

# ── 色彩 ──────────────────────────────────────────────────
C_BG = '#f0f4f8'
C_CARD = '#ffffff'
C_TITLE = '#1e293b'
C_SUB = '#64748b'
C_BTN_BLUE = '#2563eb'
C_BTN_GREEN = '#16a34a'
C_LOG_BG = '#1e293b'
C_LOG_FG = '#94a3b8'
C_OK = '#4ade80'
C_ERR = '#f87171'
C_JIAN = '#BDD7EE'

DAYS = ['一', '二', '三', '四', '五']


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {'pdf': DEFAULT_PDF, 'excel': DEFAULT_EXCEL}


def save_config(cfg):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('課表查詢系統 v1.0')
        self.resizable(True, True)
        self.minsize(860, 720)
        self.configure(bg=C_BG)

        self.cfg = load_config()
        self.schedule_data = {}   # {教師: {科別, schedule}}
        self.all_teachers = []
        self.selected_teachers = []   # 複選教師清單（有序）
        self.preview_records = []     # 目前預覽中的資料（含 '教師' 欄）
        self.overrides = schedule_parser.load_overrides(OVERRIDES_PATH)

        self._build_ui()
        self.after(100, self._init_load)

    # ── UI 建構 ──────────────────────────────────────────
    def _build_ui(self):
        # Treeview 字型放大（需透過 ttk.Style 設定）
        style = ttk.Style(self)
        style.configure('Treeview', font=('微軟正黑體', 12), rowheight=28)
        style.configure('Treeview.Heading', font=('微軟正黑體', 12, 'bold'))

        # Combobox 下拉清單字型
        self.option_add('*TCombobox*Listbox.font', ('微軟正黑體', 12))
        self.option_add('*TCombobox*Listbox.selectBackground', '#2563eb')

        # 主視窗 grid 設定：預覽列(3)和記錄列(7)會隨視窗縮放
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=3)   # 預覽卡得到較多空間
        self.rowconfigure(7, weight=1)   # 記錄區得到較少空間

        # Row 0：標題
        header = tk.Frame(self, bg=C_BG)
        header.grid(row=0, column=0, sticky='ew', padx=20, pady=(16, 4))
        tk.Label(header, text='課表查詢系統', font=('微軟正黑體', 22, 'bold'),
                 bg=C_BG, fg=C_TITLE).pack(anchor='w')
        tk.Label(header, text='嘉義市立北興國中 114 學年度第二學期',
                 font=('微軟正黑體', 12), bg=C_BG, fg=C_SUB).pack(anchor='w')

        # Row 1：檔案設定卡
        file_card = self._card(self, '  檔案設定  ')
        file_card.grid(row=1, column=0, sticky='ew', padx=20, pady=(8, 4))

        self.pdf_var = tk.StringVar(value=self.cfg.get('pdf', DEFAULT_PDF))
        self.excel_var = tk.StringVar(value=self.cfg.get('excel', DEFAULT_EXCEL))

        self._file_row(file_card, 'PDF 課表：', self.pdf_var, self._browse_pdf)
        self._file_row(file_card, 'Excel 代課單：', self.excel_var, self._browse_excel)

        btn_row = tk.Frame(file_card, bg=C_CARD)
        btn_row.pack(fill='x', pady=(4, 0))
        tk.Button(btn_row, text='修正科別',
                  font=('微軟正黑體', 11), bg='#e2e8f0',
                  relief='flat', padx=8, cursor='hand2',
                  command=self._open_override_dialog).pack(side='left')
        tk.Button(btn_row, text='重新解析課表 PDF',
                  font=('微軟正黑體', 11), bg='#e2e8f0',
                  relief='flat', padx=8, cursor='hand2',
                  command=self._force_reload).pack(side='right')

        # Row 2：查詢條件卡
        query_card = self._card(self, '  查詢條件  ')
        query_card.grid(row=2, column=0, sticky='ew', padx=20, pady=4)

        # ── 教師搜尋列
        teacher_row = tk.Frame(query_card, bg=C_CARD)
        teacher_row.pack(fill='x', pady=(0, 4))
        tk.Label(teacher_row, text='搜尋教師：', font=('微軟正黑體', 12),
                 bg=C_CARD, fg=C_TITLE, width=10, anchor='w').pack(side='left')

        self.teacher_var = tk.StringVar()
        self.teacher_combo = ttk.Combobox(teacher_row, textvariable=self.teacher_var,
                                          font=('微軟正黑體', 12), width=18, state='normal')
        self.teacher_combo.pack(side='left', ipady=3, padx=(0, 6))
        self.teacher_combo.bind('<KeyRelease>', self._filter_teachers)
        self.teacher_combo.bind('<<ComboboxSelected>>', lambda e: self._add_teacher())
        tk.Button(teacher_row, text='加入', bg=C_BTN_BLUE, fg='white',
                  font=('微軟正黑體', 11, 'bold'), relief='flat',
                  padx=10, cursor='hand2',
                  command=self._add_teacher).pack(side='left')
        tk.Button(teacher_row, text='全部清除', bg='#e2e8f0',
                  font=('微軟正黑體', 11), relief='flat',
                  padx=8, cursor='hand2',
                  command=self._clear_teachers).pack(side='left', padx=(6, 0))

        # ── 已選教師清單
        sel_row = tk.Frame(query_card, bg=C_CARD)
        sel_row.pack(fill='x', pady=(0, 6))
        tk.Label(sel_row, text='已選教師：', font=('微軟正黑體', 12),
                 bg=C_CARD, fg=C_TITLE, width=10, anchor='nw').pack(side='left')

        sel_inner = tk.Frame(sel_row, bg=C_CARD)
        sel_inner.pack(side='left', fill='both', expand=True)

        self.sel_listbox = tk.Listbox(sel_inner,
                                      font=('微軟正黑體', 12), height=4,
                                      selectmode='extended',
                                      bg='#f8fafc', fg=C_TITLE,
                                      selectbackground=C_BTN_BLUE,
                                      selectforeground='white',
                                      relief='solid', bd=1)
        self.sel_listbox.pack(side='left', fill='both', expand=True)

        sel_scroll = ttk.Scrollbar(sel_inner, orient='vertical',
                                   command=self.sel_listbox.yview)
        self.sel_listbox.configure(yscrollcommand=sel_scroll.set)
        sel_scroll.pack(side='left', fill='y')

        tk.Button(sel_row, text='移除選取', bg='#e2e8f0',
                  font=('微軟正黑體', 11), relief='flat',
                  padx=8, cursor='hand2',
                  command=self._remove_selected_teachers).pack(side='left', padx=(6, 0), anchor='n')

        day_row = tk.Frame(query_card, bg=C_CARD)
        day_row.pack(fill='x', pady=(0, 4))
        tk.Label(day_row, text='選擇星期：', font=('微軟正黑體', 12),
                 bg=C_CARD, fg=C_TITLE, width=10, anchor='w').pack(side='left')

        self.day_vars = {}
        for day in DAYS:
            v = tk.BooleanVar(value=False)
            self.day_vars[day] = v
            tk.Checkbutton(day_row, text=f'星期{day}', variable=v,
                           font=('微軟正黑體', 12), bg=C_CARD, fg=C_TITLE,
                           activebackground=C_CARD, selectcolor=C_CARD).pack(side='left', padx=4)

        # 週別選擇
        week_row = tk.Frame(query_card, bg=C_CARD)
        week_row.pack(fill='x', pady=(0, 4))
        tk.Label(week_row, text='選擇週別：', font=('微軟正黑體', 12),
                 bg=C_CARD, fg=C_TITLE, width=10, anchor='w').pack(side='left')
        self.week_var = tk.StringVar(value='全部')
        for w in ['全部', '單週', '雙週']:
            tk.Radiobutton(week_row, text=w, variable=self.week_var, value=w,
                           font=('微軟正黑體', 12), bg=C_CARD, fg=C_TITLE,
                           activebackground=C_CARD, selectcolor=C_CARD).pack(side='left', padx=8)

        tk.Button(query_card, text='查詢', bg=C_BTN_BLUE, fg='white',
                  font=('微軟正黑體', 12, 'bold'), relief='flat',
                  padx=16, cursor='hand2', command=self._query).pack(anchor='e', pady=(4, 0))

        # Row 3：預覽卡（隨視窗縱向擴展）
        preview_card = self._card(self, '  課表預覽  ')
        preview_card.grid(row=3, column=0, sticky='nsew', padx=20, pady=4)
        preview_card.columnconfigure(0, weight=1)
        preview_card.rowconfigure(0, weight=1)

        cols = ('教師', '節次', '星期', '科目', '班級', '備註')
        self.tree = ttk.Treeview(preview_card, columns=cols, show='headings')
        col_widths = {'教師': 90, '節次': 60, '星期': 80, '科目': 160, '班級': 80, '備註': 80}
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=col_widths[c], anchor='center', stretch=True)
        self.tree.tag_configure('jian', background=C_JIAN)

        vsb = ttk.Scrollbar(preview_card, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')

        # Row 4：預覽計數
        self.preview_label = tk.Label(self, text='', font=('微軟正黑體', 11),
                                      bg=C_BG, fg=C_SUB)
        self.preview_label.grid(row=4, column=0, sticky='e', padx=22)

        # Row 5：寫入按鈕
        tk.Button(self, text='寫入總表', bg=C_BTN_GREEN, fg='white',
                  font=('微軟正黑體', 15, 'bold'), relief='flat',
                  padx=30, pady=10, cursor='hand2',
                  command=self._write).grid(row=5, column=0, pady=(8, 4))

        # Row 6：進度條
        self.progress = ttk.Progressbar(self, orient='horizontal', mode='determinate')
        self.progress.grid(row=6, column=0, sticky='ew', padx=20, pady=(0, 4))

        # Row 7：記錄區（隨視窗縱向擴展）
        self.log = ScrolledText(self, bg=C_LOG_BG, fg=C_LOG_FG,
                                font=('Consolas', 11), relief='flat',
                                state='disabled', wrap='word')
        self.log.grid(row=7, column=0, sticky='nsew', padx=20, pady=(0, 16))
        self.log.tag_config('ok', foreground=C_OK)
        self.log.tag_config('err', foreground=C_ERR)
        self.log.tag_config('sep', foreground='#475569')

    def _card(self, parent, title):
        return tk.LabelFrame(parent, text=title,
                              font=('微軟正黑體', 12, 'bold'),
                              bg=C_CARD, fg='#334155',
                              relief='groove', bd=1, padx=10, pady=8)

    def _file_row(self, parent, label, var, cmd):
        row = tk.Frame(parent, bg=C_CARD)
        row.pack(fill='x', pady=2)
        tk.Label(row, text=label, font=('微軟正黑體', 11),
                 bg=C_CARD, fg=C_TITLE, width=12, anchor='w').pack(side='left')
        tk.Entry(row, textvariable=var, font=('微軟正黑體', 11),
                 relief='solid', bd=1, width=40).pack(side='left', ipady=3, padx=(0, 4))
        tk.Button(row, text='瀏覽', font=('微軟正黑體', 11), bg='#e2e8f0',
                  relief='flat', padx=6, cursor='hand2', command=cmd).pack(side='left')

    # ── 檔案瀏覽 ──────────────────────────────────────────
    def _browse_pdf(self):
        path = filedialog.askopenfilename(
            title='選擇 PDF 課表',
            filetypes=[('PDF 檔案', '*.pdf'), ('所有檔案', '*.*')])
        if path:
            self.pdf_var.set(path)
            self._save_paths()

    def _browse_excel(self):
        path = filedialog.askopenfilename(
            title='選擇 Excel 代課單',
            filetypes=[('Excel 檔案', '*.xlsx'), ('所有檔案', '*.*')])
        if path:
            self.excel_var.set(path)
            self._save_paths()

    def _save_paths(self):
        self.cfg['pdf'] = self.pdf_var.get()
        self.cfg['excel'] = self.excel_var.get()
        save_config(self.cfg)

    # ── 初始載入 ─────────────────────────────────────────
    def _init_load(self):
        if os.path.exists(CACHE_PATH):
            self._log('📂 載入快取...', 'ok')
            try:
                self.schedule_data = schedule_parser.load_cache(CACHE_PATH)
                schedule_parser.apply_overrides(self.schedule_data, self.overrides)
                self._update_teacher_list()
                self._log(f'✅ 已載入 {len(self.schedule_data)} 位教師的課表', 'ok')
            except Exception as e:
                self._log(f'❌ 快取讀取失敗，將重新解析：{e}', 'err')
                self._parse_pdf()
        else:
            self._log('🔍 找不到快取，開始解析 PDF...', 'sep')
            self._parse_pdf()

    def _force_reload(self):
        self._log('=== 強制重新解析 PDF ===', 'sep')
        self._parse_pdf()

    def _parse_pdf(self):
        pdf = self.pdf_var.get()
        excel = self.excel_var.get()
        if not os.path.exists(pdf):
            self._log(f'❌ 找不到 PDF：{pdf}', 'err')
            return
        if not os.path.exists(excel):
            self._log(f'❌ 找不到 Excel：{excel}', 'err')
            return

        self._save_paths()
        self.progress['value'] = 0

        def run():
            try:
                def cb(done, total):
                    pct = int(done / total * 100)
                    self.progress['value'] = pct
                    if done % 20 == 0 or done == total:
                        self._log(f'  解析中 {done}/{total}...', 'sep')

                data = schedule_parser.parse_pdf(pdf, excel, progress_callback=cb)
                schedule_parser.apply_overrides(data, self.overrides)
                schedule_parser.save_cache(data, CACHE_PATH)
                self.schedule_data = data
                self._update_teacher_list()
                self._log(f'✅ 解析完成，共 {len(data)} 位教師，已儲存快取', 'ok')
                self.progress['value'] = 100
            except Exception as e:
                self._log(f'❌ 解析失敗：{e}', 'err')

        threading.Thread(target=run, daemon=True).start()

    def _update_teacher_list(self):
        self.all_teachers = sorted(self.schedule_data.keys())
        self.teacher_combo['values'] = self.all_teachers

    # ── 教師篩選 ─────────────────────────────────────────
    def _filter_teachers(self, event=None):
        typed = self.teacher_var.get()
        if typed:
            filtered = [t for t in self.all_teachers if typed in t]
        else:
            filtered = self.all_teachers
        self.teacher_combo['values'] = filtered

    # ── 複選教師管理 ─────────────────────────────────────
    def _add_teacher(self):
        name = self.teacher_var.get().strip()
        if not name:
            return
        if name not in self.schedule_data:
            messagebox.showwarning('提示', f'找不到教師「{name}」的課表資料')
            return
        if name in self.selected_teachers:
            return  # 已在清單中，不重複加入
        self.selected_teachers.append(name)
        self.sel_listbox.insert('end', name)
        self.teacher_var.set('')
        self.teacher_combo['values'] = self.all_teachers

    def _remove_selected_teachers(self):
        # 從後往前刪，避免 index 偏移
        indices = list(self.sel_listbox.curselection())
        for i in reversed(indices):
            self.sel_listbox.delete(i)
            del self.selected_teachers[i]

    def _clear_teachers(self):
        self.selected_teachers.clear()
        self.sel_listbox.delete(0, 'end')

    # ── 查詢 ─────────────────────────────────────────────
    def _query(self):
        # 若搜尋欄還有文字但尚未加入，自動嘗試加入
        typed = self.teacher_var.get().strip()
        if typed and typed in self.schedule_data and typed not in self.selected_teachers:
            self._add_teacher()

        if not self.selected_teachers:
            messagebox.showwarning('提示', '請先加入至少一位教師')
            return

        selected_days = [d for d in DAYS if self.day_vars[d].get()]
        if not selected_days:
            messagebox.showwarning('提示', '請至少勾選一個星期')
            return

        week_filter = self.week_var.get()  # '全部' / '單週' / '雙週'
        records = []

        for teacher in self.selected_teachers:
            if teacher not in self.schedule_data:
                continue
            info = self.schedule_data[teacher]
            for day in DAYS:
                if day not in selected_days:
                    continue
                for entry in info['schedule'].get(day, []):
                    wk = entry.get('週別', '')
                    if week_filter == '單週' and wk == '雙週':
                        continue
                    if week_filter == '雙週' and wk == '單週':
                        continue
                    records.append({
                        '教師': teacher,
                        '星期': day,
                        '節次': entry['節次'],
                        '科目': entry['科目'],
                        '班級': entry['班級'],
                        '兼課': entry['兼課'],
                        '週別': wk,
                    })

        # 依教師順序、星期、節次排序
        teacher_order = {t: i for i, t in enumerate(self.selected_teachers)}
        records.sort(key=lambda r: (teacher_order[r['教師']], DAYS.index(r['星期']), r['節次']))
        self.preview_records = records

        # 清空並填入 Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        for r in records:
            tag = ('jian',) if r['兼課'] else ()
            notes = []
            if r['兼課']: notes.append('兼課')
            if r['週別']: notes.append(r['週別'])
            self.tree.insert('', 'end',
                             values=(r['教師'], r['節次'], f"星期{r['星期']}",
                                     r['科目'], r['班級'], ' '.join(notes)),
                             tags=tag)

        days_str = '、'.join(f'星期{d}' for d in selected_days)
        teachers_str = '、'.join(self.selected_teachers)
        self.preview_label.config(
            text=f'{teachers_str}  {days_str}  共 {len(records)} 節')
        self._log(f'📋 查詢 {teachers_str} {days_str}：{len(records)} 筆', 'ok')

    # ── 寫入總表 ─────────────────────────────────────────
    def _write(self):
        if not self.preview_records:
            messagebox.showwarning('提示', '請先執行查詢')
            return

        excel = self.excel_var.get()
        if not os.path.exists(excel):
            self._log(f'❌ 找不到 Excel：{excel}', 'err')
            return

        # 依教師分組
        from collections import defaultdict
        records_by_teacher = defaultdict(list)
        for r in self.preview_records:
            records_by_teacher[r['教師']].append(r)

        # 重複寫入防呆（每位教師各別確認）
        try:
            import openpyxl as _xl
            _wb = _xl.load_workbook(excel)
            _ws = _wb['總表']
            skip_teachers = set()
            for teacher, recs in records_by_teacher.items():
                selected_days = list({r['星期'] for r in recs})
                dupes = excel_writer.check_duplicate(_ws, teacher, selected_days)
                if dupes:
                    days_str = '、'.join(f'星期{d}' for d in sorted(dupes, key=DAYS.index))
                    ok = messagebox.askyesno(
                        '重複確認',
                        f'總表中已有「{teacher}」{days_str}的資料。\n確定要繼續寫入嗎？')
                    if not ok:
                        skip_teachers.add(teacher)
                        self._log(f'⚠️ 跳過 {teacher}', 'err')
        except Exception as e:
            self._log(f'⚠️ 重複檢查失敗（仍繼續寫入）：{e}', 'err')
            skip_teachers = set()

        def run():
            total = 0
            for teacher, recs in records_by_teacher.items():
                if teacher in skip_teachers:
                    continue
                subject = self.schedule_data[teacher]['科別']
                try:
                    count = excel_writer.write_to_zongbiao(excel, teacher, subject, recs)
                    self._log(f'✅ {teacher}：寫入 {count} 筆', 'ok')
                    total += count
                except Exception as e:
                    self._log(f'❌ {teacher} 寫入失敗：{e}', 'err')
            if total:
                self._log(f'=== 共寫入 {total} 筆到總表 ===', 'sep')

        threading.Thread(target=run, daemon=True).start()

    # ── 修正科別彈窗 ─────────────────────────────────────
    def _open_override_dialog(self):
        if not self.all_teachers:
            messagebox.showwarning('提示', '請先載入課表後再修正科別')
            return

        win = tk.Toplevel(self)
        win.title('修正科別')
        win.resizable(False, False)
        win.configure(bg=C_BG)
        win.grab_set()

        # 取科別清單（從現有資料 + 常見科別）
        all_depts = sorted({v['科別'] for v in self.schedule_data.values() if v['科別']})
        extra = ['國文','英語','數學','生物','理化','科技','資訊','歷史',
                 '地理','公民','音樂','美術','表藝','健教','體育','家政',
                 '童軍','輔導','特教']
        dept_list = sorted(set(all_depts + extra))

        pad = dict(padx=14, pady=6)

        tk.Label(win, text='修正教師科別對應', font=('微軟正黑體', 15, 'bold'),
                 bg=C_BG, fg=C_TITLE).grid(row=0, column=0, columnspan=2, **pad)

        # 教師選單
        tk.Label(win, text='教師姓名：', font=('微軟正黑體', 12),
                 bg=C_BG, fg=C_TITLE).grid(row=1, column=0, sticky='e', padx=(14,4), pady=4)
        t_var = tk.StringVar()
        t_combo = ttk.Combobox(win, textvariable=t_var, values=self.all_teachers,
                               font=('微軟正黑體', 12), width=16)
        t_combo.grid(row=1, column=1, sticky='w', padx=(0,14), pady=4)

        # 顯示目前科別
        cur_lbl = tk.Label(win, text='目前科別：—', font=('微軟正黑體', 11),
                           bg=C_BG, fg=C_SUB)
        cur_lbl.grid(row=2, column=0, columnspan=2, pady=(0,4))

        def on_teacher_select(event=None):
            t = t_var.get()
            if t in self.schedule_data:
                dept = self.schedule_data[t]['科別']
                cur_lbl.config(text=f'目前科別：{dept or "（未設定）"}')
                if dept in dept_list:
                    d_combo.set(dept)

        t_combo.bind('<<ComboboxSelected>>', on_teacher_select)
        t_combo.bind('<KeyRelease>', lambda e: [
            t_combo.configure(values=[x for x in self.all_teachers if t_var.get() in x]),
            on_teacher_select()
        ])

        # 科別選單
        tk.Label(win, text='修正為：', font=('微軟正黑體', 12),
                 bg=C_BG, fg=C_TITLE).grid(row=3, column=0, sticky='e', padx=(14,4), pady=4)
        d_var = tk.StringVar()
        d_combo = ttk.Combobox(win, textvariable=d_var, values=dept_list,
                               font=('微軟正黑體', 12), width=16)
        d_combo.grid(row=3, column=1, sticky='w', padx=(0,14), pady=4)

        # 現有覆蓋清單
        tk.Label(win, text='已修正的對應：', font=('微軟正黑體', 11, 'bold'),
                 bg=C_BG, fg=C_TITLE).grid(row=4, column=0, columnspan=2, pady=(8,2))
        list_frame = tk.Frame(win, bg=C_LOG_BG, bd=1, relief='solid')
        list_frame.grid(row=5, column=0, columnspan=2, padx=14, pady=(0,8), sticky='ew')
        list_box = tk.Listbox(list_frame, font=('微軟正黑體', 11), height=5,
                              bg=C_LOG_BG, fg=C_LOG_FG, selectbackground='#334155',
                              relief='flat', bd=0)
        list_box.pack(fill='both', padx=4, pady=4)

        def refresh_list():
            list_box.delete(0, 'end')
            for name, dept in sorted(self.overrides.items()):
                list_box.insert('end', f'{name}  →  {dept}')

        refresh_list()

        def do_save():
            teacher = t_var.get().strip()
            dept = d_var.get().strip()
            if not teacher or not dept:
                messagebox.showwarning('提示', '請選擇教師與科別', parent=win)
                return
            self.overrides[teacher] = dept
            schedule_parser.save_overrides(self.overrides, OVERRIDES_PATH)
            schedule_parser.apply_overrides(self.schedule_data, self.overrides)
            refresh_list()
            cur_lbl.config(text=f'目前科別：{dept}')
            self._log(f'✅ 已修正 {teacher} 科別 → {dept}', 'ok')

        def do_delete():
            teacher = t_var.get().strip()
            if teacher in self.overrides:
                del self.overrides[teacher]
                schedule_parser.save_overrides(self.overrides, OVERRIDES_PATH)
                refresh_list()
                self._log(f'🗑 已移除 {teacher} 的科別覆蓋', 'sep')

        btn_f = tk.Frame(win, bg=C_BG)
        btn_f.grid(row=6, column=0, columnspan=2, pady=(0,12))
        tk.Button(btn_f, text='儲存', bg=C_BTN_GREEN, fg='white',
                  font=('微軟正黑體', 12, 'bold'), relief='flat',
                  padx=16, cursor='hand2', command=do_save).pack(side='left', padx=6)
        tk.Button(btn_f, text='移除覆蓋', bg='#e2e8f0',
                  font=('微軟正黑體', 11), relief='flat',
                  padx=10, cursor='hand2', command=do_delete).pack(side='left', padx=6)
        tk.Button(btn_f, text='關閉', bg='#e2e8f0',
                  font=('微軟正黑體', 11), relief='flat',
                  padx=10, cursor='hand2', command=win.destroy).pack(side='left', padx=6)

    # ── 記錄區 ───────────────────────────────────────────
    def _log(self, msg, tag=''):
        def _do():
            self.log.config(state='normal')
            self.log.insert('end', msg + '\n', tag or '')
            self.log.see('end')
            self.log.config(state='disabled')
        self.after(0, _do)


if __name__ == '__main__':
    app = App()
    app.mainloop()
