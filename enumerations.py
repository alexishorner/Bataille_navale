from enum import IntEnum, unique


@unique
class Mode(IntEnum):
    tortue = 0
    console = 1

@unique  # Assure que chaque valeur de l'énumération est unique
class Etat(IntEnum):
    """
    Énumération décrivant les états possibles d'une case.

    "vide" veut dire que la case n'a rien de spécial.
    "bateauInv" veut dire qu'un bateau est présent, mais que la case est blanche
    "dansLEau" signifie que la case ne contient aucun bateau, mais qu'un coup a déjà été tiré dessus
    "touche" veut dire qu'un bateau a été touché sur cette case
    "coule" signifie qu'un bateau a été coulé ici
    "selectionne" veut dire que la case est en train d'être cliquée
    """

    vide = 0
    bateauInv = 1
    dansLEau = 2
    touche = 3
    coule = 4
    selectionne = 5


@unique  # Assure que chaque valeur de l'énumération est unique
class Coord(IntEnum):
    """
    Énumération permettant d'augmenter la lisibilité du code.

    "x" représente l'index de la coordonnée x
    "y" représente l'index de la coordonnée y
    """
    x = 0
    y = 1
