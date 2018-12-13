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
    COULEUR_ARRIERE_PLAN = "white"


    def __init__(self):
        """
        constructeur de la classe "Tortue"
        """
        turtle.Turtle.__init__(self)
        self.hideturtle()  # cache la tortue
        self.screen.tracer(0, 0)  # rend le dessin instantané, mais l'écran doit être rafraîchit manuellement en appelant "self.screen.update()"
        self.fillcolor(self.couleur_case(Etat.VIDE))
        self.ancien_message = ""
        self.ancienne_position = (0, 0)
        self.ancien_alignement = "left"
        self.ancienne_police = ("Arial", 8, "normal")

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

    def _effacer_ancien_message(self):
        self._ecrire(self.ancien_message, self.ancienne_position, self.ancien_alignement, self.ancienne_police, self.COULEUR_ARRIERE_PLAN)
        # TODO: faire en sorte de pouvoir effacer le nombre de coups séparément du retour de tir

    def _ecrire(self, message, position, alignement="left", police=("Arial", 8, "normal"), couleur="black"):
        """
        Écrit un message à l'écran

        :param message: message à écrire
        :param position: endroit où écrire le message
        :param alignement: alignement du texte
        :param police: police à utiliser
        :param couleur: couleur du texte
        :return: "None"
        """
        ancienne_couleur = self.pencolor()  # Enregistre la couleur de la tortue
        self.pencolor(couleur)
        self.up()
        self.goto(position)
        self.down()
        self.write(message, align=alignement, font=police)
        self.pencolor(ancienne_couleur)  # Rétablit la couleur de la tortue

    def afficher_message(self, message, position, alignement="left", police=("Arial", 8, "normal")):
        """
        Affiche un message à une certaine position.

        :param message: message à afficher
        :param alignement: alignement du texte
        :param position: endroit où afficher le message
        :param police: police à utiliser pour écrire
        :return: "None"
        """
        self._effacer_ancien_message()
        self._ecrire(message, position, alignement, police)
        self.ancienne_position = position
        self.ancien_message = message
        self.ancien_alignement = alignement
        self.ancienne_police = police

    def dessiner_graduations(self, origine, cote_grille):
        """
        Dessine les graduations à côté de la grille.

        :param origine: origine de la case supérieure gauche de la grille.
        :param cote_grille: nombre de cases composant le côté de la grille
        :return: "None"
        """
        x_0, y_0 = origine
        decimales_max = decimales(cote_grille)  # Nombre de caractères pour écrire le nombre
        cote_case = Case.TAILLE  # Taille en pixels de la case
        taille_police = int(Case.TAILLE/10.0+8)  # Taille de la police
        for i in range(cote_grille):
            x = x_0+i*cote_case+cote_case/2.0
            y = y_0+cote_case+decimales_max*taille_police/2.0
            self._ecrire(string.ascii_uppercase[i], (x, y), alignement="center", police=("Arial", taille_police, "bold"))
            x = x_0-decimales_max*taille_police/2.0
            y = y_0-(i-1)*cote_case-cote_case/2.0-taille_police
            self._ecrire(str(i+1), (x, y), alignement="right", police=("Arial", taille_police, "bold"))

    def dessiner_case(self, case):
        """
        Dessine une case à l'écran.

        :param case: case à dessiner
        :return: "None"
        """
        self.fillcolor(self.couleur_case(case.etat))
        points = case.carre()
        self.up()
        self.goto(points[0])  # Va au point inférieur droite de la case
        self.down()
        self.begin_fill()
        for i in range(1, len(points)):  # la tortue est déjà à "points[0]", donc on commence à 1
            self.goto(points[i])
        self.goto(points[0])
        self.end_fill()

    def dessiner_grille(self, cases):  # TODO: ajuster taille cases dynamiquement
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


class Afficheur:  # TODO: ajouter menu, taille grille variable, niveaux, afficher bateaux restants et coulés
    """
    Cette classe permet de dessiner les objets à l'écran. Elle utilise un objet "Tortue" ou la console pour dessiner à l'écran.
    """
    NOMBRE_DE_COUPS_MAX = 50
    TEMPS_MAX = 120  # TODO: implémenter contrainte de temps
    def __init__(self, grille):
        """
        constructeur de la classe "Afficheur"

        :param grille: grille de jeu à afficher
        """
        self.grille = grille
        self.tortue = Tortue()
        self.nombre_de_coups = 0

    def coups_restants(self):
        """
        Retourne le nombre de coups restants

        :return: nombre de coups restants
        """
        return self.NOMBRE_DE_COUPS_MAX-self.nombre_de_coups

    def joueur_a_perdu(self):  # TODO: ajouter autres contraintes
        """
        Détermine si le joueur a perdu

        :return: Booléen indiquant si le joueur a perdu
        """
        if self.coups_restants() <= 0:
            return True
        return False

    def joueur_a_gagne(self):
        """
        Détermine si le joueur a gagné

        :return: Booléen indiquant si le joueur a gagné
        """
        for bateau in self.grille.bateaux:
            if not bateau.est_coule():
                return False
        return True

    def afficher(self, message, fin="\n"):
        """
        Affiche un message.

        :param message: message à afficher
        :param fin: caractère à placer après le message
        :return:
        """
        print(message, end=fin)
        self.tortue.afficher_message(message+fin, (0, -(self.grille.TAILLE+4)*Case.TAILLE/2.0), alignement="center")

    def afficher_coups_restants(self):
        self.afficher("Coups restants : " + str(self.coups_restants()))

    def afficher_erreur(self):
        """
        Indique à l'utilisateur qu'une erreur s'est produite.

        :return: "None"
        """
        self.afficher("Une erreur s'est produite.")

    def recevoir_entree(self, texte_a_afficher=""):
        """
        Fonction équivalente à "raw_input()", mais compatible avec python 3

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

    def rejouer(self):
        """
        Démarre une nouvelle partie

        :return: "None"
        """
        self.nombre_de_coups = 0
        if not self.grille.placer_bateaux():
            self.afficher("Impossible de placer les bateaux, la grille est peut-être trop petite par rapport au nombre de bateaux.")
            exit(1)  # TODO: éventuellement changer le comportement en cas d'erreur
        self.dessiner_tout()

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

    def dessiner_grille_console(self):  # TODO: faire en sorte de pouvoir actualiser la grille sans l'afficher plusieurs fois
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

    def tirer(self, coordonnees):
        """
        Tire sur une case en utilisant la fonction correspondant au mode
        :param coordonnees: coordonnées où tirer
        :return:  État de la case après le tir si celui-ci a réussi, "None" si la case a déjà reçu un tir et "False"
        s'il y a eu une erreur
        """
        return self.grille.tirer(coordonnees)

    def afficher_retour_tir(self, retour, cases):
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
                type = cases[0].bateau().TYPE  # On récupère le type du bateau touché
                type = type[0].upper() + type[1:len(type)]  # On met la première lettre en majuscules
                self.afficher(type + " coulé")
            self.nombre_de_coups += 1
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
            self.afficher_retour_tir(retour, cases)  # TODO: continuer
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
        self.rejouer()
        continuer = True
        while continuer:
            entree = self.recevoir_entree("\n>>> ")  # Équivalent à "raw_input("\n>>> ")", mais compatible avec python 3
            #entree = string.ascii_uppercase[random.randint(0, self.grille.TAILLE)] + str(random.randint(0, self.grille.TAILLE))
            # TODO: enlever ligne de test
            continuer = self.avancer_d_un_tour(entree)






