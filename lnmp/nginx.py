import subprocess
import os,sys
import time

src = "./src/"
nginxpath = "/usr/local/nginx"


def install_nginx():
    subprocess.run("cd {} && tar -zxf nginx-1.16.1.tar.gz".format(src), shell=True)
    ng_config = subprocess.call(
        '''cd {}nginx-1.16.1 && ./configure --prefix={} --user=www --group=www --with-ld-opt=-Wl,-rpath,/usr/local/luajit/lib --without-http_memcached_module --with-http_stub_status_module --with-http_ssl_module --with-http_gzip_static_module --with-http_realip_module --with-stream --with-http_v2_module >> ../../log/nginx.log'''.format(src, nginxpath),
        shell=True)
    if ng_config == 0:
        print('=========== 开始编译安装 =============')
        make = subprocess.call("cd {}nginx-1.16.1 && make && make install >> ../../log/nginx.log ".format(src),
                              shell=True)
        print("make is {}\n".format(make))
        if make == 0:
            os.popen("ln -s {}/sbin/nginx /usr/bin/nginx".format(nginxpath))
            os.popen("useradd www")
            os.popen("\cp config/nginx.conf  /usr/local/nginx/conf/")
            subprocess.call("nginx -v ", shell=True)
            print("\n nginx 安装完成！在 /usr/local/nginx 下,请按需修改nginx配置文件。\n启动方式：nginx")
        else:
            print("安装失败，请看 log/nginx.log")
            sys.exit()
    else:
        print("编译失败，请看 log/nginx.log")
        time.sleep(1)
        sys.exit()


def nginx():
    ng_pwd = "./nginx_module/"
    # 安装依赖
    runstat = subprocess.run(
        "yum install -y gcc gcc-c++ pcre pcre-devel zlib zlib-devel openssl openssl-devel lua-devel",
        shell=True)
    if "1" is str(runstat)[-2]:
        print("依赖环境安装失败，请检查yum环境！")
        sys.exit()
    print("=======================开始安装nginx====================")
    time.sleep(1)
    subprocess.run("mkdir log", shell=True)
    subprocess.run("mkdir {}".format(nginxpath), shell=True)
    lua_mould = os.path.exists("{}lua-nginx-module-master".format(ng_pwd))
    nginx_http = os.path.exists("{}nginx-http-concat".format(ng_pwd))
    ngx_devel = os.path.exists("{}ngx_devel_kit-master".format(ng_pwd))
    if lua_mould and nginx_http and ngx_devel:
        os.popen("cp -r ./nginx_module/* /usr/local/src/")
    else:
        print("请查看lua-nginx-module-master，nginx-http-concat，ngx_devel_kit-master文件是否存在")
        sys.exit()

    # 开始安装 nginx
    if os.path.isfile("{}nginx-1.16.1.tar.gz".format(src)):
        install_nginx()
    else:
        print("nginx-1.16.1.tar.gz不存在")
        # 如果文件不存在，则下载
        subprocess.call("wget https://nginx.org/download/nginx-1.16.1.tar.gz -P src/", shell=True)
        install_nginx()
