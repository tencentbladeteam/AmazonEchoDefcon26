#! /usr/bin/python
# a simple tcp server
import socket,os,time

count = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.bind(('10.0.0.231', 9999))  
sock.listen(5)  
print "Waiting for Echo device to connect @ %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
while True:  
    connection,address = sock.accept()  
    count += 1
    print "[%s] : Echo device is succeessfully connected! \r\n Device Address = %s, Attack Success Count = %d\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), address, count)           
    connection.close()

sock.close()
