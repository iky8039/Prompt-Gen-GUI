import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import sys

from . import __version__, APP_NAME

# --- Constants ---
# .exe化しても実行ファイルと同じ場所に設定ファイルを保存するためのパス設定
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        BASE_DIR = os.getcwd()

CONFIG_FILE = os.path.join(BASE_DIR, "keywords_config.json")

# カラーパレット（モダンな配色）
COLORS = {
    "bg_main": "#f5f7f9",
    "bg_sidebar": "#ffffff",
    "primary": "#4a90e2",
    "secondary": "#6c757d",
    "success": "#67c23a",
    "danger": "#f56c6c",
    "warning": "#e6a23c",
    "info": "#909399",
    "text_main": "#333333",
    "text_light": "#ffffff",
    "border": "#dcdfe6"
}

# フォント設定
FONT_TITLE = ("Segoe UI", 12, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)

class PromptBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{__version__}")
        self.root.geometry("700x600")
        self.root.minsize(500, 400)
        self.root.configure(bg=COLORS["bg_main"])

        # 初期キーワード
        self.default_keywords = ['AI', 'Research', 'Code', 'Python', 'Data Science', 'Machine Learning',
                                'NLP', 'GANs', 'Deep Learning', 'Neural Networks']

        self.load_initial_keywords()
        self.delete_mode = False

        # --- UI コンポーネント ---
        self.main_frame = tk.Frame(root, bg=COLORS["bg_main"], padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        # プロンプト入力エリア
        tk.Label(self.main_frame, text="Prompt Composition", font=FONT_TITLE, bg=COLORS["bg_main"], fg=COLORS["text_main"]).pack(anchor="w", pady=(0, 5))
        self.prompt_text = tk.Text(self.main_frame, height=5, font=FONT_NORMAL, bg="#ffffff", fg=COLORS["text_main"],
                                   relief="flat", highlightthickness=1, highlightbackground=COLORS["border"], padx=10, pady=10)
        self.prompt_text.pack(fill="x", pady=(0, 10))

        # ボタン類
        self.btn_frame = tk.Frame(self.main_frame, bg=COLORS["bg_main"])
        self.btn_frame.pack(fill="x", pady=(0, 20))

        self.create_btn(self.btn_frame, "Copy", self.copy_to_clipboard, COLORS["primary"])
        self.create_btn(self.btn_frame, "Save As...", self.save_keywords_as, COLORS["info"])
        self.create_btn(self.btn_frame, "Load (Merge)", self.load_keywords_from, COLORS["secondary"])
        self.create_btn(self.btn_frame, "Reset", self.reset_keywords, COLORS["warning"])

        self.del_btn = tk.Button(self.btn_frame, text="Delete Mode: OFF", command=self.toggle_delete_mode,
                                 bg=COLORS["info"], fg="white", relief="flat", font=FONT_SMALL, padx=10)
        self.del_btn.pack(side="right")

        # 検索・追加エリア
        self.search_frame = tk.Frame(self.main_frame, bg="#ffffff", pady=15, padx=15,
                                     highlightthickness=1, highlightbackground=COLORS["border"])
        self.search_frame.pack(fill="x", pady=(0, 20))

        tk.Label(self.search_frame, text="Search / Add Keywords:", font=FONT_NORMAL, bg="#ffffff", fg=COLORS["text_main"]).pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.update_keyword_ui())
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var, font=FONT_NORMAL,
                                     relief="flat", highlightthickness=1, highlightbackground=COLORS["border"])
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), ipady=3)

        tk.Button(self.search_frame, text="Add +", command=self.add_keyword,
                  bg=COLORS["success"], fg="white", relief="flat", font=FONT_NORMAL, padx=15).pack(side="right")

        # キーワード一覧（スクロール可能）
        self.canvas_container = tk.Frame(self.main_frame, bg=COLORS["bg_main"])
        self.canvas_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.canvas_container, bg=COLORS["bg_main"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.canvas_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["bg_main"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind('<Configure>', self.on_canvas_configure)
        self.root.after(100, self.update_keyword_ui)

    def load_initial_keywords(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    self.my_keywords = json.load(f)
            except Exception:
                self.my_keywords = self.default_keywords.copy()
        else:
            self.my_keywords = self.default_keywords.copy()

    def create_btn(self, parent, text, command, color):
        btn = tk.Button(parent, text=text, command=command, bg=color, fg="white",
                        relief="flat", font=FONT_SMALL, padx=12, pady=5)
        btn.pack(side="left", padx=(0, 5))
        return btn

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.update_keyword_ui()

    def auto_save_keywords(self):
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.my_keywords, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Auto-save failed: {e}")

    def update_keyword_ui(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        search_term = self.search_var.get().lower()
        filtered_keywords = [kw for kw in self.my_keywords if search_term in kw.lower()]

        container_width = self.canvas.winfo_width()
        if container_width < 100: container_width = 600

        btn_width_px = 140
        max_cols = max(1, container_width // btn_width_px)

        for i, kw in enumerate(filtered_keywords):
            tag_color = COLORS["danger"] if self.delete_mode else "#e1f0ff"
            text_color = "white" if self.delete_mode else COLORS["primary"]

            btn = tk.Button(self.scrollable_frame, text=kw,
                            command=lambda k=kw: self.on_kw_click(k),
                            bg=tag_color, fg=text_color, font=FONT_SMALL,
                            relief="flat", padx=10, pady=5,
                            wraplength=110, cursor="hand2")
            btn.grid(row=i // max_cols, column=i % max_cols, padx=5, pady=5, sticky="nsew")

    def on_kw_click(self, kw):
        if self.delete_mode:
            if kw in self.my_keywords:
                self.my_keywords.remove(kw)
                self.auto_save_keywords()
                self.update_keyword_ui()
        else:
            current = self.prompt_text.get("1.0", tk.END).strip()
            self.prompt_text.delete("1.0", tk.END)
            new_text = f"{current}, {kw}" if current else kw
            self.prompt_text.insert("1.0", new_text)

    def toggle_delete_mode(self):
        self.delete_mode = not self.delete_mode
        self.del_btn.config(text=f"Delete Mode: {'ON' if self.delete_mode else 'OFF'}",
                            bg=COLORS["danger"] if self.delete_mode else COLORS["info"])
        self.update_keyword_ui()

    def add_keyword(self):
        added_count = 0
        # 1. 入力フィールドから追加
        input_kw = self.search_var.get().strip()
        if input_kw:
            if input_kw not in self.my_keywords:
                self.my_keywords.append(input_kw)
                added_count += 1
            self.search_var.set("")

        # 2. プロンプト入力エリアから新規単語を抽出して追加
        prompt_content = self.prompt_text.get("1.0", tk.END).strip()
        if prompt_content:
            potential_tags = [t.strip() for t in prompt_content.replace('\n', ',').split(',') if t.strip()]
            for t in potential_tags:
                if t not in self.my_keywords:
                    self.my_keywords.append(t)
                    added_count += 1

        if added_count > 0:
            self.auto_save_keywords()
            self.update_keyword_ui()

    def reset_keywords(self):
        if messagebox.askyesno("Reset", "キーワードリストを初期状態に戻しますか？"):
            self.my_keywords = self.default_keywords.copy()
            self.auto_save_keywords()
            self.update_keyword_ui()

    def copy_to_clipboard(self):
        content = self.prompt_text.get("1.0", tk.END).strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Success", "プロンプトをコピーしました！")

    def save_keywords_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.my_keywords, f, ensure_ascii=False, indent=4)

    def load_keywords_from(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        # 差分取り込み（マージ）ロジック
                        old_set = set(self.my_keywords)
                        new_items = [str(item).strip() for item in data if str(item).strip() and str(item).strip() not in old_set]
                        
                        if new_items:
                            self.my_keywords.extend(new_items)
                            self.auto_save_keywords()
                            self.update_keyword_ui()
                            messagebox.showinfo("Merge Success", f"{len(new_items)}件の新しいキーワードを追加しました。")
                        else:
                            messagebox.showinfo("Merge Info", "新しいキーワードは見つかりませんでした。")
            except Exception as e:
                messagebox.showerror("Error", f"読み込み失敗: {e}")


def main():
    try:
        root = tk.Tk()
        app = PromptBuilderApp(root)
        root.mainloop()
    except tk.TclError:
        print("GUI環境が見つかりません。ローカルPCで実行してください。")


if __name__ == "__main__":
    main()
