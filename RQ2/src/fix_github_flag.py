import pandas as pd

# 读取两个 CSV 文件
filtered_path = "E:/bishe/newdata/collectiveinfo/filtered_last.csv"
correct_flag_path = "E:/bishe/data/collective/collectiveInfo/slug_flag_github_unique.csv"

df_filtered = pd.read_csv(filtered_path)
df_correct_flags = pd.read_csv(correct_flag_path)

# 创建 slug -> flag 的映射
flag_map = dict(zip(df_correct_flags['slug'], df_correct_flags['flag']))

# 修正 df_filtered 中的 flag
df_filtered['flag'] = df_filtered['slug'].apply(lambda x: flag_map.get(x, df_filtered.loc[df_filtered['slug'] == x, 'flag'].values[0]))

# 保存更新后的文件
output_path = "E:/bishe/newdata/collectiveinfo/filtered_last_corrected.csv"
df_filtered.to_csv(output_path, index=False)

print(f"✅ 修正完成，文件已保存到：{output_path}")
