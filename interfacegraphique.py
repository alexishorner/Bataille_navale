# coding: utf-8
# Attention les noms de variables ne contiennent pas d'accent, ce qui peut changer leur signification (par ex : côté devient cote)
from __future__ import print_function  # Permet d'utiliser la fonction print de python 3, qui a le paramètre "end"
from sys import stdin  # Sert à recevoir des entrées de l'utilisateur en restant compatible avec python 3
from case import Etat
import turtle
import string
import math
from sys import platform
import os


def recevoir_entree(texte_a_afficher):
    """
    Fonction équivalente à "raw_input()", mais compatible avec python 3

    :param texte_a_afficher: texte aà afficher avant de recevoir l'entrée de l'utilisateur
    :return: texte entré par l'utilisateur
    """
    print(texte_a_afficher)
    return stdin.readline().replace("\n", "")


class Tortue(turtle.Turtle):
    """
    Cette classe permet de customiser la tortue fournie par le module "turtle".
    """
    COULEUR = "white"  # couleur de l'intértieur des cases

    def __init__(self):
        """
        constructeur de la classe "Tortue"
        """
        turtle.Turtle.__init__(self)
        self.hideturtle()  # cache la tortue
        self.screen.tracer(0, 0)  # rend le dessin instantané, mais l'écran doit être rafraîchit manuellement en appelant "self.screen.update()"
        self.fillcolor(self.COULEUR)

    def _dessiner_forme(self, chemin, ferme=True):
        """
        Dessine une forme à l'écran.

        :param chemin: liste de points décrivant le chemin suivit par le stylo
        :param ferme: booléen indiquant si le style doit fermer la forme en reliant le premier et dernier point.
        :return: "None"
        """
        self.up()
        self.goto(chemin[0])
        self.down()
        self.begin_fill()
        for i in range(1, len(chemin)):  # le stylo est déjà à "chemin[0]", donc on commence à 1
            self.goto(chemin[i])
        if ferme:
            self.goto(chemin[0])
        self.end_fill()

    def dessiner_case(self, case):
        """
        Affiche une case à l'écran.

        Le dessin au centre de la case dépend de son état.
        :param case: case à dessiner
        :return: "None"
        """
        self._dessiner_forme(case.carre())
        self._dessiner_etat(case)
        self.screen.update()  # on actualise l'écran pour afficher les changements

    def _dessiner_etat(self, case):
        """
        Dessine l'état de la case.

        :param case: case dont il faut dessiner l'état
        :return: "None"
        """
        if case.etat != Etat.VIDE and case.etat != Etat.BATEAU_INTACT:
            self.up()
            self.goto(case.milieu())
            self.down()
            self.write(case.caractere_etat())


class Afficheur:
    """
    Cette classe permet de dessiner les objets à l'écran. Elle utilise un objet "Tortue" ou la console pour dessiner à l'écran.
    """
    def __init__(self, grille):
        """
        constructeur de la classe "Stylo"

        :param grille: grille de jeu à afficher
        """
        self.grille = grille
        self.tortue = Tortue()
        self.nombre_de_coups = 0

    @staticmethod
    def afficher_erreur():
        print("Une erreur s'est produite.")

    def decimales(cls, nombre):
        """
        Nombre de décimales d'un nombre.

        :param nombre: nombre dont on veut savoir les décimales
        :return: nombre de décimales
        """
        return int(math.floor(math.log10(nombre)+0.00001)+1)

    def dessiner_premiere_ligne_console(self):
        self.ajouter_espacement_avant()
        for index_x in range(self.grille.TAILLE):
            print("_" + string.ascii_uppercase[index_x], end="")
        print("_\n", end="")

    def dessiner_grille_console(self):
        """
        Dessine la grille dans la console.

        Exemple pour une grille de largeur 10 :
              _A_B_C_D_E_F_G_H_I_J_
             1|_|_|_|_|_|_|_|_|_|_|
             2|_|_|_|_|_|_|_|_|_|_|
             3|_|_|_|_|_|_|_|_|_|_|
             4|_|_|_|_|_|_|_|_|_|_|
             5|_|_|_|_|_|_|_|_|_|_|
             6|_|_|_|_|_|_|_|_|_|_|
             7|_|_|_|_|_|_|_|_|_|_|
             8|_|_|_|_|_|_|_|_|_|_|
             9|_|_|_|_|_|_|_|_|_|_|
            10|_|_|_|_|_|_|_|_|_|_|
        :return: "None"
        """
        for index_y in range(self.grille.TAILLE):
            for index_x in range(self.grille.TAILLE):
                if index_y == 0 and index_x == 0:
                    self.dessiner_premiere_ligne_console()

                if index_x == 0:
                    self.ajouter_espacement_avant(index_y+1)
                    print(str(index_y+1), end="")

                self.dessiner_case_console(index_y, index_x)

    def dessiner_case_console(self, index_y, index_x):
        """
        Dessine une case de la grille dans la console.

        :param index_y: index de la ligne
        :param index_x: index de la colonne
        :return: "None"
        """
        case = self.grille.cases[index_y][index_x]
        print("|", end="")
        print(case.caractere_etat(), end="")
        if index_x == self.grille.TAILLE-1:
            print("|\n", end="")

    def ajouter_espacement_avant(self, nombre=None):
        """
        Ajoute un espacement avant la grille pour aligner les nombres sur la droite.

        :param nombre: nombre qui doit être aligné
        :return: "None"
        """
        espacement_total = self.decimales(self.grille.TAILLE)
        if nombre is None:
            espacement = espacement_total
        else:
            espacement = espacement_total - self.decimales(nombre)
        print(" "*espacement, end="")  # Ajoute un espacement pour aligner les nombres à droite

    def _effacer_tout_console(self):
        """
        Fonction multi-plateforme permettant d'effacer le contenu de la console.

        :return: "None"
        """
        if platform == "win32":  # La commande dépend du système d'exploitation
            _ = os.system("cls")
        else:
            _ = os.system("clear")

    def boucle_des_evenements(self):
        recommencer = True
        while recommencer:
            entree = recevoir_entree("\n>>> ") # Équivalent à "raw_input("\n>>> ")", mais compatible avec python 3
            retour = self.grille.tirer(entree)
            if retour is None:
                print("\nVous avez déjà tiré sur cette case.")
            elif not retour and retour not in (Etat.DANS_L_EAU, Etat.TOUCHE, Etat.COULE):
                self.afficher_erreur()
            else:
                if retour == Etat.DANS_L_EAU:
                    print("Dans l'eau")
                    self.nombre_de_coups += 1
                elif retour == Etat.TOUCHE:
                    print("Touché")
                    self.nombre_de_coups += 1
                else:
                    print("Coulé")
                    self.nombre_de_coups += 1

