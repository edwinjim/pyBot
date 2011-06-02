import os, sys, socket, string, ConfigParser 
from subprocess import Popen, PIPE
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

build_conserver()
#daemonize()


while 1:
  data = s.recv(500)

  if 'PING ' in data:
    s.send('PONG ')

  if 'PRIVMSG {0} :!ping'.format(CHANNEL) in data:
    s.send('PRIVMSG {0} :pong\r\n'.format(CHANNEL))

  if 'PRIVMSG {0} :!loadinfo'.format(CHANNEL) in data:
    uptime = Popen("uptime", shell=False, stdout=PIPE).stdout.readline()
    up = "".join(uptime.split(",")[:2]).split("up")[1]+"".join(uptime.split(",")[3:])
    s.send(('PRIVMSG {0} :' + str(up) + '\r\n').format(CHANNEL))
  else: 
	up = ""

  if 'PRIVMSG {0} :!netinfo'.format(CHANNEL) in data:
    netgrep = Popen("ifconfig wlan0 | grep RX | grep bytes", shell=False, stdout=PIPE).stdout.readline()
    net = "".join(netgrep.split("RX")[1])
    s.send(('PRIVMSG {0} :' + str(net) + '\r\n').format(CHANNEL))
  else:
   net = ""

  #if 'PRIVMSG {0} :!netinfo'.format(CHANNEL) in data:
  

  if 'PRIVMSG {0} :!quit'.format(CHANNEL) in data:
    s.send('QUIT : \r\n' ) 
    close_con()

  print (data)
