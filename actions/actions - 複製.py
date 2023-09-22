# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 00:05:46 2023

@author: user
"""

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from pymongo import MongoClient

class GetAnswer(Action):

    def __init__(self):
        # 連接 MongoDB
        mogopath="mongodb+srv://<your password>@cluster0.ket3gr2.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(mogopath)
        self.db = self.client["your db_name"]
        self.collection = self.db["your collection_name"]

    def name(self) -> Text:
        return "action_get_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 從 tracker 中取得使用者輸入
        user_input = tracker.latest_message['text']
        
        # 以 ChatGPT 預期的格式組成 prompt
        prompt = user_input

        # 設置 OpenAI API 的請求參數
        api_key = "your api key" 
        
        #選擇 gpt 模型，這裡以 gpt-3 為例
        endpoint = "https://api.openai.com/v1/engines/davinci/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "prompt": prompt,
            "max_tokens": 100000000000000000000000,
            "temperature": 0.5,
            "top_p": 1,
            "frequency_penalty": 0,
            "best_of": 1
        }

        # 從 MongoDB 中獲取符合使用者輸入的回覆
        question = user_input
        result = self.collection.aggregate([
            {
                '$search': {
                'index':'search_q',
                "text": {
                         "query": question,
                         "path": "question",
                         "fuzzy":{}
                         }
                }
            },
            {
                '$project':{
                    'question':1,
                    'answer':1,
                    'score':{"$meta":'searchScore'}
                }
            },
            {
                '$sort': {'score': -1}
            },
            {
                '$limit':1
            }
        ]).next() if self.collection.find_one(question) is None else self.collection.find_one(question)

        if result:
            reply = result['answer']
        else:
            # 發送請求到 OpenAI API，獲取 ChatGPT 模型生成的回覆
            response = requests.post(endpoint, headers=headers, json=data).json()
            reply = response["choices"][0]["text"].strip()
            
            # 不回复 user 和 chatbot 的句子
            if reply.startswith('User:') and '\nChatbot:' in reply:
                reply = reply.split('\nChatbot:')[1]
            elif reply.startswith('Chatbot:'):
                reply = reply.split('Chatbot:')[1]

        # 回傳回覆
        dispatcher.utter_message(text=reply)

        return []


