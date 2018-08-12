#!/bin/env python
"""
A simple example of using Python sockets for a client HTTPS connection.
"""
import time
import ssl
import socket
import os
#host1 = '192.168.43.86';
#host1 = '10.0.0.173'
# change ip 

host1 = '10.0.0.173'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host1, 55443))
s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

#ASCII for 0 is 0x30
# change ip
hexurl = "http://10.0.0.231/test.pls".encode("hex")

hexid  = "0".encode("hex")
hexid2  = "1".encode("hex")

hexcookie = "0".encode("hex")
hexclientid = "0123".encode("hex")
behavior = "wtf"
# change ip
s.sendall("POST /control?cmd=downloadAudio&xmitTimeStamp=152535000&url=" +
  hexurl +
  "&id=" +
  hexid  +
  "&offsetInMilliseconds=1&cookie=" +
  hexcookie + "&AESIV=" + 
  '30'*32   + "&AESkey=" + 
  '30'*32   + "&clientId=" +
  hexclientid + "&playBehavior=" +
  behavior + " HTTP/1.1\r\nHost: 10.0.0.173\r\nConnection: close\r\n\r\n")

while True:

    new = s.recv(4096)
    if not new:
      s.close()
      break
    print new

#os.system("python msocket2.py")

quit()
