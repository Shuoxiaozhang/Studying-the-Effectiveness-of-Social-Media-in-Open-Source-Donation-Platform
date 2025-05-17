import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.neighbors import NearestNeighbors
from scipy.stats import ttest_ind

# 1. 读取数据
df = pd.read_csv('E:/bishe/newdata/collectiveinfo/updated_merged_collective_data.csv', encoding='utf-8')

# 设置变量
treatment_col = 'flag'  # 处理组标识（使用社交媒体=1）
covariates = [
    'totalFinancialContributors',
    'age',
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
outcome_col = 'contributionsCount'  # 结果变量

# 2. 数据清洗：去除缺失值
df.dropna(subset=[treatment_col], inplace=True)
df = df.dropna(subset=covariates + [outcome_col])

# 3. 使用 Logistic 回归估计倾向得分
X = df[covariates].copy()
X = sm.add_constant(X)  # 加截距项
y = df[treatment_col]
logit = sm.Logit(y, X)
result = logit.fit(maxiter=500, disp=0)
df['propensity_score'] = result.predict(X)

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


# 6. 计算匹配前后协变量平衡性（标准化均差）
def std_mean_diff(series_treat, series_ctrl):
    return (series_treat.mean() - series_ctrl.mean()) / np.sqrt((series_treat.var() + series_ctrl.var()) / 2)


print("=== 匹配前协变量平衡性 ===")
for c in covariates:
    smd_before = std_mean_diff(treated[c], control[c])
    print(f"{c}: SMD(匹配前) = {smd_before:.3f}")

print("\n=== 匹配后协变量平衡性 ===")
for c in covariates:
    smd_after = std_mean_diff(
        matched_df.loc[matched_df[treatment_col] == 1, c],
        matched_df.loc[matched_df[treatment_col] == 0, c]
    )
    print(f"{c}: SMD(匹配后) = {smd_after:.3f}")

# 7. 计算平均处理效应 (ATT)
treated_outcome = matched_df.loc[matched_df[treatment_col] == 1, outcome_col]
control_outcome = matched_df.loc[matched_df[treatment_col] == 0, outcome_col]

ATT = treated_outcome.mean() - control_outcome.mean()
print(f"\n=== 匹配后平均处理效应 (ATT) ===")
print(f"处理组 - 对照组在 {outcome_col} 上的均值差异：{ATT:.3f}")

# 进行 t 检验
t_stat, p_val = ttest_ind(treated_outcome, control_outcome, equal_var=False)
print(f"T检验: t值={t_stat:.3f}, p值={p_val:.5f}")

correlation_matrix = df[covariates].corr()

# 输出相关性矩阵为CSV文件
correlation_csv_file_path = 'E:/bishe/newdata/collectiveinfo/covariate_correlation_matrix.csv'
correlation_matrix.to_csv(correlation_csv_file_path)

print(f"协变量相关性矩阵已保存到: {correlation_csv_file_path}")
# # 8. 生成 SMD 对比表格并保存
# smd_data = {
#     'Covariate': [],
#     'SMD_Before': [],
#     'SMD_After': []
# }
#
# for c in covariates:
#     smd_before = std_mean_diff(treated[c], control[c])
#     smd_after = std_mean_diff(
#         matched_df.loc[matched_df[treatment_col] == 1, c],
#         matched_df.loc[matched_df[treatment_col] == 0, c]
#     )
#     smd_data['Covariate'].append(c)
#     smd_data['SMD_Before'].append(round(smd_before, 3))
#     smd_data['SMD_After'].append(round(smd_after, 3))
#
# smd_df = pd.DataFrame(smd_data)
# smd_df.to_csv("E:/bishe/newdata/collectiveinfo/smd_table.csv", index=False)
# print("\nSMD 对比表格已保存为 smd_table.csv")

# import statsmodels.api as sm
#
# # 匹配后的数据中，准备协变量和结果变量
# X_matched = matched_df[covariates].copy()
# X_matched = sm.add_constant(X_matched)  # 添加常数项
# y_matched = matched_df[outcome_col]
#
# # 构建 OLS 回归模型
# model = sm.OLS(y_matched, X_matched)
# results = model.fit()
#
# # 打印回归结果
# print("\n=== 匹配后协变量对 outcome 的回归结果 ===")
# print(results.summary())
#
# # 如需保存成 CSV
# summary_df = results.summary2().tables[1]  # 提取包含 coef/std err/p值 的表
# summary_df.to_csv("E:/bishe/newdata/collectiveinfo/ols_coefficients.csv")
# print("回归系数表已保存为 ols_coefficients.csv")
