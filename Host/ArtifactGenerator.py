import os
import time
import random
import threading
from winreg import *
from tkinter import *
from matplotlib import pyplot as plt



BluePill_evasion_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/out/"                        #Path of evasion.log files
BluePill_blackListFile_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/in/blacklistFile.txt"  #Path to blacklist file
BluePill_blackListKey_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/in/blacklistKey.txt"    #Path to blacklist key

ToCreateFile_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/in/toCreateFile.txt"             #Path to toCreateFile file
ToCreateKey_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/in/toCreateKey.txt"               #Path to toCreateKey file
Iteration_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/in/iteration.txt"                   #Path to Iteration file

findFile_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/find/toSearchFile.txt"               #Path to findFile file
responseFile_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/find/responseFile.txt"           #Path to findFile response file
findKey_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/find/toSearchKey.txt"                 #Path to findKey file
responseKey_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/find/responseKey.txt"             #Path to findKey response file

#List of file's paths
path_list = [BluePill_blackListFile_path, BluePill_blackListKey_path, ToCreateFile_path, ToCreateKey_path, Iteration_path, findFile_path, responseFile_path, findKey_path, responseKey_path]

#List of command Flags
command_flags = {"debugFlag" : False, "getimeFlag" : False, "compnameFlag" : False, "usernameFlag" : False, "getversionFlag" : False, "memoryFlag" : False,
                 "adpterFlag" : False, "monitorFlag": False, "timeFlag" : False, "mouseFlag" : False, "keyboardFlag" : False, "powerFlag" : False}

#List of line for each Command Flag
command_line_flag = {"debugFlag" : [], "getimeFlag" : [], "compnameFlag" : [], "usernameFlag" : [], "getversionFlag" : [], "memoryFlag" : [],
                 "adpterFlag" : [], "monitorFlag": [], "timeFlag" : [], "mouseFlag" : [], "keyboardFlag" : [], "powerFlag" : []}

#List of command Types
commandType = {"debugFlag" : ["IsDebuggerPresent", "CheckRemoteDebuggerPresent"], "getimeFlag" : ["GetLocalTime", "GetSystemTimeAsFile", "GetTimeZoneInformation"],
               "compnameFlag" : ["GetComputerName", "GetComputerNameA", "GetComputerNameW", "WNetGetProviderName", "WNetGetProviderNameA", "WNetGetProviderNameW"],
               "usernameFlag" : ["GetUserName", "GetUserNameA", "GetUserNameW"], "getversionFlag" : ["GetVersion", "GetVersionEx", "GetVersionExA", "GetVersionExW"],
               "memoryFlag" : ["GlobalMemoryStatusEx", "GetDiskFreeSpaceEx", "GetDiskFreeSpaceExA", "GetDiskFreeSpaceExW"], "adpterFlag" : ["GetAdaptersInfo"], "monitorFlag" : ["GetMonitorInfo", "GetMonitorInfoA", "GetMonitorInfoW", "GetDesktopWindow", "GetWindowRect"],
               "timeFlag" : ["NtDelayExecution", "NtQueryPerformanceCounter", "GetTickCount", "SetTimer", "WaitForSingleObject", "GetSystemTimeAsFileTime", "IcmpCreateFile", "IcmpSendEcho"],
               "mouseFlag": ["GetCursorPos"], "keyboardFlag" : ["GetKeyboardLayout"], "powerFlag" : ["GetPwrCapabilities"]}

#Weighted list of file manipulation commands
FileCommandList = {"CreateFile" : 1, "CreateFileA" : 1, "CreateFileW" : 1,
                   "GetFileAttributesA" : 4, "GetFileAttributesW" : 4, "GetFileAttributes" : 4,
                   "OpenFile" : 2,
                   "PathFileExists" : 5, "PathFileExistsA" : 5, "PathFileExistsW" : 5,
                   "FindFirstFile" : 4, "FindFirstFileA" : 4, "FindFirstFileW" : 4, "FindFirstFileEx" : 4, "FindFirstFileExA" : 4, "FindFirstFileExW" : 4,
                   "NtCreateFile" : 3, "NtQueryAttributesFile" : 3,
                   "GetModuleFileName" : 2, "GetModuleFileNameA" :2 , "GetModuleFileNameW" :2}

#Weighted list of file open modalities
ModeList = {"Create" : 1, "Replace/Create" : 1, "Overwrite/Create" :1,
            "Delete" : 1, "Exist" : 5, "Read" : 4, "Read/Write" : 4,
            "Open" :4 , "Open/Create" : 4, "Write" : 4, "Overwrite" : 4,
            "Search" : 5, "Unknow" : 2}

#Weighted list of file names
FileNameList = {"VIRTUALBOX" : 5, "VBOX" : 5, "ORACLE" : 5, "GUEST" : 4, "PHYSICALDRIVE" : 4, "VM" : 4,
                "VMMOUSE" : 5, "HGFS" : 5, "VMHGFS" : 5, "VMCI" : 5, "VMWARE" : 5, "VBOXMOUSE" : 5, "VBOXGUEST" : 5, "VBOXSF" : 5, "VBOXVIDEO" :5,
                "LOADDLL" : 3, "EMAIL" : 2,"SANDBOX" : 5, "SAMPLE" : 3, "VIRUS" : 5, "FOOBAR" : 3,
                "DRIVERS\\PRLETH" : 4, "DRIVERS\\PRLFS" : 4, "DRIVERS\\PRLMOUSE" : 4, "DRIVERS\\PRLVIDEO" : 4, "DRIVERS\\TIME" : 4,
                "*.*" : 2, "SERVICES.EXE": 10, "WINDOWS\\SYSTEM32" : 3}

#Weighted Regkeys path
RegKeyList = {"sandbox" : 5, "Hyper-V" : 5,
              "VirtualMachine" : 5, "Virtual Machine" : 5,
              "\\SYSTEM\\ControlSet001\\Services" : 5, "\\SYSTEM\\CurrentControlSet\\Enum\\PCI" : 5,
              "\\SYSTEM\\CurrentControlSet\\Services\SbieDrv" : 5, "\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Sandboxie" : 5,
              "\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_80EE" : 5, "VBOX" : 5, "Vbox" : 5, "VirtualBox Guest Additions" :5, "Oracle" : 5,
              "\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_5333" : 5, "\\SYSTEM\\ControlSet001\\Services\\vpcbus" : 5, "\\SYSTEM\\ControlSet001\\Services\\vpc-s3" : 5, "\\SYSTEM\\ControlSet001\\Services\\vpcuhub" : 5,
              "\\SYSTEM\\ControlSet001\\Services\\msvmmouf" : 5,
              "\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_15AD" : 5, "VMware" : 5, "vmware" : 5, "VMWARE" : 5, "vmdebug" : 5, "vmmouse" : 5, "VMTools" : 5, "VMMEMCTL" : 5, "vmci" : 5, "vmx86" : 5,
              "Wine" : 4, "xen" :4, "\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" : 3, "Rpc": 4}

#Weighted RegKeys Values (key : [Weight, Value])
RegKeyValueList = {"\\HARDWARE\\Description\\System" : [4, "SystemBiosDate", "SystemProductName", "SystemBiosVersion", "VideoBiosVersion"],
                   "\SOFTWARE\\Microsoft\\Windows\\CurrentVersion" : [3, "ProductID"], "\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" :  [3, "ProductID"],
                   "\\SYSTEM\\ControlSet001\\Services\\Disk\\Enum" :  [4, "DeviceDesc", "FriendlyName", "0", "1"], "\\SYSTEM\\ControlSet002\\Services\\Disk\\Enum" : [4,"DeviceDesc", "FriendlyName"], "\\SYSTEM\\ControlSet003\\Services\\Disk\\Enum" : [4, "DeviceDesc", "FriendlyName"],
                   "\\SYSTEM\CurrentControlSet\\Control\\SystemInformation" : [4, "SystemProductName" ],
                   "\\Installer\\Products" : [3, "ProductName"],
                   "\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall" : [3, "DisplayName"],
                   "{4D36E968-E325-11CE-BFC1-08002BE10318}" : [3, "CoInstallers32", "DriverDesc", "InfSection", "ProviderName", "Device Description"],
                   "HKLM\\SYSTEM\\CurrentControlSet\\Control" : [3, "SystemProductName", "Service", "Device Description"]}

#Weighted list of commands
GeneralCommandList = {"IsDebuggerPresent" : 5, "CheckRemoteDebuggerPresent" : 5, "GetLocalTime" : 3, "GetSystemTimeAsFileTime" : 3, "GetTimeZoneInformation" : 3,
                      "GetComputerNameA" : 3, "GetComputerNameW" :3, "GetUserDefaultLCID" : 2, "GetUserName" : 2, "GetUserNameA" :2, "GetUserNameW" :2,
                      "GetVersion" : 1, "GetVersionEx" :1 , "GetVersionExA" :1, "GetVersionEx" :1, "GlobalMemoryStatusEx" : 2, "getenv" : 2,
                      "GetAdaptersInfo" : 3, "GetMonitorInfo" : 2, "GetMonitorInfoA" : 2 , "GetMonitorInfoW" : 2, "EnumDisplayDevices" : 2, "GetDesktopWindow" :2, "GetWindowRect" : 2,
                      "NtDelayExecution" :4, "NtQueryPerformanceCounter" :4, "FindNextFile" : 2, "FindNextFileA" : 2, "FindNextFileW" : 2, "GetSystemInfo" : 2,
                      "GetCursorPos" : 3, "FindWindow" : 3, "FindWindowW" : 3, "FindWindowA" : 3, "WNetGetProviderName" : 4, "WNetGetProviderNameW" : 4, "WNetGetProviderNameA" : 4,
                      "GetKeyboardLayout" : 3, "GetKeyboardLayout-lib" : 3, "GetPwrCapabilities" : 5, "ChangeServiceConfigW" : 2,
                      "SetupDiGetDeviceRegistryProperty" : 2, "SetupDiGetDeviceRegistryPropertyW" : 2, "SetupDiGetDeviceRegistryPropertyA" : 2,
                      "GetWindowText" : 3, "GetWindowTextA" : 3, "GetWindowTextW" : 3, "FindWindow" : 3, "LoadLibraryA" : 2, "LoadLibraryW" : 2, "LoadLibraryExA" :2 , "LoadLibraryExW" :2,
                      "GetDiskFreeSpaceEx" :2 , "GetDiskFreeSpaceExW" :2 , "GetDiskFreeSpaceExA" :2,
                      "GetTickCount" :4, "SetTimer" : 4, "WaitForSingleObject" : 4, "GetSystemTimeAsFileTime" :4 , "IcmpCreateFile" : 4, "IcmpSendEcho" : 4,
                      "WMI-Query" : 5, "NtQueryDO" : 2, "NtOpenKey" : 2, "NtEnumerateKey" :2 , "NtQueryValueKey":2 , "NtQueryAttributesFile" :2}

#List of Files to not modificate
whitelistFile = ["SVCHOST.EXE", "ACLAYERS.DLL", "CMD.EXE", "SORTDEFAULT.NLS", "DESKTOP.INI", "EE.EXE", "APPDATA", "MOUNTPOINTMANAGER", "EN", "STATICCACHE.DAT", "OLEACCRC.DLL", "ACXTRNAL.DLL", "MSVFW32.DLL.MUI", "AVICAP32.DLL.MUI",
                 "KERNELBASE.DLL.MUI", "MSCTF.DLL.MUI", "WERFAULT.EXE.MUI", "FAULTREP.DLL.MUI", "DWM.EXE", "EXPLORER.EXE", "WMIPRVSE.EXE", "PIN.EXE", "RSAENH.DLL", "SXBOY.EXE",
                 "OSSPROXY.PDB", "SERVICES.EXE", "SUP.DLL", "D3D8THK.DLL", "VERSION.DLL", "MSIMG32.DLL", "WINNSI.DLL", "DHCPCSVC.DLL", "PROFAPI.DLL", "D3D9.DLL", "DWMAPI.DLL", "RASAPI32.DLL",
                 "FAULTREP.DLL", "RTUTILS.DLL", "MFC42U.DLL", "ODBC32.DLL", "API-MS-WIN-CORE-FIBERS-L1-1-1.DLL", "API-MS-WIN-CORE-FIBERS-I1-1-1.DLL", "WSOCK32.DLL"]

#List of Keys to not modificate
whitelistKey = ["MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager", "Machine\\SYSTEM\\CurrentControlSet\\Control\\Session Manager", "\\REGISTRY\\MACHINE", "Machine\\SOFTWARE\\Policies\\Microsoft\\Windows\\Safer\\CodeIdentifiers",
                "Machine\\SYSTEM\\CurrentControlSet\\Control\\Nls\\Sorting\\Versions", "MACHINE\SYSTEM\CurrentControlSet\Control\SafeBoot\Option", "\Registry\Machine\System\CurrentControlSet\Control\Srp\GP\DLL", "Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Diagnostics",
                "Machine\SYSTEM\CurrentControlSet\Control\Srp\GP\DLL", "USER\S-1-5-21-3859524018-1065375656-672923527-1001\Software\Policies\Microsoft\Windows\Safer\CodeIdentifiers", "Machine\SYSTEM\CurrentControlSet\Control\Terminal Server",
                "Machine\\SYSTEM\\CurrentControlSet\\Control\\Error Message Instrument\\", "Machine\\SOFTWARE\\Microsoft\\OLEAUT", "Machine\\SOFTWARE\\Microsoft\\OLE\\Tracing", "Machine\\SOFTWARE\\Microsoft\\OLE", "Machine\\CONTROL PANEL\\Desktop\\MuiCached\MachineLanguageConfiguration",
                "Machine\\CONTROL PANEL\\Desktop\\LanguageConfiguration", "Machine\\CONTROL PANEL\\Desktop\\MuiCached", "Machine\\SYSTEM\\CurrentControlSet\\Services\\EventLog\\Application\\Error Instrument\\", "Machine\\SYSTEM\\CurrentControlSet\\Services\\EventLog\\Application\\Error Instrument",
                "Machine\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting\\WMR", "Machine\\SOFTWARE\\Microsoft\\Windows", "MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppCompat", "MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\SideBySide",
                "USER\\S-1-5-21-3859524018-1065375656-672923527-1001", "Machine\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders", "Machine\\SOFTWARE\\Policies\\Microsoft\\Windows\\System", "Machine\\HTTP\\shell\\open\\command",
                "Machine\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\Run", "USER\\S-1-5-21-3859524018-1065375656-672923527-1001_CLASSES", "Machine\\SOFTWARE\\Classes\\http\\shell\\open\\command", "MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\AppCertDlls",
                "MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\AppCompatibility", "USER\\S-1-5-21-3859524018-1065375656-672923527-1001\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders", "USER\\S-1-5-21-3859524018-1065375656-672923527-1001\\Software\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Layers",
                "Machine\\SOFTWARE\\Policies\\Microsoft\\MUI\\Settings", "Machine\\SOFTWARE\\Policies\\Microsoft\\Control Panel\\Desktop", "USER\\S-1-5-21-3859524018-1065375656-672923527-1001\\Software\\Microsoft\\Windows NT\\CurrentVersion", "Machine\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\LanguagePack\\DataStore_V1.0",
                "Machine\\SYSTEM\\CurrentControlSet\\control\\NetworkProvider\\HwOrder", "Machine\\SYSTEM\\CurrentControlSet\\Services\\Winsock2\\Parameters", "Machine\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Custom\\uninstal.bat",
                "Machine\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Layers", "Machine\\SYSTEM\\CurrentControlSet\\Control\\SQMServiceList", "Machine\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\WinOldApp",
                "Machine\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\WOW\\boot", "Machine\\SOFTWARE\\Microsoft\\SQMClient\\Windows", "Machine\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags", "Machine\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\GRE_Initialize",
                "Machine\\SYSTEM\\CurrentControlSet\\Control\\Nls\\CustomLocale", "Machine\\SOFTWARE\\Microsoft\\CTF\\KnownClasses", "Machine\\SOFTWARE\\Microsoft\\CTF\\DirectSwitchHotkeys", "Machine\\SOFTWARE\\Policies\\Microsoft\\SQMClient\\Windows", "Machine\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer",
                "Machine\\SYSTEM\\CurrentControlSet\\Control\\ComputerName\\ActiveComputerName", "Machine\\CONTROL\\NetworkProvider\\HwOrder", "Machine\\SYSTEM\\CurrentControlSet\\Services\\Winsock\\Parameters", "Machine\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters\\Winsock",
                "Machine\\SYSTEM\\CurrentControlSet\\Services\\Psched\\Parameters\\Winsock", "Machine\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Winsock", "Machine\\SYSTEM\\CurrentControlSet\\Services\\RDPNP\\NetworkProvider", "Machine\\SYSTEM\\CurrentControlSet\\Services\\WebClient\\NetworkProvider",
                "Machine\\SYSTEM\\CurrentControlSet\\Services\\DNS", "Machine\\SYSTEM\\CurrentControlSet\\Services\\Winsock\\Setup Migration\\Providers", "Machine\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\PeerDist\\Service", "Machine\\SOFTWARE\\Classes\\CLSID"]

#List of Key Values to not modificate
whitelistValue = [["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "RunDiagnosticLoggingApplicationManagement"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\GRE_Initialize", "DisableMetaFiles"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options", "EnableDefaultReply"],
                  ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "NotifySettingChanges"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "ExecutablesToTrace"], ["Machine\MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers", "C:\Pin311\ee.exe"],
                  ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "ShutdownTimeout"], ["MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatibility", "DisableAppCompat"], ["Machine\SOFTWARE\Policies\Microsoft\MUI\Settings", "PreferredUILanguages"],
                  ["Machine\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run", "Policies"], ["Machine\SOFTWARE\Microsoft\Cryptography\Defaults\Provider\Microsoft Strong Cryptographic Provider", "Image Path"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "Load"],
                  ["Machine\SOFTWARE\Microsoft\Windows\CurrentVersion\Setup", "SourcePath"], ["Machine\SOFTWARE\Microsoft\Windows\CurrentVersion", "DevicePath"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AeDebug", "Auto"]]

#List of Peak Function
peakList = ["Getaddrinfo", "Socket", "Connect", "Send", "Sendto", "Recv", "Recvfrom", "CloseSocket", "InternetOpen", "InternetConnect", "HttpOpenRequest", "HttpSendRequest", "InternetReadFile", "WinHttpOpen", "WinHttpConnect", "WinHttpOpenRequest", "WinHttpSendRequest", "WinHttpWriteData", "WinHttpReceiveResponse", "WinHttpQueryData",
            "WinHttpReadData", "WSASocket", "WSAIoctl", "ioctlsocket", "InternetOpenUrlA", "HttpAddRequestHeadersA", "UrlDownloadToFile"] #GetKeyState, ShellExecute, WinExec

noExistFiles = []           #List of Files to be "delete" through BluePill
noExistKeys = []            #List of Keys to be "delete" through BluePill

toCreateFiles = []          #List of Files to be "create" through BluePill
toCreatekeys = []           #List of Keys to be "create" through BluePill

FileDatabase = {}           #File: [weight, isPresent, endAction, flag]
KeyDatabase = {}            #Key:  [weight, valueKey[], isPresent[], endAction[], flag[]]
IterationDatabase = {}      #Iteration: [FileDatabase, weight]

plot_x = []                 #X coordinates for plot
plot_y = []                 #Y coordinates for plot

last = 0                    #Last Action indicator

n_equal = 0                 #Weight Value of actual iteration
previous_n = 0              #Weight Value of previous iteration
peak = False                #Peak found flag
possiblyPeak = False        #Possibly peak found flag
startWeight = 0             #Weight of first iteration


class AG:
    def __init__(self, win, tex, lab, labFind, labIter):

        def writeBlackListFile():
            f = open(BluePill_blackListFile_path,"w")
            for i in noExistFiles:
                f.write(i+'\n')
            f.close()

        def writeToCreateFile():
            f = open(ToCreateFile_path,"w")
            for i in toCreateFiles:
                f.write(i+'\n')
            f.close()

        def writeBlackListKey():
            f = open(BluePill_blackListKey_path,"w")
            for i in noExistKeys:
                l = i.split("\\")
                s=""
                if len(l)>1:
                    for elem in  l[1:len(l)]:
                        if elem != l[len(l)-1]:
                            s += str(elem)+"\\"
                        else:
                            s += str(elem)
                    f.write(s+'\n')
                else:
                    f.write(i+'\n')
            f.close()

        def writeToCreateKey():
            f = open(ToCreateKey_path,"w")
            for i in toCreatekeys:
                f.write(i+'\n')
            f.close()

        def calculateWeightFile(command, mode, targetFile):
            valueCommand = FileCommandList[command]
            valueMode = 0
            if mode in ModeList.keys():
                valueMode = ModeList[mode]
            else:
                valueMode = 2
            valueName = 1
            maxName =""
            for n in FileNameList.keys():
                if n in targetFile.upper() or n in targetFile:
                    if FileNameList[n] > valueName:
                        valueName = FileNameList[n]
                        maxName = n
            return (valueCommand + valueMode + valueName)/3

        def calculateWeightKey(key, value):
            valueKey = 2
            valueValue = 0
            for k in RegKeyList.keys():
                if k in key: #or k.upper() in key.upper():
                    valueKey = RegKeyList[k]

            for k in RegKeyValueList.keys():
                if k in key:
                    if value in RegKeyValueList[k]:
                        valueValue = RegKeyValueList[k][0]
                        return (valueKey + valueValue) / 2
            return valueKey

        def calculateIterWeight(actualEvasionPath, initialFilesNumber, initialThreadsNumber):
            global possiblyPeak
            global peak
            endFilesNumber = 0
            commandsWeight = 0
            threads = []
            linesNumber = 0
            lastLine = ""
            iterLinesList = []
            for file in os.listdir(actualEvasionPath):
                if "evasion" in file:
                    f = open (actualEvasionPath + file,"r")
                    while (True):
                            try:
                                line = f.readline()
                                break
                            except:
                                None
                    while line != "":
                        thread = line.split(":")[0]
                        if thread not in threads :
                            threads.append(thread)
                        try:
                            command = line.split("[")[1].split("]")[0]
                        except:
                            command = ""
                        if  line not in iterLinesList:
                            iterLinesList.append(line)
                            if command in GeneralCommandList.keys() and line != lastLine:
                                commandsWeight += GeneralCommandList[command]
                            elif command in FileCommandList.keys() and line != lastLine:
                                commandsWeight += FileCommandList[command]
                            elif command in peakList and line != lastLine:
                                if not peak:
                                    Running.setText(win, tex, "-------Possibly Peak: "+command+'\n', "green")
                                    Running.setPeak(win, lab, "Possible", "yellow")
                                    #print("-------Possibly Peak: "+command)
                                possiblyPeak = True
                                commandsWeight += 20
                            elif line != lastLine:
                                commandsWeight += 1
                        lastLine = line
                        while (True):
                            try:
                                line = f.readline()
                                break
                            except:
                                #print("Error reading line")
                                None
                    f.close()
                endFilesNumber += 1 
            FilesNumberDiff = endFilesNumber - initialFilesNumber          #Processes Number Difference
            ThreadsNumberDiff =  len(threads) - initialThreadsNumber       #Threads Number Difference
            return (commandsWeight) * (FilesNumberDiff + ThreadsNumberDiff +1)

        def findFile(targetFile):
            f = open (findFile_path, "w")
            f.write(targetFile)
            f.close()
            os.system('VBoxManage --nologo guestcontrol "Malware_Evasion" run --exe "Z://Run_FindFile.bat" --username Edo --password edoardo1 --wait-stdout')
            f = open (responseFile_path, "r")
            res = f.readline()
            f.close()
            return int(res)

        def findKey(targetKey, valueKey):
            f = open (findKey_path, "w")
            f.write(targetKey+";"+valueKey)
            f.close()
            os.system('VBoxManage --nologo guestcontrol "Malware_Evasion" run --exe "Z://Run_FindKey.bat" --username Edo --password edoardo1 --wait-stdout')
            f = open (responseKey_path, "r")
            res = f.readline()
            f.close()
            return int(res)
            
        def actionArtifact():
            global last
            importantFile = ""
            importantKey = ""
            importantValue = ""
            maxWeightFile = 0
            maxWeightKey = 0
            if len(FileDatabase) > 0:
                for i in FileDatabase.keys():
                    if FileDatabase[i][0] > maxWeightFile and not FileDatabase[i][3]:
                        maxWeightFile = FileDatabase[i][0]
                        importantFile = i

            if len(KeyDatabase) > 0:
                for i in KeyDatabase.keys():
                    if len(KeyDatabase[i][1]) > 0:
                        for j in range(len(KeyDatabase[i][1])):
                            if KeyDatabase[i][0] > maxWeightKey and not KeyDatabase[i][4][j+1]:
                                maxWeightKey = KeyDatabase[i][0]
                                importantValue = KeyDatabase[i][1][j]
                                importantKey = i
                    else:
                        if KeyDatabase[i][0] > maxWeightKey and not KeyDatabase[i][4][0]:
                            maxWeightKey = KeyDatabase[i][0]
                            importantKey = i
                            
            if importantFile == "" and importantKey == "":
                print("Error: actionArtifact")
                return None, None

            if maxWeightFile >= maxWeightKey:
                if FileDatabase[importantFile][1] == 1:
                     last = 1
                     Running.setText(win, tex, "Deleting: "+importantFile+"..."+'\n', "coral")
                     #print("Deleting: "+importantFile+"...")
                     l = importantFile.split("\\")
                     name = l[len(l)-1]
                     path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1])
                     if name == "*.*":
                        if path+"ag.txt" in toCreateFiles:
                            toCreateFiles.remove((path+"ag"+name[1:len(name)]))
                            writeToCreateFile()
                            FileDatabase[importantFile][1] = 0
                            FileDatabase[importantFile][3] = True
                            return importantFile, None
                        noExistFiles.append(path+"ag.txt")
                        writeBlackListFile()
                     elif "*" in name:
                        if path+"ag"+name[1:len(name)] in toCreateFiles:
                            toCreateFiles.remove(path+"ag"+name[1:len(name)])
                            writeToCreateFile()
                            FileDatabase[importantFile][1] = 0
                            FileDatabase[importantFile][3] = True
                            return importantFile, None
                        noExistFiles.append(path+"ag"+name[1:len(name)])
                        writeBlackListFile()
                     else:
                         if importantFile in toCreateFiles:
                            toCreateFiles.remove(importantFile)
                            writeToCreateFile()
                            FileDatabase[importantFile][1] = 0
                            FileDatabase[importantFile][3] = True
                            return importantFile, None
                         noExistFiles.append(importantFile)
                         writeBlackListFile()
                     FileDatabase[importantFile][1] = 0
                else:
                    last = 2
                    Running.setText(win, tex, "Creating: "+importantFile+"..."+'\n', "coral")
                    #print("Creating: "+importantFile+"...")
                    l = importantFile.split("\\")
                    name = l[len(l)-1]
                    path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1])
                    if name == "*.*":
                        if path+"ag.txt" in noExistFiles:
                            noExistFiles.remove(path+"ag.txt")
                            writeBlackListFile()
                            FileDatabase[importantFile][1] = 1
                            FileDatabase[importantFile][3] = True
                            return importantFile, None
                        toCreateFilesappend(path+"ag.txt")
                        writeToCreateFile()
                    elif "*" in name:
                        if path+"ag"+name[1:len(name)] in noExistFiles:
                            noExistFiles.remove(path+"ag"+name[1:len(name)])
                            writeBlackListFile()
                            FileDatabase[importantFile][1] = 1
                            FileDatabase[importantFile][3] = True
                            return importantFile, None
                        toCreateFiles.append(path+"ag"+name[1:len(name)])
                        writeToCreateFile()
                    else:
                        if importantFile in noExistFiles:
                            noExistFiles.remove(importantFile)
                            writeBlackListFile()
                            FileDatabase[importantFile][1] = 1
                            FileDatabase[importantFile][3] = True
                            return importantFile, None
                        toCreateFiles.append(importantFile)
                        writeToCreateFile()
                    FileDatabase[importantFile][1] = 1
                FileDatabase[importantFile][3] = True
                return importantFile, None
                    
            else:
                if len(KeyDatabase[importantKey][1]) == 0 or importantValue == None:
                    if KeyDatabase[importantKey][2][0] == 1:
                        last = 3
                        Running.setText(win, tex, "Deleting: "+importantKey+"..."+'\n', "coral")
                        #print("Deleting: "+importantKey+"...")
                        if importantKey+";" in toCreatekeys:
                            toCreatekeys.remove(importantKey+";")
                            writeToCreateKey()
                            KeyDatabase[importantKey][2][0] = 0
                            KeyDatabase[importantKey][4][0] = True
                            return importantKey, None
                        noExistKeys.append(importantKey+";")
                        writeBlackListKey()
                        KeyDatabase[importantKey][2][0] = 0
                    else:
                        last = 4
                        Running.setText(win, tex, "Creating: "+importantKey+"..."+'\n', "coral")
                        #print("Creating: "+importantKey+"...")
                        if importantKey+";" in noExistKeys:
                            noExistKeys.remove(importantKey+";")
                            writeBlackListKey()
                            KeyDatabase[importantKey][2][0] = 1
                            KeyDatabase[importantKey][4][0] = True
                            return importantKey, None
                        toCreatekeys.append(importantKey+";")
                        writeToCreateKey()
                        KeyDatabase[importantKey][2][0] = 1
                    KeyDatabase[importantKey][4][0] = True
                    return importantKey, None

                else:
                    pos = (KeyDatabase[importantKey][1]).index(importantValue) + 1
                    if KeyDatabase[importantKey][2][pos] == 1:
                        last = 3
                        Running.setText(win, tex, "Deleting: "+importantKey+"  "+importantValue+"..."+'\n', "coral")
                        #print("Deleting: "+importantKey+"  "+importantValue+"...")
                        if importantKey+";"+importantValue in toCreatekeys:
                            toCreatekeys.remove(importantKey+";"+importantValue)
                            writeToCreateKey()
                            KeyDatabase[importantKey][2][pos] = 0
                            KeyDatabase[importantKey][4][pos] = True
                            return importantKey, importantValue
                        noExistKeys.append(importantKey+";"+importantValue)
                        writeBlackListKey()
                        KeyDatabase[importantKey][2][pos] = 0
                    else:
                        last = 4
                        Running.setText(win, tex, "Creating: "+importantKey+"  "+importantValue+"..."+'\n', "coral")
                        #print("Creating: "+importantKey+"  "+importantValue+"...")
                        if importantKey+";"+importantValue in noExistKeys:
                            noExistKeys.remove(importantKey+";"+importantValue)
                            writeBlackListKey()
                            KeyDatabase[importantKey][2][pos] = 1
                            KeyDatabase[importantKey][4][pos] = True
                            return importantKey, importantValue
                        toCreatekeys.append(importantKey+";"+importantValue)
                        writeToCreateKey()
                        KeyDatabase[importantKey][2][pos] = 1
                    KeyDatabase[importantKey][4][pos] = True
                    return importantKey, importantValue

        def restoreArtifact(LastTouchedElem, LastTouchedValue):
            global last
            if LastTouchedElem in FileDatabase.keys():
                if FileDatabase[LastTouchedElem][1] == 1:
                    Running.setText(win, tex, "Deleting: "+LastTouchedElem+"..."+'\n', "coral")
                    #print("Deleting: "+LastTouchedElem+"...")
                    l = LastTouchedElem.split("\\")
                    name = l[len(l)-1]
                    path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1])
                    if name == "*.*":
                        if (path+"ag.txt") in toCreateFiles:
                            toCreateFiles.remove(path+"ag"+name[1:len(name)])
                    elif "*" in name:
                       if path+"ag"+name[1:len(name)] in toCreateFiles:
                           toCreateFiles.remove((path+"ag"+name[1:len(name)]))
                    else:
                        if LastTouchedElem in toCreateFiles:
                           toCreateFiles.remove(LastTouchedElem)
                    writeToCreateFile()
                    FileDatabase[LastTouchedElem][1] = 0
                    FileDatabase[LastTouchedElem][3] = True
                else:
                    last = 2
                    Running.setText(win, tex, "Creating: "+LastTouchedElem+"..."+'\n', "coral")
                    #print("Creating: "+LastTouchedElem+"...")
                    l = LastTouchedElem.split("\\")
                    name = l[len(l)-1]
                    path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1])
                    if name == "*.*":
                        if path+"ag.txt" in noExistFiles:
                            noExistFiles.remove(path+"ag.txt")
                            writeBlackListFile()
                            FileDatabase[LastTouchedElem][1] = 1
                            FileDatabase[LastTouchedElem][3] = True
                            return
                        toCreateFiles.append(path+"ag.txt")
                        writeToCreateFile()
                    elif "*" in name:
                        if (path+"ag"+name[1:len(name)]) in noExistFiles:
                            noExistFiles.remove(path+"ag"+name[1:len(name)])
                            writeBlackListFile()
                            FileDatabase[LastTouchedElem][1] = 1
                            FileDatabase[LastTouchedElem][3] = True
                            return
                        toCreateFiles.append(path+"ag"+name[1:len(name)])
                        writeToCreateFile()
                    else:
                        if LastTouchedElem in noExistFiles:
                            noExistFiles.remove(LastTouchedElem)
                            writeBlackListFile()
                            FileDatabase[LastTouchedElem][1] = 1
                            FileDatabase[LastTouchedElem][3] = True
                            return
                        toCreateFiles.append(LastTouchedElem)
                        writeToCreateFile()
                    FileDatabase[LastTouchedElem][1] = 1
                    FileDatabase[LastTouchedElem][3] = True

            elif LastTouchedElem in KeyDatabase.keys():
                if len(KeyDatabase[LastTouchedElem][1]) == 0 or LastTouchedValue == None:
                    if KeyDatabase[LastTouchedElem][2][0] == 1:
                        Running.setText(win, tex, "Deleting: "+LastTouchedElem+"..."+'\n', "coral")
                        #print("Deleting: "+LastTouchedElem+"...")
                        if LastTouchedElem+";" in toCreatekeys:
                            toCreatekeys.remove(LastTouchedElem+";")
                            writeToCreateKey()
                        KeyDatabase[LastTouchedElem][2][0] = 0
                        KeyDatabase[LastTouchedElem][4][0] = True
                        return
                    else:
                        last = 4
                        Running.setText(win, tex, "Creating: "+LastTouchedElem+"..."+'\n', "coral")
                        #print("Creating: "+LastTouchedElem+"...")
                        if LastTouchedElem+";" in noExistKeys:
                            noExistKeys.remove(LastTouchedElem+";")
                            writeBlackListKey()
                            KeyDatabase[LastTouchedElem][2][0] = 1
                            KeyDatabase[LastTouchedElem][4][0] = True
                            return
                        toCreatekeys.append(LastTouchedElem+";")
                        writeToCreateKey()
                        KeyDatabase[LastTouchedElem][2][0] = 1
                        KeyDatabase[LastTouchedElem][4][0] = True
                        return
                else:
                    pos = (KeyDatabase[LastTouchedElem][1]).index(LastTouchedValue) + 1
                    if KeyDatabase[LastTouchedElem][2][pos] == 1:
                        Running.setText(win, tex, "Deleting: "+LastTouchedElem+"  "+LastTouchedValue+"..."+'\n', "coral")
                        #print("Deleting: "+LastTouchedElem+"  "+LastTouchedValue+"...")
                        if LastTouchedElem+";"+LastTouchedValue in toCreatekeys:
                            toCreatekeys.remove(LastTouchedElem+";"+LastTouchedValue)
                            writeToCreateKey()
                        KeyDatabase[LastTouchedElem][2][pos] = 0
                        KeyDatabase[LastTouchedElem][4][pos] = True
                    else:
                        last = 4
                        Running.setText(win, tex, "Creating: "+LastTouchedElem+"  "+LastTouchedValue+"..."+'\n', "coral")
                        #print("Creating: "+LastTouchedElem+"  "+LastTouchedValue+"...")
                        if LastTouchedElem+";"+LastTouchedValue in noExistKeys:
                            noExistKeys.remove(LastTouchedElem+";"+LastTouchedValue)
                            writeBlackListKey()
                            KeyDatabase[LastTouchedElem][2][pos] = 1
                            KeyDatabase[LastTouchedElem][4][pos] = True
                            return
                        toCreatekeys.append(LastTouchedElem+";"+LastTouchedValue)
                        writeToCreateKey()
                        KeyDatabase[LastTouchedElem][2][pos] = 1
                        KeyDatabase[LastTouchedElem][4][pos] = True
                    
        def exitCase():
            for file in FileDatabase.keys():
                if FileDatabase[file][3] != True:
                    return False
            for key in KeyDatabase.keys():
                if len(KeyDatabase[key][1]) > 0:
                    for j in range(len(KeyDatabase[key][1])):
                        if KeyDatabase[key][4][j+1] != True:
                            return False
                else:
                    if KeyDatabase[key][4][0] != True:
                            return False
            return True

        def clearPath(targetFile):
            l = targetFile.split("\\")
            path = ""
            for elem in l[2:len(l)]:
                if elem != l[len(l)-1]:
                    path += str(elem)+"\\"
                else:
                    path += str(elem)
            return path 

        def ClearKey(targetKey):
            l = targetKey.split("\\")
            ret = ""
            if l[1] == "Registry" or l[1] == "REGISTRY":
                if l[2] == "Machine" or l[2] == "MACHINE":
                    l[3] = l[3].upper()
                if l[2] == "Root" or l[2] == "ROOT":
                    l[3] = l[3].upper()
                if l[2] == "User" or l[2] == "USER":
                    l[3] = l[3].upper()
                for elem in  l[2:len(l)]:
                    if elem != l[len(l)-1]:
                        ret += str(elem)+"\\"
                    else:
                        ret += str(elem)
                return ret
            else:
                l[0] = l[0].upper()
                if l[0] == "SERVICES":
                    s="Root\\"
                else:
                    s = "Machine\\"
                for elem in  l[0:len(l)]:
                    if elem != l[len(l)-1]:
                        ret += str(elem)+"\\"
                    else:
                        ret += str(elem)
                return s+ret

        def getBestIteration():
            maxx = 0
            minn = IterationDatabase[0][0]
            best = 0
            for i in IterationDatabase.keys():
                val = int(IterationDatabase[i][0])
                if val > maxx:
                    maxx = val
                    best = i
            return best, 100 - ((minn*100)/maxx)

        def inWhiteListFile(file):
            l = file.split("\\")
            name = l[len(l)-1]
            clearF = clearPath(file)
            for f in whitelistFile:
                if f in file or f in file.upper() or f in clearF or f in clearF.upper():
                    return True
            return False
            
        def inWhiteListKey(key):
            return ClearKey(key) in whitelistKey

        def inWhiteListValue(key, value):
            for elem in whitelistValue:
                if (ClearKey(key) == elem[0] or key == elem[0]) and value == elem[1]:
                    return True
            return False 

        def inDatabaseFile(file):
            if file not in FileDatabase.keys():        
                return clearPath(file) in FileDatabase.keys()
            return True

        def inDatabaseKey(key):
            return ClearKey(key) in KeyDatabase.keys() 

        def getCommand(line):
            command = ""
            try:    
                command = line.split("[")[1].split("]")[0]
            except:
                #print("Error splitting line "+line)
                command = ""
            return command

        def controlKey(targetKey):
            try:
                l =  targetKey.split("\\")
                return not inDatabaseKey(targetKey) and len(l) > 2 and l[len(l)-1] != "\\" and not inWhiteListKey(targetKey)
            except:
                return False

        def controlKey2(targetKey):
            try:
                l =  targetKey.split("\\")
                return inDatabaseKey(targetKey) and len(l) > 2 and l[len(l)-1] != "\\" and not inWhiteListKey(targetKey)
            except:
                return False
            
        def controlFile(targetFile):
            l =  (clearPath(targetFile)).split("\\")
            return not inDatabaseFile(targetFile) and len(l) > 2 and "C:" in targetFile and not inWhiteListFile(targetFile) and targetFile[len(targetFile)-1] != "\\"

        def controlValue(targetKey, targetValue):
            try:
                l =  targetKey.split("\\")
                return targetKey in KeyDatabase.keys() and len(l) > 2 and l[len(l)-1] != "\\"  and targetValue not in  KeyDatabase[targetKey][1] and not inWhiteListValue(targetKey, targetValue) and targetValue != None and targetValue != ""
            except:
                return False

        def clearFile():
            for i in path_list:
                f = open (i, "w")
                f.write("")
                f.close()              

        def fixActionMaker():
            global last
            if last == 1:                                                                                               #Delete file case
                noExistFiles.remove(len(noExistFiles))
                writeBlackListFile()
            elif last == 2:                                                                                             #Create file case
                toCreateFiles.remove(len(toCreateFiles))
                writeToCreateFile()
            elif last == 3:                                                                                             #Delete Key case
                noExistKeys.remove(len(noExistKeys))
                writeBlackListKey()
            elif last == 4:                                                                                             #Create Key case
                del toCreatekeys[len(toCreatekeys)]
                writeToCreateKey()
            else:
                print("Error fixActionMaker")

        def findPeak(n):
            global previous_n
            global n_equal
            global peak
            
            rangeValue = int((startWeight * 2)/4)
            if n - previous_n >= -rangeValue and n - previous_n < rangeValue:
                val = random.randint(1,100)
                n_equal += 5
                if peak and val <= n_equal:
                    return True
            else:
                n_equal = 0
                if possiblyPeak and n > startWeight + 100:
                    Running.setPeak(win, lab, "Found", "green")
                    peak = True

            previous_n = n
            return False

        def writeResults(it, out):
            out.write("--------MACHINE CONFIGURATION--------\n\n")
            actualEvasionPath = BluePill_evasion_path + str(it) + "/"
            usedLine = []
            for file in os.listdir(actualEvasionPath):
                if "evasion" in file:
                    f = open (actualEvasionPath + file,"r")
                    while (True):
                        try:
                            line = f.readline()
                            break
                        except:
                            None
                    while line != "":
                        command = getCommand(line)
                        if line not in usedLine:
                            usedLine.append(line)
                            for i in commandType.keys():
                                for j in commandType[i]:
                                    if command == j and line not in command_line_flag[i]:
                                        command_line_flag[i].append(line)                                                
                        while (True):
                            try:
                                line = f.readline()
                                break
                            except:
                                None
            for i in command_line_flag.keys():
                if i == "debugFlag" and len(command_line_flag[i])>0:
                    out.write("The malware tries to figure out if it is running under debug:\n")
                    for j in command_line_flag["debugFlag"]:
                        l = j.split(": ")
                        l.remove(l[0])
                        s = ""
                        for k in l:
                            s+=k
                        out.write(s)
                        
                elif i == "getimeFlag" and len(command_line_flag[i])>0:
                    out.write("The malware takes information regarding the machine time:\n")
                    for j in command_line_flag["getimeFlag"]:
                        l = j.split(": ")
                        l.remove(l[0])
                        s = ""
                        for k in l:
                            s+=k
                        out.write(s)
                            
                elif i == "compnameFlag" and len(command_line_flag[i])>0:
                    out.write("The malware takes information regarding the machine name (we recommend the use of a name not attributable to sandobox and vm):\n")
                    for j in command_line_flag["compnameFlag"]:
                        l = j.split(": ")
                        l.remove(l[0])
                        s = ""
                        for k in l:
                            s+=k
                        out.write(s)
                            
                elif i == "usernameFlag" and len(command_line_flag[i])>0:
                    out.write("The malware takes information regarding the username name (we recommend the use of a name not attributable to sandobox and vm):\n")
                    for j in command_line_flag["usernameFlag"]:
                        l = j.split(": ")
                        l.remove(l[0])
                        s = ""
                        for k in l:
                            s+=k
                        out.write(s)
                    
                elif i == "getversionFlag" and len(command_line_flag[i])>0:
                    out.write("The malware takes information regarding the windows version of the machine (the program used windows 7 Ultimate 32 bits):\n")
                    for j in command_line_flag["getversionFlag"]:
                        l = j.split(": ")
                        l.remove(l[0])
                        s = ""
                        for k in l:
                            s+=k
                        out.write(s)
                    
                elif i == "memoryFlag" and len(command_line_flag[i])>0:
                    out.write("The malware takes information regarding ram memory and / or disk (we used ram: tot = 7.7 Gb, available = 3.7 Gb, SSD: tot = 488 Gb, available = 129 Gb)\n")
                    for j in command_line_flag["memoryFlag"]:
                        l = j.split(": ")
                        l.remove(l[0])
                        s = ""
                        for k in l:
                            s+=k
                        out.write(s)
                    
                elif i == "adpterFlag" and len(command_line_flag[i])>0:
                    out.write("The malware takes information regarding internet adapters, such as the MAC Address (we used 06: 02: 27: 9C: BB: 27):\n")
                    for j in command_line_flag["adpterFlag"]:
                        l = j.split(": ")
                        l.remove(l[0])
                        s = ""
                        for k in l:
                            s+=k
                        out.write(s)
                            
                elif i == "monitorFlag" and len(command_line_flag[i])>0:
                    out.write("The Malware takes information regarding monitor size and resolution (we recommend using a real monitor):\n")
                    for j in command_line_flag["monitorFlag"]:
                        l = j.split(": ")
                        l.remove(l[0])
                        s = ""
                        for k in l:
                            s+=k
                        out.write(s)
                            
                elif i == "timeFlag" and len(command_line_flag[i])>0:
                    out.write("The Malware attempts to detect the response time of functions:\n")
                    for j in command_line_flag["timeFlag"]:
                        l = j.split(": ")
                        l.remove(l[0])
                        s = ""
                        for k in l:
                            s+=k
                        out.write(s)
                            
                elif i == "mouseFlag" and len(command_line_flag[i])>0:
                    out.write("The malware monitors the position of the mouse (it is recommended not to keep the mouse still):\n")
                    for j in command_line_flag["mouseFlag"]:
                        l = j.split(": ")
                        l.remove(l[0])
                        s = ""
                        for k in l:
                            s+=k
                        out.write(s)
                                   
                elif i == "keyboardFlag" and len(command_line_flag[i])>0:
                    out.write("The malware takes information regarding the keyboard layout (we used En-uk):\n")
                    for j in command_line_flag["keyboardFlag"]:
                        l = j.split(": ")
                        l.remove(l[0])
                        s = ""
                        for k in l:
                            s+=k
                        out.write(s)
                                   
                elif i == "powerFlag" and len(command_line_flag[i])>0:
                    out.write("The Malware tries to understand if the machine is connected to the current (we recommend doing it):\n")
                    for j in command_line_flag["powerFlag"]:
                        l = j.split(": ")
                        l.remove(l[0])
                        s = ""
                        for k in l:
                            s+=k
                        out.write(s)





        iteration = 0                                                                                                   #Number of AG Iteration
        LastTouchedElement = ""                                                                                         #Last modified Element
        LastTouchedValue = ""                                                                                           #Last modified Key Value

        Running.setText(win, tex, "ArtifactGenerator\n"+'\n', "black")                                                                            

        os.system('VBoxManage snapshot Malware_Evasion take "AG_Snap" --description "AG_Snap"')
        os.system('VBoxManage startvm "Malware_Evasion" --type headless')
        os.system('VBoxManage guestproperty wait "Malware_Evasion" "/VirtualBox/GuestInfo/OS/LoggedInUsers"')    
        time.sleep(8)
        os.system('VBoxManage snapshot Malware_Evasion take "AG_SnapL" --description "AG_SnapL" --live')
        while(True):    
            f = open(Iteration_path, "w")
            f.write(str(iteration))
            f.close()
            
            os.system('VBoxManage --nologo guestcontrol "Malware_Evasion" run --exe "Z://Run_AG.bat" --username Edo --password edoardo1 --wait-stdout ')
            os.system('VBoxManage controlvm "Malware_Evasion" savestate')
            os.system('VBoxManage snapshot Malware_Evasion restore "AG_SnapL"')
            os.system('VBoxManage startvm "Malware_Evasion" --type headless')

            actualEvasionPath = BluePill_evasion_path + str(iteration) + "/"                                            #Path of current evasion.log

            while (True):
                try:
                    f = open (actualEvasionPath+"behaviour.log","r")
                    f.close()
                    break
                except:
                    print("----AG_ActionMaker Error----")
                    os.system('VBoxManage --nologo guestcontrol "Malware_Evasion" run --exe "Z://Run_AG.bat" --username Edo --password edoardo1 --wait-stdout ')

            FilesNumber = 0                                                                                             #Number if files in folder (Different Processes)
            threads = []                                                                                                #Number of different Treads ina file (Process)

            targetKey = ""

            PreviousLine = ""
            add_value = 0
            newFind = 0
            Running.setPeak(win, labFind, newFind, "coral")
            
            for file in os.listdir(actualEvasionPath):                                                                  #Read all files in the folder
                if "evasion" in file:
                    f = open (actualEvasionPath + file,"r")

                    while (True):
                        try:
                            line = f.readline()
                            break
                        except:
                            #print("Error reading line")
                            None

                    while line != "":
                        thread = line.split(":")[0]
                        if thread not in threads :
                            threads.append(thread)
                            
                        command = getCommand(line)                                                                      #Get the Command
                        
                        #-------NTOPENKEY Case--------------------------------------------------------------------------------------------------------------------------
                        if command == "NtOpenKey":                                                                      #REGKEY CASE
                            try:
                                key = line.split("--")[2].strip()
                            except:
                                #print("Error splitting REGKEY commad "+command)
                                key = ""
                            
                            if controlKey(key):                                                                         #Verify the Key Correctness
                                if iteration > 0:
                                    add_value+=100
                                newFind += 1
                                Running.setPeak(win, labFind, newFind, "coral")
                                targetKey = ClearKey(key)
                                isPresent = findKey(targetKey,"")                                                       #Verify if the Key is present
                                weight = calculateWeightKey(targetKey, "")                                              #Calculate the Key Weight
                                KeyDatabase[targetKey] = [weight, [], [isPresent], [""], [False]]                       #Add key to Database
                            elif controlKey2(key):
                                targetKey = ClearKey(key)
                            else:
                                targetKey = ""

                        
                        #--------FILE Case-------------------------------------------------------------------------------------------------------------------------------                                                                 
                        elif command in FileCommandList.keys():
                            targetKey = ""
                            try:
                                mode = line.split("[")[1].split("]")[1].split("--")[1].strip()                          #Get the open modality (Read, Open, ...)
                                targetFile = line.split("[")[1].split("]")[1].split("--")[2].strip()                    #Get the File path
                            except:
                                 #print("Error splitting FILE commad "+command)
                                 targetFile = ""
                            if controlFile(targetFile):                                                                 #Verify the File Correctness
                                newFind += 1
                                Running.setPeak(win, labFind, newFind, "coral")
                                if iteration > 0:
                                    add_value+=100
                                if "?" in targetFile:
                                   targetFile = clearPath(targetFile)
                                weight = calculateWeightFile(command, mode, targetFile)                                 #Calculate the File Weight
                                try:    
                                    isPresent = findFile(targetFile)                                                    #Verify if the File is present
                                    FileDatabase[targetFile] = [weight, isPresent, None, False]                         #Add File to Database
                                except:
                                    l = targetFile.split("\\")
                                    name = l[len(l)-1]
                                    whitelistFile.append(name.upper())
                                    if iteration > 0:
                                        add_value-=100
                                    print("Error file: "+targetFile)
                                    
                        #---------NTQUERYVALUEKEY Case---------------------------------------------------------------------------------------------------------------------
                        if command == "NtQueryValueKey":
                            valueKey = line.split("--")[1].strip()                                                      #Get the Query Value
                            if targetKey != "" and controlValue(targetKey, valueKey):
                                if iteration > 0:
                                    add_value+=50
                                newFind += 1
                                Running.setPeak(win, labFind, newFind, "coral")
                                KeyDatabase[targetKey][1].append(valueKey)                                              #Update the Key Database
                                isPresent = findKey(targetKey, valueKey)                                                #Verify if the Value is present
                                KeyDatabase[targetKey][2].append(isPresent)                                             #Update the Key Database
                                KeyDatabase[targetKey][3].append("")
                                weight = calculateWeightKey(targetKey, valueKey)                                        #Calculate the Key Weight
                                KeyDatabase[targetKey][0] = weight                                                      #Update the Key Database
                                KeyDatabase[targetKey][4].append(False)
                        while (True):
                            try:
                                line = f.readline()
                                break
                            except:
                                None
                        if line == PreviousLine:
                            while (True):
                                try:
                                    line = f.readline()
                                    break
                                except:
                                    None
                        PreviousLine = line
                    f.close()
                FilesNumber += 1

            if len(FileDatabase) == 0 and len(KeyDatabase) == 0:                                                        #Case of no Files and no Keys
                print("No file and Keys queries")
                break

            iterationWeight = int(calculateIterWeight(actualEvasionPath, FilesNumber, len(threads)))             #Calculate the Iteration Weight
            if iteration == 0:
                startWeight = int(iterationWeight)
            plot_x.append(int(iteration))
            plot_y.append(int(iterationWeight))
            IterationDatabase[iteration] = [iterationWeight, noExistFiles.copy(), noExistKeys.copy(), toCreateFiles.copy(), toCreatekeys.copy()]
            if findPeak(int(iterationWeight)):
                break

                        
            if iteration == 0 or IterationDatabase[iteration][0] + 0*add_value > IterationDatabase[iteration-1][0]:
                Running.setText(win, tex, str(iteration+1)+": BETTER THAN PREVIOUS ITERATION "+str(iterationWeight)+'\n', "yellow")
                #print(str(iteration+1)+": BETTER THAN PREVIOUS ITERATION "+str(iterationWeight))
                if iteration > 0 and exitCase() or iteration > 149:
                    break
                LastTouchedElement, LastTouchedValue = actionArtifact()
                if LastTouchedElement == None and LastTouchedValue == None:
                    break
            elif IterationDatabase[iteration][0] + 0*add_value == IterationDatabase[iteration-1][0]:
                Running.setText(win, tex, str(iteration+1)+": EQUAL TO PREVIOUS ITERATION "+str(iterationWeight)+'\n', "yellow")
                #print(str(iteration+1)+": EQUAL TO PREVIOUS ITERATION "+str(iterationWeight))
                p = LastTouchedElement
                restoreArtifact(LastTouchedElement, LastTouchedValue)
                if iteration > 0 and exitCase() or iteration > 149:
                    break
                LastTouchedElement, LastTouchedValue = actionArtifact()
                if LastTouchedElement == None and LastTouchedValue == None:
                    break
            else:
                Running.setText(win, tex, str(iteration+1)+": WORSE THAN PREVIOUS ITERATION "+str(iterationWeight)+'\n', "yellow")
                #print(str(iteration+1)+": WORSE THAN PREVIOUS ITERATION "+str(iterationWeight))
                if iteration > 0 and exitCase() or iteration > 149:
                    break
                restoreArtifact(LastTouchedElement, LastTouchedValue)

            iteration += 1
            Running.setPeak(win, labIter, iteration, "coral")

        try:
            os.system('VBoxManage controlvm Malware_Evasion poweroff')
            os.system('VBoxManage snapshot Malware_Evasion delete "AG_SnapL"')
            os.system('VBoxManage snapshot Malware_Evasion delete "AG_Snap"')
        except:
            print("Error during VM shutdown")
        
        try:
            f = open("report.txt","w")
            f.close()
            f = open("report.txt","a")
            f.write("ArtifactGenerator\n")
            print("")
            print("")
            f.write("\n")
            f.write("--------FILE AND KEY CONFIGURATION--------\n\n")
            bestIt, perc = getBestIteration()
            print("FILES TO BE DELETED")
            f.write("FILES TO BE DELETED\n")
            for i in IterationDatabase[bestIt][1]:
                print (i)
                f.write(i+"\n")
            f.write("\n")
            print("")
            print("FILES TO BE CREATED")
            f.write("FILES TO BE CREATED\n")
            for i in IterationDatabase[bestIt][3]:
                print (i)
                f.write(i+"\n")
            f.write("\n")
            print("")
            print("KEYS TO BE DELETED")
            f.write("KEYS TO BE DELETED\n")
            for i in IterationDatabase[bestIt][2]:
                if i.split(";")[1] != "":
                    print (i.split(";")[0]+"  Value: "+i.split(";")[1])
                    f.write(i.split(";")[0]+"  Value: "+i.split(";")[1]+"\n")
                else:
                    print(i.split(";")[0])
                    f.write(i.split(";")[0]+"\n")
            f.write("\n")
            print("")
            print("KEYS TO BE CREATED")
            f.write("KEYS TO BE CREATED\n")
            for i in IterationDatabase[bestIt][4]:
                if i.split(";")[1] != "":
                    print (i.split(";")[0]+"  Value: "+i.split(";")[1])
                    f.write(i.split(";")[0]+"  Value: "+i.split(";")[1]+"\n")
                else:
                    print(i.split(";")[0])
                    f.write(i.split(";")[0]+"\n")
            print("")
            f.write("\n")
            print("")
            f.write("\n")
            writeResults(bestIt, f)
            print("")
            f.write("\n")
            print("")
            f.write("\n")
            print("The complete report is in: "+BluePill_evasion_path + str(bestIt) + "/  with an increment of: "+str(perc)+"%")
            f.write("The complete report is in: "+BluePill_evasion_path + str(bestIt) + "/  with an increment of: "+str(perc)+"%")
            f.close()
            clearFile()
            plt.plot(plot_x,plot_y)
            plt.xlabel("Iteration")
            plt.ylabel("Value")
            plt.show()
        except:
            print("Error in during Report Writing")






class Running:    
    def __init__(self, win):
        tex = Text(win)
        tex.place(x=10, y=40, height=550, width=580)
        lab = Label(win, text="Peak Status = ", font=("Helvetica", 10))
        lab.place(x=10, y=10)
        lab2 = Label(win, text="None", font=("Helvetica", 10), fg ="coral")
        lab2.place(x=100, y=10)
        lab3 = Label(win, text="New Find = ", font=("Helvetica", 10))
        lab3.place(x=250, y=10)
        lab4 = Label(win, text="0", font=("Helvetica", 10), fg ="coral")
        lab4.place(x=320, y=10)
        lab5 = Label(win, text="Iteration = ", font=("Helvetica", 10))
        lab5.place(x=500, y=10)
        lab6 = Label(win, text="0", font=("Helvetica", 10), fg ="coral")
        lab6.place(x=560, y=10)
        p=threading.Thread(target=AG, args=(win, tex, lab2, lab4, lab6))
        p.start()
 
    def setText(self, tex, s, color):
        tex.insert(END, str(s))
        tex.see(END)

    def setPeak(self, lab2, s, c):
        lab2.config(text=s, fg=c)

class Main:
    def add(self):
        windowL=Tk()
        mywin=Running(windowL)
        windowL.title('Artifact Generator')
        windowWidth = windowL.winfo_reqwidth()
        windowHeight = windowL.winfo_reqheight()
        positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2 -200)
        positionDown = int(window.winfo_screenheight()/2 - windowHeight/2- 230)
        windowL.geometry("600x600+{}+{}".format(positionRight, positionDown))
        windowL.mainloop()
        
    def __init__(self, win):
        nameI=Entry(win)
        nameI.insert(0, 'Add Malware File')
        nameI.place(x=110, y=83)

        self.lbl=Label(win, text="Artifact Generator", font=("Helvetica", 16))
        self.lbl.place(x=100, y=30)
      
        self.btn=Button(win, text="+",height = 1, command=self.add)
        self.btn.place(x=240, y=80)
        


window=Tk()
mywin=Main(window)
window.title('Artifact Generator')
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(window.winfo_screenheight()/2 - windowHeight/2)
window.geometry("360x200+{}+{}".format(positionRight, positionDown))
window.mainloop()
