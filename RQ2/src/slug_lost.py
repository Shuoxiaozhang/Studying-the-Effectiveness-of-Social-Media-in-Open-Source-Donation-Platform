import pandas as pd

# 读取 CSV 文件
b_df = pd.read_csv("E:/bishe/data/slug/slug_classified.csv")  # a 文件
a_df = pd.read_csv("E:/bishe/newdata/collectiveinfo/slug_name_1.csv")  # b 文件（是 a 的子集）

# 获取 `slug` 列
a_slugs = set(a_df["slug"])  # a.csv 中的 slug 集合
b_slugs = set(b_df["slug"])  # b.csv 中的 slug 集合

# 筛选出 a.csv 中 **b.csv 里没有的 slug**
filtered_slugs = a_df[~a_df["slug"].isin(b_slugs)]

# 保存到新 CSV 文件
filtered_slugs.to_csv("E:/bishe/newdata/collectiveinfo/slugs_after-before.csv", index=False)

print(f"✅ 筛选完成，共 {len(filtered_slugs)} 个 slug 被保存到 E:/bishe/newdata/collectiveinfo/slugs_after-before.csv.csv")
