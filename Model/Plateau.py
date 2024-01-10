from Model.Constantes import *
from Model.Pion import *


#
# Le plateau représente la grille où sont placés les pions.
# Il constitue le coeur du jeu car c'est dans ce fichier
# où vont être programmées toutes les règles du jeu.
#
# Un plateau sera simplement une liste de liste.
# Ce sera en fait une liste de lignes.
# Les cases du plateau ne pourront contenir que None ou un pion
#
# Pour améliorer la "rapidité" du programme, il n'y aura aucun test sur les paramètres.
# (mais c'est peut-être déjà trop tard car les tests sont fait en amont, ce qui ralentit le programme...)
#

def type_plateau(plateau: list) -> bool:
    """
    Permet de vérifier que le paramètre correspond à un plateau.
    Renvoie True si c'est le cas, False sinon.

    :param plateau: Objet qu'on veut tester
    :return: True s'il correspond à un plateau, False sinon
    """
    if type(plateau) != list:
        return False
    if len(plateau) != const.NB_LINES:
        return False
    wrong = "Erreur !"
    if next((wrong for line in plateau if type(line) != list or len(line) != const.NB_COLUMNS), True) == wrong:
        return False
    if next((wrong for line in plateau for c in line if not(c is None) and not type_pion(c)), True) == wrong:
        return False
    return True

def construirePlateau()->list:
    """
    Construit une liste de liste représentant le plateau
    :return: la liste de liste représentant le plateau
    """
    plateau = []
    for i in range(const.NB_LINES):
        plateau.append([])
        for j in range(const.NB_COLUMNS):
            plateau[i].append(None)

    return plateau

def placerPionPlateau(plateau:list, pion:dict, numColonne:int)->int:
    """
    Cette fonction permet de placer un pion dans le plateau et de dire dans quelle ligne le pion se retrouve
    :param plateau: le plateau sur lequel on joue
    :param pion: le pion que l'on place
    :param numColonne: numéro de colonnes où on place le pion
    :return: la ligne où se trouve le pion
    """
    if not type_plateau(plateau):
        raise TypeError("placerPionPlateau :Le premier paramètre ne correspond pas à un plateau")
    if not type_pion(pion):
        raise TypeError("placerPionPlateau :Le second paramètre n’est pas un pion")
    if not isinstance(numColonne, int):
        raise TypeError("placerPionPlateau : Le troisième paramètre n’est pas un entier")
    if numColonne < 0 or numColonne > const.NB_COLUMNS - 1:
        raise ValueError(f"placerPionPlateau : La valeur de la colonne {numColonne} n'est pas correcte")

    i = const.NB_LINES - 1
    lignePlacement = -1
    while lignePlacement == -1 and i != -1:
        if plateau[i][numColonne] == None:
            plateau[i][numColonne] = pion
            lignePlacement = i
        i -= 1
    return lignePlacement

def toStringPlateau(plateau:list)->str:
    """
    Cette fonction affiche le tableau d'une meilleure façon
    :param plateau: le plateau à afficher
    :return: le plateau avec un meilleur affichage
    """
    bestPlateau = ""
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j] != None:
                if plateau[i][j][const.COULEUR] == const.ROUGE:
                    elmt = "\x1B[41m \x1B[0m"
                elif plateau[i][j][const.COULEUR] == const.JAUNE:
                    elmt = "\x1B[43m \x1B[0m"
            else:
                elmt = " "
            bestPlateau += "|" + elmt
            if j == const.NB_COLUMNS - 1:
                bestPlateau += "| \n"
    bestPlateau += "--------------- \n"
    bestPlateau += " 0 1 2 3 4 5 6"

    return bestPlateau

def detecter4horizontalPlateau(plateau:list, couleur:int)->list:
    """
    Cette fonction donne les séries de 4 pions alignés sur une même ligne d'une même couleur
    :param plateau: le plateau où on fait la détection
    :param couleur: la couleur dont on recherche une série
    :return: la liste des pions formant une suite de 4 d'une certaine couleur sur une même ligne
    """
    if not type_plateau(plateau):
        raise TypeError("detecter4horizontalPlateau : Le premier paramètre ne correspond pas à un plateau")
    if not isinstance(couleur, int):
        raise TypeError("detecter4horizontalPlateau : le second paramètre n’est pas un entier")
    if not couleur in const.COULEURS:
        raise ValueError(f"détecter4horizontalPlateau : La valeur de la couleur {couleur} n’est pas correcte")

    tempList = []
    listePion = []
    suite = 0
    for i in range(const.NB_LINES):
        suite = 0
        tempList = []
        for j in range(const.NB_COLUMNS):
            if plateau[i][j] != None:
                if plateau[i][j][const.COULEUR] == couleur:
                    suite += 1
                    tempList.append(plateau[i][j])
            if suite == 4:
                listePion+=tempList
                suite=0
            if plateau[i][j] == None or plateau[i][j][const.COULEUR] != couleur:
                suite = 0
                tempList = []
    return listePion

def detecter4verticalPlateau(plateau:list, couleur:int)->list:
    """
    Cette fonction donne les séries de 4 pions alignés sur une même colonne d'une même couleur
    :param plateau: le plateau où on fait la détection
    :param couleur: la couleur dont on recherche une série
    :return: la liste des pions formant une suite de 4 d'une certaine couleur sur une même colonne
    """
    if not type_plateau(plateau):
        raise TypeError("detecter4verticalPlateau : Le premier paramètre ne correspond pas à un plateau")
    if not isinstance(couleur, int):
        raise TypeError("detecter4verticalPlateau : le second paramètre n’est pas un entier")
    if not couleur in const.COULEURS:
        raise ValueError(f"detecter4verticalPlateau : La valeur de la couleur {couleur} n’est pas correcte")

    tempList = []
    listePion = []
    suite = 0
    for i in range(const.NB_COLUMNS):
        suite = 0
        tempList = []
        for j in range(const.NB_LINES):
            if plateau[j][i] != None:
                if plateau[j][i][const.COULEUR] == couleur:
                    suite += 1
                    tempList.append(plateau[j][i])
            if suite == 4:
                listePion += tempList
                suite = 0
            if plateau[j][i] == None or plateau[j][i][const.COULEUR] != couleur:
                suite = 0
                tempList = []
    return listePion



def detecter4diagonaleDirectePlateau(plateau: list, couleur: int) -> list:
    """
    Cette fonction donne les séries de 4 pions alignés sur une même diagonale d'une même couleur
    :param plateau: le plateau où on fait la détection
    :param couleur: la couleur dont on recherche une série
    :return: la liste des pions formant une suite de 4 d'une certaine couleur sur une même diagonale
    """
    if not type_plateau(plateau):
        raise TypeError("detecter4diagonaleDirectePlateau : Le premier paramètre ne correspond pas à un plateau")
    if not isinstance(couleur, int):
        raise TypeError("detecter4diagonaleDirectePlateau : le second paramètre n’est pas un entier")
    if not couleur in const.COULEURS:
        raise ValueError(f"detecter4diagonaleDirectePlateau : La valeur de la couleur {couleur} n’est pas correcte")

    decalage = 0
    suite = 0
    tempList = []
    listePion = []
    start = const.NB_COLUMNS-1
    end = const.NB_LINES-1
    for i in range(end):
        for j in range(start):
            if plateau[i+j][(i+j)-decalage] != None:
                if plateau[i+j][(i+j)-decalage][const.COULEUR] == couleur:
                    suite += 1
                    tempList.append(plateau[i+j][(i+j)-decalage])
            if suite == 4:
                listePion += tempList
                suite = 0
            if plateau[i+j][(i+j)-decalage] == None or plateau[i+j][(i+j)-decalage][const.COULEUR] != couleur:
                suite = 0
                tempList = []
        suite = 0
        tempList = []
        start -= 1
        end -= 1
        decalage+=1
    borne = const.NB_LINES
    i=0
    decalage=1
    suite = 0
    tempList = []
    while i<borne and borne > 2:
        if plateau[i][i+decalage] != None:
            if plateau[i][i+decalage][const.COULEUR] == couleur:
                suite += 1
                tempList.append(plateau[i][i+decalage])
        if suite == 4:
            listePion += tempList
            suite = 0
        if plateau[i][i+decalage] == None or plateau[i][i+decalage][const.COULEUR] != couleur:
            suite = 0
            tempList = []
        i+=1
        if i == borne:
            i=0
            borne-=1
            decalage+=1
            suite = 0
            tempList = []
    return listePion

def detecter4diagonaleIndirectePlateau(plateau: list, couleur: int) -> list:
    """
    Cette fonction donne les séries de 4 pions alignés sur une même diagonale (inverse) d'une même couleur
    :param plateau: le plateau où on fait la détection
    :param couleur: la couleur dont on recherche une série
    :return: la liste des pions formant une suite de 4 d'une certaine couleur sur une même diagonale (inverse)
    """
    if not type_plateau(plateau):
        raise TypeError("detecter4diagonaleIndirectePlateau : Le premier paramètre ne correspond pas à un plateau")
    if not isinstance(couleur, int):
        raise TypeError("detecter4diagonaleIndirectePlateau : le second paramètre n’est pas un entier")
    if not couleur in const.COULEURS:
        raise ValueError(f"detecter4diagonaleIndirectePlateau : La valeur de la couleur {couleur} n’est pas correcte")

    x = const.NB_LINES
    decalage = 0
    listePion=[]
    tempListe = []
    suite = 0

    #partie diagonale nord ouest
    while x>3:
        for i in range(x-1, -1, -1):
            if plateau[i][decalage] != None:
                if plateau[i][decalage][const.COULEUR] == couleur:
                    tempListe.append(plateau[i][decalage])
                    suite += 1
                else:
                    suite=0
                    tempListe = []
            #si la suite fait 4 pions, les ajoutés dans la liste finale
            if suite == 4:
                listePion += tempListe
                suite = 0
            if plateau[i][decalage] == None or plateau[i][decalage][const.COULEUR] != couleur:
                suite = 0
                tempListe = []

            #passer au pion suivant de la diagonale
            decalage+=1

        #changement de diagonale
        print()
        x -= 1
        decalage=0
        suite = 0
        tempListe = []

    #réinitialisation des paramètres
    x = const.NB_LINES
    decalage = 1
    tempListe = []
    suite = 0
    z=0

    # partie diagonale sud est
    while x > 3:
        for i in range(x - 1, -1, -1):
            if plateau[i+z][decalage] != None:
                if plateau[i+z][decalage][const.COULEUR] == couleur:
                    tempListe.append(plateau[i+z][decalage])
                    suite += 1
                else:
                    suite = 0
                    tempListe = []
            # si la suite fait 4 pions, les ajoutés dans la liste finale
            if suite == 4:
                listePion += tempListe
                suite = 0
            if plateau[i+z][decalage] == None or plateau[i+z][decalage][const.COULEUR] != couleur:
                suite = 0
                tempListe = []

            # passer au pion suivant de la diagonale
            decalage += 1

        # changement de diagonale
        print()
        x -= 1
        z+=1
        decalage = 1+z
        suite = 0
        tempListe = []

    return listePion

def getPionsGagnantsPlateau(plateau:list)->list:
    """
    Cette fonction donne tout  les pions étant dans une série de pion faisant gagner
    :param plateau: le plateau où l'on fait la détection
    :return: le liste de pions gagnants
    """
    if not type_plateau(plateau):
        raise TypeError("getPionsGagnantsPlateau : Le paramètre n’est pas un plateau")

    listeFinale = []
    for i in range(2):
        listeFinale += detecter4horizontalPlateau(plateau, i)
        listeFinale += detecter4verticalPlateau(plateau, i)
        listeFinale += detecter4diagonaleDirectePlateau(plateau, i)
        listeFinale += detecter4diagonaleIndirectePlateau(plateau, i)
    return listeFinale

def isRempliPlateau(plateau:list)->bool:
    """
    Cette fonction vérifie si le plateau est rempli ou non
    :param plateau: le platon où on fait la vérification
    :return: si le tableau est rempli
    """

    if not type_plateau(plateau):
        raise TypeError("isRempliPlateau : Le paramètre n’est pas un plateau")

    taillePlateau = const.NB_LINES * const.NB_COLUMNS
    nbPions = 0
    i=0
    pionManquant = False
    while i<len(plateau) and not pionManquant:
        for pion in plateau[i]:
            if pion != None:
                nbPions+=1
            else:
                pionManquant = True
        i+=1
    return nbPions == taillePlateau








