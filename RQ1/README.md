# 数据说明文档

## 目录结构总览

```
📁RQ1/
│  ├─ 📄README.md
│  ├─ 📁data/
│  │  ├─ 📄collectiveInfo.zip
│  │  ├─ 📄README.md
│  │  ├─ 📄social_media_collective_data.csv
│  │  ├─ 📄transaction.zip
│  │  ├─ 📁github_classed/
│  │  │  ├─ 📄merged_filtered_data.zip
│  │  │  ├─ 📄README.md
│  │  ├─ 📁media/
│  │  │  ├─ 📁github/
│  │  │  │  ├─ 📄commits.7z
│  │  │  │  ├─ 📄issues.zip
│  │  │  │  ├─ 📄repositories.zip
│  │  │  ├─ 📁instagram/
│  │  │  │  ├─ 📄instagram_data.csv
│  │  │  │  ├─ 📄instagram_data.csv~
│  │  │  ├─ 📁tables/
│  │  │  │  ├─ 📄discord.csv
│  │  │  │  ├─ 📄discourse.csv
│  │  │  │  ├─ 📄facebook.csv
│  │  │  │  ├─ 📄ghost.csv
│  │  │  │  ├─ 📄git.csv
│  │  │  │  ├─ 📄github.csv
│  │  │  │  ├─ 📄gitlab.csv
│  │  │  │  ├─ 📄instagram.csv
│  │  │  │  ├─ 📄linkedin.csv
│  │  │  │  ├─ 📄mastodon.csv
│  │  │  │  ├─ 📄mattermost.csv
│  │  │  │  ├─ 📄meetup.csv
│  │  │  │  ├─ 📄peertube.csv
│  │  │  │  ├─ 📄pixelfed.csv
│  │  │  │  ├─ 📄slack.csv
│  │  │  │  ├─ 📄tiktok.csv
│  │  │  │  ├─ 📄tumblr.csv
│  │  │  │  ├─ 📄twitch.csv
│  │  │  │  ├─ 📄twitter.csv
│  │  │  │  ├─ 📄website.csv
│  │  │  │  ├─ 📄youtube.csv
│  │  │  ├─ 📁twitter/
│  │  │  │  ├─ 📄twitter_data.csv
│  │  ├─ 📁RQ1/
│  │  │  ├─ 📄social_media_usage_column.png
│  │  │  ├─ 📄social_media_usage_pie.png
│  │  │  ├─ 📄social_media_usage_statistics.csv
│  │  ├─ 📁slugs/
│  │  │  ├─ 📄cleaned_project_slugs.csv
│  │  │  ├─ 📄failed_slugs.csv
│  │  │  ├─ 📄project_slugs.csv
│  │  ├─ 📁twitter_classed/
│  │  │  ├─ 📄filtered_twitter_data.csv
│  ├─ 📁src/
│  │  ├─ 📄README.md
│  │  ├─ 📁base_data_collect/
│  │  │  ├─ 📄classify-medium.py
│  │  │  ├─ 📄clean-space.py
│  │  │  ├─ 📄grab-detailOC-info.py
│  │  │  ├─ 📄grab-slugs.py
│  │  │  ├─ 📄grabtransaction.py
│  │  │  ├─ 📄merge-collectiveInfo.py
│  │  │  ├─ 📄trans-transactionscsv.py
│  │  │  ├─ 📄transJsonToCSV.py
│  │  ├─ 📁media_data_collect/
│  │  │  ├─ 📁github/
│  │  │  │  ├─ 📄grab-commit.py
│  │  │  │  ├─ 📄grab-issue.py
│  │  │  │  ├─ 📄grab-repoInfo.py
│  │  │  ├─ 📁instagram/
│  │  │  │  ├─ 📄grab-profile.py
│  │  ├─ 📁RQ1/
│  │  │  ├─ 📄media_statistic.py
│  │  ├─ 📁utils/
│  │  │  ├─ 📄adjustcsv.py
│  │  │  ├─ 📄fixJson.py