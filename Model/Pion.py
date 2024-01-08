# Model/Pion.py

from Model.Constantes import *

#
# Ce fichier implémente les données/fonctions concernant le pion
# dans le jeu du Puissance 4
#
# Un pion est caractérisé par :
# - sa couleur (const.ROUGE ou const.JAUNE)
# - un identifiant de type int (pour l'interface graphique)
#
# L'identifiant sera initialisé par défaut à None
#

def type_pion(pion: dict) -> bool:
    """
    Détermine si le paramètre peut être ou non un Pion

    :param pion: Paramètre dont on veut savoir si c'est un Pion ou non
    :return: True si le paramètre correspond à un Pion, False sinon.
    """
    return type(pion) == dict and len(pion) == 2 and const.COULEUR in pion.keys() \
        and const.ID in pion.keys() \
        and pion[const.COULEUR] in const.COULEURS \
        and (pion[const.ID] is None or type(pion[const.ID]) == int)

def construirePion(couleur:int)->dict:
    """
    Crée un pion rouge ou jaune
    :param couleur: Couleur du pion
    :return: pion construit avec cette couleur de type dict
    """
    if not isinstance(couleur, int):
        raise TypeError("construirePion : Le paramètre n’est pas de type entier")
    if not couleur in const.COULEURS:
        raise ValueError(f"construirePion : la couleur {couleur}  n’est pas correcte")
    return {const.COULEUR : couleur, const.ID : None}

def getCouleurPion(pion:dict)->int:
    """
    Retourne la couleur du pion
    :param pion: pion de type dict
    :return: couleur du pion de type int
    """
    if not type_pion(pion):
        raise TypeError("getCouleurPion : Le paramètre n’est pas un pion")
    return pion[const.COULEUR]

def setCouleurPion(pion:dict, nouvelleCouleur:int)->None:
    """
    Modifie la couleur du pion
    :param pion: le pion à modifier
    :param nouvelleCouleur: la nouvelle couleur du pion (1 pour rouge, 0 pour jaune)
    :return: Rien
    """
    if not type_pion(pion):
        raise TypeError("setCouleurPion :Le premier paramètre n’est pas un pion")
    if not isinstance(nouvelleCouleur, int):
        raise ValueError("« setCouleurPion : Le second paramètre n’est pas un entier")
    pion[const.COULEUR] = nouvelleCouleur
    return None

def getIdPion(pion:dict)->int:
    """
    La fonction renvoie l'identifiant du pion
    :param pion: le pion dont on veut récupérer l'identifiant
    :return: l'identifiant du pion
    """
    if not type_pion(pion):
        raise TypeError("getIdPion : Le paramètre n’est pas un pion")
    return pion[const.ID]

def setIdPion(pion:dict, nouvelleIdentifiant:int)->None:
    """
    La fonction modifie l'identifiant du pion avec celui passé en paramètre
    :param pion: le pion dont on veut modifier l'identifiant
    :param nouvelleIdentifiant: le nouvelle identifiant
    :return: Rien
    """
    if not type_pion(pion):
        raise TypeError("setIdPion : Le premier paramètre n’est pas un pion")
    if not isinstance(nouvelleIdentifiant, int):
        raise ValueError("setIdPion : Le second paramètre n’est pas un entier.")
    pion[const.ID] = nouvelleIdentifiant
    return None