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

