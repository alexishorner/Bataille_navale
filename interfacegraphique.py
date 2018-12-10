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
    COULEUR = "white"  # couleur de l'intértieur des cases

    def __init__(self):
        """
        constructeur de la classe "Tortue"
        """
        turtle.Turtle.__init__(self)
        self.hideturtle()  # cache la tortue
        self.screen.tracer(0, 0)  # rend le dessin instantané, mais l'écran doit être rafraîchit manuellement en appelant "self.screen.update()"
        self.fillcolor(self.COULEUR)

    def initialiser(self, sur_clic):
        """
        Démarre l'affichage avec la tortue.

        :param sur_clic: fonction à appeler lorsque la fenêtre est cliquée
        :return: "None"
        """
        self.screen.onclick(sur_clic)
        turtle.mainloop()

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

    def dessiner_case(self, case):
        """
        Affiche une case à l'écran.

        Le dessin au centre de la case dépend de son état.
        :param case: case à dessiner
        :return: "None"
        """
        self._dessiner_forme(case.carre())
        self._dessiner_etat(case)

    def dessiner_grille(self, grille):
        """
        Dessine la grille.

        :param grille: grille à dessiner
        :return: "None"
        """
        self.clear()
        for ligne in grille:
            for case in ligne:
                self.dessiner_case(case)
        self.screen.update()

    def afficher_message(self, message, position):
        """
        Affiche un message à une certaine position.

        :param message: message à afficher
        :param position: endroit où afficher le message
        :return: "None"
        """
        self.up()
        self.goto(position)
        self.down()
        self.write(message)


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
        self._mode = Mode.CONSOLE
        self.tortue = None
        self.nombre_de_coups = 0

    def afficher(self, message, fin="\n"):
        """
        Affiche un message.

        :param message: message à afficher
        :param fin: caractère à placer après le message
        :return:
        """
        if self._mode == Mode.CONSOLE:
            print(message, end=fin)
        else:
            self.tortue.afficher_message(message+fin, (0, self.grille.TAILLE*Case.TAILLE))

    def recevoir_entree(self, texte_a_afficher=""):
        """
        Fonction équivalente à "raw_input()", mais compatible avec python 3 et avec la tortue

        :param texte_a_afficher: texte aà afficher avant de recevoir l'entrée de l'utilisateur
        :return: texte entré par l'utilisateur
        """
        print(texte_a_afficher, end="")
        return stdin.readline().replace("\n", "")
        # TODO: éventuellement adapter à la tortue

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
        # TODO: adapter à la tortue
            # TODO: Possibilités: 1. ajouter champ avec Tkinter 2. créer boutons avec tortue

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
        # TODO: éventuellement adapter à la tortue

    def confirmer_tortue(self):
        """
        Confirme si l'utilisateur veut utiliser la tortue ou non.

        Si la tortue est déjà le mode de dessin, cette fonction affiche une erreur.
        :return: Booléen indiquant si l'utilisateur veut utiliser la tortue
        """
        if self._mode == Mode.CONSOLE:
            return self.confirmer_question("\nÊtes-vous sûr(e) de vouloir activer l'affichage avec la tortue?\n"
                                           "Vous ne pourrez plus revenir à l'affichage dans le terminal. o/n")
        self.afficher("La tortue est déjà le mode de dessin.")
        return False

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

    @staticmethod
    def decimales(nombre):
        """
        Nombre de décimales d'un nombre.

        :param nombre: nombre dont on veut savoir les décimales
        :return: nombre de décimales
        """
        return int(math.floor(math.log10(nombre)+0.00001)+1)

    def actualiser(self):
        """
        Actualise l'écran.

        :return: "None"
        """
        if self._mode == Mode.CONSOLE:
            self.dessiner_grille_console()
        else:
            self.tortue.dessiner_grille(self.grille)

    def changer_vers_tortue(self):
        """
        Change le mode d'affichage pour utiliser la tortue.

        :return: "None"
        """
        self._mode = Mode.TORTUE
        self.tortue = Tortue()
        self.tortue.initialiser(self.avancer_d_un_tour)

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
        if self._mode == Mode.CONSOLE:
            return self.grille.tirer_console(coordonnees)
        return self.grille.tirer_coord_ecran(coordonnees)

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
            self.nombre_de_coups += 1
        else:
            self.afficher_erreur()

    def avancer_d_un_tour(self, x=None, y=None, entree=None):
        """
        Fonction permettant au jeu d'avancer d'un tour. Elle a été conçue pour fonctionner avec la tortue et la console.

        Elle peut être passée à "turtle.Turtle.screen.onclick", car elle commence par les arguments "x" et "y"
        :param x: position x du clic sur l'écran quand la fonction est passée à "turtle.Turtle.screen.onclick"
        :param y: position y du clic sur l'écran quand la fonction est passée à "turtle.Turtle.screen.onclick"
        :param entree: entrée de l'utilisateur dans la console
        :return: booléen indiquant si le jeu doit continuer
        """
        entree_convertie = entree  # On crée une variable globale à la fonction pour avoir la même variable pour
                                   # l'entrée avec la tortue et la console
        if x is not None and y is not None:
            entree_convertie = self.grille.coord_ecran_vers_index(x, y)  # On convertit les coordonnées pour pouvoir les
                                                                         # utiliser avec d'autres méthodes
        continuer = True
        if chaine_nettoyee(entree) in ("quitter", "q"):  # Si l'utilisateur veut quitter
            continuer = not self.confirmer_quitter()
        elif chaine_nettoyee(entree) in ("tortue", "t"):
            if self.confirmer_tortue():  # Si l'utilisateur veut utiliser la tortue
                self.changer_vers_tortue()
                # Le code ne dépasse jamais ce point, car on entre dans la boucle des évènements de la tortue
        else:
            retour = self.grille.tirer_console(entree_convertie)  # On tire sur la case et on enregistre le retour de la méthode
            self.afficher_retour_tir(retour)
            self.actualiser()

            if self.joueur_a_gagne():
                print("Vous avez gagné, bravo!")
                rejouer = self.demander_rejouer()
                continuer = rejouer
                if rejouer:
                    self.grille.reinitialiser()
                    self.grille.placer_bateaux()
                    self.actualiser()
        return continuer




    def boucle_des_evenements(self):
        """
        Démarre la boucle des évènements.

        Demande à l'utlisateur où il veut tirer et tire sur la case.
        :return: "None"
        """
        self.actualiser()
        continuer = True
        while continuer:
            entree = self.recevoir_entree("\n>>> ")  # Équivalent à "raw_input("\n>>> ")", mais compatible avec python 3
            continuer = self.avancer_d_un_tour(entree=entree)






