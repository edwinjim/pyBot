from sqlite3 import dbapi2 as sqlite

connection = sqlite.connect('/tmp/badwords.db')
cursor = connection.cursor()
cursor.execute('SELECT * FROM badwords')
for row in cursor:
  print 'id:', row[0]
  print 'word:', row[1]

cursor.close()
connection.close()
