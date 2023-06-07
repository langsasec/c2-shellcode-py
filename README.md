# c2-shellcode-py
免杀360，火绒的Python-shellcode加载器，可直接生成可执行文件exe

![image](https://github.com/langsasec/c2-shellcode-py/assets/45072131/ada70466-b193-43ee-bfba-1fa15e5b4da2)
## 停更

为保证付费社群利益，本项目停更：https://mp.weixin.qq.com/s?__biz=MzI1ODM1MjUxMQ==&mid=2247493072&idx=1&sn=3e4c49d4e9d09d8ef94d8db96b6ad13d&chksm=ea0bd1c0dd7c58d6a559107f2d113cb8ad97be06bf1e7a4079c91994195a7ebb507d4ec9165d#rd

## 2023 6.4更新
浪飒loader.exe更新，g了及时反馈，不然我咋更新

https://github.com/langsasec/c2-shellcode-py/tree/main/%E6%B5%AA%E9%A3%92loader
## 2023.4.28更新
BypassAV-langsa.py你懂得，注意多了个requirement

## 2023.4.23更新
浪飒loader由于hash死的所以火绒也g了

## 2023.4.6更新

**原`Bypass.py`运行直接生成exe，还可免杀360，无法免杀火绒，火绒3.28病毒库绕过，3.30号病毒库已收录**

**新`BypassAV-浪飒.py`运行直接生成exe，已再次绕过最新火绒，360成功上线，其他杀软状况自测。**



![image-20230406175849221](https://img2023.cnblogs.com/blog/2411575/202304/2411575-20230406180433832-1347029140.png)

![image-20230406180709358](https://img2023.cnblogs.com/blog/2411575/202304/2411575-20230406180710010-930191902.png)

![image-20230406175937624](https://img2023.cnblogs.com/blog/2411575/202304/2411575-20230406180725107-1489772396.png)

## 2023.3.29更新

上传样本过多，导致部分杀毒在打包完毕在长时间后会被记录，请重新运行代码生成及时上线即可

## 2023.3.27更新

没有更改代码，发现**腾讯电脑管家**和**金山毒霸**也可绕过

![image-20230327210233644](https://img2023.cnblogs.com/blog/2411575/202303/2411575-20230327210404487-1102022697.png)

![image-20230327210540922](https://img2023.cnblogs.com/blog/2411575/202303/2411575-20230327210539969-230609198.png)



## 使用

CS4.7生成python类型shellcode

![image-20230323173046659](https://img2023.cnblogs.com/blog/2411575/202303/2411575-20230323173046883-891160038.png)

保存为payload.py与Bypass.py/BypassAV-浪飒放在一个目录下

![image-20230323174256475](https://img2023.cnblogs.com/blog/2411575/202303/2411575-20230323174256651-1588728063.png)

等待运行完毕，在dist目录下会生成exe。

![image-20230323174911474](https://img2023.cnblogs.com/blog/2411575/202303/2411575-20230323174917591-116118579.png)

上传目标机器运行直接上线

![image-20230323172532350](https://img2023.cnblogs.com/blog/2411575/202303/2411575-20230323172532786-689062764.png)

## 某60

![image-20230323175059233](https://img2023.cnblogs.com/blog/2411575/202303/2411575-20230323175059639-1587542681.png)

## 某绒

![image-20230323175351079](https://img2023.cnblogs.com/blog/2411575/202303/2411575-20230323175351380-242584426.png)
