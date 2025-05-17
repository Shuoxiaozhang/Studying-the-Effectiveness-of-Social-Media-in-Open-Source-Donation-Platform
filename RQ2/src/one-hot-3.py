import pandas as pd
from collections import Counter

# 1. 读取数据
df = pd.read_csv('E:/bishe/newdata/collectiveinfo/res_1.csv')

# 2. 将空值（如果有的话）填充为''
df['tags'] = df['tags'].fillna('')

# 3. 如果每行的tags是用逗号分隔，则先拆分
#   （若用其他分隔符比如空格、分号等，请自行替换）
df['tags_list'] = df['tags'].apply(lambda x: [tag.strip() for tag in x.split(',') if tag.strip()])

# 4. 统计所有标签的出现频率
counter = Counter()
for row_tags in df['tags_list']:
    for t in row_tags:
        counter[t] += 1

# 5. 取出现频率最高的 5 个标签
top_5_tags = [tag for tag, _ in counter.most_common(5)]
print("频率最高的 5 个标签：", top_5_tags)

# 6. 对这 5 个标签进行 one-hot 编码，生成新列
for tag in top_5_tags:
    df[f'tag_{tag}'] = df['tags_list'].apply(lambda x: 1 if tag in x else 0)

# 7. 如果不再需要 tags_list，可以把它删除
df.drop(columns=['tags_list'], inplace=True)

# 查看结果
print(df.head())
output_path = "E:/bishe/newdata/collectiveinfo/res_top5_tags_o1.csv"
df.to_csv(output_path, index=False)
