from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from pymongo import MongoClient
import pandas as pd

class GetAnswer(Action):

    def __init__(self):
        # MongoDB Configuration
        mogopath = "mongodb+srv://<your password>@cluster0.ket3gr2.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(mogopath)
        self.db = self.client["DB_name"]
        self.collection = self.db["collection_name"]

        # Load FAQ Data
        data = pd.DataFrame(list(self.collection.find()))
        self.faq_d = data.drop(['_id'], axis=1)
        qss = list(self.faq_d['question'])

        # Create NLU Examples
        with open("./data/question.yml", "wt", encoding="utf-8") as f:
            f.write('version: "2.0"\n')
            f.write("nlu: \n- intent: question\n  examples: | \n")
            for q in qss:
                f.write(f"    - {q}\n")

    def name(self) -> Text:
        return "action_get_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get user input from tracker
        user_input = tracker.latest_message['text']

        # Configure OpenAI API
        api_key = "your api key"
        endpoint = "https://api.openai.com/v1/engines/davinci/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "prompt": user_input,
            "max_tokens": 1000,  # Adjust as needed
            "temperature": 0.5,
            "top_p": 1,
            "frequency_penalty": 0,
            "best_of": 1
        }

        # MongoDB Query
        question = user_input
        result = self.collection.aggregate([
            {
                '$search': {
                    'index': 'search_q',
                    "text": {
                        "query": question,
                        "path": "question",
                        "fuzzy": {}
                    }
                }
            },
            {
                '$project': {
                    'question': 1,
                    'answer': 1,
                    'score': {"$meta": 'searchScore'}
                }
            },
            {
                '$sort': {'score': -1}
            },
            {
                '$limit': 1
            }
        ]).next() if self.collection.find_one(question) is None else self.collection.find_one(question)

        if result:
            reply = result['answer']
        else:
            # Request response from OpenAI API
            response = requests.post(endpoint, headers=headers, json=data).json()
            reply = response["choices"][0]["text"].strip()

            # Remove user and chatbot markers
            if reply.startswith('User:') and '\nChatbot:' in reply:
                reply = reply.split('\nChatbot:')[1]
            elif reply.startswith('Chatbot:'):
                reply = reply.split('Chatbot:')[1]

        # Send the response
        dispatcher.utter_message(text=reply)

        return []
