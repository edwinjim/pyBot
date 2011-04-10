from sqlite3 import dbapi2 as sqlite

connection = sqlite.connect('/tmp/badwords.db')
cursor = connection.cursor()
t = 'bla'
cursor.execute("SELECT * FROM badwords WHERE word='?'", t)
cursor.close()
connection.close()
