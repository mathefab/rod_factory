def rodbuilder(ciffile, ruffile, rodfile, template):

    # outputfiles generated
    outputfile = open(rodfile, 'w')

    # readlines of different files
    linesruf = [line for line in open(ruffile, "r")]
    linescif = [line for line in open(ciffile, "r")]
    linesrod = [line for line in open(template, "r")]

   
    # rod file INTRODUCTION
    outputfile.write("## generated rod file by the rodbuilder.py\n")


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
        outputfile.write(str(linescif[i]))

    
# Here we need to set amcsd code if exist
# Then we need to set the RRUFF ID

# From a template.rod files
# We read the raman instrumental details for 780 wave length for example

#  first need to read the rruff file to get nb lines

    nblinesruf = 0
    for line in linesruf:
        nblinesruf += 1
    

# read and copy the spectrum data from the TAG "MEASURED CHEMISTRY"

    outputfile.write("#HERE IS DATA FROM RRUFF")
    outputfile.write("loop_\n")
    outputfile.write("_raman_spectrum.raman_shift\n")
    outputfile.write("_raman_spectrum.intensity\n")

    for num, line in enumerate(linesruf, 0):
        if line.find("MEASURED CHEMISTRY") != -1:
            for i in range(1,nblinesruf-num):
                outputfile.write(str(linesruf[i+num]))

    outputfile.close()
    return (outputfile)


# END OF FONCTION rodbuilder

#TODO Get the files cod.cif by walking in the cif path copy to ciffile
#TODO Get the files (long)rruffId.txt by walking in the RRuff780 path copy to ruffile
#TODO rename the files rruffId.txt


def lookforcif(codid):
    import os
    files = os.listdir()
    #codid = str(codid)
    nb_fichiers = len(files)
    for i in range (0, nb_fichiers):
        stringfile=str(files[i])
        #print(codid)
        #print(stringfile)
        if  stringfile.find(codid) != -1:
            return(stringfile)
            
    

# read csv files to link rruff file to cod file
#TODO Read csv file get rruffid, cod code and amcsd code

def readcsv(csvfile):
    linescsv = [line for line in open(csvfile, "r")]
    for num, line in enumerate(linescsv, 0):
        stringline = str(linescsv[num])
        rruffid = stringline[0:7]
        codid = str(stringline[8:15])
        print(codid)
        #and lookforrruff(rruffid)
        stringfile=str(lookforcif(codid))
        return(stringfile)

# _______________-------------MAIN-------------_______________

print("1 - Create a single rod file")
print("2 - Create multople rod files")
      
choix=input("What do you want to do ? (1/2)")

if (choix==1):
    stringcif=input("Enter cif file name : ")
    stringcif=(str(stringcif))
    stringruf=input("Enter ruf file name : ")
    stringcruf=(str(stringruf))
    rodbuilder(stringcif, stringruf, "abhurite.rod", "template.rod")
 

else:
    stringcsv=input("Enter csv file name : ")
    stringcsv=(str(stringcsv))
    readcsv(stringcsv)
    # Call rodbuilder to make the rod files with files we need
    #rodbuilder("9009804.cif", "R060227.txt", "abhurite.rod", "template.rod")


