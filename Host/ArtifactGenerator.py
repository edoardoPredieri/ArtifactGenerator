import os
import time
from winreg import *
from matplotlib import pyplot as plt


BluePill_evasion_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/out/"             #Path of evasion.log files
BluePill_blackListFile_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/in/blacklistFile.txt" #Path to blacklist file
BluePill_blackListKey_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/in/blacklistKey.txt"   #Path to blacklist key

ToCreateFile_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/in/toCreateFile.txt" #Path to 
ToCreateKey_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/in/toCreateKey.txt"   #Path to
Iteration_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/in/iteration.txt"

findFile_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/find/toSearchFile.txt"
responseFile_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/find/responseFile.txt"
findKey_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/find/toSearchKey.txt"
responseKey_path = "C:/Users/PredieriEd/Desktop/Shared_Mal_Folder/find/responseKey.txt"

path_list = [BluePill_blackListFile_path, BluePill_blackListKey_path, ToCreateFile_path, ToCreateKey_path, Iteration_path, findFile_path, responseFile_path,
             findKey_path, responseKey_path]

#Weighted list of file manipulation commands
FileCommandList = {"CreateFile" : 1, "CreateFileA" : 1, "CreateFileW" : 1,
                   "GetFileAttributesA" : 4, "GetFileAttributesW" : 4, "GetFileAttributes" : 4,
                   "OpenFile" : 2,
                   "PathFileExists" : 5, "PathFileExistsA" : 5, "PathFileExistsW" : 5,
                   "FindFirstFile" : 4, "FindFirstFileA" : 4, "FindFirstFileW" : 4, "FindFirstFileEx" : 4, "FindFirstFileExA" : 4, "FindFirstFileExW" : 4,
                   "NtCreateFile" : 3,
                   "GetModuleFileName" : 2, "GetModuleFileNameA" :2 , "GetModuleFileNameW" :2}

#Weighted list of file open modalities
ModeList = {"Create" : 1, "Replace/Create" : 1, "Overwrite/Create" :1,
            "Delete" : 1,
            "Exist" : 5,
            "Read" : 4, "Read/Write" : 4,
            "Open" :4 , "Open/Create" : 4,
            "Write" : 4, "Overwrite" : 4,
            "Search" : 5,
            "Unknow" : 2}

#Weighted list of file names
FileNameList = {"VIRTUALBOX" : 5, "VBOX" : 5, "ORACLE" : 5, "GUEST" : 4, "PHYSICALDRIVE" : 4, "VM" : 4,
		"VMMOUSE" : 5, "HGFS" : 5, "VMHGFS" : 5, "VMCI" : 5, "VMWARE" : 5, "VBOXMOUSE" : 5, "VBOXGUEST" : 5, "VBOXSF" : 5, "VBOXVIDEO" :5,
                "LOADDLL" : 3,
                "EMAIL" : 2,
                "SANDBOX" : 5,
                "SAMPLE" : 3,
                "VIRUS" : 5,
                "FOOBAR" : 3,
                "DRIVERS\\PRLETH" : 4, "DRIVERS\\PRLFS" : 4, "DRIVERS\\PRLMOUSE" : 4, "DRIVERS\\PRLVIDEO" : 4, "DRIVERS\\TIME" : 4,
                "*.*" : 2,
                "SERVICES.EXE": 10}

#Weighted Regkeys path
RegKeyList = {"sandbox" : 5, "Hyper-V" : 5,
              "VirtualMachine" : 5, "Virtual Machine" : 5,
              "\\SYSTEM\\ControlSet001\\Services" : 5, "\\SYSTEM\\CurrentControlSet\\Enum\\PCI" : 5,
              "\\SYSTEM\\CurrentControlSet\\Services\SbieDrv" : 5, "\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Sandboxie" : 5,
              "\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_80EE" : 5, "VBOX" : 5, "Vbox" : 5, "VirtualBox Guest Additions" :5, "Oracle" : 5,
              "\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_5333" : 5, "\\SYSTEM\\ControlSet001\\Services\\vpcbus" : 5, "\\SYSTEM\\ControlSet001\\Services\\vpc-s3" : 5, "\\SYSTEM\\ControlSet001\\Services\\vpcuhub" : 5,
              "\\SYSTEM\\ControlSet001\\Services\\msvmmouf" : 5,
              "\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_15AD" : 5, "VMware" : 5, "vmware" : 5, "VMWARE" : 5, "vmdebug" : 5, "vmmouse" : 5, "VMTools" : 5, "VMMEMCTL" : 5, "vmci" : 5, "vmx86" : 5,
              "Wine" : 4,
              "xen" :4,
              "\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" : 3,
              "Rpc": 4}

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
GeneralCommandList = {"IsDebuggerPresent" : 5, "CheckRemoteDebuggerPresent" : 5,
                      "GetLocalTime" : 3, "GetSystemTimeAsFileTime" : 3, "GetTimeZoneInformation" : 3,
                      "GetComputerNameA" : 3, "GetComputerNameW" :3,
                      "GetUserDefaultLCID" : 2,
                      "GetUserName" : 2, "GetUserNameA" :2, "GetUserNameW" :2,
                      "GetVersion" : 1, "GetVersionEx" :1 , "GetVersionExA" :1, "GetVersionEx" :1,
                      "GlobalMemoryStatusEx" : 2,
                      "getenv" : 2,
                      "GetAdaptersInfo" : 3,
                      "GetMonitorInfo" : 2, "GetMonitorInfoA" : 2 , "GetMonitorInfoW" : 2, "EnumDisplayDevices" : 2,
                      "GetDesktopWindow" :2, "GetWindowRect" : 2,
                      "NtDelayExecution" :4, "NtQueryPerformanceCounter" :4,
                      "FindNextFile" : 2, "FindNextFileA" : 2, "FindNextFileW" : 2,
                      "GetSystemInfo" : 2,
                      "GetCursorPos" : 3,
                      "FindWindow" : 3, "FindWindowW" : 3, "FindWindowA" : 3,
                      "WNetGetProviderName" : 4, "WNetGetProviderNameW" : 4, "WNetGetProviderNameA" : 4,
                      "GetKeyboardLayout" : 3, "GetKeyboardLayout-lib" : 3,
                      "GetPwrCapabilities" : 5,
                      "ChangeServiceConfigW" : 2,
                      "SetupDiGetDeviceRegistryProperty" : 2, "SetupDiGetDeviceRegistryPropertyW" : 2, "SetupDiGetDeviceRegistryPropertyA" : 2,
                      "GetWindowText" : 3, "GetWindowTextA" : 3, "GetWindowTextW" : 3, "FindWindow" : 3,
                      "LoadLibraryA" : 2, "LoadLibraryW" : 2, "LoadLibraryExA" :2 , "LoadLibraryExW" :2,
                      "GetDiskFreeSpaceEx" :2 , "GetDiskFreeSpaceExW" :2 , "GetDiskFreeSpaceExA" :2,
                      "GetTickCount" :4, "SetTimer" : 4, "WaitForSingleObject" : 4, "GetSystemTimeAsFileTime" :4 , "IcmpCreateFile" : 4, "IcmpSendEcho" : 4,
                      "WMI-Query" : 5,
                      "NtQueryDO" : 2,
                      "NtOpenKey" : 2, "NtEnumerateKey" :2 , "NtQueryValueKey":2 , "NtQueryAttributesFile" :2}

#List of Files to not modificate
whitelistFile = ["SVCHOST.EXE", "ACLAYERS.DLL", "CMD.EXE", "SORTDEFAULT.NLS", "DESKTOP.INI", "EE.EXE", "EDO", "APPDATA", "USERS", "MOUNTPOINTMANAGER", "EN", "STATICCACHE.DAT", "OLEACCRC.DLL", "ACXTRNAL.DLL", "MSVFW32.DLL.MUI", "AVICAP32.DLL.MUI",
                 "KERNELBASE.DLL.MUI", "MSCTF.DLL.MUI", "WERFAULT.EXE.MUI", "FAULTREP.DLL.MUI", "DWM.EXE", "EXPLORER.EXE", "WMIPRVSE.EXE", "PIN.EXE", "RSAENH.DLL", "SXBOY.EXE"]

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
                "Machine\\SYSTEM\\CurrentControlSet\\Services\\WinSock2\\Parameters", "Machine\\SYSTEM\\CurrentControlSet\\control\\NetworkProvider\\HwOrder", "Machine\\SYSTEM\\CurrentControlSet\\Services\\Winsock2\\Parameters", "Machine\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Custom\\uninstal.bat",
                "Machine\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Layers", "Machine\\SYSTEM\\CurrentControlSet\\Control\\SQMServiceList", "Machine\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\WinOldApp",
                "Machine\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\WOW\\boot", "Machine\\SOFTWARE\\Microsoft\\SQMClient\\Windows", "Machine\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags", "Machine\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\GRE_Initialize",
                "Machine\\SYSTEM\\CurrentControlSet\\Control\\Nls\\CustomLocale", "Machine\\SOFTWARE\\Microsoft\\CTF\\KnownClasses", "Machine\\SOFTWARE\\Microsoft\\CTF\\DirectSwitchHotkeys", "Machine\\SOFTWARE\\Policies\\Microsoft\\SQMClient\\Windows", "Machine\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer",
                "Machine\\SYSTEM\\CurrentControlSet\\Control\\ComputerName\\ActiveComputerName", "Machine\\CONTROL\\NetworkProvider\\HwOrder", "Machine\\SYSTEM\\CurrentControlSet\\Services\\Winsock\\Parameters", "Machine\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters\\Winsock",
                "Machine\\SYSTEM\\CurrentControlSet\\Services\\Psched\\Parameters\\Winsock", "Machine\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Winsock", "Machine\\SYSTEM\\CurrentControlSet\\Services\\RDPNP\\NetworkProvider", "Machine\\SYSTEM\\CurrentControlSet\\Services\\WebClient\\NetworkProvider",
                "Machine\\SYSTEM\\CurrentControlSet\\Services\\DNS"]

whitelistValue = [["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "RunDiagnosticLoggingApplicationManagement"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\GRE_Initialize", "DisableMetaFiles"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options", "EnableDefaultReply"],
                  ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "NotifySettingChanges"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "ExecutablesToTrace"], ["Machine\MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers", "C:\Pin311\ee.exe"],
                  ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "ShutdownTimeout"], ["MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatibility", "DisableAppCompat"], ["Machine\SOFTWARE\Policies\Microsoft\MUI\Settings", "PreferredUILanguages"],
                  ["Machine\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run", "Policies"], ["Machine\SOFTWARE\Microsoft\Cryptography\Defaults\Provider\Microsoft Strong Cryptographic Provider", "Image Path"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "Load"],
                  ["Machine\SOFTWARE\Microsoft\Windows\CurrentVersion\Setup", "SourcePath"], ["Machine\SOFTWARE\Microsoft\Windows\CurrentVersion", "DevicePath"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AeDebug", "Auto"]]


noExistFiles = []           #List of Files to be "delete" through BluePill
noExistKeys = []            #List of Keys to be "delete" through BluePill

toCreateFiles = []
toCreatekeys = {}

FileDatabase = {}           #File: [weight, isPresent, endAction, flag]
KeyDatabase = {}            #Key:  [weight, valueKey[], isPresent[], endAction[], flag[]]
IterationDatabase = {}      #Iteration: [FileDatabase, weight]

plot_x = []
plot_y = []

last = 0

n_equal = 0
previous_n = 0
peak = False


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
    for i in toCreatekeys.keys():
        f.write(i+";"+toCreatekeys[i]+'\n')
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
        if k in key:
            valueKey = RegKeyList[k]

    for k in RegKeyValueList.keys():
        if k in key:
            if value in RegKeyValueList[k]:
                valueValue = RegKeyValueList[k][0]
                return (valueKey + valueValue) / 2
    return valueKey


def calculateIterWeight(actualEvasionPath, initialLinenumber, initialFilesNumber, initialThreadsNumber):
    endFilesNumber = 0
    commandsWeight = 0
    threads = []
    linesNumber = 0
    lastLine = ""
    for file in os.listdir(actualEvasionPath):
        if "evasion" in file:
            f = open (actualEvasionPath + file,"r")
            line = f.readline()
            while line != "":
                thread = line.split(":")[0]
                if thread not in threads :
                    threads.append(thread)
                try:
                    command = line.split("[")[1].split("]")[0]
                except:
                    command = ""
                if command in GeneralCommandList.keys() and line != lastLine:
                    commandsWeight += GeneralCommandList[command]
                if command in FileCommandList.keys() and line != lastLine:
                    commandsWeight += FileCommandList[command]
                lastLine = line
                linesNumber += 1
                line = f.readline()
            f.close()
        endFilesNumber += 1 
    FilesNumberDiff = endFilesNumber - initialFilesNumber          #Processes Number Difference
    ThreadsNumberDiff =  len(threads) - initialThreadsNumber       #Threads Number Difference
    lineNumberDiff = linesNumber - initialLinenumber               #Lines Number Difference
    return (commandsWeight + 2*(lineNumberDiff)) * (FilesNumberDiff + ThreadsNumberDiff +1)


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
             print("Deleting: "+importantFile+"...")
             l = importantFile.split("\\")
             name = l[len(l)-1]
             path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1])
             if name == "*.*":
                if path+"ag.txt" in toCreateFiles:
                    toCreateFiles.remove((path+"ag"+name[1:len(name)]))
                    writeToCreateFile()
                    FileDatabase[importantFile][1] = 0
                    FileDatabase[importantFile][3] = True
                noExistFiles.append((path+"ag.txt").upper())
                writeBlackListFile()
             elif "*" in name:
                if path+"ag"+name[1:len(name)] in toCreateFiles:
                    toCreateFiles.remove((path+"ag"+name[1:len(name)]))
                    writeToCreateFile()
                    FileDatabase[importantFile][1] = 0
                    FileDatabase[importantFile][3] = True
                noExistFiles.append(path+"ag"+name[1:len(name)])
                writeBlackListFile()
             else:
                 if importantFile in toCreateFiles:
                    toCreateFiles.remove(importantFile)
                    writeToCreateFile()
                    FileDatabase[importantFile][1] = 0
                    FileDatabase[importantFile][3] = True
                 noExistFiles.append(importantFile.upper())
                 writeBlackListFile()
             FileDatabase[importantFile][1] = 0
        else:
            last = 2
            print("Creating: "+importantFile+"...")
            l = importantFile.split("\\")
            name = l[len(l)-1]
            path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1])
            if name == "*.*":
                if (path+"ag.txt").upper() in noExistFiles:
                    noExistFiles.remove((path+"ag.txt").upper())
                    writeBlackListFile()
                    FileDatabase[importantFile][1] = 1
                    FileDatabase[importantFile][3] = True
                toCreateFilesappend(path+"ag.txt")
                writeToCreateFile()
            elif "*" in name:
                if (path+"ag"+name[1:len(name)]).upper() in noExistFiles:
                    noExistFiles.remove((path+"ag"+name[1:len(name)]).upper())
                    writeBlackListFile()
                    FileDatabase[importantFile][1] = 1
                    FileDatabase[importantFile][3] = True
                toCreateFiles.append(path+"ag"+name[1:len(name)])
                writeToCreateFile()
            else:
                if importantFile.upper() in noExistFiles:
                    noExistFiles.remove(importantFile.upper())
                    writeBlackListFile()
                    FileDatabase[importantFile][1] = 1
                    FileDatabase[importantFile][3] = True
                toCreateFiles.append(importantFile)
                writeToCreateFile()
            FileDatabase[importantFile][1] = 1
        FileDatabase[importantFile][3] = True
        return importantFile, None
            
    else:
        if len(KeyDatabase[importantKey][1]) == 0 or importantValue == None:
            if KeyDatabase[importantKey][2][0] == 1:
                last = 3
                print("Deleting: "+importantKey+"...")
                if importantKey in toCreatekeys.keys():
                    del toCreatekeys[importantKey]
                    writeToCreateKey()
                    KeyDatabase[importantKey][2][0] = 0
                    KeyDatabase[importantKey][4][0] = True
                noExistKeys.append(importantKey.upper()+";")
                writeBlackListKey()
                KeyDatabase[importantKey][2][0] = 0
            else:
                last = [importantKey]
                print("Creating: "+importantKey+"...")
                if importantKey.upper()+";" in noExistKeys:
                    noExistKeys.remove(importantKey.upper()+";")
                    writeBlackListKey()
                    KeyDatabase[importantKey][2][0] = 1
                    KeyDatabase[importantKey][4][0] = True
                toCreatekeys[importantKey] = ""
                writeToCreateKey()
                KeyDatabase[importantKey][2][0] = 1
            KeyDatabase[importantKey][4][0] = True
            return importantKey, None

        else:
            pos = (KeyDatabase[importantKey][1]).index(importantValue) + 1
            if KeyDatabase[importantKey][2][pos] == 1:
                last = 3
                print("Deleting: "+importantKey+"  "+importantValue+"...")
                if importantKey in toCreatekeys.keys() and toCreatekeys[importantKey] == importantValue:
                    del toCreatekeys[importantKey]
                    writeToCreateKey()
                    KeyDatabase[importantKey][2][pos] = 0
                    KeyDatabase[importantKey][4][pos] = True
                noExistKeys.append(importantKey+";"+importantValue.upper())
                writeBlackListKey()
                KeyDatabase[importantKey][2][pos] = 0
            else:
                last = 4
                print("Creating: "+importantKey+"  "+importantValue+"...")
                if "A;"+importantValue.upper() in noExistKeys:
                    noExistKeys.remove(importantKey+";"+importantValue.upper())
                    writeBlackListKey()
                    KeyDatabase[importantKey][2][pos] = 1
                    KeyDatabase[importantKey][4][pos] = True 
                toCreatekeys[importantKey] = importantValue
                writeToCreateKey()
                KeyDatabase[importantKey][2][pos] = 1
            KeyDatabase[importantKey][4][pos] = True
            return importantKey, importantValue

        
def restoreArtifact(LastTouchedElem, LastTouchedValue):
    global last
    if LastTouchedElem in FileDatabase.keys():
        if FileDatabase[LastTouchedElem][1] == 1:
            print("Deleting: "+LastTouchedElem+"...")
            l = LastTouchedElem.split("\\")
            name = l[len(l)-1]
            path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1])
            if name == "*.*":
                if (path+"ag.txt") in toCreateFiles:
                    toCreateFiles.remove((path+"ag"+name[1:len(name)]))
                    writeToCreateFile()
                    FileDatabase[LastTouchedElem][1] = 0
                    FileDatabase[LastTouchedElem][3] = True
                if last == 2 or last == 4:
                    noExistFiles.append((path+"ag.txt").upper())
                    writeBlackListFile()
            elif "*" in name:
               if path+"ag"+name[1:len(name)] in toCreateFiles:
                   toCreateFiles.remove((path+"ag"+name[1:len(name)]))
                   writeToCreateFile()
                   FileDatabase[LastTouchedElem][1] = 0
                   FileDatabase[LastTouchedElem][3] = True
               if last == 2 or last == 4:
                   noExistFiles.append(path+"ag"+name[1:len(name)])
                   writeBlackListFile()
            else:
                if LastTouchedElem in toCreateFiles:
                   toCreateFiles.remove(LastTouchedElem)
                   writeToCreateFile()
                   FileDatabase[LastTouchedElem][1] = 0
                   FileDatabase[LastTouchedElem][3] = True
                if last == 2 or last == 4:
                    noExistFiles.append(LastTouchedElem.upper())
                    writeBlackListFile()
            FileDatabase[LastTouchedElem][1] = 0
        else:
            last = 2
            print("Creating: "+LastTouchedElem+"...")
            l = LastTouchedElem.split("\\")
            name = l[len(l)-1]
            path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1])
            if name == "*.*":
                if (path+"ag.txt").upper() in noExistFiles:
                    noExistFiles.remove((path+"ag.txt").upper())
                    writeBlackListFile()
                    FileDatabase[LastTouchedElem][1] = 1
                    FileDatabase[LastTouchedElem][3] = True
                    return
                toCreateFiles.append(path+"ag.txt")
                writeToCreateFile()
            elif "*" in name:
                if (path+"ag"+name[1:len(name)]).upper() in noExistFiles:
                    noExistFiles.remove((path+"ag"+name[1:len(name)]).upper())
                    writeBlackListFile()
                    FileDatabase[LastTouchedElem][1] = 1
                    FileDatabase[LastTouchedElem][3] = True
                    return
                toCreateFiles.append(path+"ag"+name[1:len(name)])
                writeToCreateFile()
            else:
                if LastTouchedElem.upper() in noExistFiles:
                    noExistFiles.remove(LastTouchedElem.upper())
                    writeBlackListFile()
                    FileDatabase[LastTouchedElem][1] = 1
                    FileDatabase[LastTouchedElem][3] = True
                    return
                toCreateFiles.append(LastTouchedElem)
                writeToCreateFile()
            FileDatabase[LastTouchedElem][1] = 1
        FileDatabase[LastTouchedElem][3] = True
        return

    elif LastTouchedElem in KeyDatabase.keys():
        if len(KeyDatabase[LastTouchedElem][1]) == 0 or LastTouchedValue == None:
            if KeyDatabase[LastTouchedElem][2][0] == 1:
                print("Deleting: "+LastTouchedElem+"...")
                if LastTouchedElem in toCreatekeys.keys():
                    del toCreatekeys[LastTouchedElem]
                    writeToCreateKey()
                    KeyDatabase[LastTouchedElem][2][0] = 0
                    KeyDatabase[LastTouchedElem][4][0] = True
                if last == 2 or last == 4:
                    noExistKeys.append(LastTouchedElem.upper()+";")
                    writeBlackListKey()
                KeyDatabase[LastTouchedElem][2][0] = 0
            else:
                last = 4
                print("Creating: "+LastTouchedElem+"...")
                if LastTouchedElem.upper()+";" in noExistKeys:
                    noExistKeys.remove(LastTouchedElem.upper()+";")
                    writeBlackListKey()
                    KeyDatabase[LastTouchedElem][2][0] = 1
                    KeyDatabase[LastTouchedElem][4][0] = True
                    return
                toCreatekeys[LastTouchedElem] = ""
                writeToCreateKey()
                KeyDatabase[LastTouchedElem][2][0] = 1
            KeyDatabase[LastTouchedElem][4][0] = True
            return
        else:
            pos = (KeyDatabase[LastTouchedElem][1]).index(LastTouchedValue) + 1
            if KeyDatabase[LastTouchedElem][2][pos] == 1:
                last = 3
                print("Deleting: "+LastTouchedElem+"  "+LastTouchedValue+"...")
                if LastTouchedElem in toCreatekeys.keys() and toCreatekeys[LastTouchedElem] == LastTouchedValue:
                    del toCreatekeys[LastTouchedElem]
                    writeToCreateKey()
                    KeyDatabase[LastTouchedElem][2][pos] = 0
                    KeyDatabase[LastTouchedElem][4][pos] = True
                    return
                noExistKeys.append(LastTouchedElem+";"+LastTouchedValue.upper())
                writeBlackListKey()
                KeyDatabase[LastTouchedElem][2][pos] = 0
            else:
                last = 4
                print("Creating: "+LastTouchedElem+"  "+LastTouchedValue+"...")
                if "A;"+LastTouchedElem.upper() in noExistKeys:
                    noExistKeys.remove(LastTouchedElem+";"+LastTouchedValue.upper())
                    writeBlackListKey()
                    KeyDatabase[LastTouchedElem][2][pos] = 1
                    KeyDatabase[LastTouchedElem][4][pos] = True
                    return
                toCreatekeys[LastTouchedElem] = LastTouchedValue
                writeToCreateKey()
                KeyDatabase[LastTouchedElem][2][pos] = 1
            KeyDatabase[LastTouchedElem][4][pos] = True
            


def validationElem(elem, value, mode): 
    if elem in FileDatabase.keys():
        if mode == 0:                                       #Better Case
            if FileDatabase[elem][1] == 1:
                FileDatabase[elem][2] = "To be Created"
            else:
                FileDatabase[elem][2] = "To be Deleted"
        elif mode == 1:                                     #Equal Case
            FileDatabase[elem][2] = "No modification"
        else:                                               #Worse Case
            if FileDatabase[elem][1] == 0:
                FileDatabase[elem][2] = "To be Created"
            else:
                FileDatabase[elem][2] = "To be Deleted"
    elif elem in KeyDatabase.keys():
        if value:
            pos = (KeyDatabase[elem][1]).index(value) + 1
            if mode == 0:                                       #Better Case
                if KeyDatabase[elem][2][pos] == 1:
                    KeyDatabase[elem][3][pos] = "To be Created"
                else:
                    KeyDatabase[elem][3][pos] = ("To be Deleted")
            elif mode == 1:                                     #Equal Case
                KeyDatabase[elem][3][pos] = ("No modification")
            else:                                               #Worse Case
                if KeyDatabase[elem][2][pos] == 0:
                    KeyDatabase[elem][3][pos] = ("To be Created")
                else:
                    KeyDatabase[elem][3][pos] = ("To be Deleted")
        else:
            if mode == 0:                                       #Better Case
                if KeyDatabase[elem][2][0] == 1:
                    KeyDatabase[elem][3][0] = "To be Created"
                else:
                    KeyDatabase[elem][3][0] = "To be Deleted"
            elif mode == 1:                                     #Equal Case
                KeyDatabase[elem][3][0] = "No modification"
            else:                                               #Worse Case
                if KeyDatabase[elem][2][0] == 0:
                    KeyDatabase[elem][3][0] = "To be Created"
                else:
                    KeyDatabase[elem][3][0] = "To be Deleted"


def exitCase():
    for file in FileDatabase.keys():
        if FileDatabase[file][2] == None:
            return False
    for key in KeyDatabase.keys():
        if len(KeyDatabase[key][1]) > 0:
            for j in range(len(KeyDatabase[key][1])):
                if KeyDatabase[key][3][j+1] == "":
                    return False
        else:
            if KeyDatabase[key][3][0] == "":
                    return False
    return True


def clearPath(targetFile):
    l = targetFile.split("\\")
    path = ""
    for elem in l[2:len(l)]:
        if elem != l[len(l)-1]:
            path += str(elem)+"\\\\"
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
        #val = calculateIterWeight(IterationDatabase[i][2], IterationDatabase[i][4], IterationDatabase[i][5], IterationDatabase[i][6])
        val = int(IterationDatabase[i][0])
        if val > maxx:
            maxx = val
            best = i
    return best, 100 - ((minn*100)/maxx)


def inWhiteListFile(file):
    l = file.split("\\")
    name = l[len(l)-1]
    return name in whitelistFile


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
        print("Error splitting line "+line)
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
    return not inDatabaseFile(targetFile) and len(targetFile) > 3 and "C:" in targetFile and not inWhiteListFile(targetFile.upper()) and targetFile[len(targetFile)-1] != "\\"


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
    if previous_n - n <= 5 or previous_n - n > 5:
        n_equal += 1
        if peak and n_equal >= 10:
            return True
    else:
        n_equal = 0
        if n > 8000:
            peak = True


    previous_n = n
    return False
    
    



iteration = 0                                                                                                   #Number of AG Iteration
LastTouchedElement = ""                                                                                         #Last modified Element
LastTouchedValue = ""                                                                                           #Last modified Key Value
                                                                            
print("ArtifactGenerator")
print("")

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
           
    actualEvasionPath = BluePill_evasion_path + str(iteration) + "/"                                            #Path of current evasion.log

    try:
        f = open (actualEvasionPath+"behaviour.log","r")
        f.close()
    except:
        print("----AG_ActionMaker Error----")
        fixActionMaker()
        os.system('VBoxManage --nologo guestcontrol "Malware_Evasion" run --exe "Z://Run_AG.bat" --username Edo --password edoardo1 --wait-stdout ')

    FilesNumber = 0                                                                                             #Number if files in folder (Different Processes)
    LinesNumber = 0                                                                                             #Number of lines (Commands) in the file
    threads = []                                                                                                #Number of different Treads ina file (Process)

    targetKey = ""

    PreviousLine = ""
    add_value = 0
    
    for file in os.listdir(actualEvasionPath):                                                                  #Read all files in the folder
        if "evasion" in file:
            f = open (actualEvasionPath + file,"r")

            try:
                line = f.readline()
            except:
                #print("Error reading line")
                line = f.readline()

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
                        if iteration > 0:
                            add_value+=100
                        if "?" in targetFile:
                           targetFile = clearPath(targetFile)
                        weight = calculateWeightFile(command, mode, targetFile)                                 #Calculate the File Weight
                        try:    
                            isPresent = findFile(targetFile)                                                    #Verify if the File is present
                            FileDatabase[targetFile] = [weight, isPresent, None, False]                         #Add File to Database
                        except:
                            print("Error file: "+targetFile)
                            
                #---------NTQUERYVALUEKEY Case---------------------------------------------------------------------------------------------------------------------
                if command == "NtQueryValueKey":
                    valueKey = line.split("--")[1].strip()                                                      #Get the Query Value
                    if targetKey != "" and controlValue(targetKey, valueKey):
                        if iteration > 0:
                            add_value+=30
                        KeyDatabase[targetKey][1].append(valueKey)                                              #Update the Key Database
                        isPresent = findKey(targetKey, valueKey)                                                #Verify if the Value is present
                        KeyDatabase[targetKey][2].append(isPresent)                                             #Update the Key Database
                        KeyDatabase[targetKey][3].append("")
                        weight = calculateWeightKey(targetKey, valueKey)                                        #Calculate the Key Weight
                        KeyDatabase[targetKey][0] = weight                                                      #Update the Key Database
                        KeyDatabase[targetKey][4].append(False)

                LinesNumber += 1
                try:
                    line = f.readline()
                except:
                    print("Error reading line")
                    line = f.readline()
                if line == PreviousLine:
                    line = f.readline()
                PreviousLine = line
            f.close()
        FilesNumber += 1

    if len(FileDatabase) == 0 and len(KeyDatabase) == 0:                                                        #Case of no Files and no Keys
        print("No file and Keys queries")
        break

    iterationWeight = int(calculateIterWeight(actualEvasionPath, LinesNumber, FilesNumber, len(threads))) #+ add_value            #Calculate the Iteration Weight
    plot_x.append(int(iteration))
    plot_y.append(int(iterationWeight))
    IterationDatabase[iteration] = [iterationWeight, noExistFiles.copy(), noExistKeys.copy(), toCreateFiles.copy(), toCreatekeys.copy()]
    if findPeak(int(iterationWeight)):
        break
    
    if iteration == 0 or IterationDatabase[iteration][0] > IterationDatabase[iteration-1][0]:
        print(str(iteration)+": BETTER THAN PREVIOUS ITERATION "+str(iterationWeight))
        if iteration > 0:
            validationElem(LastTouchedElement, LastTouchedValue, 0)
        if iteration > 0 and exitCase() or iteration > 200:
            break
        LastTouchedElement, LastTouchedValue = actionArtifact()
        if LastTouchedElement == None and LastTouchedValue == None:
            break
    elif IterationDatabase[iteration][0] == IterationDatabase[iteration-1][0]:
        print(str(iteration)+": EQUAL TO PREVIOUS ITERATION "+str(iterationWeight))
        p = LastTouchedElement
        restoreArtifact(LastTouchedElement, LastTouchedValue)
        validationElem(LastTouchedElement, LastTouchedValue, 1)
        if iteration > 0 and exitCase() or iteration > 200:
            break
        LastTouchedElement, LastTouchedValue = actionArtifact()
        if LastTouchedElement == None and LastTouchedValue == None:
            break
    else:
        print(str(iteration)+": WORSE THAN PREVIOUS ITERATION "+str(iterationWeight))
        validationElem(LastTouchedElement, LastTouchedValue, 2)
        if iteration > 0 and exitCase() or iteration > 200:
            break
        restoreArtifact(LastTouchedElement, LastTouchedValue)

    os.system('VBoxManage snapshot Malware_Evasion restore AG_SnapL')
    iteration += 1

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
    bestIt, perc = getBestIteration()
    print("FILES TO BE DELETED")
    f.write("FILES TO BE DELETED\n")
    for i in IterationDatabase[bestIt][1]:
        print (i)
        f.write(i+"\n")
    print("")
    print("FILES TO BE CREATED")
    f.write("FILES TO BE CREATED\n")
    for i in IterationDatabase[bestIt][3]:
        print (i)
        f.write(i+"\n")
    print("")
    print("KEYS TO BE DELETED")
    f.write("KEYS TO BE DELETED\n")
    for i in IterationDatabase[bestIt][2]:
        if i.split(";")[1] != "":
            print (i.split(";")[0]+"  Value: "+i.split(";")[1])
            f.write(i.split(";")[0]+"  Value: "+i.split(";")[1])
        else:
            print(i.split(";")[0])
            f.write(i.split(";")[0]+"\n")
    print("")
    print("KEYS TO BE CREATED")
    f.write("KEYS TO BE CREATED\n")
    for i in IterationDatabase[bestIt][4].keys():
        if len(IterationDatabase[bestIt][4][i])>0:
            print (i+"  Value: "+IterationDatabase[bestIt][4][i])
            f.write(i+"  Value: "+IterationDatabase[bestIt][4][i]+"\n")
        else:
            print (i)
            f.write(i+"\n")
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
