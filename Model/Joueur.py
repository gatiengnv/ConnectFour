from Model.Constantes import *
from Model.Pion import *
from Model.Plateau import *
from typing import Callable
from random import randint



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

def _placerPionJoueur(joueur:dict)->int:
    """
    Cette fonction choisi une colonne aléatoire
    :param joueur: le joueur (IA) qui joue
    :return: la colonne choisi aléatoirement
    """

    if not type_joueur(joueur):
        raise TypeError("_placerPionJoueur : Le paramètre n’est pas un joueur")

    #si mode étendu
    if getModeEtenduJoueur(joueur):
        placer = False
        nbPions = 0
        while not placer:
            placement = randint(-const.NB_LINES, const.NB_COLUMNS + const.NB_LINES - 1)
            # vérifier si le nombre de pions dans une colonne est bien inférieur ou égal au nombre de ligne
            #si l'odinateur choisi une colonne
            if placement >= 0 and placement <= const.NB_COLUMNS - 1:
                for i in range(const.NB_LINES):
                    if joueur[const.PLATEAU][i][placement] != None:
                        nbPions += 1
                if nbPions <= const.NB_LINES - 1:
                        placer = True
                nbPions = 0
            #si l'ordinateur choisi une ligne
            else:
                placer = True

    #si pas en mode étendu
    else:

        if not isRempliPlateau(joueur[const.PLATEAU]):
            placer = False
            nbPionsColonne = 0
            while not placer:
                placement = randint(0, const.NB_COLUMNS - 1)
                # vérifier si le nombre de pions dans une colonne est bien inférieur ou égal au nombre de ligne
                for i in range(const.NB_LINES):
                    if joueur[const.PLATEAU][i][placement] != None:
                        nbPionsColonne += 1
                if nbPionsColonne <= const.NB_LINES - 1:
                    placer = True
                nbPionsColonne = 0
        else:
            placement = -1

    return placement


def initialiserIAJoueur(joueur:dict, joueEnPremier:bool)->None:
    """
    Cette fonction definie la fonction pour jouer à l'IA
    :param joueur: Le joueur (IA)
    :param joueEnPremier: Est ce que l'IA joue en première ?
    :return: Rien
    """
    if not type_joueur(joueur):
        raise TypeError("initialiserIAJoueur : Le premier paramètre n’est pas un joueur")
    if not isinstance(joueEnPremier, bool):
        raise TypeError("initialiserIAJoueur : Le second paramètre n’est pas un booléen")
    setPlacerPionJoueur(joueur, _placerPionJoueur)

    return None

def getModeEtenduJoueur(joueur:dict)->bool:
    """
    Cette fonction nous dit s'il on est en mode étendu ou non
    :param joueur: le joueur dont on veut savoir s'il est en mode étendu
    :return: Mode étendu ?
    """
    if not type_joueur(joueur):
        raise TypeError("getModeEtenduJoueur : le paramètre ne correspond pas à un joueur.")

    return const.MODE_ETENDU in joueur

def setModeEtenduJoueur(joueur:dict, avoirCle:bool=True)->None:
    """
    Cette fonction ajoute ou supprime l'information de si le joueur est mode étendu ou non
    :param joueur: le joueur dont on veut régler le mode étendu ou non
    :param avoirCle: devons nous avoir la clé comme quoi le joueur est en mode étendu?
    :return: Rien
    """
    if not type_joueur(joueur):
        raise TypeError("setModeEtenduJoueur : le premier paramètre ne correspond pas à un joueur.")
    if not isinstance(avoirCle, bool):
        raise TypeError("setModeEtenduJoueur : le second paramètre ne correspond pas à un booléen")
    if avoirCle:
        joueur[const.MODE_ETENDU] = True
    else:
        if const.MODE_ETENDU in joueur:
            del joueur[const.MODE_ETENDU]
    return None



