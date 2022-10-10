import subprocess
import os
import sys
import pymysql
import file

src = "./src/"
cnf = '/etc/my.cnf'
mysql_package = 'mysql-5.7.39-linux-glibc2.12-x86_64.tar.gz'
mysql_package_path = src+mysql_package
mysql_path = '/usr/local/mysql5.7/'
mysqld = '/usr/local/mysql5.7/bin/mysqld'
mysql_datapath = '/usr/local/mysql5.7/data/'
mysql_logpath = '/usr/local/mysql5.7/logs'


def install_mysql():
    # 判断mysql用户是否存在，若不存在则创建
    isuser = subprocess.call("grep mysql /etc/passwd", shell=True)
    if isuser == 0:
        print("mysql 用户已存在！")
    else:
        os.system("groupadd mysql && useradd mysql -g mysql")
    # 判断mysql压缩包是否存在，并解压
    if os.path.isfile(mysql_package_path):
        subprocess.call('tar -xf {} -C src/'.format(mysql_package_path), shell=True)
        subprocess.call('mv ./src/mysql-5.7.39-linux-glibc2.12-x86_64 /usr/local/mysql5.7', shell=True)
    else:
        subprocess.call('wget https://cdn.mysql.com//Downloads/MySQL-5.7/{} -P {}'.format(mysql_package, src),
                        shell=True)
        subprocess.call('cd ./src && tar -xf {} '.format(mysql_package_path), shell=True)
        subprocess.call('mv ./src/mysql-5.7.39-linux-glibc2.12-x86_64 /usr/local/mysql5.7', shell=True)
    # 安装mysql,及mysql 初始化
    if os.path.exists('/usr/local/mysql5.7'):
        os.system('mkdir {} && chown -R mysql.mysql {}'.format(mysql_datapath, mysql_datapath))
        os.system('mkdir {} && chown -R mysql.mysql {}'.format(mysql_logpath, mysql_logpath))
        subprocess.call('cp ./config/my.cnf {}'.format(cnf), shell=True)
        subprocess.call('{} --defaults-file={} --basedir=/usr/local/mysql5.7/ --datadir={} --user=mysql --initialize'
                        .format(mysqld, cnf, mysql_datapath), shell=True)
        # 设置mysql 启动脚本
        subprocess.call('cp /usr/local/mysql5.7/support-files/mysql.server /etc/init.d/mysql', shell=True)
        file.exact_match('/etc/init.d/mysql', 'basedir=', 'basedir=/usr/local/mysql5.7')
        file.exact_match('/etc/init.d/mysql', 'datadir=', 'datadir=/usr/local/mysql5.7/data')
        subprocess.call('chmod +x /etc/init.d/mysql', shell=True)
        subprocess.call('ln -s /usr/local/mysql5.7/bin/mysql /usr/sbin/', shell=True)
        # 设置开机自启动
        subprocess.call('cp ./config/mysql.service /etc/systemd/system/', shell=True)
        subprocess.call('systemctl daemon-reload', shell=True)
        subprocess.call('systemctl enable mysql', shell=True)
        subprocess.call('systemctl start mysql', shell=True)
    else:
        print("mysql未安装，请检查mysql是否安装在/usr/local/下")
        sys.exit()


def operation_mysql(passwd):
    try:
        old_password = "123145"
        db = pymysql.connect(host='localhost', user='root', password=old_password, port=3306)
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # 使用 execute()  方法执行 SQL,设置密码
        cursor.execute("flush privileges")
        cursor.execute("set password for 'root'@'localhost' = password("+"'"+passwd+"')")
        # 关闭mysql连接
        db.close()
        subprocess.call('systemctl stop mysql', shell=True)
        file.exact_match('/etc/my.cnf', 'skip-grant-tables', '#skip-grant-tables')
        os.system('systemctl start mysql')
    except Exception as e:
        print('连接失败，请检查！错误信息{}'.format(e))
        sys.exit()


def uninstall_mysql():
    subprocess.call('/etc/init.d/mysql stop', shell=True)
    os.system('rm -rf /etc/init.d/mysql /usr/local/mysql5.7 /etc/my.cnf ')
    os.system('rm -rf /usr/sbin/mysql')


if __name__ == '__main__':
    password = input('请输入mysql密码：')
    install_mysql()
    # 判断mysql状态
    mysql_status = subprocess.call('netstat -atnlp|grep mysql > /dev/null', shell=True)
    if mysql_status == 0:
        operation_mysql(password)
        subprocess.call('/etc/init.d/mysql status', shell=True)
    else:
        print('mysql 启动失败，请检查原因！')
