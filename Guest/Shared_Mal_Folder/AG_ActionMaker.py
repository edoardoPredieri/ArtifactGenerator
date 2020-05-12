import os
from winreg import *

ToCreateFile_path = "Z:/in/toCreateFile.txt" 
ToCreateKey_path = "Z:/in/toCreateKey.txt"
Iteration_path = "Z:/in/iteration.txt"


def findFile(targetFile):
    l = targetFile.split("\\")
    name = l[len(l)-1]
    path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1]).strip()
    for files in os.listdir(path):
        if name == "*.*" and len(files)> 1:
            return True
        if name in files:
            return True
    return False


def CreateElement():
    file = open (ToCreateFile_path,"r")
    line = file.readline().strip()
    while line != "":
        l = line.split("\\")
        name = l[len(l)-1]
        path = "".join(str(elem)+"\\\\" for elem in l[0:len(l)-1])
        if name == "*.*":
            f = open (path+"ag.txt", "w")
            f.write("Created by Artifact Generator")
            f.close()
        elif "*" in name:
            f = open (path+"ag"+name[1:len(name)], "w")
            f.write("Created by Artifact Generator")
            f.close()
        else:
            f = open (path+name.strip(), "w")
            f.write("Created by Artifact Generator")
            f.close()
        line = file.readline()
    file.close()

    file = open (ToCreateKey_path,"r")
    line = file.readline().strip()
    while line != "":
        reg = line.split(";")[0]
        value = line.split(";")[1]
        
        if value != "" and value != None:
            l = reg.split("\\")
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

            SetValueEx(k, value, 0, REG_SZ, "1")
            CloseKey(k)
        else:
            try:
                l = reg.split("\\")
                k = "".join(str(elem)+"\\" for elem in l[1:len(l)])
                if l[0] == "Machine" or l[0] == "MACHINE":
                    CreateKey(HKEY_LOCAL_MACHINE, k)
                if l[0] == "Root" or l[0] == "ROOT":
                    CreateKey(HKEY_CLASSES_ROOT, k)
                if l[0] == "User" or l[0] == "USER":
                    CreateKey(HKEY_CURRENT_USER, k)
            except:
                print("Error during creation: "+reg)

        line = file.readline().strip()
    file.close()





def ExecuteBluePill():
    f = open (Iteration_path, "r")
    iteration = f.readline().strip()
    f.close()
    
    #os.system("C: & cd C:/Pin311 & echo F | xcopy ee.exe eeC.exe /y")
    os.system("C: & cd C:/Pin311 & pin -follow_execv -t bluepill32 -evasions -iter "+str(iteration)+" -- ee.exe")    #BluePill Execution Command
    if not findFile("C:\\Pin311\\ee.exe"):
        print("Auto-Eliminate Malware   iteration = "+str(iteration))
        #os.system("C: & cd C:/Pin311 & rename eeC.exe ee.exe")



try:
    CreateElement()
except:
    print("Error Element Creation")
    os.system("timeout 10")
    
try:
    ExecuteBluePill()
except:
    print("Error BluePill")
    os.system("timeout 10")
    








