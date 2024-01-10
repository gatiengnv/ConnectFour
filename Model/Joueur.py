from Model.Constantes import *
from Model.Pion import *
from Model.Plateau import *
from typing import Callable



#
# Ce fichier contient les fonctions gérant le joueur
#
# Un joueur sera un dictionnaire avec comme clé :
# - const.COULEUR : la couleur du joueur entre const.ROUGE et const.JAUNE
# - const.PLACER_PION : la fonction lui permettant de placer un pion, None par défaut,
#                       signifiant que le placement passe par l'interface graphique.
# - const.PLATEAU : référence sur le plateau de jeu, nécessaire pour l'IA, None par défaut
# - d'autres constantes nécessaires pour lui permettre de jouer à ajouter par la suite...
#

def type_joueur(joueur: dict) -> bool:
    """
    Détermine si le paramètre peut correspondre à un joueur.

    :param joueur: Paramètre à tester
    :return: True s'il peut correspondre à un joueur, False sinon.
    """
    if type(joueur) != dict:
        return False
    if const.COULEUR not in joueur or joueur[const.COULEUR] not in const.COULEURS:
        return False
    if const.PLACER_PION not in joueur or (joueur[const.PLACER_PION] is not None
            and not callable(joueur[const.PLACER_PION])):
        return False
    if const.PLATEAU not in joueur or (joueur[const.PLATEAU] is not None and
        not type_plateau(joueur[const.PLATEAU])):
        return False
    return True


def construireJoueur(couleur: int)->dict:
    """
    Cette fonction construit le joeur
    :param couleur: la couleur du joueur
    :return: la représentation du joueur
    """

    if not isinstance(couleur, int):
        raise TypeError("construireJoueur : Le paramètre n’est pas un entier")
    if not couleur in const.COULEURS:
        raise ValueError(f"construireJoueur : L’entier donné {couleur} n’est pas une couleur. »")
    return {const.COULEUR: couleur, const.PLATEAU: None, const.PLACER_PION: None}

def getCouleurJoueur(joueur:dict)->int:
    """
    Cette fonction donne la couleur du joueur
    :param joueur: la représentation joueur
    :return: la couleur du joueur
    """
    if not type_joueur(joueur):
        raise TypeError("getCouleurJoueur : Le paramètre ne correspond pas à un joueur")

    return joueur[const.COULEUR]

def getPlateauJoueur(joueur:dict)->list:
    """
    Cette fonction donne le plateau sur lequel le joueur joue
    :param joueur: la représentation joueur
    :return: le plateau sur lequel il joue
    """
    if not type_joueur(joueur):
        raise TypeError("getPlateauJoueur : le paramètre ne correspond pas à un joueur ")

    return joueur[const.PLATEAU]

def getPlacerPionJoueur(joueur:dict)->Callable:
    """
    Cette fonction donne la fonction faisant jouer le joueur
    :param joueur: le joueur dont on veut la fonction
    :return: la fonction obtenue
    """
    if not type_joueur(joueur):
        raise TypeError("getPlacerPionJoueur: le paramètre ne correspond pas à un joueur ")

    return joueur[const.PLACER_PION]

def getPionJoueur(joueur:dict)->dict:
    """
    Cette fonction construit un pion de la couleur du joueur
    :param joueur: le joueur dont on récupère la couleur pour construire un pion
    :return: le pion ayant la couleur du joueur
    """
    if not type_joueur(joueur):
        raise TypeError("getPionJoueur: le paramètre ne correspond pas à un joueur ")

    return construirePion(getCouleurJoueur(joueur))

def setPlateauJoueur(joueur:dict, plateau:list)->None:
    """
    Cette fonction affecte un plateau au joueur
    :param joueur: le joueur recevant un tableau
    :param plateau: le plateau qui est affecté
    :return: Rien
    """
    if not type_joueur(joueur):
        raise TypeError("setPlateauJoueur: le premier paramètre ne correspond pas à un joueur ")
    if not type_plateau(plateau):
        raise TypeError("setPlateauJoueur : Le second paramètre ne correspond pas à un plateau")

    joueur[const.PLATEAU] = plateau

    return None

def setPlacerPionJoueur(joueur:dict, fn:Callable)->None:
    """
    Cette fonction affecte une fonction au joueur pour placer un pion
    :param joueur: le joueur auquel on affecte une fonction
    :param fn: la fonction à affecté
    :return: Rien
    """

    if not type_joueur(joueur):
        raise TypeError("setPlacerPionJoueur: le premier paramètre ne correspond pas à un joueur ")
    if not callable(fn):
        raise TypeError("setPlacerPionJoueur : le second paramètre n’est pas une fonction")

    joueur[const.PLACER_PION] = fn

    return None





