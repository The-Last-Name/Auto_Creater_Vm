#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# BY: The Last Name
# Time: 2020.3.19
# System: Windows
# Python version: 3


import os,time

Vmrun_Path=r"D:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"
Vm_Template_Path=r"F:\Virtual Machines\模板机"
Vm_Template_HostName="CentOS_7"
Vm_Template_Snapshot_Name="快照 2"
Vm_Creater_Base_Paht="F:\Virtual Machines"
Vm_Creater_Cluster="test"
Vm_Creater_HostName="test"

def Vm_Create(Vm_Creater_Sum=1):
    Full_Vm_Template_Path=os.path.join(Vm_Template_Path, Vm_Template_HostName, Vm_Template_HostName + ".vmx")
    for index in range(Vm_Creater_Sum):
        Full_Vm_Creater_Path = os.path.join(Vm_Creater_Base_Paht, Vm_Creater_Cluster, Vm_Creater_HostName + "_" + str(index + 1) ,Vm_Creater_HostName + "_" + str(index + 1) + ".vmx")
        Vm_Create_Cmd='"' + Vmrun_Path + '" -T ws clone "' + Full_Vm_Template_Path + '" "' + Full_Vm_Creater_Path + '" full -snapshot="' + Vm_Template_Snapshot_Name + '" -cloneName="' + Vm_Creater_HostName + "_" + str(index + 1) + '"'
        print("Debug:开始克隆-",index)
        os.popen(Vm_Create_Cmd)
        # 这个等待是保证虚拟机被复制结束被开机,硬盘速度决定时间大小
        time.sleep(7)
        print("Debug:开始启动-",index)
        Vm_Satrt_Cmd='"' + Vmrun_Path + '" -T ws start "' + Full_Vm_Creater_Path + '"'
        os.popen(Vm_Satrt_Cmd)

    # 等待所有主机被开机
    time.sleep(60)
    for index in range(Vm_Creater_Sum):
        Full_Vm_Creater_Path = os.path.join(Vm_Creater_Base_Paht, Vm_Creater_Cluster,Vm_Creater_HostName + "_" + str(index + 1),Vm_Creater_HostName + "_" + str(index + 1) + ".vmx")
        Vm_Host_Set_Ip_Cmd='"' + Vmrun_Path + '" -T ws -gu root -gp djlyly runProgramInGuest "' + Full_Vm_Creater_Path + '" /root/set.sh '+ str(10 + index)
        print("Debug:开始设置IP-", index)
        os.popen(Vm_Host_Set_Ip_Cmd)
        time.sleep(2)
        Vm_Host_Close_Cmd = '"' + Vmrun_Path + '" -T ws -gu root -gp djlyly runProgramInGuest "' + Full_Vm_Creater_Path + '" /sbin/init 0'
        os.popen(Vm_Host_Close_Cmd)

    # 等待所有主机被关机
    time.sleep(60)
    for index in range(Vm_Creater_Sum):
        Full_Vm_Creater_Path = os.path.join(Vm_Creater_Base_Paht, Vm_Creater_Cluster,Vm_Creater_HostName + "_" + str(index + 1),Vm_Creater_HostName + "_" + str(index + 1) + ".vmx")
        Vm_Snapshot_Cmd='"' + Vmrun_Path + '" -T ws snapshot "' + Full_Vm_Creater_Path + '" "' +  '快照 1' + '"'
        print("Debug:开始快照-", index)
        os.popen(Vm_Snapshot_Cmd)

#默认IP从10开始设置
Vm_Create(3)
