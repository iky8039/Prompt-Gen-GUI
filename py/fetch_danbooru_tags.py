

import requests
import json
import time
import os

USERNAME = "wintermute112358"
API_KEY = "aWyMb7n3ok9HQjRCyMoT498d"

output_path = "py/japanese_tags.json"
INTERVAL = 1.5  # 秒（1.5秒ごとにリクエスト）

# 既存データの読み込み
if os.path.exists(output_path):
    with open(output_path, "r", encoding="utf-8") as f:
        jp_dict = json.load(f)
else:
    jp_dict = {}

# 既存件数から再開ページを推定（1ページ=1000件）
existing_tags = sum(len(v) for v in jp_dict.values())
start_page = max(1, existing_tags // 1000)
print(f"Resuming from page {start_page} (existing tags: {existing_tags})")

tags = []
page = start_page
while True:
    url = f"https://danbooru.donmai.us/tags.json?search[order]=count&limit=1000&page={page}"
    res = requests.get(url, auth=(USERNAME, API_KEY))
    if res.status_code != 200:
        print(f"Error: {res.status_code}")
        break
    data = res.json()
    if not data:
        break
    tags.extend(data)
    print(f"Page {page} done, total tags: {existing_tags + len(tags)}")
    page += 1
    time.sleep(INTERVAL)

# 日本語訳があるものだけ抽出し、既存データにマージ
for tag in tags:
    jp = tag.get("name_translated")
    en = tag.get("name")
    if jp and en:
        if jp not in jp_dict:
            jp_dict[jp] = []
        if en not in jp_dict[jp]:
            jp_dict[jp].append(en)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(jp_dict, f, ensure_ascii=False, indent=2)

print(f"Saved {len(jp_dict)} Japanese tags to {output_path}")
