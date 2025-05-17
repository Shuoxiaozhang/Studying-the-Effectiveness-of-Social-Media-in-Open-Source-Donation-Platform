import pandas as pd

# 1. 读取数据
df = pd.read_csv('E:/bishe/newdata/collectiveinfo/res_top5_tags_o1.csv')

# 2. 处理 type 列（示例：有三类"技术型，公益型，教育型"）
df_type_dummy = pd.get_dummies(df['type'], prefix='type')
df = pd.concat([df, df_type_dummy], axis=1)

# 3. 处理 country 列（筛选出现最多的前 5 个国家）
df['country'] = df['country'].fillna('Unknown')  # 处理空值

# 统计国家出现的次数，并取前 5 个
top_5_countries = df['country'].value_counts().head(5).index

# 仅对前 5 个国家进行 one-hot 编码，其他国家归为 "Other"
df['country'] = df['country'].apply(lambda x: x if x in top_5_countries else 'Other')

# 进行 one-hot 编码（新增 5 列 + 1 列 'Other'）
df_country_dummy = pd.get_dummies(df['country'], prefix='country')

# 合并数据
df = pd.concat([df, df_country_dummy], axis=1)

# 4. 保存文件
output_path = "E:/bishe/newdata/collectiveinfo/last.csv"
df.to_csv(output_path, index=False)
