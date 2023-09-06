# rateCrawling
爬取匯率串接華苓BPMS系統
參考網址：https://gist.github.com/Phate334/6128165184b20ba5d3525e7769e59990 

https://malagege.github.io/blog/posts/Python-3-7-%E5%AE%89%E8%A3%9D%E7%AD%86%E8%A8%98/ 

[root@bpmstest]# cd /usr/src 

[root@bpmstest src]# yum -y install zlib-devel gcc make wget openssl-devel libffi-devel 

[root@bpmstest src]# wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz 
(不知為啥裝3.7.0無法成功，所以先改用3.6.8) 

[root@bpmstest src]# wget https://bootstrap.pypa.io/get-pip.py 

(他會跑跑跑跑 最後會有一行 Saving to: 'get-pip.py') 

[root@bpmstest src]# tar xzf Python-3.6.8.tgz 
[root@bpmstest src]# cd Python-3.6.8 
[root@bpmstest Python-3.6.8]# ./configure --enable-optimizations 

如果紅字部分不用這段，會卡在下一句 
[root@bpmstest Python-3.6.8]# make altinstall 

[root@bpmstest Python-3.6.8]# cd /usr/bin/ 

[root@bpmstest bin]# ln -s /usr/src/Python-3.6.8/python python3 
[root@bpmstest bin]# python3 -V 

Python 3.6.8 

確認版本 

[root@bpmstest src]# python3 get-pip.py 
