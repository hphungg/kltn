import streamlit as st
from neo4j import GraphDatabase

URI = st.secrets["AURA_URI"]
USERNAME = st.secrets["AURA_USERNAME"]
PASSWORD = st.secrets["AURA_PASSWORD"]

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