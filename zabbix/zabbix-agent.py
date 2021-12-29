import os.path
import subprocess
import socket, os


def zabbix_agent():
    # 安装zabbix-agent
    if os.path.isfile('zabbix-agent-5.0.10-1.el7.x86_64.rpm'):
        subprocess.call('yum -y localinstall zabbix-agent-5.0.10-1.el7.x86_64.rpm', shell=True)
        # 获取主机名
        hostname = socket.getfqdn(socket.gethostname())
        # 备份原先zabbix_agentd.conf文件
        subprocess.run('cp /etc/zabbix/zabbix_agentd.conf /etc/zabbix/zabbix_agentd.conf.bak', shell=True)
        # 修改zabbix_agentd.conf 中，hostname信息
        subprocess.run('sed -i "s/^Hostname.*$/Hostname={}/g" /etc/zabbix/zabbix_agentd.conf'.format(hostname),
                       shell=True)
        subprocess.run('sed -i "s/^Server=.*$/Server=127.0.0.1/g" /etc/zabbix/zabbix_agentd.conf', shell=True)
        subprocess.run('sed -i "s/^ServerActive=.*$/ServerActive=127.0.0.1/g" /etc/zabbix/zabbix_agentd.conf',
                       shell=True)
        # 启动zabbix-agent
        subprocess.run('systemctl start zabbix-agent', shell=True)
        subprocess.run('systemctl enable zabbix-agent', shell=True)
        subprocess.run('rm -rf zabbix-agent-5.0.10-1.el7.x86_64.rpm', shell=True)

    else:
        print("未找到zabbix-agent，安装包，请检查")


if __name__ == '__main__':
    # 下载zabbix-agent rpm包
    subprocess.call('wget http://repo.zabbix.com/zabbix/5.0/rhel/7/x86_64/zabbix-agent-5.0.10-1.el7.x86_64.rpm',
                    shell=True)
    zabbix_agent()
