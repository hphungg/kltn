import streamlit as st

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

URI = st.secrets["MONGO_URI"]

class MongoDBConnector:
    def __init__(self):
        self.uri = URI
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client['questions']

    def get_exercises_by_tags(self, knowledge_list):
        collection = self.db['questions']
        query = {
            "$or": [
                {"knowledge_tags": {"$in": knowledge_list}},  
                {"knowledge_tags": {"$size": 0}}             
            ]
        }
        exercises = collection.find(query).limit(3)
        return list(exercises)