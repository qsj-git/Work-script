import mysql
import nginx
import phpfpm

if __name__ == '__main__':
    software = int(input('''
    1.nginx
    2.php-fpm
    3.mysql
    4.docker
    5.lnmp(default) 
    请输入要安装的软件 :'''))

    if software == 1:
        nginx.nginx()
    elif software == 2:
        phpfpm.wget_php()
    elif software == 3:
        pass
    else:
        print("请输入对应的数字！")
