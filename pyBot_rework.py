#
# this will be a system information bot... somewhen
#

import os, sys, socket, string, ConfigParser, commands
from signal import SIGTERM

## open file and get information from there
config = ConfigParser.ConfigParser()
config.read("config.ini")

HOST = config.get("connect", "server")
PORT = config.get("connect", "port")
CHANNEL = config.get("connect", "channel")
NICK = config.get("connect", "nick")

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

  s.send('NICK {0}\r\n'.format(NICK))
  s.send('USER %s %s pyBot :%s\r\n' % (IDENT, HOST, REALNAME))
  s.send('JOIN {0}\r\n'.format(CHANNEL))
  s.send('MODE {0}\r\n'.format(MODE))

def daemonize():
  try:
    pid = os.fork() 
    if pid > 0:
      sys.exit(0) 
  except OSError as err:                                               
    sys.stderr.write('fork #1 failed: {0}\n'.format(err))
    sys.exit(1)

  os.setsid()
  os.umask(0)

  try:
    pid = os.fork()
    if pid > 0:
      sys.exit(0)
  except OSError as err :
    sys.stderr.write('fork #2 failed: {0}\n'.format(err))
    sys.exit(1)

  for fd in (0, 1, 2):
    try:
      os.close(fd)
    except OSError:
      pass

def close_con():
  s.close()
  pf = os.getpid()
  os.kill(pf, SIGTERM)
  sys.exit()

up = commands.getstatusoutput('uptime')

build_conserver()
#daemonize()


while 1:
  data = s.recv(500)

  if 'PING ' in data:
    s.send('PONG ')

  if 'PRIVMSG {0} :!ping'.format(CHANNEL) in data:
    s.send('PRIVMSG {0} :pong\r\n'.format(CHANNEL))

  if 'PRIVMSG {0} :!sysinfo'.format(CHANNEL) in data:
    s.send(('PRIVMSG {0} :' + str(up) + '\r\n').format(CHANNEL))
    up = ""

  if 'PRIVMSG {0} :!quit'.format(CHANNEL) in data:
    s.send('QUIT : \r\n' ) 
    close_con()

  print (data)