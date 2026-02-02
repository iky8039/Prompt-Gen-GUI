# Prompt Gen GUI ✅

**Windows デスクトップ用のインタラクティブなプロンプトビルダー（exe 配布）**

概要:
- キーワードを選択してカンマ区切りのプロンプトを素早く作成し、クリップボードにコピーできます。
- キーワードの追加・検索・差分マージ・エクスポート（JSON）などの管理機能を備えています。

---

## 📥 ダウンロード
- 最新の Windows 実行ファイルは GitHub Releases（`v1.3` 等）からダウンロードしてください: https://github.com/iky8039/Prompt-Gen-GUI/releases

---

## 🖥️ システム要件
- Windows 10 / 11（x64 推奨）
- メモリ: 1GB 以上

---

## 🚀 使い方（exe をダウンロードした場合）
1. リリースページから `Prompt.Gen.GUI.1.3.exe` をダウンロード。
2. ダブルクリックで起動。
3. ウィンドウタイトルに **Interactive Prompt Builder v1.3** と表示されます。
4. キーワードをクリックしてプロンプトを作成 → `Copy` ボタンでクリップボードにコピー。

---

## 🔒 配布の安全性（確認方法）
- リリースページに掲載している **SHA256** ハッシュ値とダウンロードしたファイルのハッシュを比較してください。
  - PowerShell:
    ```powershell
    Get-FileHash -Algorithm SHA256 "C:\path\to\Prompt.Gen.GUI.1.3.exe"
    ```
- exe に署名がある場合は署名を確認してください（現在のリリースは署名がない可能性があります）。

---

## 🛠 トラブルシューティング
- 起動時にGUI エラーが出る／ウィンドウが表示されない場合は、ローカル環境で `python -m prompt_gen_gui` を実行してログを確認してください（Python が必要）。
- バグや要望は Issues に報告してください: https://github.com/iky8039/Prompt-Gen-GUI/issues

---

## ✍️ 開発者向け（簡単に）
- ソースから起動: `python -m prompt_gen_gui` または `prompt-gen-gui`（インストール後）
- Windows exe ビルド例（PyInstaller）:
  ```powershell
  pyinstaller --onefile --windowed --name "Prompt Gen GUI 1.3" --version-file=build/version.txt "src/prompt_gen_gui/__main__.py"
  ```
- `build/version.txt` を編集して Windows の FileVersion/ProductVersion を埋め込むことができます。

---

## 🤝 貢献・ライセンス
- PR を歓迎します — 小さな改善はブランチを切って Pull Request を作成してください。
- ライセンス: **MIT**（`LICENSE` を参照）

---

*最終更新: v1.3 リリースに合わせて更新*