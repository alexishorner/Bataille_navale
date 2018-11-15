from enum import IntEnum, unique


@unique  # Assure que chaque valeur de l'énumération est unique
class Etat(IntEnum):
    """
    Énumération décrivant les états possibles d'une case.

    "VIDE" veut dire que la case n'a rien de spécial.
    "BATEAU_INTACT" veut dire qu'un bateau est présent, mais que la case est blanche
    "DANS_L_EAU" signifie que la case ne contient aucun bateau, mais qu'un coup a déjà été tiré dessus
    "TOUCHE" veut dire qu'un bateau a été touché sur cette case
    "COULE" signifie qu'un bateau a été coulé ici
    """

    VIDE = 0
    BATEAU_INTACT = 1
    DANS_L_EAU = 2
    TOUCHE = 3
    COULE = 4


@unique  # Assure que chaque valeur de l'énumération est unique
class Coord(IntEnum):
    """
    Énumération permettant d'augmenter la lisibilité du code.

    "x" représente l'index de la coordonnée x
    "y" représente l'index de la coordonnée y
    """
    x = 0
    y = 1
