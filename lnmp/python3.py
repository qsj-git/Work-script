# -*- coding: UTF-8 -*-
import subprocess
import os, sys
import platform
import re,time


'''初始化环境，配置阿里云yum源'''
def configure_yum ():

    subprocess.call('mkdir /etc/yum.repos.d/bak', shell=True)
    subprocess.call('mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/bak/', shell=True)
    version_num = re.split('el|\.', platform.release())

    if version_num[4] == '7':
        subprocess.call('curl -o /etc/yum.repos.d/Centos7.repo http://mirrors.aliyun.com/repo/Centos-7.repo',
                        shell=True)
    elif version_num[4] == '6':
        subprocess.call('curl -o /etc/yum.repos.d/Centos6.repo https://mirrors.aliyun.com/repo/Centos-vault-6.10.repo',
                        shell=True)

    if os.path.isfile("/etc/yum.repos.d/Centos7.repo") :
        subprocess.call('yum clean all && yum makecache', shell=True)
        print("yum源已安装！")
        time.sleep(3)


'''安装python 3 '''
def python3():
    install = subprocess.call('''yum -y install libffi-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel zlib zlib-devel gcc make wget''', shell=True)
    subprocess.call('mkdir /usr/local/python3.7', shell=True)

    if 1 == install:
        print("依赖环境安装失败，请检查yum环境")
        sys.exit()

    print("=="*15+"下载安装包"+"=="*15)
    subprocess.call(" wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tgz -O ./src/Python-3.7.1.tgz",
                    shell=True)
    if not os.path.exists("./src/Python-3.7.1.tgz"):
        print("Python包不存在，请检查是否下载成功")
        sys.exit()

    print("==" * 15 + "开始安装" + "==" * 15)
    subprocess.call("tar zxf src/Python-3.7.1.tgz -C src/", shell=True)
    if os.path.isdir('./src/Python-3.7.1'):
        subprocess.call("cd ./src/Python-3.7.1 &&  ./configure --prefix=/usr/local/python3.7 ", shell=True)
        status = subprocess.call("cd ./src/Python-3.7.1 && make && make install", shell=True)
        if status == 0:
            subprocess.call("ln -s /usr/local/python3.7/bin/python3 /usr/bin/python3", shell=True)
            subprocess.call("ln -s /usr/local/python3.7/bin/pip3 /usr/bin/pip3", shell=True)
            print('\n=========== python3 安装完成！============')
            time.sleep(2)
        else:
            print('编译安装失败，请检查！')
    else:
        print("目录不存在！请检查")
        sys.exit()


if __name__ == '__main__':
    configure_yum()
    python3()
