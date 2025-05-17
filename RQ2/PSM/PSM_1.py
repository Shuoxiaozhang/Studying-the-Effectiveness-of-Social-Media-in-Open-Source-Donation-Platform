import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
from scipy.stats import ttest_ind

# 1. 读取数据
df = pd.read_csv('E:/bishe/newdata/collectiveinfo/Cleaned_Merged_Data__No_Index_Column_.csv', encoding='utf-8')

# 设置变量
treatment_col = 'flag'  # 处理组标识（使用社交媒体=1）
covariates = [
    'totalFinancialContributors',
    'age',
    'members',
    'updates',
    'type_公益型',
    'type_技术型',
    'type_教育型',
    'country_DE',
    'country_FR',
    'country_GB',
    'country_Other',
    'country_US',
    'country_Unknown'
]
outcome_col = 'amount'  # 结果变量

# 2. 数据清洗：去除缺失值
df.dropna(subset=[treatment_col], inplace=True)
df = df.dropna(subset=covariates + [outcome_col])

# 3. 使用 Logistic 回归估计倾向得分（使用正则化）
X = df[covariates].copy()
X = pd.get_dummies(X, drop_first=True)  # 如果有分类变量，使用 get_dummies 进行处理
y = df[treatment_col]

# 使用 LogisticRegression 进行拟合，添加 L2 正则化（默认）
log_reg = LogisticRegression(max_iter=1000, penalty='l2')  # L2 正则化
log_reg.fit(X, y)

# 估计倾向得分
df['propensity_score'] = log_reg.predict_proba(X)[:, 1]

# 4. 分离处理组和对照组
treated = df[df[treatment_col] == 1].copy()
control = df[df[treatment_col] == 0].copy()

# 设置匹配参数
caliper = 0.02  # caliper 阈值
n_neighbors = 3  # 每个处理组样本匹配的控制组样本数

# 使用 NearestNeighbors 进行匹配
nn = NearestNeighbors(n_neighbors=n_neighbors)
nn.fit(control[['propensity_score']])
distances, indices = nn.kneighbors(treated[['propensity_score']])

# 记录匹配信息
matched_treated_list = []
matched_control_list = []
matched_pairs = []

# 遍历每个处理组样本，匹配合适的控制组样本
for i, (dists, inds) in enumerate(zip(distances, indices)):
    valid_idx = np.where(dists <= caliper)[0]  # 筛选满足 caliper 的控制组样本
    if valid_idx.size > 0:
        for j in valid_idx:
            matched_treated_list.append(treated.iloc[i])
            matched_control_list.append(control.iloc[inds[j]])
            matched_pairs.append({
                "treated_index": treated.index[i],  # 记录原始数据中的索引
                "control_index": control.index[inds[j]],  # 记录匹配的对照组索引
                "treated_score": treated.iloc[i]['propensity_score'],
                "control_score": control.iloc[inds[j]]['propensity_score']
            })

# 5. 生成匹配后的 DataFrame
if len(matched_treated_list) == 0:
    print("在指定 caliper 范围内未匹配到任何控制组样本，请检查 caliper 阈值设置。")
else:
    matched_treated_df = pd.DataFrame(matched_treated_list)
    matched_control_df = pd.DataFrame(matched_control_list)

    # 合并匹配后的处理组和对照组数据
    matched_df = pd.concat([matched_treated_df, matched_control_df], axis=0)

    # 保存匹配数据
    matched_df.to_csv("E:/bishe/newdata/collectiveinfo/matched_data.csv", index=False)

    # 保存匹配对信息
    matched_pairs_df = pd.DataFrame(matched_pairs)
    matched_pairs_df.to_csv("E:/bishe/newdata/collectiveinfo/matched_pairs.csv", index=False)

    print(f"匹配数据已保存到: matched_data.csv")
    print(f"匹配对信息已保存到: matched_pairs.csv")

# 6. 计算曝光组和匹配对照组均值
treated_mean = treated[outcome_col].mean()  # 曝光组均值
control_mean = control[outcome_col].mean()  # 匹配对照组均值

# 7. 计算平均处理效应 (ATT)
treated_matched_mean = matched_df.loc[matched_df[treatment_col] == 1, outcome_col].mean()  # 曝光组均值 (基于匹配数据)
control_matched_mean = matched_df.loc[matched_df[treatment_col] == 0, outcome_col].mean()  # 匹配对照组均值 (基于匹配数据)

# 计算 ATT
ATT = treated_matched_mean - control_matched_mean

# 进行 t 检验
t_stat, p_val = ttest_ind(
    matched_df.loc[matched_df[treatment_col] == 1, outcome_col],
    matched_df.loc[matched_df[treatment_col] == 0, outcome_col],
    equal_var=False
)

# 输出曝光组和匹配对照组均值以及 ATT
result_table = pd.DataFrame({
    '结果变量': [outcome_col],
    '曝光组均值': [treated_matched_mean],
    '匹配对照组均值': [control_matched_mean],
    'ATT': [ATT],
    '显著性(p值)': [p_val]
})

result_table['ATT'] = result_table['ATT'].apply(lambda x: f"{x:.3f}")
result_table['显著性(p值)'] = result_table['显著性(p值)'].apply(lambda x: f"{x:.5f}")


# 打印结果
print(result_table)

# 设定Bootstrap参数
n_bootstrap = 1000  # 设置Bootstrap样本数量
bootstrap_coefs = []  # 用于存储每次Bootstrap的回归系数

# 进行Bootstrap抽样并拟合Logistic回归
for _ in range(n_bootstrap):
    # 随机抽取数据（有放回）
    bootstrap_sample = df.sample(n=len(df), replace=True)

    # 获取自变量和因变量
    X_bootstrap = bootstrap_sample[covariates].copy()
    X_bootstrap = pd.get_dummies(X_bootstrap, drop_first=True)  # 处理分类变量
    y_bootstrap = bootstrap_sample[treatment_col]

    # 拟合Logistic回归模型
    log_reg_bootstrap = LogisticRegression(max_iter=1000, penalty='l2')  # L2 正则化
    log_reg_bootstrap.fit(X_bootstrap, y_bootstrap)

    # 获取回归系数
    bootstrap_coefs.append(log_reg_bootstrap.coef_.flatten())  # 将回归系数存储为一维数组

# 将所有Bootstrap回归系数转换为numpy数组
bootstrap_coefs = np.array(bootstrap_coefs)

# 计算回归系数的标准误（即标准差）
bootstrap_se = bootstrap_coefs.std(axis=0)

# 输出回归系数的标准误
coef_names = X.columns  # 回归系数的名字
for i, coef_se in enumerate(bootstrap_se):
    print(f"回归系数 {coef_names[i]} 的标准误: {coef_se:.5f}")
