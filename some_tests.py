from Model.Constantes import *
from Model.Plateau import *
from Model.Pion import *
from random import *
from Model.Joueur import *
"""
p = construirePlateau()
print(p)
pion = construirePion(const.JAUNE)
line = placerPionPlateau(p, pion, 2)
print("Placement d’un pion en colonne 2. Numéro de ligne :", line)
print(p)
"""
# Essais sur les couleurs
print("\x1B[43m \x1B[0m : carré jaune ")
print("\x1B[41m \x1B[0m : carré rouge ")
print("\x1B[41mA\x1B[0m : A sur fond rouge")

p = construirePlateau()
p2 = construirePlateau()
for i in range(10):
     placerPionPlateau(p, construirePion(choice(const.COULEURS)), randint(0, const.NB_COLUMNS - 1))
print(toStringPlateau(p))
#print(detecter4horizontalPlateau(p, 1))
#print(detecter4verticalPlateau(p, 1))
#print(detecter4diagonaleIndirectePlateau(p, 1))
#print(getPionsGagnantsPlateau(p))
#print(isRempliPlateau(p))

#histo = {}
#print(toStringPlateau(p))

joueur = construireJoueur(1)
print(getModeEtenduJoueur(joueur))
