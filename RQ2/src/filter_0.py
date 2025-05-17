import pandas as pd

# 1. 读取数据
df = pd.read_csv('E:/bishe/newdata/collectiveinfo/last.csv', encoding='utf-8')

# 2. 删除 contributionsCount 值为 0 的行
df_filtered = df[df['contributionsCount'] != 0]

# 3. 将筛选后的数据保存为新的 CSV 文件
df_filtered.to_csv('E:/bishe/newdata/collectiveinfo/filtered_last.csv', index=False, encoding='utf-8')

print(f"原始数据行数: {len(df)}, 过滤后数据行数: {len(df_filtered)}")
print("新数据已保存为 filtered_last.csv")
