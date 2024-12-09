import streamlit as st

def question_query(knowledge_list, db):
    questions = db.get_exercises_by_tags(knowledge_list)
    return questions