import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.neighbors import NearestNeighbors
from scipy.stats import ttest_ind

# 1. 读取数据
df = pd.read_csv('E:/bishe/newdata/collectiveinfo/filtered_last_corrected.csv', encoding='utf-8')

# 设置变量
treatment_col = 'flag'  # 处理组标识（使用社交媒体=1）
covariates = [
    'totalFinancialContributors',
    'tag_community',
    'tag_open source',
    'tag_javascript',
    'tag_other',
    'tag_association',
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
result = logit.fit(maxiter=200, disp=0)
df['propensity_score'] = result.predict(X)

# 4. 分离处理组和对照组
treated = df[df[treatment_col] == 1].copy()
control = df[df[treatment_col] == 0].copy()

# 设置匹配参数
caliper = 0.05  # caliper 阈值
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

import pandas as pd
import statsmodels.api as sm

# After performing the matching, perform OLS regression on the matched dataset
X_matched = matched_df[covariates].copy()
X_matched = sm.add_constant(X_matched)  # Add a constant (intercept)
y_matched = matched_df[outcome_col]

# OLS regression
model = sm.OLS(y_matched, X_matched)
results = model.fit()

# Extract coefficients, standard errors, and p-values
coef_table = pd.DataFrame({
    'Covariate': X_matched.columns,
    'Coefficient': results.params,
    'Std Error': results.bse,
    'P-value': results.pvalues
})

# Significance stars based on p-value
def significance_stars(p_value):
    if p_value < 0.001:
        return '***'
    elif p_value < 0.01:
        return '**'
    elif p_value < 0.05:
        return '*'
    else:
        return ''

coef_table['Significance'] = coef_table['P-value'].apply(significance_stars)

# Format the table to match the desired output
formatted_table = coef_table[['Covariate', 'Coefficient', 'Std Error', 'Significance']]


# Optionally save the table to a CSV file if needed
formatted_table.to_csv("E:/bishe/newdata/collectiveinfo/regression_coefficients.csv", index=False)

print("Regression coefficients table saved as regression_coefficients.csv")
