import sys
import socket
import string

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
s.send ('PRIVMSG %s :hello human life forms\r\n' % CHANNEL)

while 1:                                                                             
  data = s.recv (4096)
  if data.find ('PING') != -1:
    s.send ('PONG')
  print data
