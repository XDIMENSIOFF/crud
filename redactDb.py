from tinydb import TinyDB, Query

db = TinyDB('db.json')

user = db.get(doc_id=1)
print(user.doc_id)