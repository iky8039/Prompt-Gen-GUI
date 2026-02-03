# Prompt Gen GUI

**Windows デスクトップ用のインタラクティブなプロンプトビルダー（exe 配布）**

概要:
- 発行元（Publisher）: iky8039
- キーワードをクリックしてカンマ区切りのプロンプトを素早く作成し、クリップボードにコピーできます。
- 単語の追加: 検索欄から直接新しい単語を追加できます。
- プロンプトからの差分追加: プロンプト入力欄にテキストを入力して「Add」を押すと、既存のキーワードと比較して新しい単語だけを追加します（差分マージ）。
- 単語の削除: Delete Mode を切り替えてキーワードをクリックすると削除できます。
- 検索機能: キーワードを検索して絞り込みができます。検索欄からの直接追加にも対応しています。
- エクスポート/インポート: キーワードを JSON ファイルとして出力し、JSON ファイルを読み込んで差分マージできます。
- 自動保存: キーワードが更新されるたび、またアプリを閉じる際に自動保存されます.

---

## ダウンロード
- 最新の Windows 実行ファイルは GitHub Releases（`v1.3` 等）からダウンロードしてください: https://github.com/iky8039/Prompt-Gen-GUI/releases

---

## システム要件
- Windows 10 / 11（x64 推奨）
- メモリ: 1GB 以上

---


## 使い方（v1.5以降・リリースzipの場合）
1. GitHubリリースから `PromptGenGUI15_release.zip` をダウンロードし、任意のフォルダに展開してください。
2. 展開後、`dist/PromptGenGUI15.exe` をダブルクリックで起動します。
3. 初回起動時から多言語エイリアス辞書（`py/keyword_aliases.json`）が有効です。
4. 検索欄・プロンプト欄でShift+Enterを押すと、未登録ワードが自動追加されます。
5. キーワードをクリックしてプロンプトを作成 → `Copy` ボタンでクリップボードにコピー。

---

## 単語帳（キーワードリスト）を共有したい場合
- 他のユーザーと単語帳を共有する際は、`py/keyword_aliases.json` ファイルを共有してください。
- 受け取った側は、同じ場所（`py/keyword_aliases.json`）に上書き・配置することで、同じ単語帳・エイリアス辞書を利用できます。
- バックアップやカスタマイズもこのファイル単体で管理できます。

---

## 配布の安全性（確認方法）
- リリースページに掲載している **SHA256** ハッシュ値とダウンロードしたファイルのハッシュを比較してください。
  - PowerShell:
    ```powershell
    Get-FileHash -Algorithm SHA256 "C:\path\to\Prompt.Gen.GUI.1.3.exe"
    ```
- exe に署名がある場合は署名を確認してください（現在のリリースは署名がない可能性があります）。

---

## トラブルシューティング
- 起動時にGUI エラーが出る／ウィンドウが表示されない場合は、ローカル環境で `python -m prompt_gen_gui` を実行してログを確認してください（Python が必要）。
- バグや要望は Issues に報告してください: https://github.com/iky8039/Prompt-Gen-GUI/issues

---

## 開発者向け（簡単に）
- ソースから起動: `python -m prompt_gen_gui` または `prompt-gen-gui`（インストール後）
- Windows exe ビルド例（PyInstaller）:
  ```powershell
  pyinstaller --onefile --windowed --name "Prompt Gen GUI 1.3" --version-file=build/version.txt "src/prompt_gen_gui/__main__.py"
  ```
- `build/version.txt` を編集して Windows の FileVersion/ProductVersion を埋め込むことができます。

---

## 貢献・ライセンス
- PR を歓迎します — 小さな改善はブランチを切って Pull Request を作成してください。
- ライセンス: **MIT**（`LICENSE` を参照）

---

*最終更新: v1.3 リリースに合わせて更新*