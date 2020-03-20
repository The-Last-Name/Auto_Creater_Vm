#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# BY: The Last Name
# Time: 2020.03.19
# System: Windows
# Python version: 3

import os,time,winreg,subprocess,psutil

def Scan_Window_Install_Vm_Path():
    # 自动获取Vmrun.exe路径
    Vmrun_Path=""
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
                    Vm_Install_Path,_ = winreg.QueryValueEx(each_key, 'DisplayIcon')
                    Vmrun_Path = (os.path.join(os.path.dirname(Vm_Install_Path),"vmrun.exe"))
            except WindowsError:
                pass
    return Vmrun_Path

def Vm_Create(Vmrun_Path,Full_Vm_Template_Path,Vm_Template_Snapshot_Name,Full_Vm_Creater_Path,Vm_Creater_HostName):
    # vmrun.exe路径,完整模板路径,模板的快照名称，虚拟机克隆的完整路径,虚拟机的名称
    Vm_Create_Cmd = '"' + Vmrun_Path + '" -T ws clone "' + Full_Vm_Template_Path + '" "' + Full_Vm_Creater_Path + '" full -snapshot="' + Vm_Template_Snapshot_Name + '" -cloneName="' + Vm_Creater_HostName + '"'
    print("Debug:开始克隆-",Vm_Creater_HostName)
    Process = subprocess.Popen(Vm_Create_Cmd)
    return Process.pid

def Vm_Start(Vmrun_Path,Full_Vm_Creater_Path):
    Vm_Satrt_Cmd='"' + Vmrun_Path + '" -T ws start "' + Full_Vm_Creater_Path + '"'
    os.popen(Vm_Satrt_Cmd)

def Vm_Host_Set_Ip(Vmrun_Path,Full_Vm_Creater_Path,Vm_Host_Passwd,Ip_Addr):
    Vm_Host_Set_Ip_Cmd = '"' + Vmrun_Path + '" -T ws -gu root -gp ' + Vm_Host_Passwd + ' runProgramInGuest "' + Full_Vm_Creater_Path + '" /root/set.sh ' + Ip_Addr + '"'
    os.popen(Vm_Host_Set_Ip_Cmd)
    Vm_Host_Close_Cmd = '"' + Vmrun_Path + '" -T ws -gu root -gp ' + Vm_Host_Passwd + ' runProgramInGuest "' + Full_Vm_Creater_Path + '" /sbin/init 0'
    os.popen(Vm_Host_Close_Cmd)

def Vm_Snapshot(Vmrun_Path,Full_Vm_Creater_Path):
    Vm_Snapshot_Cmd = '"' + Vmrun_Path + '" -T ws snapshot "' + Full_Vm_Creater_Path + '" "' + '快照 1' + '"'
    os.popen(Vm_Snapshot_Cmd)


if  __name__=="__main__":

    if Scan_Window_Install_Vm_Path() != "":
        Vmrun_Path = Scan_Window_Install_Vm_Path()
    else:
        exit(1)

    #核心逻辑去需要编写
    Pid_List=[]
    for i in range(5):
        Pid_List.append(Vm_Create(Vmrun_Path,r"F:\Virtual Machines\模板机\CentOS_7\CentOS_7.vmx","快照 2",r"F:\Virtual Machines\test\test_"+str(i)+r"\test"+ str(i) +".vmx","test_"+str(i)))

    while Pid_List != []:
        for Pid_index in Pid_List:
            if not psutil.pid_exists(Pid_index):
                Pid_List.remove(Pid_index)
        time.sleep(3)
    print("Debug:克隆完成")

    #处理ip地址问题

