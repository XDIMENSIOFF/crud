# ЧЕРНОВИК ДЛЯ РАБОТЫ С БД

from tinydb import TinyDB, Query

db = TinyDB("db.json")

od = sorted(db.all(), key=lambda k: k['mins'])

print(od)