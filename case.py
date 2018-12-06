# coding: utf-8
from enum import IntEnum, unique
import string


def trier_bateaux_par_taille(bateaux, decroissant = False):
    """
    Trie une liste de bateaux par taille
    :param bateaux: liste de bateaux
    :param decroissant: détermine si la liste doit être triée dans l'ordre croissant ou décroissant
    :return: liste triée
    """
    return sorted(bateaux, key=lambda x: x.TAILLE, reverse=decroissant)


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

    VIDE, BATEAU_INTACT, DANS_L_EAU, TOUCHE, COULE = range(5)


@unique  # Assure que chaque valeur de l'énumération est unique
class Coord(IntEnum):
    """
    Énumération permettant d'augmenter la lisibilité du code.

    "x" représente l'index de la coordonnée x
    "y" représente l'index de la coordonnée y
    """
    x, y = range(2)


class Case:
    """
    Classe permettant de créer des objets de type case, composants élémentaires de la grille de jeu.
    """
    TAILLE = 10  # taille en pixels, le nom est en majuscules par convention, car c'est une constante
    CARACTERES_ETAT = ["_", "_", "o", "x", "#"]

    def __init__(self, position, etat=Etat.VIDE, bateau=None):
        """
        constructeur de la classe "Case"

        ATTENTION : comme suggéré par le caractère "_" dans le nom de l'attribut "_bateau",
        il ne faut pas modifier cet attribut directement, mais faire appel à la méthode "set_bateau(self, bateau)"
        :param position: position cartésienne du coin inférieur gauche de la case sur la grille
        :param etat: État de la case, lire la docstring de la classe "Etat" pour plus d'informations.
        :param bateau: Bateau présent sur cette case. Si la case est vide, ce paramètre vaut "None"
        """
        self.position = list(position)
        self.etat = etat
        self._bateau = bateau

    @staticmethod
    def sont_alignees(cases):
        """
        Fonction déterminant si plusieurs cases sont alignées entre elles.
        :param cases: liste d'objets de type "Case" dont on veut tester l'alignement
        :return: booléen indiquant si les cases sont alignées
        """
        if cases is not None and len(cases) > 0:
            if cases[0].position[Coord.x] == cases[-1].position[Coord.x]:  # si la première case a la même coordonnée x que la dernière
                coord = Coord.x  # on défini une variable indiquant qu'il faut regarder l'alignement sur x
            elif cases[0].position[Coord.y] == cases[-1].position[Coord.y]:  # si la première case a la même coordonnée y que la dernière
                coord = Coord.y  # on défini une variable indiquant qu'il faut regarder l'alignement sur y
            else:
                return False

            premiere_case = cases[0]
            for i in range(1, len(cases)-1):  # on ne teste pas la première et la dernière, car cela a déjà été fait avant
                if abs(cases[i].position[coord] - premiere_case.position[coord]) > 0.0001:  # si la case n'est pas alignée avec la première case
                    return False
            return True
        return False

    @classmethod
    def sont_adjacentes(cls, cases):
        """
        Vérifie si un plusieurs cases sont adjacentes

        Exemples:
            1)
             _ _ _ _ _
            |_|_|_|_|_|
                |_|_
                  |_|
            Cette configuration renverra "False", car la case du bas est isolée (les sommets ne comptent pas)
            2)
             _ _ _ _ _
            |_|_|_|_|_|
                |_|_
                |_|_|
            Cette configuration renverra "True", car chaque case a au moins une voisine
        :param cases: cases à vérifier
        :return: "True" si toutes les cases ont au moins un voisin, "False" sinon
        """
        for case1 in cases:
            autres_cases = list(cases)  # Crée une copie de la liste "cases"
            autres_cases.remove(case1)  # Enlève la case "case1"
            case1_a_un_voisin = False
            for case2 in autres_cases:
                if cls.sont_alignees((case1, case2)):
                    separation_horizontale = abs(case1.position[Coord.x] - case2.position[Coord.x])
                    separation_verticale = abs(case1.position[Coord.y] - case2.position[Coord.y])
                    if separation_horizontale < cls.TAILLE or separation_verticale < cls.TAILLE:
                        case1_a_un_voisin = True
            if not case1_a_un_voisin:
                return False
        return True

    def carre(self):
        """
        :return: carré occupé par la case
        """
        x = self.position[Coord.x]
        y = self.position[Coord.y]
        cote = self.__class__.TAILLE
        return [x, y], [x+cote, y], [x+cote, y+cote], [x, y+cote]

    def milieu(self):
        """
        :return: position du milieu de la case
        """
        x = self.position[Coord.x]
        y = self.position[Coord.y]
        demi_longueur = self.TAILLE/2.0
        return x + demi_longueur, y + demi_longueur

    def caractere_etat(self):
        """
        :return: caractère symbolisant l'état de la case
        """
        return self.CARACTERES_ETAT[self.etat]

    def bateau(self):
        """
        Accesseur de l'attribut "_bateau". Il permet d'accéder à l'attribut.

        :return: attribut "_bateau"
        """
        return self._bateau

    def set_bateau(self, bateau):
        """
        Mutateur de l'attribut "_bateau". Il sert à changer de bateau de manière sécurisée à condition qu'aucun coup n'ait été tiré.

        :param bateau: nouveau bateau
        :return: renvoie le succès de l'opération
        """
        if self.etat != Etat.VIDE and self.etat != Etat.BATEAU_INTACT:
            return False
        if bateau is not None:
            if self.etat == Etat.VIDE:
                self.etat = Etat.BATEAU_INTACT
        else:
            if self.etat == Etat.BATEAU_INTACT:
                self.etat = Etat.VIDE
        self._bateau = bateau
        return True

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

    C'est un tableau en deux dimensions stockant des cases.
    Les cases sont accédées de la manière suivante: self.cases[ligne][colonne]
    """
    TAILLE_MAX = 26  # Si la taille excède 26, les coordonnées nécessitent plusieurs lettres

    def __init__(self, taille=10):
        if taille < 26:
            self.TAILLE = taille
        else:
            self.TAILLE = self.__class__.TAILLE_MAX
        self.cases = []
        for i in range(self.TAILLE):
            colonne = []
            for j in range(self.TAILLE):
                position = (i*Case.TAILLE, -j*Case.TAILLE)
                colonne.append(Case(position))
            self.cases.append(colonne)

    def cases_libres(self):
        """
        Fonction retournant les cases libres de la grille
        :return: liste contenant les cases libres
        """
        libres = []
        for ligne in self.cases:
            libres_sur_ligne = []
            for case in ligne:
                if case.bateau() is None:  # Si la case est vide
                    libres_sur_ligne.append(case)
                else:
                    libres_sur_ligne.append(None)
            libres.append(libres_sur_ligne)
        return libres

    def placer_bateaux(self, bateaux):
        nombre_de_cases = 0
        for bateau in bateaux:
            nombre_de_cases += bateau.TAILLE
        bateaux_a_placer = trier_bateaux_par_taille(bateaux)


    @staticmethod
    def coord_ecran_vers_index(coordonnees):
        pass

    @staticmethod
    def coord_bataille_vers_index(coordonnees):
        """
        Convertit les coordonnées de la bataille navale (ex : "A5" ou ("A", 5)) en coordonnées de la grille (ex: (1, 5)).

        :param coordonnees: coordonnées de la bataille navale
        :return: coordonnées équivalentes sur la grille
        """
        copie_coordonnees = "".join(coordonnees)  # On assure que "copieCoordonnes" est une chaîne de caractères et non une liste ou un tuple
        copie_coordonnees = copie_coordonnees.replace(" ", "")  # On enlève les espaces.
        copie_coordonnees = copie_coordonnees.replace(".", "")  # On enlève les points
        copie_coordonnees = copie_coordonnees.lower()  # On met tout en minuscules.

        x = ""
        lettres = ""
        while copie_coordonnees[0].isalpha():
            lettres += copie_coordonnees[0]  # On copie toutes les lettres du début dans "x" et on les enlève de "copie_coordonnees".
            copie_coordonnees = copie_coordonnees[1:len(copie_coordonnees)]
        for c in lettres:
            x += str(string.ascii_letters(c).index())  # On transforme les lettres en nombres TODO: Augmenter sécurité
        x = int(x)

        y = int(copie_coordonnees) - 1

        return x, y

    @staticmethod
    def index_vers_coord_bataille(index):
        """
        Convertit les coordonnées de la grille vers celles de la bataille navale.

        :param index: tuple ou liste représentant l'index de la case sur la grille
        :return: chaîne de caractères des coordonnées équivalentes dans la bataille navale (ex : "B8")
        """
        lettre = string.ascii_uppercase[index[Coord.x]]  # On convertit la coordonnée x en lettre majuscule
        nombre = index[Coord.y] + 1
        return lettre + str(nombre)
