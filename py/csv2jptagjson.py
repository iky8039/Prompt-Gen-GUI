import csv
import json

csv_path = "py/danbooru_translations_jp.csv"
json_path = "py/japanese_tags.json"

jp_dict = {}

with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if not row or row[0].startswith('#') or row[0].startswith('"""'):
            continue
        en_tag = row[0].strip()
        # 2列目以降を日本語エイリアスとして扱う
        for cell in row[1:]:
            for jp in cell.split(','):
                jp = jp.strip().strip('"')
                if jp:
                    if jp not in jp_dict:
                        jp_dict[jp] = []
                    if en_tag not in jp_dict[jp]:
                        jp_dict[jp].append(en_tag)

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(jp_dict, f, ensure_ascii=False, indent=2)

print(f"Saved {len(jp_dict)} Japanese tags to {json_path}")
