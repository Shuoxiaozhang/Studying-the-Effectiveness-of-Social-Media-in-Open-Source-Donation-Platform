import json
import csv

# 读取 JSON 文件
file_path = "E:/bishe/newdata/collectiveinfo/fixed_success_collective_data.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)  # 解析 JSON

# 提取需要的字段
result = []
for item in data:
    try:
        collective = item["data"]["collective"]

        slug = collective.get("slug", "N/A")  # 组织唯一标识
        name = collective.get("name", "N/A")  # 组织名称

        # 确保 tags 是列表，否则设为空列表
        tags = collective.get("tags", [])
        if not isinstance(tags, list):  # 避免 None 或非列表类型
            tags = []
        tags_str = ", ".join(tags)  # 处理 tags 列表为字符串

        contributions_count = collective.get("stats", {}).get("contributionsCount", 0)  # 贡献次数
        total_financial_contributors = collective.get("totalFinancialContributors", 0)  # 财务贡献者总数

        # 处理 location，确保不为 None
        location = collective.get("location")
        country = location["country"] if isinstance(location, dict) and "country" in location else "N/A"

        result.append((slug, name, tags_str, contributions_count, total_financial_contributors, country))

    except KeyError as e:
        print(f"⚠️ 缺少字段 {e}，跳过: {item}")

# 写入 CSV 文件
csv_path = "E:/bishe/newdata/collectiveinfo/full_1.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["slug", "name", "tags", "contributionsCount", "totalFinancialContributors", "country"])  # 写入表头
    writer.writerows(result)  # 写入数据

print(f"✅ 数据已成功写入 {csv_path}")
