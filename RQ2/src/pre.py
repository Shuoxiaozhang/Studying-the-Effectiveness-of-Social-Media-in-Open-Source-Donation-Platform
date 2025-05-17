import pandas as pd
import requests
import json
import time
import concurrent.futures

# GraphQL 端点
url = "https://api.opencollective.com/graphql/v2"

# 你的个人令牌
personal_token = "f2e80a439066362a24289599eaf145349cc03c5a"

# 请求头
headers = {
    "Content-Type": "application/json",
    "Personal-Token": personal_token
}

# 代理设置（根据你的代理工具修改端口）
proxies = {
    "http": "http://127.0.0.1:12334",  # HTTP 代理
    "https": "http://127.0.0.1:12334",
    # 如果使用 SOCKS5 代理，改为：
    # "http": "socks5h://127.0.0.1:7897",
    # "https": "socks5h://127.0.0.1:7897",
}

# 读取 cleaned_project_slugs.csv
slugs_df = pd.read_csv('E:/bishe/newdata/collectiveinfo/filtered_slugs.csv')

# 从第多少行开始爬取
start_index = 0
slugs_to_query = slugs_df.iloc[start_index:]['slug']

# GraphQL 查询
query = """
query($slug: String) {
  collective(slug: $slug) {
    slug
    name
    type
    tags
    categories
    orders {
        totalCount
    }
    stats {
        contributionsCount
        contributorsCount
    }
    totalFinancialContributors
    location{
        country
    }
  }
}
"""

# 每个线程处理的 slug 数量
batch_size = 100

# 将 slug 划分为多个批次
def chunk_slugs(slugs, batch_size):
    for i in range(0, len(slugs), batch_size):
        yield slugs[i:i + batch_size]

# 并行爬取数据
def fetch_data(batch_slugs):
    batch_data = []
    failed_slugs = []
    for slug in batch_slugs:
        variables = {"slug": slug}
        retries = 0
        while retries < 5:  # 最多重试 5 次
            try:
                response = requests.post(
                    url,
                    json={"query": query, "variables": variables},
                    headers=headers,
                    proxies=proxies,  # 使用代理
                    timeout=10  # 设置超时时间，避免无限等待
                )

                if response.status_code == 200:
                    data = response.json()

                    # 检查 API 是否返回错误
                    if 'errors' in data:
                        print(f"❌ 错误: {slug} - {data['errors']}")
                        failed_slugs.append(slug)
                    else:
                        batch_data.append(data)
                        print(f"✅ 成功: {slug}")
                    break  # 请求成功，跳出重试循环

                elif response.status_code == 429:
                    print(f"⚠️ 请求过多 (429)，等待 10 秒后重试...")
                    time.sleep(10)
                    retries += 1

                elif response.status_code == 403:
                    print(f"🚫 访问被拒绝 (403) - {slug}，可能是 API 限制或代理问题")
                    failed_slugs.append(slug)
                    break

                else:
                    print(f"❗ 请求失败，状态码 {response.status_code} - {slug}")
                    failed_slugs.append(slug)
                    break

            except requests.exceptions.RequestException as e:
                print(f"🌐 请求异常，错误: {e}")
                failed_slugs.append(slug)
                break

    return batch_data, failed_slugs

# 保存查询成功的结果到 JSON 文件
def save_to_file(batch_data, filename):
    with open(filename, 'a', encoding='utf-8') as file:
        if batch_data:
            for data in batch_data:
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.write("\n")

# 打开文件，准备保存查询成功的结果
success_file = 'E:/bishe/newdata/collectiveinfo/success_collective_data_lost.json'
failed_file = 'E:/bishe/newdata/collectiveinfo/failed_slugs_lost.csv'

with open(success_file, 'w', encoding='utf-8') as f:
    f.write('[')  # JSON 数组起始

    # 使用线程池并行爬取数据
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:  # 限制线程数为 2
        slugs_batches = list(chunk_slugs(slugs_to_query, batch_size))
        futures = [executor.submit(fetch_data, batch) for batch in slugs_batches]

        # 获取线程结果并保存
        all_failed_slugs = []
        for future in concurrent.futures.as_completed(futures):
            batch_data, failed_slugs = future.result()
            save_to_file(batch_data, success_file)
            all_failed_slugs.extend(failed_slugs)
            print(f"📦 处理完一批数据")

    # 结束 JSON 数组
    with open(success_file, 'a', encoding='utf-8') as f:
        f.write(']')

# 保存查询失败的 slug 到 CSV 文件
failed_slugs_df = pd.DataFrame(all_failed_slugs, columns=['Failed Slugs'])
failed_slugs_df.to_csv(failed_file, index=False)

print(f"📂 查询失败的 slug 已保存到 {failed_file}")
