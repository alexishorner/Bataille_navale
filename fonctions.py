from case import *

def sontAlignees(cases):
    """
    Fonction déterminant si plusieurs cases sont alignées entre elles.
    :param cases: liste d'objets de type "Case" dont on veut tester l'alignement
    :return: booléen indiquant si les cases sont alignées
    """
    if cases is not None and len(cases) > 0:
        if cases[0].position[Coord.x] == cases[-1].position[Coord.x]: # si la première case a la même coordonnée x que la dernière
            coord = Coord.x # on défini une variable indiquant qu'il faut regarder l'alignement sur x
        elif cases [0].position[Coord.y] == cases[-1].position[Coord.y]: # si la première case a la même coordonnée y que la dernière
            coord = Coord.y # on défini une variable indiquant qu'il faut regarder l'alignement sur y
        else:
            return False

        premCase = cases[0] # première case
        for i in range(1, len(cases)-2): # on ne teste pas la première et la dernière, car cela a déjà été fait avant
            if cases[i].position[coord] != premCase.position[coord]: # si la case n'est pas alignée avec la première case
                return False
        return True
    return False
