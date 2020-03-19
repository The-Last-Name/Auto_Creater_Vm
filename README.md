# Auto_Creater_Vm
## 功能描述
帮助您快速创建虚拟机并使用

## 参数帮助
- Vmrun_Path：您的VMware Workstation安装目录下vmrun.exe
- Vm_Template_Path：您的模板主机基础路径
- Vm_Template_HostName：模板主机基础路径下的主机名
- Vm_Template_Snapshot_Name：模板主机的快照名,基于那个快照做克隆
- Vm_Creater_Base_Paht：新创建的主机基础路径
- Vm_Creater_Cluster：新创建主机的集群名
- Vm_Creater_HostName：新创建主机的主机名, "_"号跟数字1开始

## 使用帮助
- 重要说明
    - 此程序仅支持VMware Workstation
    - windows主机需要python2/3环境
    - 您的模板主机Centos需要/root/set.sh脚本
    - 自动设置从xx.xx.xx.10开始
1. 根据上述参数描述更改参数
2. 修改Vm_Create(3)中的参数
3. python Auto_Create_Vm.py


## 版本更新记录及此版本说明
- 0.0.1 
    - 时间：2020.03.19
    - 仅仅将基本逻辑代码书写，用于demo测试
    - 批量克隆克隆
    - 批量修改IP地址
    - 批量关机(init 0)
    - 批量快照
