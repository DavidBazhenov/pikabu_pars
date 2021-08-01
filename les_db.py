import sqlite3

with sqlite3.connect('new_data.db') as db:
	cursor = db.cursor()
	query = """CREATE TABLE IF NOT EXISTS points(name INTEGER,id_from INTEGER,id_to INTEGER)"""
	query1 = """INSERT INTO points VALUES(?,?,?)"""
	cursor.executemany(query,)
	cursor.execute(query1)
	db.commit()
