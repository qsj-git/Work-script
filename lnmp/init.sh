# 设置时区并同步时间
rm -rf /etc/localtime
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

if  ! crontab -l |grep ntpdate 2&>/dev/null ; then
    (echo "* 1 * * * ntpdate ntp1.aliyun.com >/dev/null 2>&1";crontab -l ) |crontab
fi


# 禁用selinux
sed  -i '/SELINUX/{s/permissive/disabled/}' /etc/selinux/config 

# 清空防火墙默认策略
#systemctl stop firewalld
#systemctl stop iptables
#systemctl disabled firewalld
#systemctl disabled iptables

# 历史命令显示操作时间
echo 'export HISTTIMEFORMAT="%F %T `whoami` "'>> /etc/bashrc
source /etc/bashrc
# 禁止root远程登录
#sed -i 's/#permitRootLogin yes /permitRootLogin no/' /etc/ssh/sshd_config
#systemctl restart sshd 

# 禁止定时任务发送邮件
sed -i 's/^MAILTO=root/MAILTO=""/' /etc/crontab

# 设置最大打开文件数
if ! grep "* soft nofile 65535" /etc/security/limits.conf &> /dev/null; then
	cat >> /etc/security/limits.conf << EOF
* soft nofile 65535
* hard nofile 65535
EOF
fi

# 减少Swap使用,注意不是关闭swap
echo "0" > /proc/sys/vm/swappiness

# 系统内核参数优化
cat >> /etc/sysctl.conf << EOF
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_tw_buckets = 20480
net.ipv4.tcp_max_syn_backlog = 20480
net.core.netdev_max_backlog = 262144
net.ipv4.tcp_fin_timeout = 20
EOF


# 配置阿里云yum源 && 安装python3
python ./python3.py

# 安装系统性能分析工具及其他 
yum -y install make vim net-tools iostat itop lrzsz wget ntpdate

# 安装环境所需依赖
yum -y install gcc gcc-c++ libffi-devel bzip2-devel openssl openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel zlib zlib-devel  pcre pcre-devel lua-devel