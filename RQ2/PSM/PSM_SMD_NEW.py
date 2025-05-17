import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
from scipy.stats import ttest_ind

# 计算标准化均差（SMD）函数
def std_mean_diff(series_treat, series_ctrl):
    return (series_treat.mean() - series_ctrl.mean()) / np.sqrt((series_treat.var() + series_ctrl.var()) / 2)

# 1. 读取数据
df = pd.read_csv('E:/bishe/newdata/collectiveinfo/updated_merged_collective_data.csv', encoding='utf-8')

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
outcome_col = 'contributionsCount'  # 结果变量

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
calipers = [None, 0.02]  # 无卡尺和卡尺阈值
neighbors = [1, 3]  # 1对1匹配和1对3匹配

# 存储匹配结果
matching_results = {}

# 5. 匹配策略：分别使用 1对1/1对3 和有/无 caliper
for n_neighbors in neighbors:
    for caliper in calipers:
        # 使用 NearestNeighbors 进行匹配
        nn = NearestNeighbors(n_neighbors=n_neighbors)
        nn.fit(control[['propensity_score']])
        distances, indices = nn.kneighbors(treated[['propensity_score']])

        matched_treated_list = []
        matched_control_list = []
        matched_pairs = []

        # 遍历每个处理组样本，匹配合适的控制组样本
        for i, (dists, inds) in enumerate(zip(distances, indices)):
            if caliper is None:  # 无卡尺
                valid_idx = np.arange(n_neighbors)
            else:  # 有卡尺
                valid_idx = np.where(dists <= caliper)[0]

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

        # 生成匹配后的 DataFrame
        if len(matched_treated_list) > 0:
            matched_treated_df = pd.DataFrame(matched_treated_list)
            matched_control_df = pd.DataFrame(matched_control_list)

            # 合并匹配后的处理组和对照组数据
            matched_df = pd.concat([matched_treated_df, matched_control_df], axis=0)

            # 计算匹配成功率
            matching_success_rate = len(matched_treated_list) / len(treated)

            # 保存匹配数据
            matched_df.to_csv(f"E:/bishe/newdata/collectiveinfo/matched_data_{n_neighbors}_neighbors_{caliper if caliper else 'no_caliper'}.csv", index=False)

            # 保存匹配对信息
            matched_pairs_df = pd.DataFrame(matched_pairs)
            matched_pairs_df.to_csv(f"E:/bishe/newdata/collectiveinfo/matched_pairs_{n_neighbors}_neighbors_{caliper if caliper else 'no_caliper'}.csv", index=False)

            print(f"匹配数据（{n_neighbors}-对{n_neighbors}，{'有卡尺' if caliper else '无卡尺'}）已保存。")
            print(f"匹配成功率：{matching_success_rate:.4f}")

            # 保存 SMD 结果
            smd_data = {
                'Covariate': [],
                'SMD_Before': [],
                'SMD_After': []
            }

            # 匹配前 SMD 计算
            for c in covariates:
                smd_before = std_mean_diff(treated[c], control[c])
                smd_data['Covariate'].append(c)
                smd_data['SMD_Before'].append(round(smd_before, 3))

                # 匹配后 SMD 计算
                smd_after = std_mean_diff(
                    matched_df.loc[matched_df[treatment_col] == 1, c],
                    matched_df.loc[matched_df[treatment_col] == 0, c]
                )
                smd_data['SMD_After'].append(round(smd_after, 3))

            smd_df = pd.DataFrame(smd_data)
            smd_df.to_csv(f"E:/bishe/newdata/collectiveinfo/smd_table_{n_neighbors}_neighbors_{caliper if caliper else 'no_caliper'}.csv", index=False)

# 6. 打印匹配后的平均处理效应 (ATT) 和 T 检验结果
for n_neighbors in neighbors:
    for caliper in calipers:
        matched_df = pd.read_csv(f"E:/bishe/newdata/collectiveinfo/matched_data_{n_neighbors}_neighbors_{caliper if caliper else 'no_caliper'}.csv")
        treated_outcome = matched_df.loc[matched_df[treatment_col] == 1, outcome_col]
        control_outcome = matched_df.loc[matched_df[treatment_col] == 0, outcome_col]

        ATT = treated_outcome.mean() - control_outcome.mean()
        print(f"\n=== 匹配后平均处理效应 (ATT) ===")
        print(f"匹配策略: {n_neighbors}-对{n_neighbors}, {'有卡尺' if caliper else '无卡尺'}")
        print(f"处理组 - 对照组在 {outcome_col} 上的均值差异：{ATT:.3f}")

        # 进行 t 检验
        t_stat, p_val = ttest_ind(treated_outcome, control_outcome, equal_var=False)
        print(f"T检验: t值={t_stat:.3f}, p值={p_val:.5f}")
