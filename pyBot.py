import os, sys, socket, string
from sqlite3 import dbapi2 as sqlite
from signal import SIGTERM

global connection 
connection = sqlite.connect('/tmp/badwords.db')

global cursor
cursor = connection.cursor()

HOST='irc.ph2network.org'
PORT=6667
CHANNEL='#bottest'

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
    except (socket.error, msg):
        snet = None
        continue
    try:
        s.connect(sa)
    except (socket.error, msg):
        s.close()
        s = None
        continue
    break
  if s is None:
    sys.exit(1) 

  s.send(bytes('NICK {0}\r\n'.format(NICK), 'utf-8'))
  s.send(bytes('USER %s %s pyBot :%s\r\n' % (IDENT, HOST, REALNAME), 'utf-8'))
  s.send(bytes('JOIN {0}\r\n'.format(CHANNEL), 'utf-8'))
  s.send(bytes('MODE {0}\r\n'.format(MODE), 'utf-8'))

def open_condb():
  cursor.execute('CREATE TABLE IF NOT EXISTS badwords (id INTEGER PRIMARY KEY,word TEXT UNIQUE)') 
 
def close_con():
  cursor.close()
  connection.close()
  s.close()
#  try:
#    with open(self.pidfile,'r') as pf:
#      pid = int(pf.read().strip())
#  except IOError:
#    pid = None
#  
#  try:
#    while 1:
#      os.kill(pid, signal.SIGTERM)
#      time.sleep(0.1)
#  except OSError as err:
#    e = str(err.args)
#    if e.find("No such process") > 0:
#      if os.path.exists(self.pidfile):
#        os.remove(self.pidfile)
#      else:
#        print (str(err.args))
#        sys.exit(1)
  sys.exit()
  clear(data)
#def check_badword(data):
#  badword =  ((data.split(CHANNEL)[1]).replace('\n','').replace('\r','').split()[0])
#  words = data.split(CHANNEL)[1]
#  badword = words.split()[0]
#  cursor.execute('SELECT * FROM badwords WHERE word MATCH lower(?)', (badword,))
#  if not 'None'
#  s.send('PRIVMSG %s :bad word detected\r\n' % CHANNEL)

def write_db(data):
  #badword = ((data.split('!learn')[1]).replace('\n','').replace('\r','').split()[0])
  learn = data.split('!learn')[1].replace('\r','').replace('\n','')
  badword = learn.split()[0]
  cursor.execute('INSERT OR REPLACE INTO badwords VALUES (null,lower("{0}"))'.format(badword))
  connection.commit()
  print (badword)
  return badword

def remword_db(data):
  #badword = ((data.split('!forget')[1]).replace('\n','').replace('\r','').split()[0])
  forget = data.split('!forget')[1].replace('\r','').replace('\n','')
  badword = forget.split()[0]
  cursor.execute('DELETE FROM badwords WHERE word=lower(?)',(badword,))
  print (badword)
  return badword

#def daemonize():
#  try:
#    pid = os.fork() 
#    if pid > 0:
#      sys.exit(0) 
#  except OSError as err:                                               
#    sys.stderr.write('fork #1 failed: {0}\n'.format(err))
#    sys.exit(1)
#
#  os.setsid()
#  os.umask(0)
#
#  try:
#    pid = os.fork()
#    if pid > 0:
#      sys.exit(0)
#  except OSError as err :
#    sys.stderr.write('fork #2 failed: {0}\n'.format(err))
#    sys.exit(1)
#
#  for fd in (0, 1, 2):
#    try:
#      os.close(fd)
#    except OSError:
#      pass

build_conserver()
open_condb()
#daemonize()

while 1:
  data = str(s.recv(4096))

  if 'PING ' in data:
    s.send(bytes(('PONG '),'utf-8'))
  
  if 'PRIVMSG {0} :!version'.format(CHANNEL) in data:
    s.send(bytes('PRIVMSG {0} :i am written in python3 and not yet stable\r\n'.format(CHANNEL), 'utf-8'))

  if 'PRIVMSG {0} :!ping'.format(CHANNEL) in data:
    s.send(bytes('PRIVMSG {0} :pong\r\n'.format(CHANNEL), 'utf-8'))

  if 'PRIVMSG {0} :!forget'.format(CHANNEL) in data:
    s.send(bytes('PRIVMSG {0} :bad word deleted: '.format(CHANNEL), 'utf-8'))
    remword_db(data)

  if 'PRIVMSG {0} :!learn'.format(CHANNEL) in data:
    s.send(bytes('PRIVMSG {0} :new bad word added: '.format(CHANNEL), 'utf-8')) 
    write_db(data)
  
  if 'PRIVMSG {0} :!quit'.format(CHANNEL) in data:
    s.send(bytes(('QUIT : \r\n'), 'utf-8'))
    close_con()
# on some evening on some day someone did some not working blackmagic here
#((i + ' ' in data.split('#game-dev')[1].replace('\r\n', '') or len(data.split('#game-dev')[1].split(i)[1].replace('\r\n', ''))==0) or (' ' + i in data.split('#game-dev')[1]  or len(data.split('#game-dev')[1].split(i)[0].replace('\r\n', '') or ':' + i in data.split('#game-dev')[1])==0)):
#######################
  
  print (data)
