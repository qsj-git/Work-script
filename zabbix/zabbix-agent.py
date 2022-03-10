# -*- coding: utf-8 -*-
import os
import subprocess
import socket


def zabbix_agent():
    # 安装 zabbix-agent 服务
    print("安装 zabbix-agent 服务")
    if os.path.isfile("zabbix-agent-5.0.10-1.el7.x86_64.rpm"):
        subprocess.call('yum -y localinstall zabbix-agent-5.0.10-1.el7.x86_64.rpm', shell=True)
    else:
        print("未找到安装包，请前往 https://repo.zabbix.com/zabbix/5.0/rhel/7/x86_64/ 网站下载")

    # 备份 /etc/zabbix/zabbix_agentd.conf
    print(" 备份 /etc/zabbix/zabbix_agentd.conf")
    os.popen("mv /etc/zabbix/zabbix_agentd.conf /etc/zabbix/zabbix_agentd.conf.bak")
    os.popen("cat /etc/zabbix/zabbix_agentd.conf.bak |egrep -v '^#|^$' >> /etc/zabbix/zabbix_agentd.conf")

    # 获取主机名
    hostname = socket.getfqdn(socket.gethostname())

    # 修改zabbix-agent配置文件，Hostname参数
    with open('/etc/zabbix/zabbix_agentd.conf', 'r', encoding='utf-8') as f:
        conf = f.readlines()
        newconf = []
        print(newconf)
        for i in conf:
            if "Hostname" in i:
                i = "Hostname={}".format(hostname)
                newconf.append(i + '\n')
            elif "Server=" in i:
                i = "Server=10.33.1.25"
                newconf.append(i + '\n')
            elif "ServerActive=" in i:
                i = "ServerActive=10.33.1.25"
                newconf.append(i + '\n')
            else:
                newconf.append(i)

    with open('zabbix_agentd.conf', 'w', encoding='utf-8') as f:
        for i in newconf:
            f.write(i)

    # 移动zabbix_agent.conf 文件到 /etc/zabbix/ 下
    subprocess.call("mv zabbix_agentd.conf /etc/zabbix/", shell=True)

    # 启动zabbix-agent
    print("启动zabbix-agent")
    os.popen("systemctl start zabbix-agent && systemctl enable zabbix-agent")

    # 删除rpm包
    os.popen("rm -rf zabbix-agent-5.0.10-1.el7.x86_64.rpm")


if __name__ == '__main__':
    # 下载zabbix-agent安装包
    subprocess.call('wget http://repo.zabbix.com/zabbix/5.0/rhel/7/x86_64/zabbix-agent-5.0.10-1.el7.x86_64.rpm',
                    shell=True)
    zabbix_agent()
