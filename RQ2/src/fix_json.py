import json

# 文件路径
file_path = 'E:/bishe/newdata/collectiveinfo/time.json'  # 替换为实际路径

# 读取原始数据
with open(file_path, 'r', encoding='utf-8') as f:
    raw_data = f.read()

# 试着修正JSON格式问题，确保每个对象之间都有逗号
# 1. 删除任何可能的多余空行和不需要的空白字符
raw_data = raw_data.replace("\n", "")  # 删除换行符
raw_data = raw_data.replace("}{", "},\n{")  # 确保对象间有逗号和换行

# 2. 将整个内容包裹在一个列表中
raw_data = "[" + raw_data + "]"

# 解析修正后的JSON数据
try:
    # 尝试加载修正后的JSON数据
    data = json.loads(raw_data)

    # 将数据写入一个新的JSON文件
    with open('E:/bishe/newdata/collectiveinfo/fixed_time.json', 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, indent=2, ensure_ascii=False)

    print("修复后的JSON文件已保存为 'fixed_time.json'")

except json.JSONDecodeError as e:
    print(f"JSON解析错误: {e}")
