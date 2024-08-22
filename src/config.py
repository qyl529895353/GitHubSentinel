import json
import requests

class Config:
    def __init__(self):
        self.access_token = None
        self.load_config()
        self.gitlab_url = "http://39.108.179.79:8929"

    def load_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.github_token = config.get('github_token')
            self.notification_settings = config.get('notification_settings')
            self.subscriptions_file_map = config.get('subscriptions_file', {})
            self.subscriptions_file = self.subscriptions_file_map.keys()
            self.update_interval = config.get('update_interval', 24 * 60 * 60)  # Default to 24 hours
            self.baidu_app_key = config.get("BAIDU_KEY")
            self.baidu_app_secret = config.get("BAIDU_SECRET")
            self.set_access_token()

    def set_access_token(self):

        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.baidu_app_key}&client_secret={self.baidu_app_secret}"

        payload = ""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        try:
            response = requests.post(url, data=payload, headers=headers).json()
        except Exception as e:
            return
        if response.get("error_code"):
            return
        self.access_token = response["access_token"]





