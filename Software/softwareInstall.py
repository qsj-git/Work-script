# -*- coding: UTF-8 -*-
import subprocess
import os,time,sys


def python3():
    install = subprocess.call('''yum -y install libffi-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel zlib zlib-devel gcc make wget''', shell=True)
    subprocess.call('mkdir /usr/local/python3.7', shell=True)

    if 1 == install:
        print("依赖环境安装失败，请检查yum环境")
        sys.exit()

    print("=="*15+"下载安装包"+"=="*15)
    subprocess.call(" wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tgz", shell=True)
    if not os.path.exists("Python-3.7.1.tgz"):
        print("Python包不存在，请检查是否下载成功")
        sys.exit()

    print("==" * 15 + "开始安装" + "==" * 15)
    subprocess.call("tar zxf Python-3.7.1.tgz", shell=True)
    status = subprocess.call("cd Python-3.7.1 &&  ./configure --prefix=/usr/local/python3.7 && make && make install",
                    shell=True)
    if status == 0:
        subprocess.call("ln -s /usr/local/python3.7/bin/python3 /usr/bin/python3", shell=True)
        subprocess.call("ln -s /usr/local/python3.7/bin/pip3 /usr/bin/pip3", shell=True)
    else:
        print('编译安装失败，请检查！')


def php72():
    subprocess.run('''yum -y install gcc gcc-c++  make mysql-devel zlib zlib-devel pcre pcre-devel  libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel libxml2 libxml2-devel glibc glibc-devel glib2 glib2-devel bzip2 bzip2-devel ncurses ncurses-devel curl curl-devel e2fsprogs e2fsprogs-devel krb5 krb5-devel openssl openssl-devel openldap openldap-devel nss_ldap openldap-clients openldap-servers ''', shell=True)
    subprocess.call('yum -y install autoconf ', shell=True)
    os.popen("mkdir /usr/local/php72")

    if os.path.isfile("php-7.2.0.tar.gz"):
        subprocess.run("tar -zxf php-7.2.0.tar.gz", shell=True)
        instat = subprocess.run('''cd php-7.2.0 && ./configure --prefix=/usr/local/php72 --with-config-file-path=/usr/local/php72 --enable-mbstring --with-openssl --enable-ftp --with-gd --with-jpeg-dir=/usr --with-png-dir=/usr --with-mysql=mysqlnd --with-mysqli=mysqlnd --with-pdo-mysql=mysqlnd --with-pear --enable-sockets --with-freetype-dir=/usr --with-zlib --with-libxml-dir=/usr --with-xmlrpc --enable-zip --enable-fpm --enable-xml --enable-sockets --with-gd --with-zlib --with-iconv --enable-zip --with-freetype-dir=/usr/lib/ --enable-soap --enable-pcntl --enable-cli --with-curl''', shell=True)

        if "0" == str(instat)[-2]:
            subprocess.run("cd php-7.2.0 &&  make && make install", shell=True)
            os.popen("cp php-7.2.0/php.ini-production /usr/local/php72/php.ini")
            os.popen("cp php-7.2.0/sapi/fpm/init.d.php-fpm /etc/init.d/php-fpm && chmod +x /etc/init.d/php-fpm")
            os.popen("cp /usr/local/php72/etc/php-fpm.conf.default /usr/local/php72/etc/php-fpm.conf")
            newfile1 = []
            print("\n修改php-fpm.conf配置文件")
            time.sleep(2)

            with open("/usr/local/php72/etc/php-fpm.conf", 'r', encoding="utf-8") as file1:
                phpid = "pid = run/php-fpm.pid"
                phpinclude = "include=/usr/local/php72/etc/php-fpm.d/*.conf"
                file1_content = file1.readlines()
                for i in file1_content:
                    if phpid in i:
                        newfile1.append(phpid)
                    elif "include=" in i:
                        newfile1.append(phpinclude)
                    else:
                        newfile1.append(i)
            with open("/usr/local/php72/etc/php-fpm.conf", 'w', encoding="utf-8") as file2:
                for content in newfile1:
                    file2.write(content)

            os.popen("cp /usr/local/php72/etc/php-fpm.d/www.conf.default /usr/local/php72/etc/php-fpm.d/www.conf ")
            print('''\n php已安装完成,请按需修改/usr/local/php72/etc/php-fpm.d/www.conf 文件后
                     通过/etc/init.d/php-fpm start 命令启动''')
        else:
            print("\n 编译失败，请检查原因\n")


def phpredis():
    print("准备安装 redis 扩展模块")
    time.sleep(3)
    if os.path.isfile('redis-4.0.2.tgz'):
        subprocess.call("tar -zxf redis-4.0.2.tgz", shell=True)
        subprocess.call("cd redis-4.0.2 && /usr/local/php72/bin/phpize ", shell=True)
        subprocess.call("cd redis-4.0.2 && ./configure --with-php-config=/usr/local/php72/bin/php-config", shell=True)
        subprocess.call("cd redis-4.0.2 && make && make install", shell=True)

        # 修改php.ini 配置文件
        with open('/usr/local/php72/php.ini', 'a', encoding='utf-8') as file:
            file.write('extension_dir="/usr/local/php72/lib/php/extensions/no-debug-non-zts-20170718"'+'\n'+'extension=redis.so'+'\n')

        os.popen("/etc/init.d/php-fpm restart")
    else:
        print("请确认该模块下是否存在redis-4.0.2.tgz 包！")


def nginx():
    runstat = subprocess.run(
        "yum install -y gcc gcc-c++ pcre pcre-devel zlib zlib-devel openssl openssl-devel lua-devel wget ",
        shell=True)
    if "1" is str(runstat)[-2]:
        print("依赖环境安装失败，请检查yum环境！")
        sys.exit()
    print("开始安装nginx")
    subprocess.run("mkdir /usr/local/nginx", shell=True)
    if os.path.isdir("lua-nginx-module-master") and os.path.isdir("nginx-http-concat") and os.path.isdir("ngx_devel_kit-master"):
        os.popen("mv lua-nginx-module-master nginx-http-concat ngx_devel_kit-master /usr/local/src/")

    if os.path.isfile("nginx-1.16.1.tar.gz"):
        subprocess.run("tar -zxf nginx-1.16.1.tar.gz", shell=True)
        subprocess.run(
            '''cd nginx-1.16.1 && ./configure --prefix=/usr/local/nginx --user=www --group=www --with-ld-opt=-Wl,-rpath,/usr/local/luajit/lib --add-module=/usr/local/src/ngx_devel_kit-master --add-module=/usr/local/src/lua-nginx-module-master --add-module=/usr/local/src/nginx-http-concat --without-http_memcached_module --with-http_stub_status_module --with-http_ssl_module --with-http_gzip_static_module --with-http_realip_module --with-stream --with-http_v2_module''',
            shell=True)

        install = subprocess.run("cd nginx-1.16.1 && make && make install", shell=True)
        if "0" is str(install)[-2]:
            os.popen("useradd www")
            print("\n nginx 安装完成！在 /usr/local/nginx 下,请按需修改nginx配置文件，"
                  "启动方式：/usr/local/nginx/sbin/nginx")
        else:
            sys.exit()


def redis():
    if os.path.isfile('redis-5.0.13.tar.gz'):
        os.system("yum -y install make gcc*")
        os.system('tar -xzf redis-5.0.13.tar.gz && mv redis-5.0.13 /usr/local/redis5')
        redis = subprocess.run('cd /usr/local/redis5 && make && make install', shell=True)
        if str(redis)[-2] == '0':
            print('''\nredis 安装成功，请前往 /usr/local/redis5 下修改 redis.conf 配置文件。
                     启动方式：redis-server /usr/local/redis5/redis.conf。
                     连接redis：redis-cli''')
        else:
            print("redis 安装失败，请查看")
    else:
        print("请检查该目录下是否有redis-5.0.13.tar.gz 安装包")


if __name__ == '__main__':
    software = input("请选择要安装的软件(python3(1)/php72(2)/nginx(3)/redis(4)/phpredis(5)):")
    if software == "2":
        php72()
        module = input("需要安装模块吗(yes/No):")
        if module == "yes":
            phpredis()
        else:
            sys.exit()
    elif software == "3":
        nginx()
    elif software == "4":
        redis()
    elif software == "1":
        python3()
    elif software == "5":
        phpredis()
    else:
        print("请选择括号内的软件！")
