import pandas as pd
import re
df = pd.read_csv('E:/bishe/data/all_issues_1.csv')
df['slug'] = df['html_url'].apply(lambda x: re.sub(r'https://github.com/', '', x).split('/')[0])

# 根据 'slug' 统计每个 A 的出现次数
slug_counts = df['slug'].value_counts().reset_index()
slug_counts.columns = ['slug', 'count']

# 保存到新的 CSV 文件
output_path = 'slug_counts.csv'
slug_counts.to_csv(output_path, index=False)

print(f"生成的 CSV 文件保存在：{output_path}")