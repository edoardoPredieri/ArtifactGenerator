import os
from winreg import *


BluePill_evasion_path = "C:/Pin311/Iterations/"             #Path of evasion.log files
BluePill_blackListFile_path = "C:/Pin311/blacklistFile.txt" #Path to blacklist file
BluePill_blackListKey_path = "C:/Pin311/blacklistKey.txt"   #Path to blacklist key


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
                "*.*" : 2}

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
              "\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" : 3}

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
                 "KERNELBASE.DLL.MUI", "MSCTF.DLL.MUI", "WERFAULT.EXE.MUI", "FAULTREP.DLL.MUI", "DWM.EXE", "EXPLORER.EXE", "WMIPRVSE.EXE", "PIN.EXE"]

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
                "Machine\\SYSTEM\\CurrentControlSet\\Control\\ComputerName\\ActiveComputerName"]

whitelistValue = [["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "RunDiagnosticLoggingApplicationManagement"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\GRE_Initialize", "DisableMetaFiles"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options", "EnableDefaultReply"],
                  ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "NotifySettingChanges"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "ExecutablesToTrace"], ["Machine\MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers", "C:\Pin311\ee.exe"],
                  ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "ShutdownTimeout"], ["MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatibility", "DisableAppCompat"], ["Machine\SOFTWARE\Policies\Microsoft\MUI\Settings", "PreferredUILanguages"],
                  ["Machine\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run", "Policies"], ["Machine\SOFTWARE\Microsoft\Cryptography\Defaults\Provider\Microsoft Strong Cryptographic Provider", "Image Path"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows", "Load"],
                  ["Machine\SOFTWARE\Microsoft\Windows\CurrentVersion\Setup", "SourcePath"], ["Machine\SOFTWARE\Microsoft\Windows\CurrentVersion", "DevicePath"], ["Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AeDebug", "Auto"], ["Machine\SOFTWARE\Policies\Microsoft\Windows NT\Rpc", "IgnoreDelegationFailure"],
                  ["Machine\SOFTWARE\Policies\Microsoft\Windows NT\Rpc", "EnableTcpPortScaling"]]

noExistFiles = []           #List of Files to be "delete" through BluePill
noExistKeys = []            #List of Keys to be "delete" through BluePill

FileDatabase = {}           #File: [weight, isPresent, endAction, flag]
KeyDatabase = {}            #Key:  [weight, valueKey[], isPresent[], endAction[], flag[]]
IterationDatabase = {}      #Iteration: [FileDatabase, weight]


def writeBlackListFile():
    f = open(BluePill_blackListFile_path,"w")
    for i in noExistFiles:
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
        if n in targetFile:
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
    l = targetFile.split("\\")
    name = l[len(l)-1]
    path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1]).strip()
    for files in os.listdir(path):
        if name == "*.*" and len(files)> 1:
            return 1
        if name in files:
            return 1
    return 0


def findKey(targetKey, valueKey):
    try:
        l = targetKey.split("\\")
        aReg = None
        if l[0] == "Machine" or l[0] == "MACHINE":
             aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        if l[0] == "Root" or l[0] == "ROOT":
            aReg = ConnectRegistry(None, HKEY_CLASSES_ROOT)
        if l[0] == "User" or l[0] == "USER":
            aReg = ConnectRegistry(None, HKEY_CURRENT_USER)
        key = "".join(str(elem)+"\\" for elem in l[1:len(l)]).strip()
        
        k = OpenKey(aReg, key)
        
        if valueKey == "":
            CloseKey(k)
            return 1
        else:
            value = QueryValueEx(k, valueKey)
            CloseKey(k)
            return 1
    except:
        return 0
    
    
def actionArtifact():
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
             print("Deleting: "+importantFile+"...")
             l = importantFile.split("\\")
             name = l[len(l)-1]
             path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1])
             if name == "*.*":
                 noExistFiles.append((path+"ag.txt").upper())
                 writeBlackListFile()
             else:
                 noExistFiles.append(importantFile.upper())
                 writeBlackListFile()
             FileDatabase[importantFile][1] = 0
        else:
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
                    return importantFile
                f = open (path+"ag.txt", "w")
                f.write("Created by Artifact Generator")
                f.close()
            elif "*" in name:
                if (path+"ag"+name[1:len(name)]).upper() in noExistFiles:
                    noExistFiles.remove((path+"ag"+name[1:len(name)]).upper())
                    writeBlackListFile()
                    FileDatabase[importantFile][1] = 1
                    FileDatabase[importantFile][3] = True
                    return importantFile
                f = open (path+"ag"+name[1:len(name)], "w")
                f.write("Created by Artifact Generator")
                f.close()
            else:
                if importantFile.upper() in noExistFiles:
                    noExistFiles.remove(importantFile.upper())
                    writeBlackListFile()
                    FileDatabase[importantFile][1] = 1
                    FileDatabase[importantFile][3] = True
                    return importantFile
                f = open (importantFile, "w")
                f.write("Created by Artifact Generator")
                f.close()
            FileDatabase[importantFile][1] = 1

        FileDatabase[importantFile][3] = True
        return importantFile, None
            
    else:
        if len(KeyDatabase[importantKey][1]) == 0 or importantValue == None:
            if KeyDatabase[importantKey][2][0] == 1:
                print("Deleting: "+importantKey+"...")
                noExistKeys.append(importantKey.upper()+";")
                writeBlackListKey()
                KeyDatabase[importantKey][2][0] = 0
            else:
                print("Creating: "+importantKey+"...")
                if importantKey.upper()+";" in noExistKeys:
                    noExistKeys.remove(importantKey.upper()+";")
                    writeBlackListKey()
                
                    KeyDatabase[importantKey][2][0] = 1
                    KeyDatabase[importantKey][4][0] = True
                    return importantKey
                try:
                    l = importantKey.split("\\")
                    k = "".join(str(elem)+"\\" for elem in l[1:len(l)])
                    if l[0] == "Machine" or l[0] == "MACHINE":
                        CreateKey(HKEY_LOCAL_MACHINE, k)
                    if l[0] == "Root" or l[0] == "ROOT":
                        CreateKey(HKEY_CLASSES_ROOT, k)
                    if l[0] == "User" or l[0] == "USER":
                        CreateKey(HKEY_CURRENT_USER, k)
                except:
                    print("Error during creation: "+importantKey)
                    del KeyDatabase[importantKey]
                    return importantKey, None

                KeyDatabase[importantKey][2][0] = 1
                 
            KeyDatabase[importantKey][4][0] = True
            return importantKey, None

        else:
            pos = (KeyDatabase[importantKey][1]).index(importantValue) + 1
            if KeyDatabase[importantKey][2][pos] == 1:
                print("Deleting: "+importantKey+"  "+importantValue+"...")
                noExistKeys.append("A;"+importantValue.upper())
                writeBlackListKey()
                KeyDatabase[importantKey][2][pos] = 0
            else:
                print("Creating: "+importantKey+"  "+importantValue+"...")
                if "A;"+importantValue.upper() in noExistKeys:
                    noExistKeys.remove("A;"+importantValue.upper())
                    writeBlackListKey()
                
                    KeyDatabase[importantKey][2][pos] = 1
                    KeyDatabase[importantKey][4][pos] = True
                    return importantKey, importantValue
                
                l = importantKey.split("\\")
                key = "".join(str(elem)+"\\" for elem in l[1:len(l)])
                aReg = None
                if l[0] == "Machine" or l[0] == "MACHINE":
                    aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
                if l[0] == "Root" or l[0] == "ROOT":
                    aReg = ConnectRegistry(None, HKEY_CLASSES_ROOT)
                if l[0] == "User" or l[0] == "USER":
                    aReg = ConnectRegistry(None, HKEY_CURRENT_USER)

                try:
                    k = OpenKey(aReg, key, 0 ,KEY_SET_VALUE)
                except:
                    if l[0] == "Machine" or l[0] == "MACHINE":
                        CreateKey(HKEY_LOCAL_MACHINE, key)
                    if l[0] == "Root" or l[0] == "ROOT":
                        CreateKey(HKEY_CLASSES_ROOT, key)
                    if l[0] == "User" or l[0] == "USER":
                        CreateKey(HKEY_CURRENT_USER, key)
                    k = OpenKey(aReg, key, 0 ,KEY_SET_VALUE)

                SetValueEx(k, importantValue, 0, REG_SZ, "1")
                CloseKey(k)
                
                KeyDatabase[importantKey][2][pos] = 1

            KeyDatabase[importantKey][4][pos] = True
            return importantKey, importantValue

        
def restoreArtifact(LastTouchedElem, LastTouchedValue):
    if LastTouchedElem in FileDatabase.keys():
        if FileDatabase[LastTouchedElem][1] == 1:
            print("Deleting: "+LastTouchedElem+"...")
            l = LastTouchedElem.split("\\")
            name = l[len(l)-1]
            path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1])
            if name == "*.*":
                noExistFiles.append((path+"ag.txt").upper())
                writeBlackListFile()
            else:
                noExistFiles.append(LastTouchedElem.upper())
                writeBlackListFile()
            FileDatabase[LastTouchedElem][1] = 0
        else:
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
                f = open (path+"ag.txt", "w")
                f.write("Created by Artifact Generator")
                f.close()
            elif "*" in name:
                if (path+"ag"+name[1:len(name)]).upper() in noExistFiles:
                    noExistFiles.remove((path+"ag"+name[1:len(name)]).upper())
                    writeBlackListFile()
                    FileDatabase[importantFile][1] = 1
                    FileDatabase[importantFile][3] = True
                    return importantFile
                f = open (path+"ag"+name[1:len(name)], "w")
                f.write("Created by Artifact Generator")
                f.close()
            else:
                if LastTouchedElem.upper() in noExistFiles:
                    noExistFiles.remove(LastTouchedElem.upper())
                    writeBlackListFile()
                    FileDatabase[LastTouchedElem][1] = 1
                    FileDatabase[LastTouchedElem][3] = True
                    return
                f = open (LastTouchedFile, "w")
                f.write("Created by Artifact Generator")
                f.close()
            FileDatabase[LastTouchedElem][1] = 1

        FileDatabase[LastTouchedElem][3] = True

    elif LastTouchedElem in KeyDatabase.keys():
        if len(KeyDatabase[LastTouchedElem][1]) == 0 or LastTouchedValue == None:
            if KeyDatabase[LastTouchedElem][2][0] == 1:
                print("Deleting: "+LastTouchedElem+"...")
                noExistKeys.append(LastTouchedElem.upper()+";")
                writeBlackListKey()
                KeyDatabase[LastTouchedElem][2][0] = 0
            else:
                print("Creating: "+LastTouchedElem+"...")
                if LastTouchedElem.upper()+";" in noExistKeys:
                    noExistKeys.remove(LastTouchedElem.upper()+";")
                    writeBlackListKey()
                
                    KeyDatabase[LastTouchedElem][2][0] = 1
                    KeyDatabase[LastTouchedElem][4][0] = True
                    return

                try:
                    l = LastTouchedElem.split("\\")
                    k = "".join(str(elem)+"\\" for elem in l[1:len(l)])
                    if l[0] == "Machine" or l[0] == "MACHINE":
                        CreateKey(HKEY_LOCAL_MACHINE, k)
                    if l[0] == "Root" or l[0] == "ROOT":
                        CreateKey(HKEY_CLASSES_ROOT, k)
                    if l[0] == "User" or l[0] == "USER":
                        CreateKey(HKEY_CURRENT_USER, k)
                except:
                    print("Error during creation: "+LastTouchedElem)
                    del KeyDatabase[LastTouchedElem]
                    return

                KeyDatabase[LastTouchedElem][2][0] = 1
                 
            KeyDatabase[LastTouchedElem][4][0] = True
            return

        else:
            pos = (KeyDatabase[LastTouchedElem][1]).index(LastTouchedValue) + 1
            if KeyDatabase[LastTouchedElem][2][pos] == 1:
                print("Deleting: "+LastTouchedElem+"  "+LastTouchedValue+"...")
                noExistKeys.append("A;"+LastTouchedValue.upper())
                writeBlackListKey()
                KeyDatabase[LastTouchedElem][2][pos] = 0
            else:
                print("Creating: "+LastTouchedElem+"  "+LastTouchedValue+"...")
                if "A;"+LastTouchedValue.upper() in noExistKeys:
                    noExistKeys.remove("A;"+LastTouchedValue.upper())
                    writeBlackListKey()
                
                    KeyDatabase[LastTouchedElem][2][pos] = 1
                    KeyDatabase[LastTouchedElem][4][pos] = True
                    return
                
                l = LastTouchedElem.split("\\")
                key = "".join(str(elem)+"\\" for elem in l[1:len(l)])
                aReg = None
                if l[0] == "Machine" or l[0] == "MACHINE":
                    aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
                if l[0] == "Root" or l[0] == "ROOT":
                    aReg = ConnectRegistry(None, HKEY_CLASSES_ROOT)
                if l[0] == "User" or l[0] == "USER":
                    aReg = ConnectRegistry(None, HKEY_CURRENT_USER)

                try:
                    k = OpenKey(aReg, key, 0 ,KEY_SET_VALUE)
                except:
                    if l[0] == "Machine" or l[0] == "MACHINE":
                        CreateKey(HKEY_LOCAL_MACHINE, key)
                    if l[0] == "Root" or l[0] == "ROOT":
                        CreateKey(HKEY_CLASSES_ROOT, key)
                    if l[0] == "User" or l[0] == "USER":
                        CreateKey(HKEY_CURRENT_USER, key)
                    k = OpenKey(aReg, key, 0 ,KEY_SET_VALUE)

                SetValueEx(k, LastTouchedValue, 0, REG_SZ, "1")
                CloseKey(k)
                
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
        s = "Machine\\"
        for elem in  l[0:len(l)]:
            if elem != l[len(l)-1]:
                ret += str(elem)+"\\"
            else:
                ret += str(elem)
        return s+ret


def getBestIteration():
    maxx = 0
    minn = IterationDatabase[0][2]
    best = 0
    for i in IterationDatabase.keys():
        val = calculateIterWeight(IterationDatabase[i][3], IterationDatabase[i][4], IterationDatabase[i][5], IterationDatabase[i][6])
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
    
        
    
    



iteration = 0                                                                                                   #Number of AG Iteration
LastTouchedElement = ""                                                                                         #Last modified Element
LastTouchedValue = ""                                                                                           #Last modified Key Value
                                                                            
print("ArtifactGenerator")
print("")
os.system("cd C:/Pin311 & echo F | xcopy ee.exe eeC.exe /y")
while(True):
    os.system("cd C:/Pin311 & pin -follow_execv -t bluepill32 -evasions -iter "+str(iteration)+" -- ee.exe")    #BluePill Execution Command
   
    if not findFile("C:\\Pin311\\ee.exe"):
        print("Auto-Eliminate Malware   iteration = "+str(iteration))
        os.system("cd C:/Pin311 & rename eeC.exe ee.exe")
        iteration -= 1

    actualEvasionPath = BluePill_evasion_path + str(iteration) + "/"                                            #Path of current evasion.log

    FilesNumber = 0                                                                                             #Number if files in folder (Different Processes)
    LinesNumber = 0                                                                                             #Number of lines (Commands) in the file
    threads = []                                                                                                #Number of different Treads ina file (Process)

    targetKey = ""

    PreviousLine = ""
    
    for file in os.listdir(actualEvasionPath):                                                                  #Read all files in the folder
        if "evasion" in file:
            f = open (actualEvasionPath + file,"r")
            
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
                        print("Error splitting REGKEY commad "+command)
                        key = ""
                    
                    if controlKey(key):                                                                         #Verify the Key Correctness
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
                         print("Error splitting FILE commad "+command)
                         targetFile = ""
                    if controlFile(targetFile):                                                                 #Verify the File Correctness
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

    iterationWeight = calculateIterWeight(actualEvasionPath, LinesNumber, FilesNumber, len(threads))            #Calculate the Iteration Weight
    IterationDatabase[iteration] = [FileDatabase.copy(), KeyDatabase.copy(), iterationWeight, actualEvasionPath, LinesNumber, FilesNumber, len(threads)]                   #Save the actual Iteration
    
    if iteration == 0 or IterationDatabase[iteration][2] > IterationDatabase[iteration-1][2]:
        print("BETTER THAN PREVIOUS ITERATION")
        if iteration > 0:
            validationElem(LastTouchedElement, LastTouchedValue, 0)
        if iteration > 0 and exitCase() or iteration > 200:
            break
        LastTouchedElement, LastTouchedValue = actionArtifact()
        if LastTouchedElement == None and LastTouchedValue == None:
            break
    elif IterationDatabase[iteration][2] == IterationDatabase[iteration-1][2]:
        print("EQUAL TO PREVIOUS ITERATION")
        p = LastTouchedElement
        restoreArtifact(LastTouchedElement, LastTouchedValue)
        validationElem(LastTouchedElement, LastTouchedValue, 1)
        if iteration > 0 and exitCase() or iteration > 200:
            break
        LastTouchedElement, LastTouchedValue = actionArtifact()
        if LastTouchedElement == None and LastTouchedValue == None:
            break
    else:
        print("WORSE THAN PREVIOUS ITERATION")
        validationElem(LastTouchedElement, LastTouchedValue, 2)
        if iteration > 0 and exitCase() or iteration > 200:
            break
        restoreArtifact(LastTouchedElement, LastTouchedValue)
        
    iteration += 1

try:
    f = open("report.txt","w")
    f.close()
    f = open("report.txt","a")
    f.write("ArtifactGenerator\n")
    print("")
    print("")
    f.write("\n")
    print("FILES")
    f.write("FILES\n")
    for i in IterationDatabase[iteration][0].keys():
        print (i+": "+IterationDatabase[iteration][0][i][2])
        f.write(i+": "+IterationDatabase[iteration][0][i][2]+"\n")
    print("")
    f.write("\n")
    print("KEYS")
    f.write("KEYS\n")
    for j in IterationDatabase[iteration][1].keys():
        if len(IterationDatabase[iteration][1][j][1]) == 0:
            print (j+": "+IterationDatabase[iteration][1][j][3][0])
            f.write((j+": "+IterationDatabase[iteration][1][j][3][0]))
        else:
            for value in range(len(IterationDatabase[iteration][1][j][1])):
                print (j+" Value = "+ IterationDatabase[iteration][1][j][1][value]+": "+IterationDatabase[iteration][1][j][3][value+1])
                f.write((j+" Value = "+ IterationDatabase[iteration][1][j][1][value]+": "+IterationDatabase[iteration][1][j][3][value+1]))
    f.write("\n")
    print("")
    f.write("\n")
    bestIt, perc = getBestIteration()
    print("The complete report is in: "+BluePill_evasion_path + str(bestIt) + "/  with an increment of: "+str(perc)+"%")
    f.write("The complete report is in: "+BluePill_evasion_path + str(bestIt) + "/  with an increment of: "+str(perc)+"%")
    f.close()
    noExistFiles.clear()
    writeBlackListFile()
    noExistKeys.clear()
    writeBlackListKey()
except:
    print("Error in during Report Writing")
