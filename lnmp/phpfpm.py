import subprocess
import os,sys
import time
import file

src = "./src/"
php_package = "php-7.4.30.tar.gz"
php_path = src+'php-7.4.30'
php_PackagePath = src+php_package


def install_php():
    # 安装依赖
    os.popen("mkdir /usr/local/php-fpm7.4")
    subprocess.call("yum -y install libxml2 libxml2-devel  bzip2 bzip2-devel libcurl libcurl-devel libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel gmp gmp-devel libmcrypt libmcrypt-devel readline readline-devel libxslt libxslt-devel gd sqlite sqlite-devel net-snmp net-snmp-devel oniguruma oniguruma-devel"
                    , shell=True)
    oniguruma = subprocess.call("rpm -qa |grep oniguruma*", shell=True)
    if oniguruma == 1:
        subprocess.call("yum -y install http://down.24kplus.com/linux/oniguruma/oniguruma-6.7.0-1.el7.x86_64.rpm",
                        shell=True)
        subprocess.call("yum -y install http://down.24kplus.com/linux/oniguruma/oniguruma-devel-6.7.0-1.el7.x86_64.rpm",
                        shell=True)
    else:
        print("===============准备安装php==========")
        time.sleep(3)

    # 安装php-7.4.30
    if os.path.isfile(php_PackagePath):
        subprocess.run("tar -zxf {} -C {}".format(php_PackagePath, src), shell=True)
        # 编译
        instat = subprocess.run('''cd {} && ./configure --prefix=/usr/local/php-fpm7.4 --with-config-file-path=/usr/local/php-fpm7.4/etc --with-mysqli=mysqlnd --enable-pdo --with-pdo-mysql=mysqlnd --with-iconv-dir=/usr/local/ --enable-fpm --with-fpm-user=www --with-fpm-group=www --with-pcre-regex --with-zlib --with-bz2 --enable-calendar --with-curl --enable-dba --with-libxml-dir --enable-ftp --with-gd --with-jpeg-dir --with-png-dir --with-zlib-dir --with-freetype-dir --enable-gd-jis-conv --with-mhash --enable-mbstring --disable-opcache --enable-pcntl --enable-xml --disable-rpath --enable-shmop --enable-sockets --enable-zip --enable-bcmath --with-snmp --disable-ipv6 --with-gettext --disable-rpath --disable-debug --enable-embedded-mysqli --with-mysql-sock=/usr/local/mysql >> ../../log/php.log'''
                                .format(php_path), shell=True)

        if "0" == str(instat)[-2]:
            # 安装
            subprocess.run("cd {} &&  make && make install >> ../../log/php.log".format(php_path), shell=True)
            # 拷贝ini 等文件
            os.popen("cp ./src/php-7.4.30/php.ini-production /usr/local/php-fpm7.4/etc/php.ini")
            os.popen("cp ./src/php-7.4.30/sapi/fpm/init.d.php-fpm /etc/init.d/php-fpm && chmod +x /etc/init.d/php-fpm")
            os.popen("cp /usr/local/php-fpm7.4/etc/php-fpm.conf.default /usr/local/php-fpm7.4/etc/php-fpm.conf")
            time.sleep(2)

            os.popen("cp /usr/local/php-fpm7.4/etc/php-fpm.d/www.conf.default /usr/local/php-fpm7.4/etc/php-fpm.d/www.conf ")
            print('''\n php已安装完成,请按需修改/usr/local/php-fpm7.4/etc/php-fpm.d/www.conf 文件后
                     通过/etc/init.d/php-fpm start 命令启动''')
        else:
            print("\n 编译失败，请检查原因\n")
    else:
        print("php-7.4.30.tar.gz 不存在，请查看src目录下是否有该文件！")


def wget_php():
    if os.path.isfile("src/php-7.4.30.tar.gz"):
        install_php()
    else:
        # 下载php7.4.30tar包，如果超时60秒终端进程。
        try:
            subprocess.call("wget https://www.php.net/distributions/php-7.4.30.tar.gz -O ./src/php-7.4.30.tar.gz",
                            shell=True, timeout=60)
            install_php()
        except subprocess.TimeoutExpired as e:
            print("cmd:{},timeout:{}".format(e.cmd, e.timeout))
            sys.exit()


if __name__ == '__main__':
    install_php()