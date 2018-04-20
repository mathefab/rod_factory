def rodbuilder(ciffile, ruffile, rodfile, template):

    # definition du fichier à générer
    outputfile = open(rodfile, 'w')

    # récupération des lignes des fichiers
    linesruf = [line for line in open(ruffile, "r")]
    linescif = [line for line in open(ciffile, "r")]
    linesrod = [line for line in open(template, "r")]

    #calcul du nombre de lignes du fichier RRUFF

    nblinesruf = 0
    for line in linesruf:
        nblinesruf += 1
    nblinesruf -= 1

    # écriture du fichier rod INTRO
    outputfile.write("## generated rod file\n")
    for i in range(0,12):
        outputfile.write(str(linesrod[i]))

    # écriture du fichier rod PREMIER CHAPITRE
    outputfile.write("_loop\n")
            
    for num, line in enumerate(linesrod, 0):
        if line.find("_publ_author_name") != -1:
            for i in range(0,8):
                outputfile.write(str(linesrod[num + i]))


    # lecture des infos Cid depuis le TAG : _chemical_formula_sum
    # jusqu'au TAG : _cell_volume

    for num, line in enumerate(linescif, 0):
        if line.find("_chemical_formula_sum") != -1:
            for i in range(0,12):
                outputfile.write(str(linescif[num + i]))


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
    outputfile.write(str(ciffile[0:7]))
    outputfile.write(" COD")
    outputfile.write(" http://www.crystallography.net/cod/")
    outputfile.write(str(ciffile[0:7]))
    outputfile.write(".html\n")

    # lecture des infos ruf depuis le TAG : MEASURED CHEMISTRY
    # écriture des données RAMAN jusqu'à la fin du fichier

    outputfile.write("loop_\n")
    outputfile.write("_raman_spectrum.raman_shift\n")
    outputfile.write("_raman_spectrum.intensity\n")

    for num, line in enumerate(linesruf, 0):
        if line.find("MEASURED CHEMISTRY") != -1:
            for i in range(1,nblinesruf-num):
                outputfile.write(str(linesruf[num + i]))

    outputfile.close()
    return (outputfile)
# fin de la fonction
# TODO : lire les fichiers d'un dossier et lancer la fonction rodbuilder

import os
files = os.listdir()

nb_fichiers = len(files)
for i in range (0, nb_fichiers):
    _, ext =os.path.splitext(files[i])
    if ext==".txt":
        ruffile = (files[i])
    if ext==".cif":
        ciffile = (files[i])
    

rodbuilder(ciffile, ruffile, "abhurite.rod", "template.rod")
