# src/llm.py

import os
import requests
from openai import OpenAI
from logger import LOG
from config import Config

base_config = Config()

class LLM:
    def __init__(self):
        self.client = OpenAI()
        LOG.add("daily_progress/llm_logs.log", rotation="1 MB", level="DEBUG")

    def generate_daily_report(self, markdown_content, dry_run=False):
        prompt = f"以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题；:\n\n{markdown_content}"
        
        if dry_run:
            LOG.info("Dry run mode enabled. Saving prompt to file.")
            with open("daily_progress/prompt.txt", "w+") as f:
                f.write(prompt)
            LOG.debug("Prompt saved to daily_progress/prompt.txt")
            return "DRY RUN"

        LOG.info("Starting report generation using GPT model.")
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是项目报告总结达人,擅长将项目不同片段信息进行整合并撰写出让boss满意的简报,要求撰写的内容使用中文"},
                    {"role": "user", "content": prompt}
                ]
            )
            LOG.debug("GPT response: {}", response)
            return response.choices[0].message.content
        except Exception as e:
            LOG.error("An error occurred while generating the report: {}", e)
            raise


class ChatErnieBotTurbo:
    default_model = 'ernie-speed-128k'

    def generate_daily_report(self, markdown_content, dry_run=False):
        prompt = f"以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题；:\n\n{markdown_content}"

        if dry_run:
            LOG.info("Dry run mode enabled. Saving prompt to file.")
            with open("daily_progress/prompt.txt", "w+") as f:
                f.write(prompt)
            LOG.debug("Prompt saved to daily_progress/prompt.txt")
            return "DRY RUN"

        LOG.info("Starting report generation using GPT model.")

        data = {
            "messages": [
                # {"role": "system", "content": "你是项目报告总结达人,擅长将项目不同片段信息进行整合并撰写出让boss满意的简报,要求撰写的内容使用中文 ，以下待处理的内容 ###"},
                {"role": "user", "content": "你是项目报告总结达人,擅长将项目不同片段信息进行整合并撰写出让boss满意的简报,要求撰写的内容使用中文 ，以下待处理的内容 ###" + prompt}
            ],
            "temperature": 0.5,
            "stream": False,
            "user_id": "test_suer"
        }
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{self.default_model}?access_token={base_config.access_token}"

        header = {
            "Content-Type": "application/json"
        }
        print(data)
        try:
            resp = requests.post(url, json=data, headers=header, stream=False).json()
        except Exception as e:
            LOG.error("An error occurred while generating the report: {}", e)
            raise
        print(resp)
        return resp["result"]