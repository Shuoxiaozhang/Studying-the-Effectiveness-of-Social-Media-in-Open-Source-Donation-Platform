import requests
import json
import pandas as pd
import os
import time

# GitHub的API基础URL
github_api_url = "https://api.github.com/repos"
access_token = "GITHUB_TOKEN"  # 替换为你的 GitHub Personal Access Token

# 设置请求头
headers = {
    "Authorization": f"token {access_token}"
}

# 读取CSV文件，假设文件名为github.csv
df = pd.read_csv("E:/bishe/newdata/slug/Merged_Data.csv")

# 创建pull requests存储目录，如果没有的话
if not os.path.exists("E:/bishe/newdata/github/pulls"):
    os.makedirs("E:/bishe/newdata/github/pulls")

# 提取GitHub仓库的URL和项目slug
for _, row in df.iterrows():
    slug = row['slug']
    github_url = row['github-url']

    # 如果github_url为空，跳过该行
    if pd.isna(github_url):
        print(f"跳过空的GitHub URL: {slug}")
        continue

    try:
        # 检查URL是否是组织页面，处理没有repo的情况
        if "github.com" in github_url:
            parts = github_url.split('github.com/')[1].split('/')
            if len(parts) == 2:
                owner, repo = parts[0], parts[1]
            else:
                owner = parts[0]
                repo = None  # 这里没有repo名，后续处理时需要获取组织下的所有仓库
        else:
            print(f"跳过无效URL: {github_url} 的 {slug}")
            continue

        # 如果是组织（没有repo），获取组织下所有仓库
        if repo is None:
            org_repos_url = f"https://api.github.com/orgs/{owner}/repos"
            response = requests.get(org_repos_url, headers=headers)
            if response.status_code == 200:
                repos = response.json()
                for repo_info in repos:
                    repo = repo_info['name']
                    pulls_url = f"{github_api_url}/{owner}/{repo}/pulls"
                    pull_response = requests.get(pulls_url, headers=headers)
                    if pull_response.status_code == 200:
                        pulls = pull_response.json()

                        # 将pull requests保存为JSON文件
                        filename = f"E:/bishe/newdata/github/pulls/{slug}_{repo}_pulls.json"
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(pulls, f, ensure_ascii=False, indent=4)
                        print(f"{slug} 的{repo}的pull requests数据已保存为 {filename}")
                    else:
                        print(f"无法获取 {slug} 的{repo}的pull requests数据，状态码：{pull_response.status_code}")
            else:
                print(f"无法获取 {slug} 的组织仓库，状态码：{response.status_code}")
        else:
            # 处理单个repo
            pulls_url = f"{github_api_url}/{owner}/{repo}/pulls"
            response = requests.get(pulls_url, headers=headers)

            if response.status_code == 200:
                pulls = response.json()

                # 将pull requests保存为JSON文件
                filename = f"E:/bishe/newdata/github/pulls/{slug}_pulls.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(pulls, f, ensure_ascii=False, indent=4)
                print(f"{slug} 的pull requests数据已保存为 {filename}")
            else:
                print(f"无法获取 {slug} 的pull requests数据，状态码：{response.status_code}")

    except Exception as e:
        print(f"请求 {slug} 出错: {e}")
    # time.sleep(1)
