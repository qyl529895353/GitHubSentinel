import requests
from datetime import datetime, date, timedelta
import os
from logger import LOG  # 假设这个LOG模块已经正确设置
from utils import match_record
from config import Config
base_config = Config()
gitlab_url = base_config.gitlab_url


class GitLabClient:
    def __init__(self, private_token):
        self.private_token = private_token
        self.headers = {'PRIVATE-TOKEN': self.private_token}

    def fetch_updates(self, project_id, since=None, until=None):
        if since:
            since = (datetime.strptime(since, '%Y-%m-%d') + timedelta(-1)).isoformat()
        if until:
            until = (datetime.strptime(until, '%Y-%m-%d') + timedelta(1)).isoformat()
        updates = {
            'commits': self.fetch_commits(project_id, since, until),
            'issues': self.fetch_issues(project_id, since, until),
            'pull_requests': self.fetch_merge_requests(project_id, since, until)
        }
        return updates

    def fetch_commits(self, project_id, since=None, until=None):
        url = f'{gitlab_url}/api/v4/projects/{project_id}/repository/commits'

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return match_record(response.json(), since, until)

    def fetch_issues(self, project_id, since=None, until=None):
        url = f'{gitlab_url}/api/v4/projects/{project_id}/issues'
        params = {}
        if since:
            params['created_after'] = since
        if until:
            params['created_before'] = until
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_merge_requests(self, project_id, since=None, until=None):
        # GitLab 使用 'created_after' 和 'created_before' 而不是 'since' 和 'until'
        url = f'{gitlab_url}/api/v4/projects/{project_id}/merge_requests'

        params = {
            'state': 'merged',  # GitLab 中使用 'merged' 来表示已合并的 Merge Request
            'created_after': since,
            'created_before': until
        }
        response = requests.get(url, headers=self.headers, params=params)

        response.raise_for_status()
        return response.json()

    def export_daily_progress(self, project_id):
        today = datetime.now().date().isoformat()
        print("today", project_id)
        updates = self.fetch_updates(project_id, since=today)
        cn_repo = base_config.subscriptions_file_map[str(project_id)].replace("/", "_")
        repo_dir = os.path.join('daily_progress', cn_repo)
        os.makedirs(repo_dir, exist_ok=True)

        file_path = os.path.join(repo_dir, f'{today}.md')
        with open(file_path, 'w') as file:
            file.write(f"# Daily Progress for {cn_repo} ({today})\n\n")
            file.write("\n## Issues Closed Today\n")
            for issue in updates['issues']:
                file.write(f"- {issue['title']} #{issue['id']}\n")

            file.write("\n## commits Today\n")
            for cm in updates["commits"]:
                file.write(f"- {cm['title']} #{cm['id']}\n")

            file.write("\n## Pull Requests Merged Today\n")
            for pr in updates['pull_requests']:
                file.write(f"- {pr['title']} #{pr['id']}\n")

        LOG.info(f"Exported daily progress to {file_path}")
        return file_path

    def export_progress_by_date_range(self, project_id, days):
        today = datetime.now().date()
        since = today - timedelta(days=days)

        updates = self.fetch_updates(project_id, since=since.isoformat())
        cn_repo = base_config.subscriptions_file_map[str(project_id)].replace("/", "_")
        repo_dir = os.path.join('daily_progress', cn_repo)
        os.makedirs(repo_dir, exist_ok=True)

        file_path = os.path.join(repo_dir, f'{today}.md')
        with open(file_path, 'w') as file:
            file.write(f"# Daily Progress for {cn_repo} ({today})\n\n")
            file.write("\n## Issues Closed Today\n")
            for issue in updates['issues']:
                file.write(f"- {issue['title']} #{issue['id']}\n")

            file.write("\n## commits Today\n")
            for cm in updates["commits"]:
                file.write(f"- {cm['title']} #{cm['id']}\n")

            file.write("\n## Pull Requests Merged Today\n")
            for pr in updates['pull_requests']:
                file.write(f"- {pr['title']} #{pr['id']}\n")

        LOG.info(f"Exported daily progress to {file_path}")
        return file_path