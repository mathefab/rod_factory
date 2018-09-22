def rodbuilder(ciffile, ruffile, rodfile, template, codid, rruffid):
    import os

    # outputfiles generated
    outputfile = open("D:/generated_532/"+rodfile, 'w')

    # path ruff
    path_ruf = "D:/rod/Ruff/excellent_unoriented/532/"

    # readlines of different files
    if open("D:/rod/Ruff/excellent_unoriented/532/"+ruffile, "r"):
        linesruf = [line for line in open("D:/rod/Ruff/excellent_unoriented/532/"+ruffile, "r")]
    linescif = [line for line in open(ciffile, "r")]
    linesrod = [line for line in open(template, "r")]

   
    # rod file INTRODUCTION
    outputfile.write("#\#CIF_2.0\n")
    outputfile.write("data_3500000\n")
    outputfile.write("## generated rod file by the rodbuilder.py\n")
    outputfile.write("## generated from RRUFF.info files\n")
    outputfile.write("## RRUFFID _ : "+rruffid)
    outputfile.write("\n")
    # if _chemical_compound_source does not exist then we write it
    chemical = 0
    for num, line in enumerate(linescif, 0):
            if (line.find("_chemical_compound_source")) != -1:
                print ("_chemical_compound_source already known")
                chemical = 1
                break

    if (chemical == 0):
        outputfile.write("_chemical_compound_source ")
        outputfile.write("'"+rruffid)
        outputfile.write("'")              
        outputfile.write("\n")

    
    
    # find lines from tag "loop" to "_cod_database_code"
    
    for num, line in enumerate(linescif, 0):
        if line.find("loop_") != -1:
            firstline = num
            break
        
    for num, line in enumerate(linescif, 0):
        if line.find("_cod_database_code") != -1:
            lastline = num +1
            break

    # copy these lines ro rodfiles
    
    for i in range(firstline,lastline):
        if linescif[i].find("_database_code_amcsd") != -1:
            outputfile.write("#"+str(linescif[i]))
        else:
            outputfile.write(str(linescif[i]))

    
# Here we need to set amcsd code if exist
# Then we need to set the RRUFF ID

# From a template.rod files
# We read the raman instrumental details for 780 wave length for example

        # lecture des infos rod depuis un template depuis _raman_determination_method
    # jusqu'au TAG : _rod_related_entry.uri

    for num, line in enumerate(linesrod, 0):
        if line.find("_rod_related_entry.uri") != -1:
            linestop = num;


    for num, line in enumerate(linesrod, 0):
        if line.find("_raman_determination_method") != -1:
                    for i in range(0,linestop-num+1):
                        outputfile.write(str(linesrod[num + i]))


    # lecture des infos cif depuis le TAG : #$URL
    #TODO récupérer l'URL de la ligne 4 pour l'implanter _rod_related_entry.description
    #1 1011291 COD http://www.crystallography.net/cod/1011291.html
    #;


    outputfile.write("_rod_related_entry.description\n")
    outputfile.write("1 ")
    outputfile.write(str(codid[0:7]))
    outputfile.write(" COD")
    outputfile.write(" http://www.crystallography.net/cod/")
    outputfile.write(str(codid[0:7]))
    outputfile.write(".html\n")
    outputfile.write(";\n")
    outputfile.write("XRD analysis data was done.\n")
    outputfile.write(";\n")

    # lecture des infos ruf depuis le TAG : MEASURED CHEMISTRY
    # écriture des données RAMAN jusqu'à la fin du fichier

#  first need to read the rruff file to get nb lines

    nblinesruf = 0
    for line in linesruf:
        nblinesruf += 1
    

# read and copy the spectrum data from the TAG "MEASURED CHEMISTRY"

    outputfile.write("#HERE IS DATA FROM RRUFF\n")
    outputfile.write("loop_\n")
    outputfile.write("_raman_spectrum.raman_shift\n")
    outputfile.write("_raman_spectrum.intensity\n")

    for num, line in enumerate(linesruf, 0):
        if line.find("URL=rruff.info") != -1:
            start=1
            if str(linesruf[1+num]).find("MEASURED CHEMISTRY") != -1:
                start=2
            for i in range(start,nblinesruf-num-4):
                if (i==nblinesruf-num-5):
                    linetowrite=(str(linesruf[i+num]))
                    linetowrite=linetowrite.replace("," ,"")
                    outputfile.write(linetowrite[:-1])
                else :
                    linetowrite=(str(linesruf[i+num]))
                    linetowrite=linetowrite.replace("," ,"")
                    outputfile.write(linetowrite)
       
    outputfile.close()
    return (outputfile)


# END OF FONCTION rodbuilder



#TODO Get the files cod.cif by walking in the cif path copy to ciffile
#TODO Get the files (long)rruffId.txt by walking in the RRuff780 path copy to ruffile
#TODO rename the files rruffId.txt



            
def lookforcif(codid):
    import shutil
    import os
    folder_path = "D:/rod/all COD/cif/"
    for path, dirs, files in os.walk(folder_path):
        for filename in files:
            filetofind=str(filename)
            if  filetofind.find(codid) != -1:
                pathfile=str(path)
                pathfile.replace("\\" ,"boot")
                pathfile=str(""+pathfile+"/"+filetofind)
                return(pathfile)

def lookforruf(rruffid):
    import os
    folder_path = "D:/rod/Ruff/excellent_unoriented/532/"
    for path, dirs, files in os.walk(folder_path):
        for filename in files:
            filetofind=str(filename)
            if  filetofind.find(rruffid) != -1:
                return(filetofind)        

# read csv files to link rruff file to cod file
#TODO Read csv file get rruffid, cod code and amcsd code

def readcsvforcif(csvfile):
    linescsv = [line for line in open(csvfile, "r")]
    for num, line in enumerate(linescsv, 0):
        stringline = str(linescsv[num])
        rruffid = stringline[0:7]
        codid = str(stringline[8:15])
        return(codid)

def readcsvforruf(csvfile):
    linescsv = [line for line in open(csvfile, "r")]
    for num, line in enumerate(linescsv, 0):
        stringline = str(linescsv[num])
        rruffid = stringline[0:7]
        return(rruffid)

# _______________-------------MAIN-------------_______________

print("1 - Create a single rod file")
print("2 - Create multiple rod files")

choix=input("What do you want to do ? (1/2)")
choix=int(choix)  
if (choix==1):
    stringcif=input("Enter cif file name : ")
    stringcif=(str(stringcif))
    stringruf=input("Enter ruf file name : ")
    stringruf=(str(stringruf))
    rodbuilder(stringcif, stringruf, stringruf+".rod", "templaterod.txt", stringcif, stringruf)
    
    
 

else:
    stringcsv=input("Enter csv file name : ")
    stringcsv=(str(stringcsv))
    linescsv = [line for line in open(stringcsv, "r")]
    for num, line in enumerate(linescsv, 0):
        stringline = str(linescsv[num])
        rruffid = stringline[0:7]
        codid = str(stringline[8:15])
        foundedcif = str(lookforcif(codid))
        print(foundedcif)
        foundedruf = str(lookforruf(rruffid))
        print(foundedruf)
        # Call rodbuilder to make the rod files with files we need
        try:
            open("D:/rod/Ruff/excellent_unoriented/532/"+foundedruf, "r")
            rodbuilder(foundedcif, foundedruf, rruffid+".rod", "templaterod532.txt", codid, rruffid)
        except IOError as e:
            print("NOT FOUND : "+foundedruf)

            


