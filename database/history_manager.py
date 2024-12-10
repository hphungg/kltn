import shelve

def load_chat_history(hash_key):
    with shelve.open("chat_history_" + hash_key) as db:
        return db.get("messages", [])

def save_chat_history(messages, hash_key):
    with shelve.open("chat_history_" + hash_key) as db:
        db["messages"] = messages