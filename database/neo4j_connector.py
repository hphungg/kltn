from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv('.env.local') 
URI = os.getenv('AURA_URI')
USERNAME = os.getenv('AURA_USERNAME')
PASSWORD = os.getenv('AURA_PASSWORD')

class Neo4jConnector:
    def __init__(self):
        self.uri = URI
        self.user = USERNAME
        self.password = PASSWORD
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def query(self, query):
        with self.driver.session() as session:
            results = session.run(query)
            return [record for record in results]