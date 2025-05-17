# 数据说明文档

## 目录结构总览

```
 📁RQ2/
│  ├─ 📄README.md
│  ├─ 📁data/
│  │  ├─ 📁collectiveinfo/
│  │  │  ├─ 📄Cleaned_Merged_Data__No_Index_Column_.csv
│  │  │  ├─ 📄covariate_correlation_matrix.csv
│  │  │  ├─ 📄failed_slugs.csv
│  │  │  ├─ 📄failed_slugs_lost.csv
│  │  │  ├─ 📄failed_slugs_lost_update.csv
│  │  │  ├─ 📄filtered_last.csv
│  │  │  ├─ 📄filtered_last_corrected.csv
│  │  │  ├─ 📄filtered_slugs.csv
│  │  │  ├─ 📄fixed_success_collective_data.json
│  │  │  ├─ 📄fixed_success_collective_data_lost.json
│  │  │  ├─ 📄fixed_time.json
│  │  │  ├─ 📄full_1.csv
│  │  │  ├─ 📄last.csv
│  │  │  ├─ 📄logistic_regression_coefficients.csv
│  │  │  ├─ 📄matched_data.csv
│  │  │  ├─ 📄matched_data_1_neighbors_0.02.csv
│  │  │  ├─ 📄matched_data_1_neighbors_0.05.csv
│  │  │  ├─ 📄matched_data_1_neighbors_no_caliper.csv
│  │  │  ├─ 📄matched_data_3_neighbors_0.02.csv
│  │  │  ├─ 📄matched_data_3_neighbors_0.05.csv
│  │  │  ├─ 📄matched_data_3_neighbors_no_caliper.csv
│  │  │  ├─ 📄matched_pairs.csv
│  │  │  ├─ 📄matched_pairs_1_neighbors_0.02.csv
│  │  │  ├─ 📄matched_pairs_1_neighbors_0.05.csv
│  │  │  ├─ 📄matched_pairs_1_neighbors_no_caliper.csv
│  │  │  ├─ 📄matched_pairs_3_neighbors_0.02.csv
│  │  │  ├─ 📄matched_pairs_3_neighbors_0.05.csv
│  │  │  ├─ 📄matched_pairs_3_neighbors_no_caliper.csv
│  │  │  ├─ 📄Merged_Data_with_Age.csv
│  │  │  ├─ 📄ols_coefficients.csv
│  │  │  ├─ 📄regression_coefficients.csv
│  │  │  ├─ 📄res.csv
│  │  │  ├─ 📄res_1.csv
│  │  │  ├─ 📄res_2.csv
│  │  │  ├─ 📄res_first.csv
│  │  │  ├─ 📄res_one_hot.csv
│  │  │  ├─ 📄res_top5_tags.csv
│  │  │  ├─ 📄res_top5_tags_fixed.csv
│  │  │  ├─ 📄res_top5_tags_o1.csv
│  │  │  ├─ 📄slugs_after-before.csv
│  │  │  ├─ 📄slug_name_1.csv
│  │  │  ├─ 📄smd_table.csv
│  │  │  ├─ 📄smd_table_1_neighbors_0.02.csv
│  │  │  ├─ 📄smd_table_1_neighbors_0.05.csv
│  │  │  ├─ 📄smd_table_1_neighbors_no_caliper.csv
│  │  │  ├─ 📄smd_table_3_neighbors_0.02.csv
│  │  │  ├─ 📄smd_table_3_neighbors_0.05.csv
│  │  │  ├─ 📄smd_table_3_neighbors_no_caliper.csv
│  │  │  ├─ 📄success_collective_data.json
│  │  │  ├─ 📄success_collective_data_update.json
│  │  │  ├─ 📄time.json
│  │  │  ├─ 📄updated_merged_collective_data.csv
│  │  ├─ 📁slug/
│  │  │  ├─ 📄cleaned_project_slugs.csv
│  │  │  ├─ 📄Merged_Data.csv
│  │  │  ├─ 📄slug_first_time.csv
│  ├─ 📁PSM/
│  │  ├─ 📄PSM_1.py     进行倾向评分
│  │  ├─ 📄PSM_2.py
│  │  ├─ 📄PSM_3.py
│  │  ├─ 📄PSM_PAIR.py
│  │  ├─ 📄PSM_SMD_NEW.py
│  ├─ 📁src/
│  │  ├─ 📄byslug.py
│  │  ├─ 📄creat_time.py
│  │  ├─ 📄filter_0.py
│  │  ├─ 📄fix_github_flag.py
│  │  ├─ 📄fix_json.py
│  │  ├─ 📄full_data.py
│  │  ├─ 📄get_discussion.py
│  │  ├─ 📄get_pull_request.py
│  │  ├─ 📄get_release.py
│  │  ├─ 📄get_time.py
│  │  ├─ 📄github_flag.py
│  │  ├─ 📄one-hot-2.py
│  │  ├─ 📄one-hot-3.py
│  │  ├─ 📄one-hot-4.py
│  │  ├─ 📄one-hot.py
│  │  ├─ 📄pre.py
│  │  ├─ 📄PSM_SMD.py
│  │  ├─ 📄slug_lost.py
│  │  ├─ 📄slug_unique.py
│  │  ├─ 📄sociallink.py
│  │  ├─ 📄sociallink_github.py
│  │  ├─ 📄unique.py
```
