import pandas as pd
import ast  # 解析字符串列表
from sklearn.preprocessing import MultiLabelBinarizer

# 读取 CSV 文件
csv_path = "E:/bishe/newdata/collectiveinfo/res_1.csv"
df = pd.read_csv(csv_path)

# **函数：安全解析 `tags`**
def parse_tags(x):
    if pd.isna(x) or x == "":  # 处理 NaN 或 空字符串
        return []
    try:
        parsed = ast.literal_eval(x)  # 尝试解析字符串列表
        if isinstance(parsed, list):
            return parsed
    except:
        pass
    return [x]  # 如果不是列表，则当作单个 tag 放入列表

# **应用解析**
df["tags"] = df["tags"].apply(parse_tags)

# **使用 MultiLabelBinarizer 进行 One-Hot Encoding**
mlb = MultiLabelBinarizer()
tag_encoded = pd.DataFrame(mlb.fit_transform(df["tags"]), columns=mlb.classes_)

# **确保索引对齐**
tag_encoded.reset_index(drop=True, inplace=True)
df.reset_index(drop=True, inplace=True)

# **新增 `tags_one_hot` 列**
df["tags_one_hot"] = tag_encoded.apply(lambda row: ",".join([col for col in tag_encoded.columns if row[col] == 1]), axis=1)

# **显示前 5 行**
print(df[["tags", "tags_one_hot"]].head())

# **保存数据**
output_path = "E:/bishe/newdata/collectiveinfo/res_2.csv"
df.to_csv(output_path, index=False)
print(f"✅ 处理完成，已保存至 {output_path}")
