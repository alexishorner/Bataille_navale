from enumerations import *
import string

class Case:
    """
    Classe permettant de créer des objets de type case, composants élémentaires de la grille de jeu.
    """
    TAILLE = 10  # taille en pixels, le nom est en majuscules par convention, car c'est une constante

    def __init__(self, position, etat=Etat.vide, bateau=None):
        """
        constructeur de la classe "Case"

        ATTENTION : comme suggéré par le caractère "_" dans le nom de l'attribut _bateau,
        il ne faut pas modifier cet attribut directement, mais faire appel à la méthode "setBateau(self, bateau)"
        :param position: position cartésienne du coin inférieur gauche de la case sur la grille
        :param etat: État de la case, lire la docstring de la classe "Etat" pour plus d'informations.
        :param bateau: Bateau présent sur cette case. Si la case est vide, ce paramètre vaut "None"
        """
        self.position = list(position)
        self.etat = etat
        self._bateau = bateau

    def carre(self):
        """
        :return: carré occupé par la case
        """
        x = self.position[Coord.x]
        y = self.position[Coord.y]
        cote = self.__class__.TAILLE
        return ([x, y], [x+cote, y], [x+cote, y+cote], [x, y+cote])

    def milieu(self):
        """
        :return: position du milieu de la case
        """
        x = self.position[Coord.x]
        y = self.position[Coord.y]
        demiLong = self.TAILLE/2.0
        return x + demiLong, y + demiLong

    def set_bateau(self, bateau):
        """
        Mutateur de l'attribut "_bateau". Il sert à changer de bateau de manière sécurisée à condition qu'aucun coup n'ait été tiré.

        :param bateau: nouveau bateau
        :return: pas de sortie spécifiée
        """
        if bateau is not None:
            if self.etat == Etat.vide:
                self.etat = Etat.bateauInv
        else:
            if self.etat == Etat.bateauInv:
                self.etat = Etat.vide
        self._bateau = bateau

    def recevoir_tir(self):
        """
        Méthode appelée lorsqu'un tir est dirigé vers cette case.

        :return: booléen indiquant le succès de l'opération
        """
        if self._bateau is not None:  # si un bateau est présent sur la case
            return self._bateau.recevoir_tir(self)
        else:
            return False


class Grille:
    """
    Classe représentant la grille de jeu de la bataille navale.

    C'est un tableau en deux dimensions de cases
    """
    def __init__(self, taille = 10):
        self.TAILLE = taille
        self.cases = []
        for i in range(self.TAILLE):
            ligne = []
            for j in range(self.TAILLE):
                position = (j*Case.TAILLE, i*Case.TAILLE)
                ligne.append(Case(position))
            self.cases.append(ligne)

    def coord_bataile_vers_grille(self, coordonnees):
        copieCoordonnees = coordonnees
        x = None
        y = None
        if type(copieCoordonnees == str):
            copieCoordonnees.replace(" ", "")
            copieCoordonnees = copieCoordonnees.lower()
            x = ""
            while copieCoordonnees[0].sdigit():
                x += copieCoordonnees[0]    string.ascii_letters(copieCoordonnees).index()
