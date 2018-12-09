# coding: utf-8
from enum import IntEnum, unique
import string
import random
from numpy import array


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
    CARACTERES_ETAT = ["_", "*", "o", "x", "#"]  # TODO: remettre "_" (tiret en bas) à la place de "*"

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
        Mutateur de l'attribut "_bateau". Il sert à changer de bateau de manière sécurisée.

        :param bateau: nouveau bateau
        :return: "None"
        """
        if bateau is None:
            self.etat = Etat.VIDE
        else:
            self.etat = Etat.BATEAU_INTACT
        self._bateau = bateau
        return True

    def recevoir_tir(self):
        """
        Méthode appelée lorsqu'un tir est dirigé vers cette case.

        :return: État de la case après l'opération ou "None" si la case a déjà reçu un tir ou "False" s'il y a eu une erreur
        """
        if self._bateau is not None:  # si un bateau est présent sur la case
            return self._bateau.recevoir_tir(self)
        else:
            self.etat = Etat.DANS_L_EAU
            return self.etat


class Grille:
    """
    Classe représentant la grille de jeu de la bataille navale.

    C'est un tableau en deux dimensions stockant des cases.
    Les cases sont accédées de la manière suivante: self.cases[ligne][colonne]
    """
    TAILLE_MAX = 26  # Si la taille excède 26, les coordonnées nécessitent plusieurs lettres

    def __init__(self, bateaux, taille=10):
        self.bateaux = bateaux
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

    @staticmethod
    def element_dans_liste(element, liste):
        """
        Méthode statique déterminant si un élément est contenu dans une liste

        :param element: élément à chercher
        :param liste: liste dans laquelle il faut chercher
        :return: "True" si la liste contient l'élément, "False" sinon
        """
        return element in array(liste).flat

    def vider(self):
        """
        Enlève tous les bateaux de la grille.

        :return: "None"
        """
        for ligne in self.cases:
            for case in ligne:
                if case.bateau() is not None:
                    case.bateau().set_cases(None)  # enlève les bateaux un à un

    def reinitialiser(self):
        self.vider()  # Enlève tous les bateaux
        for ligne in self.cases:
            for case in ligne:
                case.etat = Etat.VIDE  # Remet l'état de chaque case à zéro

    def cases_libres(self):
        """
        Méthode retournant des groupes de cases libres alignées et adjacentes.
        Exemple:
             _A_B_C_D_E_
            1|_|x|_|_|_|
            2|_|x|x|x|x|
            3|_|x|_|x|x|
            4|_|_|x|x|x|
            5|_|_|x|_|_|
        Ici la liste sera la suivante : [[C1, D1, E1], [C3], [A4, B4], [A5, B5], [D5, E5], [A1, A2, A3, A4], [B4, B5]]

        :return: liste contenant les cases libres
        """
        libres_horizontales = []
        libres_verticales = []
        for l in range(len(self.cases)):
            for c in range(len(self.cases[l])):
                if not self.element_dans_liste(self.cases[l][c], libres_horizontales):  # Si la case n'a pas déjà été
                                                                                        # comptée horizontalement
                    groupe_horizontal = []
                    i = 0
                    while (c+i < len(self.cases[l]) and          # Tant qu'on est dans les bornes et
                          self.cases[l][c+i].bateau() is None):  # que la case est vide
                        groupe_horizontal.append(self.cases[l][c+i])
                        i += 1
                    if groupe_horizontal:  # Si le groupe horizontal contient au moins une case
                        libres_horizontales.append(groupe_horizontal)  # ajoute le groupe s'il contient au moins une case
                if not self.element_dans_liste(self.cases[l][c], libres_verticales):    # Si la case n'a pas déjà été
                                                                                        # comptée verticalement
                    groupe_vertical = []
                    i = 0
                    while (l+i < len(self.cases) and                # Tant qu'on est dans les bornes et
                           self.cases[l+i][c].bateau() is None):    # que la case est vide
                        groupe_vertical.append(self.cases[l+i][c])
                        i += 1
                    if groupe_vertical:  # Si le groupe vertical contient au moins une case
                        libres_verticales.append(groupe_vertical)  # ajoute le groupe s'il contient au moins une case

        # On enlève les cases qui sont comptées à double alors qu'elle ne devaient pas
        for groupe in libres_horizontales:
            if len(groupe) == 1:  # Si c'est une case isolée horizontalement
                if self.element_dans_liste(groupe[0], libres_verticales):  # Si la case est déjà comptée verticalement
                    libres_horizontales.remove(groupe)
        for groupe in libres_verticales:
            if len(groupe) == 1:  # Si c'est une case isolée verticalement
                if self.element_dans_liste(groupe[0], libres_horizontales):  # Si la case est déjà comptée horizontalement
                    libres_verticales.remove(groupe)

        cases_libres = libres_horizontales + libres_verticales
        return sorted(cases_libres, key=lambda x: len(x))  # On renvoie les groupes de cases par ordre croissant de taille

    def groupes_de_cases_libres(self, longueur):
        """
        Fonction renvoyant tous les groupes de cases libres possibles ayant une certaine longueur.

        :param longueur: longueur des groupes
        :return: liste contenant les groupes de cases libres
        """
        cases_libres = self.cases_libres()
        groupes = list(cases_libres)  # On crée une copie des cases libres
        for groupe in cases_libres:
            if len(groupe) < longueur:
                groupes.remove(groupe)  # On enlève tous les groupes qui sont trop petits
            elif len(groupe) > longueur:
                for i in range(len(groupe)-longueur):
                    groupes.append(groupe[i:longueur+i])    # Si un groupe est trop grand, on le divise en plusieurs
                                                            # groupes possibles
                groupes.remove(groupe)
        return groupes

    def placer_bateaux(self):
        """
        Fonction permettant de placer des bateaux de manière aléatoire sur la grille

        :param bateaux: bateaux à placer
        :return: réussite de l'opération
        """
        bateaux_a_placer = trier_bateaux_par_taille(self.bateaux, True)  # On trie les bateaux dans l'ordre décroissant pour
                                                                    # placer les plus grands en premier
        for bateau in bateaux_a_placer:
            cases_possibles = self.groupes_de_cases_libres(bateau.TAILLE)  # TODO: attention bugs possibles si aucun groupe n'est trouvé
            bateau.set_cases(random.choice(cases_possibles))  # Sélectionne un groupe de cases aléatoire pour les cases du bateau
        return True

    @staticmethod
    def coord_ecran_vers_index(coordonnees):
        pass

    def coord_bataille_vers_index(self, coordonnees):
        """
        Convertit les coordonnées de la bataille navale (ex : "A5" ou ("A", 5)) en coordonnées de la grille (ex: (1, 5)).

        :param coordonnees: coordonnées de la bataille navale
        :return: coordonnées équivalentes sur la grille ou "False" si l'opération a échoué
        """
        copie_coordonnees = "".join(coordonnees)  # On assure que "copieCoordonnes" est une chaîne de caractères et non une liste ou un tuple
        copie_coordonnees = copie_coordonnees.replace(" ", "")  # On enlève les espaces.
        copie_coordonnees = copie_coordonnees.replace(".", "")  # On enlève les points
        copie_coordonnees = copie_coordonnees.replace(",", "")  # On enlève les virgules
        copie_coordonnees = copie_coordonnees.lower()  # On met tout en minuscules.

        x = ""
        lettres = ""
        while copie_coordonnees[0].isalpha():
            lettres += copie_coordonnees[0]  # On copie toutes les lettres du début dans "x" et on les enlève de "copie_coordonnees".
            copie_coordonnees = copie_coordonnees[1:len(copie_coordonnees)]
        for c in lettres:
            x += str(string.ascii_letters.index(c))  # On transforme les lettres en nombres TODO: Augmenter sécurité
        x = int(x)

        y = int(copie_coordonnees) - 1
        if x in range(self.TAILLE) and y in range(self.TAILLE):
            return x, y
        else:
            return False

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

    def tirer_coord_ecran(self, coordonnees):
        pass
        # TODO: terminer méthode

    def sont_coordonnees_index(self, coordonnees):
        """
        Détermine si "coordonnees" représente l'index d'une case de la grille.

        :param coordonnees: coordonnées à tester
        :return: Booléen valant "True" si "coordonnées" représente un index, "False" sinon.
        """
        if type(coordonnees) is tuple or type(coordonnees) is list:  # Si les coordonnées sont une liste ou un tuple
            if len(coordonnees) == 2:
                for coordonnee in coordonnees:
                    if (type(coordonnee) is not int and type(coordonnees) is not float # Si le type des coordonnées n'est pas un nombre
                    or coordonnee not in range(self.TAILLE)):  # ou si les coordonnées n'ont pas la bonne valeur
                        return False
                    return True
        return False  # Si une des conditions plus haut n'est pas satisfaite, on renvoie "False"

    def tirer(self, coordonnees):
        """
        Méthode permettant de tirer aux coordonnées "coordonnees".

        Les coordonnées peuvent être sous deux formes différentes : index de la case ou coordonnées de la bataille
        navale, par ex : "A6".
        :param coordonnees: coordonnées où tirer
        :return: État de la case après le tir si celui-ci a réussi, "None" si la case a déjà reçu un tir et "False"
        s'il y a eu une erreur
        """
        # On vérifie que les coordonnées sont valides et on les convertit en index
        if type(coordonnees) is str:  # Si les coordonnées sont présentées en coordonnées de la bataille navale
            coordonnees_index = self.coord_bataille_vers_index(coordonnees)
        elif self.sont_coordonnees_index(coordonnees):
            coordonnees_index = coordonnees
        else:
            return False
        if not coordonnees_index:
            return False

        case = self.cases[coordonnees_index[1]][coordonnees_index[0]]   # On accède la case visée, tout en faisant
                                                                        # attention à mettre la coordonnée y en premier
        return case.recevoir_tir()
