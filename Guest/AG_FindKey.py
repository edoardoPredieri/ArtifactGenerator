from winreg import *

in_path = "Z:/find/toSearchkey.txt"
out_path = "Z:/find/responseKey.txt" 




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


f = open (in_path,"r")
f2 = open (out_path,"w")
line = f.readline()
k = line.split(";")
ret = findKey(k[0], k[1])
f2.write(str(ret))
f.close()
f2.close()
