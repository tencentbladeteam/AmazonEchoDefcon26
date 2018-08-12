#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pwnlib

# libc_base = 0xf76cd000
# libcrypto_base = 0xf750c000

libc_base = 0
libcrypto_base = 0

class GenGadgets(object):
    def __init__(self, libc_base, libcrypto_base):
        self.libc_base = libc_base
        self.libcrypto_base = libcrypto_base


    def find_symbol(self, elf, symbol_name):
        return elf.symbols[symbol_name]

    def find_arm_gadget(self, elf, gadget, validate = False):
        gadget_bytes = pwnlib.asm.asm(gadget, arch='arm')
        gadget_address = None
        for address in elf.search(gadget_bytes):
            if address % 4 == 0:
                gadget_address = address
                if validate:
                    if gadget_bytes == elf.read(gadget_address, len(gadget_bytes)):
                        print pwnlib.asm.disasm(gadget_bytes, vma=gadget_address, arch='arm')

                    break

        return gadget_address

    def find_thumb_gadget(self, elf, gadget, validate = False):
        gadget_bytes = pwnlib.asm.asm(gadget, arch='thumb')
        gadget_address = None
        for address in elf.search(gadget_bytes):
            if address % 2 == 0:
                gadget_address = address + 1
                if validate:
                    if gadget_bytes == elf.read(gadget_address - 1, len(gadget_bytes)):
                        print pwnlib.asm.disasm(gadget_bytes, vma=gadget_address-1, arch='thumb')

                    break

        return gadget_address

    def find_gadget(self, elf, gadget):
        gadget_address = self.find_thumb_gadget(elf, gadget, True)
        if gadget_address is not None:
            return gadget_address

        return self.find_arm_gadget(elf, gadget, True)

    def find_libc_rop_gadgets(self, path):
        elf = pwnlib.elf.ELF(path)
        elf.address = self.libc_base

        mprotect = elf.symbols['mprotect']
        print '[*] mprotect : 0x{:08x}'.format(mprotect)

        mprotect = elf.symbols['signal']
        print '[*] signal : 0x{:08x}'.format(mprotect)

        pop_r4_lr_bx_lr_asm = 'pop {r4, lr}\n'
        pop_r4_lr_bx_lr_asm += 'bx lr'
        pop_r4_lr_bx_lr = self.find_gadget(elf, pop_r4_lr_bx_lr_asm)
        print '[*] pop_r4_lr_bx_lr : 0x{:08x}\n'.format(pop_r4_lr_bx_lr)
        
        pop_pc_asm = 'pop {pc}'
        pop_pc = self.find_gadget(elf, pop_pc_asm)
        print '[*] pop_pc : 0x{:08x}\n'.format(pop_pc)

        pop_r0_r1_r2_pc_asm = 'pop {r0, r1, r2, pc}'
        pop_r0_r1_r2_pc = self.find_gadget(elf, pop_r0_r1_r2_pc_asm)
        print '[*] pop_r0_r1_r2_pc : 0x{:08x}\n'.format(pop_r0_r1_r2_pc)

    def find_pivot_gadgets(self, path):
        elf = pwnlib.elf.ELF(path)
        elf.address = self.libcrypto_base
        pivot_asm = 'ldm r0, {r1, r7, ip, sp, pc}'
        pivot = self.find_arm_gadget(elf, pivot_asm, True)
        print '[*] pivot : 0x{:08x}\n'.format(pivot)


if __name__ == '__main__':
    gadgets = GenGadgets(libc_base, libcrypto_base)
    gadgets.find_pivot_gadgets('libcrypto.so')
    gadgets.find_libc_rop_gadgets('libc.so')



