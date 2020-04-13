import os

BluePill_evasion_path = "C:/Pin311/Iterations/"

FileCommandList = {"CreateFile" : 1, "CreateFileA" : 1, "CreateFileW" : 1,
                   "GetFileAttributesA" : 4, "GetFileAttributesW" : 4,
                   "OpenFile" : 2,
                   "PathFileExists" : 5, "PathFileExistsA" : 5, "PathFileExistsW" : 5,
                   "FindFirstFile" : 4, "FindFirstFileA" : 4, "FindFirstFileW" : 4, "FindFirstFileEx" : 4, "FindFirstFileExA" : 4, "FindFirstFileExW" : 4,
                   "NtCreateFile" : 3,
                   "GetModuleFileName" : 2, "GetModuleFileNameA" :2 , "GetModuleFileNameW" :2}

ModeList = {"Create" : 1, "Replace/Create" : 1, "Overwrite/Create" :1,
            "Delete" : 1,
            "Exist" : 5,
            "Read" : 4, "Read/Write" : 4,
            "Open" :4 , "Open/Create" : 4,
            "Write" : 4, "Overwrite" : 4,
            "Search" : 5,
            "Unknow" : 2}

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



FileDatabase = {}         # file: [weight, isPresent, endAction, flag]
IterationDatabase = {}  # iteration [FileDatabase, weight]



def calculateWeight(command, mode, targetFile):
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


def calculateIterWeight(actualEvasionPath, initialLinenumber, initialFilesNumber, initialThreadsNumber):
    endFilesNumber = 0
    commandsWeight = 0
    threads = []
    linesNumber = 0
    for file in os.listdir(actualEvasionPath):
        if "evasion_final" in file:
            f = open (actualEvasionPath + file,"r")
            line = f.readline()
            while line != "":
                thread = line.split(":")[0]
                if thread not in threads :
                    threads.append(thread)
                    
                command = line.split("[")[1].split("]")[0]
                if command in GeneralCommandList.keys():
                    commandsWeight += GeneralCommandList[command]
                if command in FileCommandList.keys():
                    commandsWeight += FileCommandList[command]
                    
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
    

def actionArtifactFile():
    importantFile = ""
    maxWeight = 0
    for i in FileDatabase.keys():
        if FileDatabase[i][0] > maxWeight and not FileDatabase[i][3]:
            maxWeight = FileDatabase[i][0]
            importantFile = i

    if FileDatabase[importantFile][1] == 1:
         print("Deleting: "+importantFile+"...")
         l = importantFile.split("\\")
         name = l[len(l)-1]
         path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1]).strip()
         if name == "*.*":
            os.remove(path+"ag.txt")
         else:
             os.remove(importantFile)
         FileDatabase[importantFile][1] = 0
    else:
        print("Creating: "+importantFile+"...")
        l = importantFile.split("\\")
        name = l[len(l)-1]
        path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1]).strip()
        if name == "*.*":
            f = open (path+"ag.txt", "w")
            f.write("Created by Artifact Generator")
            f.close()
        else:
            f = open (importantFile, "w")
            f.write("Created by Artifact Generator")
            f.close()
        FileDatabase[importantFile][1] = 1
    
    FileDatabase[importantFile][3] = True
    return importantFile


def restoreArtifact(LastTouchedFile):
    if FileDatabase[LastTouchedFile][1] == 1:
        print("Deleting: "+LastTouchedFile+"...")
        l = LastTouchedFile.split("\\")
        name = l[len(l)-1]
        path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1]).strip()
        if name == "*.*":
            os.remove(path+"ag.txt")
        else:
            os.remove(LastTouchedFile)
        FileDatabase[LastTouchedFile][1] = 0
    else:
        print("Creating: "+LastTouchedFile+"...")
        l = LastTouchedFile.split("\\")
        name = l[len(l)-1]
        path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1]).strip()
        if name == "*.*":
            f = open (path+"ag.txt", "w")
            f.write("Created by Artifact Generator")
            f.close()
        else:
            f = open (LastTouchedFile, "w")
            f.write("Created by Artifact Generator")
            f.close()
        FileDatabase[LastTouchedFile][1] = 1

    FileDatabase[LastTouchedFile][3] = True
    FileDatabase[LastTouchedFile][2] = "No modification"
    LastTouchedFile = ""


def validationFile():
    for i in FileDatabase.keys():
        if FileDatabase[i][3] and FileDatabase[i][2] == None :
             if  FileDatabase[i][1] == 1:
                FileDatabase[i][2] = "To be Created"
             else:
                FileDatabase[i][2] = "To be Deleted"


def exitCase():
    for i in FileDatabase.keys():
        if FileDatabase[i][2] == None:
            return False
    return True



iteration = 0
LastTouchedFile = ""
print("ArtifactGenerator")
print("")
while(True):
    os.system("cd C:/Pin311 & pin -t bluepill32 -evasions -iter "+str(iteration)+" -- ee.exe")
    actualEvasionPath = BluePill_evasion_path + str(iteration) + "/"

    FilesNumber = 0
    LinesNumber = 0
    threads = []

    for file in os.listdir(actualEvasionPath):
        if "evasion_final" in file:
            f = open (actualEvasionPath + file,"r")
            line = f.readline()
            while line != "":
                thread = line.split(":")[0]
                if thread not in threads :
                    threads.append(thread)
                    
                command = line.split("[")[1].split("]")[0]
                if command in FileCommandList.keys():
                    mode = line.split("[")[1].split("]")[1].split("-")[1].strip()
                    targetFile = line.split("[")[1].split("]")[1].split("-")[2].strip()

                    if targetFile not in FileDatabase.keys() and len(targetFile) > 3:
                        weight = calculateWeight(command, mode, targetFile)
                        isPresent = findFile(targetFile)
                        FileDatabase[targetFile] = [weight, isPresent, None, False]
                        
                LinesNumber += 1    
                line = f.readline()
            f.close()
        FilesNumber += 1

    iterationWeight = calculateIterWeight(actualEvasionPath, LinesNumber, FilesNumber, len(threads))
    IterationDatabase[iteration] = [FileDatabase.copy(), iterationWeight]
    
    if iteration == 0 or IterationDatabase[iteration][1] > IterationDatabase[iteration-1][1]:
        print("BETTER THAN PREVIOUS ITERATION")
        validationFile()
        if iteration > 0 and exitCase():
            break
        LastTouchedFile = actionArtifactFile()
    elif IterationDatabase[iteration][1] == IterationDatabase[iteration-1][1]:
        print("EQUAL TO PREVIOUS ITERATION")
        if iteration > 0 and exitCase():
            break
        restoreArtifact(LastTouchedFile)
        LastTouchedFile = actionArtifactFile()
    else:
        print("WORSE THAN PREVIOUS ITERATION")
        validationFile()
        restoreArtifact(LastTouchedFile)
        if iteration > 0 and exitCase():
            break
        LastTouchedFile = actionArtifactFile()

    iteration += 1


f = open("report.txt","w")
f.close()
f = open("report.txt","a")
f.write("ArtifactGenerator\n")
print("")
f.write("\n")
for i in IterationDatabase[iteration][0].keys():
    print (i+": "+IterationDatabase[iteration][0][i][2])
    f.write(i+": "+IterationDatabase[iteration][0][i][2]+"\n")
print("")
f.write("\n")
print("The complete report is in: "+BluePill_evasion_path + str(iteration) + "/")
f.write("The complete report is in: "+BluePill_evasion_path + str(iteration) + "/")
f.close()
