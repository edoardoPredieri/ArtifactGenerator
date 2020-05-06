import os
in_path = "Z:/find/toSearchFile.txt"
out_path = "Z:/find/responseFile.txt" 

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


f = open (in_path,"r")
f2 = open (out_path,"w")
line = f.readline()
ret = findFile(line)
f2.write(str(ret))
f.close()
f2.close()
