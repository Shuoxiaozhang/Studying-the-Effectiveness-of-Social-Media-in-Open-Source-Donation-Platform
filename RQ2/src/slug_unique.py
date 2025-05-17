import pandas as pd

# 读取 CSV 文件
csv_path = "E:/bishe/newdata/collectiveinfo/slug_name_1.csv"
df = pd.read_csv(csv_path)

# 按 slug 去重，保留第一条出现的记录
df_unique = df.drop_duplicates(subset=["slug"], keep="first")

# 保存去重后的 CSV 文件
df_unique.to_csv(csv_path, index=False)

print(f"✅ 去重完成，已保存至 {csv_path}")
