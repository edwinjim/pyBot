import sys
import socket
import string
from sqlite3 import dbapi2 as sqlite

HOST='127.0.0.1'
CHANNEL='#bot'
PORT=6667

NICK='pyBot'
IDENT=('%s' % NICK)
REALNAME=('%s' % NICK)
MODE=('%s +B' % NICK)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('NICK %s\r\n' % NICK)
s.send('USER %s %s bla :%s\r\n' % (IDENT, HOST, REALNAME))
s.send('JOIN %s\r\n' % CHANNEL)
s.send('MODE %s\r\n' % MODE)

def check_badword():
  try:
    fileHandle = open ('badwords.txt', 'r')
    badwords = fileHandle.read()
    global blacklist 
    blacklist = badwords.replace('\r\n','').split(',')
      
  except:
    fileHandle = open ('badwords.txt', 'w')
  fileHandle.close() 

def db_write(data):
  try:
    fileHandle = open ('badwords.db', 'r')
    connection = sqlite.connect('badwords.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO badwords VALUES (null," %s")' % data )
    connection.commit()
   
  except:
    connection = sqlite.connect('badwords.db') 
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE badwords (id INTEGER PRIMARY KEY,word VARCHAR(50))')
    connection.commit()
  fileHandle.close()

def learn_badword(data):
  fileHandle = open ('badwords.txt', 'a')
  badword = ((data.split('!learn')[1]).replace('\n','').replace('\r','').split()[0]+',')
  fileHandle.write(badword)
  fileHandle.close()
  return badword

check_badword() 
 
while 1:
  data = s.recv (4096)
  if data.find ('PING') != -1:
    s.send ('PONG '+ data.split() [1] + '\r\n')
  elif data.find ('PRIVMSG %s :!quit' % CHANNEL) != -1:
    s.send ('QUIT : \r\n')
    s.close()
  elif data.find ('PRIVMSG %s :!version' % CHANNEL) != -1:
    s.send('PRIVMSG %s :i dont have one\r\n' % CHANNEL)
  elif data.find ('PRIVMSG %s :!ping' % CHANNEL or 'PRIVMSG %s :pyBot: !ping' % CHANNEL) != -1:
    s.send('PRIVMSG %s :pong\r\n' % CHANNEL)
  elif data.find('PRIVMSG %s :' % CHANNEL) != -1:
    for i in blacklist:
      if i in data.split(CHANNEL)[1].replace('\r\n', '').replace(':', '').split(): 
        s.send('PRIVMSG %s :bad word detected\r\n' % CHANNEL)
  if data.find('PRIVMSG %s :!learn' % CHANNEL) != -1:
    s.send('PRIVMSG %s :new bad word added: ' % CHANNEL + learn_badword(data) + db_write(data)+ i + '\r\n')
# on some evening on some day someone did some not working blackmagic here
#((i + ' ' in data.split('#game-dev')[1].replace('\r\n', '') or len(data.split('#game-dev')[1].split(i)[1].replace('\r\n', ''))==0) or (' ' + i in data.split('#game-dev')[1]  or len(data.split('#game-dev')[1].split(i)[0].replace('\r\n', '') or ':' + i in data.split('#game-dev')[1])==0)):
#######################
      
  print data
