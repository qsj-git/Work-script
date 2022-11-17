from subprocess import PIPE,Popen,call
import os
import sys
OLD = "http://192.168.100.107:8082/"
NEW = "http://192.168.100.108:8082/"
USER = 'root'
GROUP = "cloudzone"
addr = "/home/gitlab/data"


def clone():
    print("clone代码")
    with open('gitwa', 'r')as f:
        for line in f:
            proc = Popen('git clone {0}{1}/{2}'.format(OLD, USER, line), shell=True, stdout=PIPE, stdin=PIPE)
            txt = proc.stdout.read()
            res = proc.wait()
            print(txt, res)


def modify():
    print("修改代码地址")
    with open('gitwa', 'r') as f:
        for line in f:
            strs = line.split('.')[0]
            print(strs)
            if os.path.isdir("{0}/{1}".format(addr, strs)):
                os.chdir("{0}/{1}".format(addr, strs))
            else:
                pwd = "{0}/{1}".format(addr, strs)
                call("mkdir {0}".format(pwd), shell=True)
                os.chdir("{0}/{1}".format(addr, strs))
            print(os.getcwd())
            Popen('git init', shell=True)
            proc = Popen('git remote set-url origin {0}{1}/{2}'.format(NEW, USER, line), shell=True, stdout=PIPE, stdin=PIPE)
            if proc.wait() == 0:
                print(proc.stdout.read())
            else:
                print("error")
                sys.exit(1)


def push():
    print("推送代码到远程仓库")
    with open('gitwa', 'r') as f:
        for line in f.readlines():
            strs = line.split('.')[0]
            os.chdir("{0}/{1}".format(addr, strs))
            os.system("git add *")
            os.system("git remote add origin {0}{1}/{2}".format(NEW, USER, strs))
            os.system('git commit -m "Initial commit"')
            os.system('git push -u origin master')


if __name__ == '__main__':
    clone()
    modify()
    push()
