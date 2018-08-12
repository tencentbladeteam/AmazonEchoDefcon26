#! /usr/bin/python
# a simple tcp server
import socket,os,time

count = 0

FINSH_FILE = 'finish.txt'

if os.path.exists(FINSH_FILE):
    print 'start rm finish.txt ...'
    os.system('rm finish.txt')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.bind(('10.0.0.141', 9999))  
sock.listen(5)  
print "Begin Time: %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
while True:  
    connection,address = sock.accept()
    count += 1
    print "[%s] : address = %s, count = %d\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), address, count)           
    pcm_path = 'record_%s_%d.pcm' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), count)
    print "record write to %s" % (pcm_path)
    with open(FINSH_FILE, 'w') as fd:
        fd.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) 

    f = open(pcm_path, 'w')
    while True:
        data = connection.recv(1024)
        if not data:
            print "client close" 
            break
        else:
            #print data
            f.write(data) 
            f.flush()

sock.close()
