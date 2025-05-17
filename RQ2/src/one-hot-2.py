import pandas as pd
import ast  # 解析字符串列表
from sklearn.preprocessing import MultiLabelBinarizer

# 读取 CSV 文件
csv_path = "E:/bishe/newdata/collectiveinfo/res_1.csv"
df = pd.read_csv(csv_path)

# **解析 `tags` 确保为列表格式**
def parse_tags(x):
    if pd.isna(x) or x.strip() == "":  # 处理 NaN 或 空字符串
        return []
    try:
        return ast.literal_eval(x) if x.startswith("[") else [x]  # 解析 JSON 列表
    except:
        return [x]  # 处理单个 tag

df["tags"] = df["tags"].apply(parse_tags)

# **统计所有 `tags` 出现频率**
all_tags = [tag for sublist in df["tags"] for tag in sublist]  # 展开列表
tag_counts = pd.Series(all_tags).value_counts()  # 统计出现次数

# **选出前 5 个最高频的 `tags`**
top_5_tags = tag_counts.nlargest(5).index.tolist()
print(f"📌 选择的前 5 个 tags：{top_5_tags}")

# **只对前 5 个 tags 进行 One-Hot Encoding**
mlb = MultiLabelBinarizer(classes=top_5_tags)  # 只 One-Hot 编码前 5 个标签
tag_encoded = pd.DataFrame(mlb.fit_transform(df["tags"]), columns=mlb.classes_)

# **合并回原 DataFrame**
df = df.join(tag_encoded)

# **保存数据**
output_path = "E:/bishe/newdata/collectiveinfo/res_top5_tags_fixed.csv"
df.to_csv(output_path, index=False)
print(f"✅ 修正完成，已保存至 {output_path}")
