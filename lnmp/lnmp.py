import subprocess
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
        password = input('请输入mysql密码：')
        mysql.install_mysql()
        # 判断mysql状态
        mysql_status = subprocess.call('netstat -atnlp|grep mysql > /dev/null', shell=True)
        if mysql_status == 0:
            mysql.operation_mysql(password)
            subprocess.call('/etc/init.d/mysql status', shell=True)
        else:
            print('mysql 启动失败，请检查原因！')
    else:
        print("请输入对应的数字！")
