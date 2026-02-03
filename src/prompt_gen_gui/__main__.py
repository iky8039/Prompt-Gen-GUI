import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import sys

# 本地導入部分（保留原樣）
try:
    from . import __version__, APP_NAME
except ImportError:
    __version__ = "1.0.0"
    APP_NAME = "Prompt Gen GUI"

# --- Constants ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        BASE_DIR = os.getcwd()

CONFIG_FILE = os.path.join(BASE_DIR, "tags.json")

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

FONT_TITLE = ("Segoe UI", 12, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)

class PromptBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{__version__}")
        self.root.geometry("700x700")
        self.root.minsize(500, 400)
        self.root.configure(bg=COLORS["bg_main"])

        self.default_keywords = {
            "常用": ['AI', 'Research', 'Code', 'Python'],
            "風格": ['Masterpiece', 'High Quality', 'Cyberpunk'],
            "人物": ['1girl', 'Portrait', 'Smiling']
        }

        self.load_initial_keywords()
        self.delete_mode = False
        self.current_category = list(self.my_keywords.keys())[0] if self.my_keywords else "常用"

        self.main_frame = tk.Frame(root, bg=COLORS["bg_main"], padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(self.main_frame, text="Prompt Composition", font=FONT_TITLE, bg=COLORS["bg_main"], fg=COLORS["text_main"]).pack(anchor="w", pady=(0, 5))
        self.prompt_text = tk.Text(self.main_frame, height=5, font=FONT_NORMAL, bg="#ffffff", fg=COLORS["text_main"],
                                   relief="flat", highlightthickness=1, highlightbackground=COLORS["border"], padx=10, pady=10)
        self.prompt_text.pack(fill="x", pady=(0, 10))

        self.btn_frame = tk.Frame(self.main_frame, bg=COLORS["bg_main"])
        self.btn_frame.pack(fill="x", pady=(0, 20))

        self.create_btn(self.btn_frame, "Copy", self.copy_to_clipboard, COLORS["primary"])
        self.create_btn(self.btn_frame, "Save As...", self.save_keywords_as, COLORS["info"])
        self.create_btn(self.btn_frame, "Load (Merge)", self.load_keywords_from, COLORS["secondary"])
        self.create_btn(self.btn_frame, "Reset", self.reset_keywords, COLORS["warning"])

        self.del_btn = tk.Button(self.btn_frame, text="Delete Mode: OFF", command=self.toggle_delete_mode,
                                 bg=COLORS["info"], fg="white", relief="flat", font=FONT_SMALL, padx=10)
        self.del_btn.pack(side="right")

        self.search_frame = tk.Frame(self.main_frame, bg="#ffffff", pady=15, padx=15,
                                     highlightthickness=1, highlightbackground=COLORS["border"])
        self.search_frame.pack(fill="x", pady=(0, 10))

        tk.Label(self.search_frame, text="Search / Add Keywords:", font=FONT_NORMAL, bg="#ffffff", fg=COLORS["text_main"]).pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.update_keyword_ui())
        
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var, font=FONT_NORMAL,
                                     relief="flat", highlightthickness=1, highlightbackground=COLORS["border"])
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), ipady=3)

        tk.Button(self.search_frame, text="Add +", command=self.add_keyword,
                  bg=COLORS["success"], fg="white", relief="flat", font=FONT_NORMAL, padx=15).pack(side="right")

        self.cat_frame = tk.Frame(self.main_frame, bg=COLORS["bg_main"])
        self.cat_frame.pack(fill="x", pady=(0, 10))
        self.render_category_buttons()

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
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.my_keywords = data
                    else:
                        self.my_keywords = self.default_keywords.copy()
            except Exception:
                self.my_keywords = self.default_keywords.copy()
        else:
            self.my_keywords = self.default_keywords.copy()

    def create_btn(self, parent, text, command, color):
        btn = tk.Button(parent, text=text, command=command, bg=color, fg="white",
                        relief="flat", font=FONT_SMALL, padx=12, pady=5)
        btn.pack(side="left", padx=(0, 5))
        return btn

    def render_category_buttons(self):
        for widget in self.cat_frame.winfo_children():
            widget.destroy()
        for cat in self.my_keywords.keys():
            is_active = (cat == self.current_category)
            bg_color = COLORS["primary"] if is_active else COLORS["secondary"]
            btn = tk.Button(self.cat_frame, text=cat, command=lambda c=cat: self.switch_category(c),
                            bg=bg_color, fg="white", relief="flat", font=FONT_SMALL, padx=10, pady=2)
            btn.pack(side="left", padx=(0, 5))

    def switch_category(self, category):
        self.current_category = category
        self.render_category_buttons()
        self.update_keyword_ui()

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
        
        if search_term:
            filtered_keywords = []
            seen = set()
            for cat_tags in self.my_keywords.values():
                for kw in cat_tags:
                    if search_term in kw.lower() and kw not in seen:
                        filtered_keywords.append(kw)
                        seen.add(kw)
        else:
            filtered_keywords = self.my_keywords.get(self.current_category, [])

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
            found_in_categories = [cat for cat, tags in self.my_keywords.items() if kw in tags]
            if not found_in_categories:
                return

            if len(found_in_categories) > 1:
                msg = f"關鍵字 '{kw}' 存在於多個分類：\n" + ", ".join(found_in_categories) + "\n\n是否從所有分類中移除？"
                if messagebox.askyesno("多重分類確認", msg):
                    for cat in found_in_categories:
                        if kw in self.my_keywords[cat]:
                            self.my_keywords[cat].remove(kw)
                else:
                    if self.current_category in found_in_categories:
                        self.my_keywords[self.current_category].remove(kw)
            else:
                target_cat = found_in_categories[0]
                if kw in self.my_keywords[target_cat]:
                    self.my_keywords[target_cat].remove(kw)
                
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
        input_kw = self.search_var.get().strip()
        if not input_kw: return
        
        if self.current_category not in self.my_keywords:
            self.my_keywords[self.current_category] = []

        if input_kw not in self.my_keywords[self.current_category]:
            self.my_keywords[self.current_category].append(input_kw)
            self.auto_save_keywords()
            self.search_var.set("")
            self.update_keyword_ui()

    def reset_keywords(self):
        if messagebox.askyesno("Reset", "キーワードリストを初期状態に戻しますか？"):
            self.my_keywords = self.default_keywords.copy()
            self.current_category = list(self.my_keywords.keys())[0]
            self.auto_save_keywords()
            self.render_category_buttons()
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
                    if isinstance(data, dict):
                        for cat, tags in data.items():
                            if cat in self.my_keywords:
                                old_set = set(self.my_keywords[cat])
                                new_tags = [t for t in tags if t not in old_set]
                                self.my_keywords[cat].extend(new_tags)
                            else:
                                self.my_keywords[cat] = tags
                        self.auto_save_keywords()
                        self.render_category_buttons()
                        self.update_keyword_ui()
                        messagebox.showinfo("Merge Success", "分類與關鍵字已成功合併。")
            except Exception as e:
                messagebox.showerror("Error", f"読み込み失敗: {e}")

def main():
    root = tk.Tk()
    app = PromptBuilderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()