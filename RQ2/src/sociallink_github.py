import json
import csv

# 读取 slug_counts.csv 中的所有 slug
slug_counts_path = "E:/bishe/getdata/slug_counts.csv"
with open(slug_counts_path, "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # 跳过表头
    valid_slugs = {row[0] for row in reader}  # 存储所有有效的 slug

# 读取 JSON 文件
json_path = "E:/bishe/data/collective/collectiveInfo/merged_collective_data.json"
with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)  # 解析 JSON 数据

# 创建结果列表
result = []
for item in data:
    slug = item.get("slug", "N/A")
    social_links = item.get("socialLinks", [])

    # 获取 socialLinks 中所有的 type 值
    types = {link.get("type") for link in social_links if link.get("type")}

    # 判断条件
    if (types in [{"WEBSITE"}, {"GITHUB"}, {"WEBSITE", "GITHUB"}, set()]) and slug not in valid_slugs:
        flag = 0
    else:
        flag = 1

    # 添加结果到列表
    result.append((slug, flag))

# 写入结果到新的 CSV 文件
output_path = "E:/bishe/data/collective/collectiveInfo/slug_flag_github.csv"
with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["slug", "flag"])  # 写入表头
    writer.writerows(result)  # 写入数据

print(f"✅ 数据已成功写入 {output_path}")
