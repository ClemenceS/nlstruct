import os
import re

def changeFormat(path):
    all_files = os.listdir(path)
    all_ann = []
    for file in all_files:
        if file.split(".")[-1] == 'ann':
            all_ann.append(file)

    for fileAnn in all_ann:
        file = open(path + "/" + fileAnn, "r", encoding="utf-8")
        lines = file.readlines()
        file.close()

        name_bis = "new_" + fileAnn
        file_new = open(path + "/" + name_bis, "w", encoding="utf-8")

        idxA = 1
        for line in lines:
            try:
                typeE_un = re.search(r"\['.*'\]", line).group(0)
                typeE = typeE_un.replace(r"['", "").replace("']", "")

                typeE = typeE.split(",")
                for i in range (len(typeE)):
                    if "'" in typeE[i]:
                        typeE[i] = typeE[i].replace("'", "")
                    typeE[i] = typeE[i].strip() 

                new_line = line.split(typeE_un)[0]
                if len(typeE) == 1:
                    new_line += typeE[0] + line.split(typeE_un)[-1] 
                    file_new.write(new_line)
                else:
                    if typeE[-1].find(':') != -1: #il ya des : dans le 2nd
                        if typeE[0].find(':') == -1:
                            new_line += typeE[0]  + line.split(typeE_un)[-1] 
                            file_new.write(new_line)
                    else:
                        new_line += typeE[-1]  + line.split(typeE_un)[-1] 
                        new2 = f"A{str(idxA)}\t{typeE[0].split(':')[0]} {line.split()[0]}\n"
                        idxA +=1
                        file_new.write(new_line)
                        file_new.write(new2)
            except:
                None
            
        file_new.close()
        
        os.remove(path + "/" + fileAnn)
        os.rename(path + "/" + name_bis, path + "/" + fileAnn)
