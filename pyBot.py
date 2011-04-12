import os, sys, socket, string
from sqlite3 import dbapi2 as sqlite
from signal import SIGTERM

global connection 
connection = sqlite.connect('/tmp/badwords.db')

global cursor
cursor = connection.cursor()

HOST='irc.ph2network.org'
CHANNEL='#bottest'
PORT=6667

NICK='pyBot_alpha'
IDENT=('%s' % NICK)
REALNAME=('%s' % NICK)
MODE=('%s +B' % NICK)

def build_conserver():
  global s
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
  cursor.execute('CREATE TABLE IF NOT EXISTS badwords (id INTEGER PRIMARY KEY,word VARCHAR(50) UNIQUE)') 
 
def close_con():
  cursor.close()
  connection.close()
  s.close()
  pf = os.getpid()
  os.kill(pf, SIGTERM) 
  sys.exit()

#def check_badword(data):
#  badword =  ((data.split(CHANNEL)[1]).replace('\n','').replace('\r','').split()[0])
#  cursor.execute('SELECT * FROM badwords WHERE word MATCH lower(?)', (badword,))
#  if not 'None'
#  s.send('PRIVMSG %s :bad word detected\r\n' % CHANNEL)

def write_db(data):
  badword = ((data.split('!learn')[1]).replace('\n','').replace('\r','').split()[0])
  cursor.execute('INSERT OR REPLACE INTO badwords VALUES (null,lower("{0}"))'.format(badword))
  connection.commit()
  return badword

def remword_db(data):
  badword = ((data.split('!forget')[1]).replace('\n','').replace('\r','').split()[0])
  cursor.execute('DELETE FROM badwords WHERE word=lower(?)',(badword,))
  return badword

def daemonize():
  try:
    pid = os.fork()
    if pid > 0:
      sys.exit(0) 
  except OSError, e:
    sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
    sys.exit(-2)

  os.setsid()
  os.umask(0)

  try:
    pid = os.fork()
    if pid > 0:
      try:
        f = file('pybot.pid', 'w')
        f.write(str(pid))
        f.close()
      except IOError, e:
        logging.error(e)
        sys.stderr.write(repr(e))
      sys.exit(0)
  except OSError, e:
    sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
    sys.exit(-2)

  for fd in (0, 1, 2):
    try:
      os.close(fd)
    except OSError:
      pass

build_conserver()
open_condb()
daemonize()

while 1:
  data = s.recv (4096)
  if data.find ('PING') != -1:
    s.send ('PONG '+ data.split()[1] + '\r\n')
  
  if data.find ('PRIVMSG {0} :!version'.format(CHANNEL)) != -1:
    s.send('PRIVMSG {0} :i am bleeding edge and might be broken\r\n'.format(CHANNEL))
  
  if data.find ('PRIVMSG {0} :!ping'.format(CHANNEL)) != -1:
    s.send('PRIVMSG {0} :pong\r\n'.format(CHANNEL))
  
  if data.find('PRIVMSG {0} :!forget'.format(CHANNEL)) != -1:
    s.send('PRIVMSG {0} :bad word deleted: '.format(CHANNEL) + remword_db(data) + '\r\n')

#  if data.find('PRIVMSG %s :' % CHANNEL) != -1:
#    for i in data:
#      if i in data.split(CHANNEL)[1].replace('\r\n', '').replace(':', '').split(): 
  
  if data.find('PRIVMSG {0} :!learn'.format(CHANNEL)) != -1:
    s.send('PRIVMSG {0} :new bad word added: '.format(CHANNEL) + write_db(data) + '\r\n')
  
  if data.find ('PRIVMSG {0} :!quit'.format(CHANNEL)) != -1:                       
    s.send('QUIT : \r\n' ) 
    close_con()
# on some evening on some day someone did some not working blackmagic here
#((i + ' ' in data.split('#game-dev')[1].replace('\r\n', '') or len(data.split('#game-dev')[1].split(i)[1].replace('\r\n', ''))==0) or (' ' + i in data.split('#game-dev')[1]  or len(data.split('#game-dev')[1].split(i)[0].replace('\r\n', '') or ':' + i in data.split('#game-dev')[1])==0)):
#######################
  
  #print (data)      

