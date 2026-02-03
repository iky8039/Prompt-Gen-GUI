# Prompt Gen GUI 1.5
# v1.4をベースに、Shift+Enterで差分追加機能を実装


from .__main__ import *

def get_diff_words(input_text, alias_dict, my_keywords):
	# カンマ・改行区切りで単語抽出
	words = [w.strip() for w in input_text.replace('\n', ',').split(',') if w.strip()]
	diff = []
	for w in words:
		# 既存キーワードにもエイリアスにもなければ追加対象
		if w not in my_keywords and w not in alias_dict:
			diff.append(w)
	return diff

class PromptBuilderAppV15(PromptBuilderApp):
	def __init__(self, root):
		super().__init__(root)
		# 検索欄: Shift+Enterで差分追加
		self.search_entry.bind('<Shift-Return>', self.on_shift_enter_search)
		# プロンプト欄: Shift+Enterで差分追加
		self.prompt_text.bind('<Shift-Return>', self.on_shift_enter_prompt)

	def on_shift_enter_search(self, event=None):
		input_text = self.search_var.get()
		diff = get_diff_words(input_text, self.alias_dict, self.my_keywords.get(self.current_category, []))
		if diff:
			for w in diff:
				self.my_keywords[self.current_category].append(w)
			self.auto_save_keywords()
			self.update_keyword_ui()
			messagebox.showinfo("追加", f"{len(diff)}件の新規ワードを追加しました。\n{diff}")
		else:
			messagebox.showinfo("追加", "追加対象の新規ワードはありません。")

	def on_shift_enter_prompt(self, event=None):
		input_text = self.prompt_text.get("1.0", tk.END)
		diff = get_diff_words(input_text, self.alias_dict, self.my_keywords.get(self.current_category, []))
		if diff:
			for w in diff:
				self.my_keywords[self.current_category].append(w)
			self.auto_save_keywords()
			self.update_keyword_ui()
			messagebox.showinfo("追加", f"{len(diff)}件の新規ワードを追加しました。\n{diff}")
		else:
			messagebox.showinfo("追加", "追加対象の新規ワードはありません。")

def main():
	root = tk.Tk()
	app = PromptBuilderAppV15(root)
	root.mainloop()

if __name__ == "__main__":
	main()
