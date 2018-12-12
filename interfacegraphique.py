# coding: utf-8
# Attention les noms de variables ne contiennent pas d'accent, ce qui peut changer leur signification (par ex : côté devient cote)
from __future__ import print_function  # Permet d'utiliser la fonction print de python 3, qui a le paramètre "end"
from sys import stdin  # Sert à recevoir des entrées de l'utilisateur en restant compatible avec python 3
from case import Etat, Case, Grille
import turtle
import string
import math
from sys import platform
import os
from enum import IntEnum, unique
import random


def chaine_nettoyee(chaine):
    """
    Renvoie une chaîne de caractères identique à "chaine", mais en minuscules et sans espaces

    :param chaine: Chaîne de caractères à nettoyer
    :return: Chaîne nettoyée
    """
    return chaine.lower().replace(" ", "")


def decimales(nombre):
        """
        Nombre de décimales d'un nombre.

        :param nombre: nombre dont on veut savoir les décimales
        :return: nombre de décimales
        """
        return int(math.floor(math.log10(nombre)+0.00001)+1)


@unique
class Mode(IntEnum):
    """
    Énumération décrivant les différents modes d'affichage.

    "CONSOLE" est l'affichage dans la console
    "TORTUE" est l'affichage avec la tortue
    """
    CONSOLE, TORTUE = range(2)


class Tortue(turtle.Turtle):
    """
    Cette classe permet de customiser la tortue fournie par le module "turtle".
    """
    COULEUR_DEFAUT = "white"  # couleur de l'intértieur des cases


    def __init__(self):
        """
        constructeur de la classe "Tortue"
        """
        turtle.Turtle.__init__(self)
        self.hideturtle()  # cache la tortue
        self.screen.tracer(0, 0)  # rend le dessin instantané, mais l'écran doit être rafraîchit manuellement en appelant "self.screen.update()"
        self.fillcolor(self.couleur_case(Etat.VIDE))

    @staticmethod
    def couleur_case(etat):
        """
        Retourne la couleur correspondant à l'état de la case.

        :param etat: état de la case à dessiner
        :return: couleur correspondant à l'état de la case
        """
        if etat == Etat.DANS_L_EAU:
            return "blue"
        elif etat == Etat.TOUCHE:
            return "orange"
        elif etat == Etat.COULE:
            return "red"
        else:
            return "white"

    def afficher_message(self, message, position, alignement="left", police=("Arial", 8, "normal")):
        """
        Affiche un message à une certaine position.

        :param message: message à afficher
        :param alignement: alignement du texte
        :param position: endroit où afficher le message
        :param police: police à utiliser pour écrire
        :return: "None"
        """
        self.up()
        self.goto(position)
        self.down()
        self.write(message, align=alignement, font=police)

    def dessiner_graduations(self, origine, cote_grille):
        x_0, y_0= origine
        decimales_max = decimales(cote_grille)
        cote_case = Case.TAILLE
        taille_police = int(Case.TAILLE/10.0+8)
        for i in range(cote_grille):
            x = x_0+i*cote_case+cote_case/2.0
            y = y_0+cote_case+decimales_max*taille_police/2.0
            self.afficher_message(string.ascii_uppercase[i], (x, y), alignement="center", police=("Arial", taille_police, "bold"))
            x = x_0-decimales_max*taille_police/2.0
            y = y_0-(i-1)*cote_case-cote_case/2.0-taille_police
            self.afficher_message(str(i+1), (x, y), alignement="right", police=("Arial", taille_police, "bold"))

    def dessiner_case(self, case):
        """
        Dessine une case à l'écran.

        :param case: case à dessiner
        :return: "None"
        """
        self.fillcolor(self.couleur_case(case.etat))
        points = case.carre()
        self.up()
        self.goto(points[0])
        self.down()
        self.begin_fill()
        for i in range(1, len(points)):  # la tortue est déjà à "points[0]", donc on commence à 1
            self.goto(points[i])
        self.goto(points[0])
        self.end_fill()

    def dessiner_grille(self, cases):
        """
        Dessine la grille.

        :param cases: grille à dessiner
        :return: "None"
        """
        self.clear()
        self.dessiner_graduations(cases[0][0].position, len(cases))
        for ligne in cases:
            for case in ligne:
                self.dessiner_case(case)
        self.screen.update()


class Afficheur:
    """
    Cette classe permet de dessiner les objets à l'écran. Elle utilise un objet "Tortue" ou la console pour dessiner à l'écran.
    """
    NOMBRE_DE_COUPS_MAX = 30
    def __init__(self, grille):
        """
        constructeur de la classe "Stylo"

        :param grille: grille de jeu à afficher
        """
        self.grille = grille
        self.tortue = Tortue()
        self._nombre_de_coups = 0

    def coups_restants(self):
        return self.NOMBRE_DE_COUPS_MAX-self._nombre_de_coups

    def rejouer(self):
        self.grille.reinitialiser()
        self.grille.placer_bateaux()
        self.dessiner_tout()
        self._nombre_de_coups = 0

    def sur_coup_joue(self):
        self._nombre_de_coups += 1

    def joueur_a_perdu(self):
        if self.coups_restants() <= 0:
            return True
        return False

    def afficher(self, message, fin="\n"):
        """
        Affiche un message.

        :param message: message à afficher
        :param fin: caractère à placer après le message
        :return:
        """
        print(message, end=fin)
        self.tortue.afficher_message(message+fin, (0, self.grille.TAILLE*Case.TAILLE))

    def recevoir_entree(self, texte_a_afficher=""):
        """
        Fonction équivalente à "raw_input()", mais compatible avec python 3 et avec la tortue

        :param texte_a_afficher: texte aà afficher avant de recevoir l'entrée de l'utilisateur
        :return: texte entré par l'utilisateur
        """
        print(texte_a_afficher, end="")
        return stdin.readline().replace("\n", "")

    def confirmer_question(self, question):
        """
        Confirme si l'utilisateur répond oui à une question.

        :param question: question posée
        :return: Booléen indiquant si l'utilisateur a répondu par l'affirmative
        """
        entree = self.recevoir_entree(question)
        entree = chaine_nettoyee(entree)
        if entree in ("oui", "o"):
            return True
        return False

    def afficher_erreur(self):
        """
        Indique à l'utilisateur qu'une erreur s'est produite.

        :return: "None"
        """
        self.afficher("Une erreur s'est produite.")

    def confirmer_quitter(self):
        """
        Demande la confirmation à l'utilisateur si il veut réellement quitter.

        :return: Booléen indiquant si l'utilisateur veut quitter.
        """
        return self.confirmer_question("\nÊtes-vous sûr(e) de vouloir quitter? o/n\n")

    def demander_rejouer(self):
        """
        Demande à l'utilisateur si il veut rejouer.

        :return: Booléen indiquant si le joueur veut rejouer
        """
        while True:
            entree = self.recevoir_entree("Voulez-vous rejouer? o/n ")
            if entree.lower() in ("o", "oui"):
                return True
            elif entree.lower() in ("n", "non"):
                return False
            else:
                self.afficher("Erreur, entrée invalide")

    def dessiner_tout(self):
        """
        Dessine la grille en entier avec la tortue et dans la console et affiche différentes informations.

        C'est ici que les éléments à l'écran ne changeant pas, comme le fond d'écran, sont dessinés.
        :return: "None"
        """
        self.dessiner_grille_console()
        self.tortue.dessiner_grille(self.grille.cases)
        self.afficher_coups_restants()

    def actualiser(self, cases=None):
        """
        Actualise l'écran.

        :param cases: liste de cases à actualiser
        :return: "None"
        """
        self.dessiner_grille_console()
        if cases is not None:
            for case in cases:
                self.tortue.dessiner_case(case)
        self.tortue.screen.update()
        self.afficher_coups_restants()

    def ajouter_espacement_avant(self, nombre=None):
        """
        Ajoute un espacement avant la grille pour aligner les nombres sur la droite.

        :param nombre: nombre qui doit être aligné
        :return: "None"
        """
        espacement_total = decimales(self.grille.TAILLE)
        if nombre is None:
            espacement = espacement_total
        else:
            espacement = espacement_total - decimales(nombre)
        print(" "*espacement, end="")  # Ajoute un espacement pour aligner les nombres à droite

    def dessiner_premiere_ligne_console(self):
        """
        Dessine la ligne de numérotation des colonnes de la grille.

        Exemple: _A_B_C_D_E_F_G_H_I_J_
        :return: "None"
        """
        self.ajouter_espacement_avant()
        for index_x in range(self.grille.TAILLE):
            print("_" + string.ascii_uppercase[index_x], end="")
        print("_\n", end="")

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

    def _effacer_tout_console(self):
        """
        Fonction multi-plateforme permettant d'effacer le contenu de la console.

        :return: "None"
        """
        if platform == "win32":  # La commande dépend du système d'exploitation
            _ = os.system("cls")    # Le "_" avant le signe "=" sert à récupérer le retour de la fonction pour empêcher
                                    # qu'il soit imprimé
        else:
            _ = os.system("clear")  # Idem

    def afficher_coups_restants(self):
        print("Coups restants : " + str(self.coups_restants()))

    def joueur_a_gagne(self):
        """
        Détermine si le joueur a gagné

        :return: Booléen indiquant si le joueur a gagné
        """
        for bateau in self.grille.bateaux:
            if not bateau.est_coule():
                return False
        return True

    def tirer(self, coordonnees):
        """
        Tire sur une case en utilisant la fonction correspondant au mode
        :param coordonnees: coordonnées où tirer
        :return:  État de la case après le tir si celui-ci a réussi, "None" si la case a déjà reçu un tir et "False"
        s'il y a eu une erreur
        """
        return self.grille.tirer(coordonnees)

    def afficher_retour_tir(self, retour):
        """
        Affiche un message à l'écran en fonction du retour de la fonction de tir

        :param retour: retour de la fonction de tir
        :return: "None"
        """
        if retour is None:
            self.afficher("\nVous avez déjà tiré sur cette case.")
        elif retour in (Etat.DANS_L_EAU, Etat.TOUCHE, Etat.COULE):
            if retour == Etat.DANS_L_EAU:
                self.afficher("Dans l'eau")
            elif retour == Etat.TOUCHE:
                self.afficher("Touché")
            else:
                self.afficher("Coulé")
            self.sur_coup_joue()
        else:
            self.afficher_erreur()

    def avancer_d_un_tour(self, entree):
        """
        Fonction permettant au jeu d'avancer d'un tour.

        Elle peut être passée à "turtle.Turtle.screen.onclick", car elle commence par les arguments "x" et "y"
        :param entree: entrée de l'utilisateur dans la console
        :return: booléen indiquant si le jeu doit continuer
        """
        continuer = True
        if chaine_nettoyee(entree) in ("quitter", "q"):  # Si l'utilisateur veut quitter
            continuer = not self.confirmer_quitter()
        else:
            retour, cases = self.grille.tirer(entree)  # On tire sur la case et on enregistre le retour de la méthode
            self.afficher_retour_tir(retour)  # TODO: continuer
            self.actualiser(cases)

            if self.joueur_a_gagne():
                print("Vous avez gagné, bravo!")
                rejouer = self.demander_rejouer()
                continuer = rejouer
                if rejouer:
                    self.rejouer()
            elif self.joueur_a_perdu():
                print("Vous avez perdu!")
                if self.demander_rejouer():
                    self.rejouer()
        return continuer




    def boucle_des_evenements(self):
        """
        Démarre la boucle des évènements.

        Demande à l'utlisateur où il veut tirer et tire sur la case.
        :return: "None"
        """
        self.dessiner_tout()
        continuer = True
        while continuer:
            entree = self.recevoir_entree("\n>>> ")  # Équivalent à "raw_input("\n>>> ")", mais compatible avec python 3
            #entree = string.ascii_uppercase[random.randint(0, self.grille.TAILLE)] + str(random.randint(0, self.grille.TAILLE))
            # TODO: enlever ligne de test
            continuer = self.avancer_d_un_tour(entree)






