from enum import IntEnum, unique
class Case:
    """
    Classe permettant de créer des objets de type case, composants élémentaires de la grille de jeu.
    """
    def __init__(self, etat = Etat.vide):
        self.etat = etat
        self.position =


    def position(self):
        return self.position


@unique #Assure que chaque valeur de l'énumération est unique
class Etat(IntEnum):
    """
    Énumération décrivant les états possibles d'une case.
    "vide" veut dire que la case n'a rien de spécial.
    "bateauInv" veut dire qu'un bateau est présent, mais que la case est blanche
    "touche" veut dire qu'un bateau a été touché sur cette case
    "coule" signifie qu'un bateau a été coulé ici
    "selectionne" veut dire que la case est en train d'être cliquée
    """

    vide = 0
    bateauInv = 1
    touche = 2
    coule = 3
    selectionne = 4
