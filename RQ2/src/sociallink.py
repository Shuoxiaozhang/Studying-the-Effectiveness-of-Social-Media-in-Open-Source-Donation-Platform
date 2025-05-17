import json
import csv

# 读取 JSON 文件
file_path = "E:/bishe/data/collective/collectiveInfo/merged_collective_data.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)  # 解析 JSON

# 提取 slug 和 flag
result = []
for item in data:
    slug = item.get("slug", "N/A")
    social_links = item.get("socialLinks", [])

    # 检查 socialLinks 是否为空或仅包含 "type": "WEBSITE"
    if not social_links or all(link.get("type") == "WEBSITE" for link in social_links):
        flag = 0
    else:
        flag = 1

    result.append((slug, flag))

# 写入 CSV 文件
csv_path = "E:/bishe/data/collective/collectiveInfo/slug_flag.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["slug", "flag"])  # 写入表头
    writer.writerows(result)  # 写入数据

print(f"✅ 数据已成功写入 {csv_path}")
