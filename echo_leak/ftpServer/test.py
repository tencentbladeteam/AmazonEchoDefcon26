import struct
from pwn import *

s = 'd1f220f7'
def conver_to_address(s):
    data = s.decode('hex')
    address = u32(data)
    return address

if __name__ == '__main__':
    conver_to_address(s)