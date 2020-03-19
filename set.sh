#!/bin/bash
# BY: The Last Name
# Time: 2020.03.19
# System: Centos

if [[ $# -eq 0 ]];then
  echo "usage: `basename $0` num"
  exit 1
fi
[[ $1 =~ ^[0-9]+$ ]]
if [[ $? -ne 0 ]];then
  echo "usage: `basename $0` 210~240"
  exit 1
fi

cat > /etc/sysconfig/network-scripts/ifcfg-ens33 << EOF
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens33
DEVICE=ens33
ONBOOT=yes
IPADDR=192.168.26.${1}
NETMASK=255.255.255.0
GATEWAY=192.168.26.2
DNS1=180.76.76.76
DNS2=223.5.5.5
EOF

systemctl restart network &> /dev/null
hostnamectl set-hostname vms${1}.k8s.wnag