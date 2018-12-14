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
import time
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

@unique
class Difficulte(IntEnum):
    """
    Énumération décrivant les différentes difficultés.
    """
    FACILE, MOYEN, DIFFICILE = range(3)


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

    def aller_a(self, x, y=None):
        """
        Va à une position sans laisser de traces.

        :param x: entier représentant la coordonnée x ou liste contenant les deux coordonnées.
        :param y: entier représentant la coordonnée y
        :return: "None"
        """
        self.up()
        if y is None:
            self.goto(x)
        else:
            self.goto(x, y)
        self.down()

    def ecrire(self, message, position, alignement="left", police=("Arial", 8, "normal"), couleur="black"):
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
        self.aller_a(position)
        self.write(message, align=alignement, font=police)
        self.pencolor(ancienne_couleur)  # Rétablit la couleur de la tortue

    def dessiner_graduations(self, origine, cote_grille):
        """
        Dessine les graduations à côté de la grille.

        :param origine: origine de la case supérieure gauche de la grille.
        :param cote_grille: nombre de cases composant le côté de la grille
        :return: "None"
        """
        x_0, y_0 = origine
        decimales_max = decimales(cote_grille)  # Nombre de caractères pour écrire le nombre
        cote_case = Case.largeur_pixels  # Taille en pixels de la case
        taille_police = int(Case.largeur_pixels / 10.0 + 8)  # Taille de la police
        for i in range(cote_grille):
            x = x_0+i*cote_case+cote_case/2.0
            y = y_0+cote_case+decimales_max*taille_police/2.0
            self.ecrire(string.ascii_uppercase[i], (x, y), alignement="center", police=("Arial", taille_police, "bold"))
            x = x_0-decimales_max*taille_police/2.0
            y = y_0-(i-1)*cote_case-cote_case/2.0-taille_police
            self.ecrire(str(i + 1), (x, y), alignement="right", police=("Arial", taille_police, "bold"))

    def dessiner_case(self, case):
        """
        Dessine une case à l'écran.

        :param case: case à dessiner
        :return: "None"
        """
        self.fillcolor(self.couleur_case(case.etat))
        points = case.carre()
        self.aller_a(points[0])  # Va au point inférieur droite de la case
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


class Afficheur:  # TODO: ajouter menu, taille grille variable, niveaux, afficher bateaux restants et coulés
    """
    Cette classe permet de dessiner les objets à l'écran. Elle utilise un objet "Tortue" ou la console pour dessiner à l'écran.
    """
    
    def __init__(self, grille):
        """
        constructeur de la classe "Afficheur"

        :param grille: grille de jeu à afficher
        """
        self.difficulte = Difficulte.MOYEN  # TODO: implémenter difficulté
        self._parametre_nombre_de_coups_maximum = "auto"
        self.temps_par_coup = 5
        self._parametre_temps_maximum = "auto"  # TODO: implémenter contrainte de temps
        self.grille = grille
        self.tortue_elements_permanents = Tortue()  # Tortue dessinant les éléments restants plusieurs tours d'affilée
        self.tortue_elements_provisoires = Tortue()  # Tortue dessinant les éléments changés à chaque tour
        self.nombre_de_coups = 0
        self.temps_depart = 0

    def chaine_difficulte(self):
        """
        Renvoie une chaîne de caractères décrivant la difficulté.

        :return: chaîne de caractères décrivant la difficulté
        """
        if self.difficulte == Difficulte.FACILE:
            return "facile"
        elif self.difficulte == Difficulte.MOYEN:
            return "moyen"
        else:
            return "difficile"
        
    def generer_nombre_de_coups_maximum(self):
        """
        Génère automatiquement une valeur pour le nombre de coups maximum en fonction de la difficulté
        
        :return: nombre maximum de coups
        """
        return int(round(self.grille.taille**2/2.0*(1-self.difficulte/10.0)))

    def nombre_de_coups_maximum(self, chaine=False):  # TODO: prendre en compte les bateaux
        """
        Retourne le nombre maximal de coups.

        :return: nombre maximal de coups
        """
        if self._parametre_nombre_de_coups_maximum == "auto":
            nombre_de_coups_maximum = self.generer_nombre_de_coups_maximum()
            if chaine:
                return self._parametre_temps_maximum + " ({0})".format(nombre_de_coups_maximum)
            return nombre_de_coups_maximum
        if chaine:
            return str(self._parametre_nombre_de_coups_maximum)
        return self._parametre_nombre_de_coups_maximum

    def coups_restants(self):
        """
        Retourne le nombre de coups restants

        :return: nombre de coups restants
        """
        return self.nombre_de_coups_maximum() - self.nombre_de_coups

    def generer_temps_maximum(self):
        """
        Génère automatiquement une valeur pour le temps maximum en fonction de la difficulté

        :return: temps maximum
        """
        return int(round(self.nombre_de_coups_maximum() * self.temps_par_coup * (1 - self.difficulte / 10.0)))

    def temps_maximum(self, chaine=False):
        """
        Retourne le temps maximal par partie.

        :param chaine: spécifie si le retour doit être une chaîne de caractères
        :return: temps maximal
        """
        if self._parametre_temps_maximum == "auto":
            temps_maximum = self.generer_temps_maximum()
            if chaine:
                return self._parametre_temps_maximum + " ({0} s)".format(temps_maximum)
            return temps_maximum
        if chaine:
            return "{0} s".format(self._parametre_temps_maximum)
        return self._parametre_temps_maximum

    def temps_restant(self):
        return self.temps_maximum()-(time.time() - self.temps_depart)

    def joueur_a_perdu(self):  # TODO: ajouter autres contraintes
        """
        Détermine si le joueur a perdu

        :return: Booléen indiquant si le joueur a perdu
        """
        if self.coups_restants() <= 0 or self.temps_restant() <= 0:
            return True
        return False

    def joueur_a_gagne(self):
        """
        Détermine si le joueur a gagné

        :return: Booléen indiquant si le joueur a gagné
        """
        if self.joueur_a_perdu():  # On vérifie que le joueur n'a pas perdu (en particulier que le temps n'est pas écoulé)
            return False
        for bateau in self.grille.bateaux:
            if not bateau.est_coule():  # On vérifie pour chaque bateau si il est coulé
                return False
        return True

    def effacer_tout(self):
        self.tortue_elements_provisoires.clear()
        self.tortue_elements_permanents.clear()

    def afficher(self, message, fin="\n"):
        """
        Affiche un message.

        :param message: message à afficher
        :param fin: caractère à placer dans la console après le message
        :return: "None"
        """
        print(message, end=fin)
        position = (0, self.grille.position_coins()[1][1]-25)  # On place en bas au milieu de la grille
        self.tortue_elements_provisoires.ecrire(message, position, alignement="center", police=("Arial", 8, "bold"))

    def afficher_parametres(self, partie_en_cours=False):  # TODO: ajouter paramètre taille grille et améliorer alignement texte
        titre = "Paramètres"
        texte = ["1. Difficulté : {0}".format(self.chaine_difficulte()),
                 "2. Nombre maximum de coups : {0}".format(self.nombre_de_coups_maximum(chaine=True)),
                 "3. Temps maximum : {0}".format(self.temps_maximum(chaine=True))]
        nombre_caracteres_max = len(max(texte, key=len))
        caracteres_a_ajouter = nombre_caracteres_max-len(titre)
        titre = " "*int(math.ceil(caracteres_a_ajouter/2.0)) + titre + " "*int(math.floor(caracteres_a_ajouter/2.0))
        recommencer = True
        while recommencer:
            recommencer = False
            self.effacer_tout()
            x, y = 0, 40
            print("\n"+titre)
            self.tortue_elements_permanents.ecrire(titre, (0, y), alignement="center", police=("Arial", 12, "bold"))
            for i, ligne in enumerate(texte):
                print(ligne)
                self.tortue_elements_permanents.ecrire(ligne, (0, y - 40 - i * 20), alignement="center", police=("Arial", 12, "normal"))
            entree = chaine_nettoyee(self.recevoir_entree(">>> "))
            if entree in ("", "<"):
                self.afficher_menu(partie_en_cours=partie_en_cours)
                return
            else:
                try:
                    entree = int(float(entree))
                except ValueError:
                    self.afficher_erreur()
                    recommencer = True
                    continue

                if entree in range(1, len(texte)+1):
                    recommencer2 = True
                    while recommencer2:
                        recommencer2 = False
                        if entree == 1:  # "Difficulté"
                            nouvelle_valeur = chaine_nettoyee(self.recevoir_entree("Nouvelle valeur (1. facile, 2. moyen, 3. difficile) : "))
                            if nouvelle_valeur in ("", "<"):
                                    self.afficher_parametres(partie_en_cours=partie_en_cours)
                                    return
                            elif nouvelle_valeur in ("a", "auto"):
                                print("La difficulté ne peut pas être automatique")
                                recommencer2 = True
                                continue
                            elif nouvelle_valeur in ("1", "1.", "f", "facile"):
                                self.difficulte = Difficulte.FACILE
                            elif nouvelle_valeur in ("2", "2.", "m", "moyen"):
                                self.difficulte = Difficulte.MOYEN
                            elif nouvelle_valeur in ("3", "3.", "d", "difficile"):
                                self.difficulte = Difficulte.DIFFICILE
                            else:
                                self.afficher_erreur()
                                recommencer2 = True
                                continue
                            print("Difficulté changée à {0}".format(self.chaine_difficulte()))
                        elif entree == 2:  # "Nombre maximum de coups"
                            min = self.grille.nombre_de_cases_occupees()
                            nouvelle_valeur = chaine_nettoyee(self.recevoir_entree("Nouvelle valeur (auto, {0}, {1}, {2}, ...) : ".format(min, min+1, min+2)))
                            if nouvelle_valeur in ("", "<"):
                                self.afficher_parametres(partie_en_cours=partie_en_cours)
                                return
                            elif nouvelle_valeur in ("a", "auto"):
                                self._parametre_nombre_de_coups_maximum = "auto"
                                print("Nombre de coups maximum changé à {0}".format(self.nombre_de_coups_maximum(chaine=True)))
                            else:
                                try:
                                    nouvelle_valeur = int(float(nouvelle_valeur))
                                except ValueError:
                                    self.afficher_erreur()
                                    recommencer2 = True
                                    continue
                                if nouvelle_valeur >= self.grille.nombre_de_cases_occupees():  # On veut que le nombre
                                                                                               # de coups soit au moins
                                                                                               # égal au nombre de cases occupées
                                    self._parametre_nombre_de_coups_maximum = nouvelle_valeur  # TODO: vérifier quand partie est en cours
                                    print("Nombre de coups maximum changé à {0}".format(self.nombre_de_coups_maximum(chaine=True)))
                                else:
                                    print("Nombre de coups insuffisant.")
                                    recommencer2 = True
                                    continue
                        else:  # "Temps maximum"
                            min = 1
                            nouvelle_valeur = chaine_nettoyee(self.recevoir_entree("Nouvelle valeur (auto, {0}, {1}, {2}, ...) : ".format(min, min+1, min+2)))
                            if nouvelle_valeur in ("", "<"):
                                self.afficher_parametres(partie_en_cours=partie_en_cours)
                                return
                            elif nouvelle_valeur in ("a", "auto"):
                                self._parametre_temps_maximum = "auto"
                            else:
                                try:
                                    nouvelle_valeur = int(float(nouvelle_valeur))
                                except ValueError:
                                    self.afficher_erreur()
                                    recommencer2 = True
                                    continue
                                if nouvelle_valeur > 0:
                                    self._parametre_temps_maximum = nouvelle_valeur
                                else:
                                    print("Temps insuffisant.")
                                    recommencer2 = True
                                    continue
                else:
                    self.afficher_erreur()
                    recommencer = True
                    continue
        self.afficher_parametres(partie_en_cours=partie_en_cours)

    def afficher_menu(self, partie_en_cours=False):
        """
        Affiche le menu.

        :return: "None"
        """
        titre = "       Menu       "
        texte = []
        if partie_en_cours:
            texte.append("Continuer      ")
        texte.extend(("Nouvelle partie",
                      "Paramètres     ",
                      "Quitter        "))
        for i in range(len(texte)):
            texte[i] = str(i+1) + ".  " + texte[i]  # On ajoute un numéro devant chaque élément du menu
        x, y = 0, 40
        entree = ""
        recommencer = True
        while recommencer:
            recommencer = False
            self.effacer_tout()  # On efface l'écran
            print("\n"+titre)
            self.tortue_elements_permanents.ecrire(titre, (x, y), alignement="center", police=("Arial", 12, "bold"))
            for i, ligne in enumerate(texte):
                print(ligne)
                self.tortue_elements_permanents.ecrire(ligne, (x, y - 40 - i * 20), alignement="center", police=("Arial", 12, "normal"))
            entree = chaine_nettoyee(self.recevoir_entree(">>> "))
            if entree in ("", "<"):  # Si l'entrée est revenir en arrière
                if partie_en_cours:
                    self.dessiner_tout()  # On continue la partie
                else:
                    print("Vous ne pouvez pas revenir en arrière ici.")
                    recommencer = True
                    continue
            else:
                try:
                    entree = int(entree)  # On convertit l'entrée en nombres, si ça ne marche pas, on affiche une erreur
                except ValueError:
                    self.afficher_erreur()  # On affiche une erreur et on recommence
                    recommencer = True
                    continue

                if partie_en_cours:  # Si on a rajouté une ligne au début, on enlève 1 à "entree" pour avoir moins de conditions
                    entree -= 1
                if entree == 0:  # "Continuer"
                    self.dessiner_tout()
                elif entree == 1:  # "Recommencer"
                    if partie_en_cours:
                        if self.confirmer_question("Êtes-vous sûr(e) de vouloir recommencer? Votre partie n'est pas finie. o/n"):
                            self.rejouer()
                        else:
                            recommencer = True
                            continue  # On recommence la boucle
                elif entree == 2:  # "Paramètres"
                    self.afficher_parametres(partie_en_cours=partie_en_cours)
                    return
                elif entree == 3:  # "Quitter"
                    if self.confirmer_quitter():
                        exit(0)
                    else:
                        recommencer = True
                        continue
                else:  # Erreur
                    self.afficher_erreur()
                    recommencer = True
                    continue


    def afficher_coups_restants(self):
        """
        Affiche le nombre de coups restants pour l'utilisateur.

        :return: "None"
        """
        self.afficher("Coups restants : " + str(self.coups_restants()))

    def afficher_temps_restant(self):
        texte = "Temps restant : {0} s".format(int(round(self.temps_restant())))
        print(texte)
        self.tortue_elements_provisoires.ecrire(texte, (-300, 300), "center")

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
        self.temps_depart = time.time()
        self.dessiner_tout()

    def dessiner_tout(self):
        """
        Dessine la grille en entier avec la tortue et dans la console et affiche différentes informations.

        C'est ici que les éléments à l'écran ne changeant pas, comme le fond d'écran, sont dessinés.
        :return: "None"
        """
        self.effacer_tout()
        self.dessiner_grille_console()
        self.tortue_elements_permanents.dessiner_grille(self.grille.cases)
        self.afficher_coups_restants()
        self.afficher_temps_restant()

    def actualiser(self, cases=None):
        """
        Actualise l'écran.

        :param cases: liste de cases à actualiser
        :return: "None"
        """
        self.tortue_elements_provisoires.clear()
        self.dessiner_grille_console()
        if cases is not None:
            for case in cases:
                self.tortue_elements_permanents.dessiner_case(case)
        self.tortue_elements_permanents.screen.update()
        self.afficher_coups_restants()
        self.afficher_temps_restant()

    def ajouter_espacement_avant(self, nombre=None):
        """
        Ajoute un espacement avant la grille pour aligner les nombres sur la droite.

        :param nombre: nombre qui doit être aligné
        :return: "None"
        """
        espacement_total = decimales(self.grille.taille)
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
        for index_x in range(self.grille.taille):
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
        if index_x == self.grille.taille-1:
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
        for index_y in range(self.grille.taille):
            for index_x in range(self.grille.taille):
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
        if chaine_nettoyee(entree) in ("quitter", "q"):  # Si l'utilisateur veut quitter
            if self.confirmer_quitter():
                exit(0)
        elif chaine_nettoyee(entree) in ("", "<", "menu", "m"):
            self.afficher_menu(partie_en_cours=True)
        elif chaine_nettoyee(entree) in ("parametres", "paramÈtres", "paramètres", "p"):
            self.afficher_parametres(partie_en_cours=True)
        else:
            retour, cases = self.grille.tirer(entree)  # On tire sur la case et on enregistre le retour de la méthode
            self.afficher_retour_tir(retour, cases)  # TODO: continuer
            self.actualiser(cases)

            if self.joueur_a_gagne():
                print("Vous avez gagné, bravo!")
                if self.demander_rejouer():
                    self.rejouer()
                else:
                    self.afficher_menu()
            elif self.joueur_a_perdu():
                print("Vous avez perdu!")
                if self.demander_rejouer():
                    self.rejouer()

    def boucle_des_evenements(self):
        """
        Démarre la boucle des évènements.

        Demande à l'utlisateur où il veut tirer et tire sur la case.
        :return: "None"
        """
        self.rejouer()
        while True:
            entree = self.recevoir_entree("\n>>> ")  # Équivalent à "raw_input("\n>>> ")", mais compatible avec python 3
            #entree = string.ascii_uppercase[random.randint(0, self.grille.largeur_pixels)] + str(random.randint(0, self.grille.largeur_pixels))
            # TODO: enlever ligne de test
            self.avancer_d_un_tour(entree)






