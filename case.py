# coding: utf-8
"""
Module contenant les classes relatives aux cases et à la grille de jeu.
"""
from enum import IntEnum, unique
import string
import random
import time


def trier_bateaux_par_taille(bateaux, decroissant=False):
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

    La position de chaque case est la position de son coin inférieur gauche.
    """
    largeur_pixels = 40  # taille en pixels, le nom est en majuscules par convention, car c'est une constante
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
            if cases[0].position[Coord.x] == cases[-1].position[Coord.x]:
                # si la première case a la même coordonnée x que la dernière
                coord = Coord.x  # on défini une variable indiquant qu'il faut regarder l'alignement sur x
            elif cases[0].position[Coord.y] == cases[-1].position[Coord.y]:
                # si la première case a la même coordonnée y que la dernière
                coord = Coord.y  # on défini une variable indiquant qu'il faut regarder l'alignement sur y
            else:
                return False

            premiere_case = cases[0]
            for i in range(1, len(
                    cases) - 1):  # on ne teste pas la première et la dernière, car cela a déjà été fait avant
                if abs(cases[i].position[coord] - premiere_case.position[coord]) > 0.0001:
                    # si la case n'est pas alignée avec la première case
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
                    if separation_horizontale < cls.largeur_pixels or separation_verticale < cls.largeur_pixels:
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
        cote = self.largeur_pixels
        return [x, y], [x + cote, y], [x + cote, y + cote], [x, y + cote]

    def milieu(self):
        """
        :return: position du milieu de la case
        """
        x = self.position[Coord.x]
        y = self.position[Coord.y]
        demi_longueur = self.largeur_pixels / 2.0
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

        :return: 1. État de la case après l'opération ou "None" si la case a déjà reçu un tir ou
                    "False" s'il y a eu une erreur
                 2. Cases modifiées s'il y en a, "None" sinon
        """
        if self._bateau is not None:  # si un bateau est présent sur la case
            return self._bateau.recevoir_tir(self)
        else:
            if self.etat != Etat.DANS_L_EAU:
                self.etat = Etat.DANS_L_EAU
                return self.etat, [self]
            return None, None


class Grille:
    """
    Classe représentant la grille de jeu de la bataille navale.

    Elle contient un tableau en deux dimensions stockant des cases. La première case est dans le coin supérieur gauche.
    Les cases sont accédées de la manière suivante: self.cases[ligne][colonne]
    """
    LARGEUR_PIXELS_IDEALE = 400.0
    TAILLE_MAX = 26  # Si la taille excède 26, les coordonnées nécessitent plusieurs lettres

    def __init__(self, bateaux, taille=10):
        self.bateaux = bateaux
        self.cases = []
        self._taille = 0  # On crée la variable "self.taille"
        self.set_taille(taille)  # On change la valeur de "self.taille"

    def creer_cases(self):
        """
        Crée les cases de la grille en ajustant leur taille pour avoir une largeur de grille approximativement fixe,
        tout en ayant un nombre entier pour la largeur de chaque case.

        :return: "None"
        """
        self.cases = []
        Case.largeur_pixels = round(
            self.LARGEUR_PIXELS_IDEALE / self._taille)  # ajuste la largeur des cases en fonction de la taille de la grille
        decalage_x = -self._taille * Case.largeur_pixels / 2.0 + 80  # décalage permettant de centrer la grille
        decalage_y = self._taille * Case.largeur_pixels / 2.0 - 40  # on décale moins, car sinon la grille est trop haute
        for i in range(self._taille):
            ligne = []
            for j in range(self._taille):
                position = (j * Case.largeur_pixels + decalage_x, -i * Case.largeur_pixels + decalage_y)
                ligne.append(Case(position))
            self.cases.append(ligne)

    def taille(self):
        """
        Accesseur de l'attribut protégé "_taille"
        :return:
        """
        return self._taille

    def set_taille(self, taille):
        """
        Change la taille de la grille.

        :param taille: nouvelle taille de la grille
        :return:
        """
        if taille <= self.TAILLE_MAX:
            self._taille = taille
        else:
            self._taille = self.TAILLE_MAX
        self._taille = taille
        self.creer_cases()

    def largeur_pixels(self):
        """
        Renvoie la largeur exacte de la grille en pixels.

        :return: largeur de la grille en pixels
        """
        return self._taille * Case.largeur_pixels

    def position_coins(self):
        """
        Retourne les coordonnées des coins de la grille.

        :return: liste contenant les quatre coins de la grille.
        """
        coin_superieur_gauche = self.cases[0][0].carre()[3]
        coin_inferieur_gauche = self.cases[self._taille - 1][0].carre()[0]
        coin_inferieur_droit = self.cases[self._taille - 1][self._taille - 1].carre()[1]
        coin_superieur_droit = self.cases[0][self._taille - 1].carre()[2]
        return coin_superieur_gauche, coin_inferieur_gauche, coin_inferieur_droit, coin_superieur_droit

    def nombre_de_cases_occupees(self):
        """
        Renvoie le nombre de cases occupées par les bateaux

        :return: nombre de cases occupées
        """
        nombre_de_cases_occupees = 0
        for bateau in self.bateaux:
            nombre_de_cases_occupees += bateau.TAILLE
        return nombre_de_cases_occupees

    def bateaux_restants(self):
        """
        Renvoie les bateaux non coulés

        :return: bateaux restants
        """
        bateaux_restants = []
        for bateau in self.bateaux:
            if not bateau.est_coule():
                bateaux_restants.append(bateau)
        return bateaux_restants

    def nombrebateauxdeboutpartype(self, typebateaux):
        """renvoie le nombre de bateaux pas coulés d'un certain type
        :param typebateaux: type des bateaux
        :return: nombre de bateaux pas coulés ayant le type demandé"""
        nombrebateauxdeboutpartype = 0  # variable comptant le nombre de bateaux debout du type voulu
        touslesbateauxrestants = self.bateaux_restants()
        for i in range(len(touslesbateauxrestants)):

            bateaurestant = touslesbateauxrestants[i]  # On regarde chaque bateau restant
            if bateaurestant.TYPE == typebateaux:
                nombrebateauxdeboutpartype += 1
        return nombrebateauxdeboutpartype

    def enlever_bateaux(self):
        """
        Enlève tous les bateaux de la grille.

        :return: "None"
        """
        for ligne in self.cases:
            for case in ligne:
                if case.bateau() is not None:
                    case.bateau().set_cases(None)  # enlève les bateaux un à un

    def reinitialiser(self):
        """
        Remet toutes les cases à leur état initial.

        :return: "None"
        """
        self.enlever_bateaux()  # Enlève tous les bateaux
        for ligne in self.cases:
            for case in ligne:
                case.etat = Etat.VIDE  # Remet l'état de chaque case à zéro

    def placer_bateaux(self):
        """
        Fonction permettant de placer des bateaux de manière aléatoire sur la grille

        :return: réussite de l'opération
        """
        self.reinitialiser()
        bateaux_a_placer = trier_bateaux_par_taille(self.bateaux,
                                                    True)  # On trie les bateaux dans l'ordre décroissant pour
        # placer les plus grands en premier
        for bateau in bateaux_a_placer:
            temps_depart = time.time()  # On regarde quand on a commencé à placer le bateau
            recommencer = True
            while recommencer and time.time() - temps_depart < 1:
                # Cette boucle se répète tant qu'on a pas réussi à placer le bateau
                cases_bateau = []
                index_premiere_case = (random.randint(0, self._taille - 1), random.randint(0, self._taille - 1))
                sens_vertical = random.choice(
                    (0, 0, -1, 1))  # Variable déterminant dans quel sens on cherche les cases horizontalement
                if sens_vertical == 0:  # Si on cherche les cases verticalement
                    sens_horizontal = random.choice((-1, 1))  # on détermine si on cherche vers la gauche ou la droite
                else:
                    sens_horizontal = 0  # La valeur 0 empêche de chercher horizontalement
                index_derniere_case = (index_premiere_case[Coord.y] + sens_vertical * bateau.TAILLE,
                                       index_premiere_case[Coord.x] + sens_horizontal * bateau.TAILLE)
                if (index_derniere_case[Coord.y] in range(self._taille) and
                        index_derniere_case[Coord.x] in range(self._taille)):  # Si la dernière case est dans la grille
                    for i in range(bateau.TAILLE):
                        index_y = index_premiere_case[Coord.y] + i * sens_vertical
                        index_x = index_premiere_case[Coord.x] + i * sens_horizontal
                        case = self.cases[index_y][index_x]
                        if case.bateau() is None:  # Si la case est vide
                            cases_bateau.append(case)
                        else:
                            break  # Si au moins une case n'est pas vide, on sort de la boucle for et on recommence au
                            # début de la boucle while
                    if len(cases_bateau) == bateau.TAILLE:  # Si toutes les cases parcourues étaient vides
                        bateau.set_cases(cases_bateau)
                        recommencer = False
            if time.time() - temps_depart >= 1:
                return False
        return True

    def coord_bataille_vers_index(self, coordonnees):
        """
        Convertit les coordonnées de la bataille navale (ex : "A5" ou ("A", 5)) en coordonnées de la grille (ex: (1, 5)).

        :param coordonnees: coordonnées de la bataille navale
        :return: coordonnées équivalentes sur la grille ou "False" si l'opération a échoué
        """
        copie_coordonnees = "".join(
            coordonnees)  # On assure que "copieCoordonnes" est une chaîne de caractères et non une liste ou un tuple
        copie_coordonnees = copie_coordonnees.replace(" ", "")  # On enlève les espaces.
        copie_coordonnees = copie_coordonnees.replace(".", "")  # On enlève les points
        copie_coordonnees = copie_coordonnees.replace(",", "")  # On enlève les virgules
        copie_coordonnees = copie_coordonnees.lower()  # On met tout en minuscules.
        x = ""
        lettres = ""
        while copie_coordonnees and copie_coordonnees[0].isalpha():
            lettres += copie_coordonnees[
                0]  # On copie toutes les lettres du début dans "x" et on les enlève de "copie_coordonnees".
            copie_coordonnees = copie_coordonnees[1:len(copie_coordonnees)]
        for c in lettres:
            x += str(string.ascii_letters.index(c))  # On transforme les lettres en nombres
        try:
            x = int(x)
            y = int(copie_coordonnees) - 1
        except ValueError:  # Si on arrive pas à convertir x ou y en nombres
            return False
        if x in range(self._taille) and y in range(self._taille):
            return x, y
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

    def sont_coordonnees_index(self, coordonnees):
        """
        Détermine si "coordonnees" représente l'index d'une case de la grille.

        :param coordonnees: coordonnées à tester
        :return: Booléen valant "True" si "coordonnées" représente un index, "False" sinon.
        """
        if type(coordonnees) is tuple or type(coordonnees) is list:  # Si les coordonnées sont une liste ou un tuple
            if len(coordonnees) == 2:
                for coordonnee in coordonnees:
                    if (type(coordonnee) is not int and type(
                            coordonnees) is not float  # Si le type des coordonnées n'est pas un nombre
                            or coordonnee not in range(
                                self._taille)):  # ou si les coordonnées n'ont pas la bonne valeur
                        return False
                    return True
        return False  # Si une des conditions plus haut n'est pas satisfaite, on renvoie "False"

    def tirer(self, coordonnees):
        """
        Méthode permettant de tirer aux coordonnées "coordonnees".

        Les coordonnées peuvent être sous deux formes différentes : index de la case ou coordonnées de la bataille
        navale, par ex : "A6".
        :param coordonnees: coordonnées où tirer
        :return: 1. État de la case après le tir si celui-ci a réussi, "None" si la case a déjà reçu un tir et "False"
                    s'il y a eu une erreur
                 2. Cases modifiées s'il y en a, "None" sinon
        """
        # On vérifie que les coordonnées sont valides et on les convertit en index
        if type(coordonnees) is str:  # Si les coordonnées sont présentées en coordonnées de la bataille navale
            coordonnees_index = self.coord_bataille_vers_index(coordonnees)
        elif self.sont_coordonnees_index(coordonnees):
            coordonnees_index = coordonnees
        else:
            return False, None
        if not coordonnees_index:
            return False, None

        case = self.cases[coordonnees_index[1]][coordonnees_index[0]]  # On accède la case visée, tout en faisant
        # attention à mettre la coordonnée y en premier
        return case.recevoir_tir()
