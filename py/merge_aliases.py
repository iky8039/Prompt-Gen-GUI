import json

# 入力ファイル
jp_json = "py/japanese_tags.json"
kw_json = "py/keyword_aliases.json"
# 出力ファイル
out_json = "py/keyword_aliases_merged.json"

# すべての言語をキーに持つ多言語エイリアス辞書を作る
alias_map = {}

# 日本語主キーjsonを読み込み
with open(jp_json, "r", encoding="utf-8") as f:
    jp_dict = json.load(f)
    for jp, aliases in jp_dict.items():
        all_tags = set([jp] + aliases)
        for tag in all_tags:
            if tag not in alias_map:
                alias_map[tag] = set()
            alias_map[tag].update(all_tags - {tag})

# 既存の英語主キーjsonもあればマージ
try:
    with open(kw_json, "r", encoding="utf-8") as f:
        kw_dict = json.load(f)
        for en, aliases in kw_dict.items():
            all_tags = set([en] + aliases)
            for tag in all_tags:
                if tag not in alias_map:
                    alias_map[tag] = set()
                alias_map[tag].update(all_tags - {tag})
except FileNotFoundError:
    pass

# set→listに変換して保存
alias_map = {k: sorted(list(v)) for k, v in alias_map.items()}
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(alias_map, f, ensure_ascii=False, indent=2)

print(f"Saved merged alias json: {out_json} (total keys: {len(alias_map)})")
