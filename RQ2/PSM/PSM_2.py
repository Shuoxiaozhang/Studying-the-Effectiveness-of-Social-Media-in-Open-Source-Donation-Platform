import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
from scipy.stats import ttest_ind
import statsmodels.api as sm

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
log_reg = LogisticRegression(max_iter=1000, penalty='l2', solver='liblinear')  # L2 正则化
log_reg.fit(X, y)

# 获取回归系数
coefficients = log_reg.coef_[0]  # 逻辑回归系数
intercept = log_reg.intercept_  # 截距项

# 计算标准误和 p 值（使用 statsmodels 或其他方法）
# statsmodels 无法直接为带正则化的模型计算标准误和 p 值，因此你可以跳过这部分或计算其他方法。

# 4. 将结果保存为 CSV 文件
coeff_df = pd.DataFrame({
    'Variable': X.columns,
    'Coefficient': coefficients
})

# 保存结果到 CSV 文件
coeff_csv_file_path = 'E:/bishe/newdata/collectiveinfo/logistic_regression_coefficients.csv'
coeff_df.to_csv(coeff_csv_file_path, index=False)

print(f"逻辑回归系数已保存到: {coeff_csv_file_path}")
