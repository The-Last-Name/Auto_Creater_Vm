#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# BY: The Last Name
# Time: 2020.03.19
# System: Windows
# Python version: 3


import os,time,winreg

Vmrun_Path=""
Vm_Template_Path=r"F:\Virtual Machines\模板机"
Vm_Template_HostName="CentOS_7"
Vm_Template_Snapshot_Name="快照 2"
Vm_Creater_Base_Paht="F:\Virtual Machines"
Vm_Creater_Cluster="test"
Vm_Creater_HostName="test"

def Scan_Window_Install_Vm_Path():
    Regedit_Key = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall']
    for Regedit_Key_Index in Regedit_Key:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, Regedit_Key_Index, 0, winreg.KEY_ALL_ACCESS)
        for Regedit_Key__Sub_Index in range(0, winreg.QueryInfoKey(key)[0] - 1):
            try:
                key_name = winreg.EnumKey(key, Regedit_Key__Sub_Index)
                key_path = Regedit_Key_Index + '\\' + key_name
                each_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS)
                DisplayName, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayName')
                if DisplayName == 'VMware Workstation':
                    global Vmrun_Path
                    Vm_Install_Path,_ = winreg.QueryValueEx(each_key, 'DisplayIcon')
                    Vmrun_Path = (os.path.join(os.path.dirname(Vm_Install_Path),"vmrun.exe"))
            except WindowsError:
                pass

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
        Vm_Host_Set_Ip_Cmd='"' + Vmrun_Path + '" -T ws -gu root -gp PASSWORD runProgramInGuest "' + Full_Vm_Creater_Path + '" /root/set.sh '+ str(10 + index)
        print("Debug:开始设置IP-", index)
        os.popen(Vm_Host_Set_Ip_Cmd)
        time.sleep(2)
        Vm_Host_Close_Cmd = '"' + Vmrun_Path + '" -T ws -gu root -gp PASSWORD runProgramInGuest "' + Full_Vm_Creater_Path + '" /sbin/init 0'
        os.popen(Vm_Host_Close_Cmd)

    # 等待所有主机被关机
    time.sleep(60)
    for index in range(Vm_Creater_Sum):
        Full_Vm_Creater_Path = os.path.join(Vm_Creater_Base_Paht, Vm_Creater_Cluster,Vm_Creater_HostName + "_" + str(index + 1),Vm_Creater_HostName + "_" + str(index + 1) + ".vmx")
        Vm_Snapshot_Cmd='"' + Vmrun_Path + '" -T ws snapshot "' + Full_Vm_Creater_Path + '" "' +  '快照 1' + '"'
        print("Debug:开始快照-", index)
        os.popen(Vm_Snapshot_Cmd)

#默认IP从10开始设置
Scan_Window_Install_Vm_Path()
Vm_Create(3)
