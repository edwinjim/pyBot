import sys, socket, string
from sqlite3 import dbapi2 as sqlite

def build_conserver():
  global CHANNEL
  global s

  HOST='irc.ph2network.org'
  CHANNEL='#bottest'
  PORT=6667
  
  NICK='pyBot_alpha'
  IDENT=('%s' % NICK)
  REALNAME=('%s' % NICK)
  MODE=('%s +B' % NICK)

  for i in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = i
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error, msg:
        snet = None
        continue
    try:
        s.connect(sa)
    except socket.error, msg:
        s.close()
        s = None
        continue
    break
  if s is None:
    sys.exit(1) 

  s.send('NICK %s\r\n' % NICK)
  s.send('USER %s %s pyBot :%s\r\n' % (IDENT, HOST, REALNAME))
  s.send('JOIN %s\r\n' % CHANNEL)
  s.send('MODE %s\r\n' % MODE)

def open_condb():
  connection = sqlite.connect('/tmp/badwords.db')
  cursor = connection.cursor()
  cursor.execute('CREATE TABLE IF NOT EXISTS badwords (id INTEGER PRIMARY KEY,word VARCHAR(50) UNIQUE)') 
 
def close_con():
  cursor.close()
  connection.close()
  s.shutdown()
  s.close()
  sys.exit(0)

def check_badword(data):
  cursor = connection.cursor()
  t =  ((data.split(CHANNEL)[1]).replace('\n','').replace('\r','').split()[0])
  cursor.execute('SELECT * FROM badwords WHERE word MATCH low(?)', t)

def write_db(data):
  connection = sqlite.connect('/tmp/badwords.db')
  cursor = connection.cursor()
  badword = ((data.split('!learn')[1]).replace('\n','').replace('\r','').split()[0])
  cursor.execute('INSERT OR REPLACE INTO badwords VALUES (null,lower("{0}"))'.format(badword))
  connection.commit()
  return badword

def remword_db(data):
  cursor = connection.cursor()
  t = ((data.split('!forget')[1]).replace('\n','').replace('\r','').split()[0])
  cursor.execute('DELETE FROM badwords WHERE word=low(?)', t)

build_conserver()
open_condb()

while 1:
  data = s.recv (4096)
  if data.find ('PING') != -1:
    s.send ('PONG '+ data.split()[1] + '\r\n')
  elif data.find ('PRIVMSG {0} :!quit'.format(CHANNEL)) != -1:
    s.send('QUIT : \r\n' ) 
    close_con
  elif data.find ('PRIVMSG {0} :!version'.format(CHANNEL)) != -1:
    s.send('PRIVMSG {0} :i am bleeding edge and might be broken\r\n'.format(CHANNEL))
  elif data.find ('PRIVMSG {0} :!ping'.format(CHANNEL)) != -1:
    s.send('PRIVMSG {0} :pong\r\n'.format(CHANNEL))
  #elif data.find()
  #  s.send('PRIVMSG {0} :bad word deleted: '.format(CHANNEL) + remword_db(data) + '\r\n')
#  elif data.find('PRIVMSG %s :' % CHANNEL) != -1:
#    for i in blacklist:
#      if i in data.split(CHANNEL)[1].replace('\r\n', '').replace(':', '').split(): 
#        s.send('PRIVMSG %s :bad word detected\r\n' % CHANNEL)
  if data.find('PRIVMSG {0} :!learn'.format(CHANNEL)) != -1:
    s.send('PRIVMSG {0} :new bad word added: '.format(CHANNEL) + write_db(data) + '\r\n')
# on some evening on some day someone did some not working blackmagic here
#((i + ' ' in data.split('#game-dev')[1].replace('\r\n', '') or len(data.split('#game-dev')[1].split(i)[1].replace('\r\n', ''))==0) or (' ' + i in data.split('#game-dev')[1]  or len(data.split('#game-dev')[1].split(i)[0].replace('\r\n', '') or ':' + i in data.split('#game-dev')[1])==0)):
#######################
      
  print(data)

