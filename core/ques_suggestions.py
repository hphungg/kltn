from database.question_db import MongoDBConnector

def query_questions(knowledge_list):
    db = MongoDBConnector()
    questions = db.get_exercises_by_tags(knowledge_list)
    return questions