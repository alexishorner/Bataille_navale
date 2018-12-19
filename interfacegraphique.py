# coding: utf-8
"""
Module contenant les classes permettant l'affichage.
"""
# Attention les noms de variables ne contiennent pas d'accent, ce qui peut changer leur signification
# (par ex : côté devient cote)
from __future__ import print_function  # Permet d'utiliser la fonction print de python 3, qui a le paramètre "end"

import math
import os
import string
import time
import turtle
from sys import platform
from sys import stdin  # Sert à recevoir des entrées de l'utilisateur en restant compatible avec python 3

from enum import IntEnum, unique

from case import Etat, Case


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
    return int(math.floor(math.log10(nombre) + 0.00001) + 1)


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
    COULEUR_FOND = "#5bc6d2"
    COULEUR_ARRIERE_PLAN = "white"

    COULEUR_CALE = "#767F7E"
    HAUTEUR_CALE = 20

    COULEUR_CHEMINEE = "#c61c10"
    HAUTEUR_CHEMINEE = 25
    LARGEUR_CHEMINEE = 8
    ESPACEMENT_CHEMINEE = 17

    LARGEUR_TOURELLE = 18
    HAUTEUR_TOURELLE = 12
    ELOIGNEMENT_TOURELLE_BORD = 2

    def __init__(self):
        """
        constructeur de la classe "Tortue"
        """
        turtle.Turtle.__init__(self)
        self.hideturtle()  # cache la tortue
        self.screen.tracer(0, 0)    # rend le dessin instantané, mais l'écran doit être rafraîchit manuellement
                                    # en appelant "self.screen.update()"

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
        etait_en_bas = self.isdown()
        self.up()
        if y is None:
            self.goto(x)
        else:
            self.goto(x, y)
        if etait_en_bas:
            self.down()

    def ecrire(self, message, position, alignement="left", fonte=("Arial", 8, "normal"), couleur="black"):
        """
        Écrit un message à l'écran

        :param message: message à écrire
        :param position: endroit où écrire le message
        :param alignement: alignement du texte
        :param fonte: fonte à utiliser
        :param couleur: couleur du texte
        :return: "None"
        """
        ancienne_couleur = self.pencolor()  # Enregistre la couleur de la tortue
        self.pencolor(couleur)
        self.aller_a(position)
        self.write(message, align=alignement, font=fonte)
        self.pencolor(ancienne_couleur)  # Rétablit la couleur de la tortue

    def dessinfond(self):
        """
        Donne une couleur à l'arrière-plan
        :return: "None"
        """
        self.fillcolor(self.COULEUR_FOND)
        self.setheading(0)
        self.begin_fill()
        self.aller_a(-4000, -4000)  # On prend large pour être sûr de remplir l'écran
        for i in range(4):
            self.forward(8000)
            self.left(90)
        self.end_fill()
        self.screen.update()

    @staticmethod
    def longueur_bateau(taille):
        """
        Définit la longueur graphique du bateau
        :param taille: nombre de case du bateau
        :return: taille graphique
        """
        return 30 * taille

    def dessincale(self, bateau):
        """
        Dessine la cale du bateau selon ce schéma:
                 _______________
        alpha -> \             / <- beta
                  \___________/
        :param bateau: bateau dont il faut dessiner la cale
        :return: "None"
        """
        alpha = 85
        beta = 60
        self.pensize(2)
        self.down()
        self.fillcolor(self.COULEUR_CALE)
        self.begin_fill()
        self.right(alpha)
        self.forward(self.HAUTEUR_CALE / math.sin(math.radians(alpha)))
        self.left(alpha)
        self.forward(self.longueur_bateau(bateau.TAILLE) - self.HAUTEUR_CALE / math.tan(
            math.radians(alpha)) - self.HAUTEUR_CALE / math.tan(math.radians(beta)))
        self.left(beta)
        self.forward(self.HAUTEUR_CALE / math.sin(math.radians(beta)))
        self.left(180 - beta)
        pos = self.pos()
        self.forward(self.longueur_bateau(bateau.TAILLE))
        self.end_fill()
        self.up()
        self.goto(pos)

    def dessintourelle(self, orientation):
        """
        Dessine une tourelle
         __
        /__\====
        
        :param orientation: défini l'orientation de la tourelle. 1 veut dire droite et -1 gauche
        :return: "None"
        """
        alpha = 70
        beta = 80
        origine = self.pos()
        self.setheading(0)
        self.down()
        self.pensize(2)
        self.fillcolor("grey")
        self.begin_fill()
        self.forward(self.LARGEUR_TOURELLE * orientation)
        self.left((180 - alpha) * orientation)
        self.forward(
            ((self.HAUTEUR_TOURELLE / math.sin(math.radians(alpha))) / 2.0 - self.HAUTEUR_TOURELLE / 6.0) * orientation)
        self.right(75 * orientation)
        self.forward(self.LARGEUR_TOURELLE * orientation)
        self.left(90 * orientation)
        self.forward(self.LARGEUR_TOURELLE / 6.0 * orientation)
        self.left(90 * orientation)
        self.forward(
            (self.LARGEUR_TOURELLE - self.LARGEUR_TOURELLE / 6.0 * math.tan(math.radians(90 - 75))) * orientation)
        self.right(105 * orientation)
        self.forward((self.HAUTEUR_TOURELLE / math.sin(math.radians(alpha))) / 2.0 * orientation)
        self.left(alpha * orientation)
        self.forward(abs(self.LARGEUR_TOURELLE - self.HAUTEUR_TOURELLE / math.tan(
            math.radians(alpha)) - self.HAUTEUR_TOURELLE / math.tan(math.radians(beta))) * orientation)
        self.left(beta * orientation)
        self.goto(origine)
        self.end_fill()
        self.up()

    def dessincheminee(self):
        """
        Dessine une cheminée pour les bateaux
        :return: "None"
        """
        origine = self.pos()
        self.setheading(90)
        self.down()
        self.pensize(1)
        self.fillcolor(self.COULEUR_CHEMINEE)
        self.begin_fill()
        self.forward(self.HAUTEUR_CHEMINEE)
        self.left(90)
        self.forward(self.LARGEUR_CHEMINEE)
        self.left(90)
        self.forward(self.HAUTEUR_CHEMINEE)
        self.right(90)
        self.goto(origine)
        self.end_fill()
        self.setheading(180)
        self.up()

    def dessinbateaux(self, grille, position):
        """Dessine les bateaux stylisés
                ___
               __|__
         __   |O O O|   __
    ====/__\__|_____|__/__\====
        \ . . . . . . . . /
         \_______________/
                  """
        bateaux_par_type = []  # liste stockant un bateau par type
        for bateau in grille.bateaux:
            type_dans_liste = False  # Est-ce que le type du bateau est déjà compté?
            for bateau_par_type in bateaux_par_type:
                if bateau.TYPE == bateau_par_type.TYPE:
                    type_dans_liste = True
            if not type_dans_liste:
                bateaux_par_type.append(bateau)  # On ne stocke qu'un bateau par type

        for i, bateau in enumerate(bateaux_par_type):
            origine = (position[0], position[1] + i * 94)
            self.aller_a(origine)
            self.setheading(0)
            self.dessincale(bateau)
            self.forward(self.LARGEUR_TOURELLE + self.ELOIGNEMENT_TOURELLE_BORD)
            self.dessintourelle(1)
            self.setheading(180)
            self.forward(
                self.longueur_bateau(bateau.TAILLE) - 2 * (self.LARGEUR_TOURELLE + self.ELOIGNEMENT_TOURELLE_BORD))
            self.dessintourelle(-1)
            self.setheading(0)

            if bateau.TAILLE <= 2:
                nombre_cheminees = 0
            elif bateau.TAILLE == 3:
                nombre_cheminees = 1
            elif bateau.TAILLE == 4:
                nombre_cheminees = 2
            else:
                nombre_cheminees = 3
            self.forward(self.longueur_bateau(bateau.TAILLE) / 2.0 - self.LARGEUR_TOURELLE
                         + (nombre_cheminees * self.LARGEUR_CHEMINEE
                            + (nombre_cheminees - 1) * self.ESPACEMENT_CHEMINEE) / 2.0
                         - self.LARGEUR_CHEMINEE)
            for j in range(nombre_cheminees):  # On dessine deux cheminées
                self.dessincheminee()
                if j < nombre_cheminees - 1:
                    self.forward(self.ESPACEMENT_CHEMINEE)
            self.screen.update()

    def dessintextenombrebateaux(self, grille, position):
        """
        Affiche le nombre de bateaux restants par type à côté du dessin des bateaux.

        :param grille: Instance de la classe "Grille" décrivant la grille de jeu.
        :param position: Tuple contenant les coordonnées où afficher le texte
        """
        for i, bateau in enumerate(grille.bateaux):
            self.aller_a(position[0] - 15, position[1] + i * 94 - 20)
            self.down()
            nombre_restant = grille.nombrebateauxdeboutpartype(bateau.TYPE)
            if nombre_restant == 0:
                self.pencolor("red")
            self.write(str(nombre_restant) + " × ", align="center", font=("Arial", 14, "bold"))
            self.pencolor("black")
        self.screen.update()

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
        taille_fonte = int(Case.largeur_pixels / 10.0 + 8)  # Taille de la fonte
        for i in range(cote_grille):
            x = x_0 + i * cote_case + cote_case / 2.0
            y = y_0 + cote_case + decimales_max * taille_fonte / 2.0
            self.ecrire(string.ascii_uppercase[i], (x, y), alignement="center", fonte=("Arial", taille_fonte, "bold"))
            x = x_0 - decimales_max * taille_fonte / 2.0
            y = y_0 - (i - 1) * cote_case - cote_case / 2.0 - taille_fonte
            self.ecrire(str(i + 1), (x, y), alignement="right", fonte=("Arial", taille_fonte, "bold"))

    def dessiner_case(self, case):
        """
        Dessine une case à l'écran.

        :param case: case à dessiner
        :return: "None"
        """
        self.down()
        self.pensize(1)
        self.color("black", self.couleur_case(case.etat))
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
        self.dessiner_graduations(cases[0][0].position, len(cases))
        for ligne in cases:
            for case in ligne:
                self.dessiner_case(case)
        self.screen.update()


class Afficheur:
    """
    Cette classe permet de dessiner les objets à l'écran.
    Elle utilise un objet "Tortue" ou la console pour dessiner à l'écran.
    """
    TAILLE_POLICE_DEFAUT = 14

    def __init__(self, grille):
        """
        constructeur de la classe "Afficheur"

        :param grille: grille de jeu à afficher
        """
        self.difficulte = Difficulte.MOYEN
        self._nouvelle_difficulte = self.difficulte
        self._parametre_nombre_de_coups_maximum = "auto"
        self._nouveau_parametre_nombre_de_coups_maximum = self._parametre_nombre_de_coups_maximum
        self.temps_par_coup = 5
        self._parametre_temps_maximum = "auto"
        self._nouveau_parametre_temps_maximum = self._parametre_temps_maximum
        self.grille = grille
        self._nouvelle_taille_grille = grille.taille()
        self.tortue_elements_permanents = Tortue()  # Tortue dessinant les éléments restants plusieurs tours d'affilée
        self.tortue_elements_provisoires = Tortue()  # Tortue dessinant les éléments changés à chaque tour
        self.tortue_questions = Tortue()  # Tortue affichant les questions
        self.tortue_erreurs = Tortue()  # tortue affichant les erreurs
        self.nombre_de_coups = 0
        self.temps_depart = 0
        self.grille_visible = False

    def chaine_nouvelle_difficulte(self):
        """
        Renvoie une chaîne de caractères décrivant le dernier paramètre de difficulté.

        :return: chaîne de caractères décrivant la difficulté
        """
        if self._nouvelle_difficulte == Difficulte.FACILE:
            return "facile"
        elif self._nouvelle_difficulte == Difficulte.MOYEN:
            return "moyen"
        else:
            return "difficile"

    def generer_nombre_de_coups_maximum(self, taille_grille=None, difficulte=None):
        """
        Génère automatiquement une valeur pour le nombre de coups maximum en fonction de la difficulté
        
        :return: nombre maximum de coups
        """
        _taille_grille = taille_grille
        _difficulte = difficulte
        if taille_grille is None:
            _taille_grille = self.grille.taille()
            if difficulte is None:
                _difficulte = self.difficulte
        nombre_cases_libres = _taille_grille ** 2 - self.grille.nombre_de_cases_occupees()
        return int(round(self.grille.nombre_de_cases_occupees() + nombre_cases_libres / 2.0 * (1 - _difficulte / 5.0)))

    def nombre_de_coups_maximum(self, taille_grille=None, difficulte=None):
        """
        Retourne le nombre maximal de coups.

        :return: nombre maximal de coups
        """
        if self._parametre_nombre_de_coups_maximum == "auto":
            nombre_de_coups_maximum = self.generer_nombre_de_coups_maximum(taille_grille, difficulte)
            return nombre_de_coups_maximum
        return self._parametre_nombre_de_coups_maximum

    def chaine_nouveau_nombre_de_coups_maximum(self):
        """
        Retourne une chaîne de caractères décrivant la nouvelle valeur du paramètre du nombre de coups maximum.

        :return: nouvelle valeur du paramètre du nombre de coups maximum
        """
        if self._nouveau_parametre_nombre_de_coups_maximum == "auto":
            return "auto ({0})".format(
                self.nombre_de_coups_maximum(self._nouvelle_taille_grille, self._nouvelle_difficulte))
        return str(self._nouveau_parametre_nombre_de_coups_maximum)

    def coups_restants(self):
        """
        Retourne le nombre de coups restants

        :return: nombre de coups restants
        """
        return self.nombre_de_coups_maximum() - self.nombre_de_coups

    def generer_temps_maximum(self, taille_grille=None, difficulte=None):
        """
        Génère automatiquement une valeur pour le temps maximum en fonction de la difficulté

        :return: temps maximum
        """
        nombre_de_coups_maximum = self.nombre_de_coups_maximum(taille_grille, difficulte)
        _difficulte = difficulte
        if difficulte is None:
            _difficulte = self.difficulte

        return int(round(nombre_de_coups_maximum * self.temps_par_coup * (1 - _difficulte / 10.0)))

    def temps_maximum(self):
        """
        Retourne le temps maximal par partie.

        :return: temps maximal
        """
        if self._parametre_temps_maximum == "auto":
            return self.generer_temps_maximum()
        return self._parametre_temps_maximum

    def chaine_nouveau_parametre_temps_maximum(self):
        """
        Retourne une chaîne de caractères décrivant le nouveau paramètre du temps maximal.

        :return: Chaîne de caractères décrivant le nouveau paramètre du temps maximal.
        """
        if self._nouveau_parametre_temps_maximum == "auto":
            return "auto ({0} s)".format(
                self.generer_temps_maximum(self._nouvelle_taille_grille, self._nouvelle_difficulte))
        return self._nouveau_parametre_temps_maximum

    def temps_restant(self):
        """
        Retourne le temps restant à l'utilisateur pour finir la partie.

        :return: temps restant
        """
        return self.temps_maximum() - (time.time() - self.temps_depart)

    def joueur_a_perdu(self):
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
        """
        Efface tout ce qui est affiché à l'écran avec la tortue.

        :return: "None"
        """
        self.tortue_elements_provisoires.clear()
        self.tortue_elements_permanents.clear()
        self.tortue_questions.clear()
        self.tortue_erreurs.clear()

    def ecrire_texte(self, lignes, position, alignement="left", fonte=("Arial", 12, "normal"), couleur="black",
                     tortue=None):
        """
        Écrit du texte à l'écran ligne par ligne.

        :param lignes: Liste contenant le texte à écrire ligne par ligne
        :param position: Endroit où écrire le texte.
        :param alignement: Alignement du texte.
        :param fonte: Fonte à utiliser pour écrire, c'est un tuple contenant la police, la taille et le style.
        :param couleur: Couleur du texte.
        :param tortue: Tortue avec laquelle effectuer l'affichage
        :return: "None"
        """
        _tortue = tortue
        if tortue is None:
            _tortue = self.tortue_elements_permanents
        x, y = 0, 0
        if position is not None:
            x = position[0]
            y = position[1]
        for i, ligne in enumerate(lignes):
            print(ligne)
            _tortue.ecrire(ligne, (x, y - i * 20), alignement=alignement, fonte=fonte, couleur=couleur)

    def afficher(self, message, fin="\n", numero_ligne=0, tortue=None):
        """
        Affiche un message.

        :param tortue: Tortue avec laquelle effectuer l'affichage.
        :param numero_ligne: Entier permettant de simuler les retours à la ligne avec la tortue.
        :param message: message à afficher
        :param fin: caractère à placer dans la console après le message
        :return: "None"
        """
        _tortue = tortue
        if tortue is None:
            _tortue = self.tortue_elements_provisoires
        print(message, end=fin)
        if self.grille_visible:
            position = (self.grille.position_coins()[1][0] + self.grille.largeur_pixels() / 2.0,
                        self.grille.position_coins()[1][1] - 25 - numero_ligne * 20)  # On place en bas au milieu de la grille
        else:
            position = (0, self.grille.position_coins()[1][1] - 25 - numero_ligne * 20)
        _tortue.ecrire(message, position, alignement="center", fonte=("Arial", self.TAILLE_POLICE_DEFAUT, "bold"))
        _tortue.screen.update()

    def afficher_titre(self):
        """
        Affiche le titre dans la console.

        :return: "None"
        """
        self.tortue_elements_permanents.ecrire("Bataille navale", (0, 200), "center", ("Arial", 24, "underline"))

    def changer_parametre(self, valeurs_possibles):
        """
        Efface la page des paramètres et affiche les valeurs possibles pour changer le paramètre sélectionné.

        :param valeurs_possibles: Liste contenant des chaînes de caractères à afficher pour changer la valeur du paramètre.
        :return: "None"
        """
        self.tortue_elements_permanents.clear()
        self.ecrire_texte(valeurs_possibles, (0, 0), alignement="center", fonte=("Arial", self.TAILLE_POLICE_DEFAUT, "normal"))
        return chaine_nettoyee(self.recevoir_entree(">>> "))

    def afficher_parametres(self, partie_en_cours=False):
        """
        Affiche les paramètres et permet à l'utilisateur de changer leur valeur.

        :param partie_en_cours: Booléen indiquant si la partie est en cours, cela a une importance pour afficher le menu.
        :return: "None"
        """
        sous_titre = "Paramètres"
        texte = ["1. Difficulté : {0}".format(self.chaine_nouvelle_difficulte()),
                 "2. Nombre maximum de coups : {0}".format(self.chaine_nouveau_nombre_de_coups_maximum()),
                 "3. Temps maximum : {0}".format(self.chaine_nouveau_parametre_temps_maximum()),
                 "4. Taille grille : {0}".format(self._nouvelle_taille_grille)]
        nombre_caracteres_max = len(max(texte, key=len))
        caracteres_a_ajouter = nombre_caracteres_max - len(sous_titre)
        sous_titre = " " * int(math.ceil(caracteres_a_ajouter / 2.0)) + sous_titre + " " * int(
            math.floor(caracteres_a_ajouter / 2.0))
        recommencer = True
        while recommencer:
            recommencer = False
            self.effacer_tout()
            self.afficher_titre()
            x, y = 0, 40
            print("\n" + sous_titre)
            self.tortue_elements_permanents.ecrire(sous_titre, (0, y), alignement="center",
                                                   fonte=("Arial", self.TAILLE_POLICE_DEFAUT, "bold"))
            self.ecrire_texte(texte, (0, 0), alignement="center", fonte=("Arial", self.TAILLE_POLICE_DEFAUT, "normal"))
            entree = chaine_nettoyee(self.recevoir_entree(">>> "))
            if entree in ("", "<"):
                self.afficher_menu(partie_en_cours=partie_en_cours)
                return
            else:
                try:
                    entree = int(float(entree))
                except ValueError:
                    self.afficher_erreur("Entrée invalide.")
                    recommencer = True
                    continue

                if entree in range(1, len(texte) + 1):
                    recommencer2 = True
                    while recommencer2:
                        recommencer2 = False
                        if entree == 1:  # "Difficulté"
                            texte = ["1. facile",
                                     "2. moyen",
                                     "3. difficile"]
                            nouvelle_valeur = self.changer_parametre(texte)
                            if nouvelle_valeur in ("", "<"):
                                self.afficher_parametres(partie_en_cours=partie_en_cours)
                                return
                            elif nouvelle_valeur in ("a", "auto"):
                                self.afficher_erreur("La difficulté ne peut pas être automatique.")
                                recommencer2 = True
                                continue
                            elif nouvelle_valeur in ("1", "1.", "f", "facile"):
                                self._nouvelle_difficulte = Difficulte.FACILE
                            elif nouvelle_valeur in ("2", "2.", "m", "moyen"):
                                self._nouvelle_difficulte = Difficulte.MOYEN
                            elif nouvelle_valeur in ("3", "3.", "d", "difficile"):
                                self._nouvelle_difficulte = Difficulte.DIFFICILE
                            else:
                                self.afficher_erreur("Entrée invalide.")
                                recommencer2 = True
                                continue
                            self.afficher(
                                "Difficulté changée à {0}, les modifications prendront effet à la prochaine partie.".format(
                                    self.chaine_nouvelle_difficulte()))
                        elif entree == 2:  # "Nombre maximum de coups"
                            minimum = self.grille.nombre_de_cases_occupees()
                            texte = ["Nouvelle valeur (auto, {0}, {1}, {2}, ...) : ".format(minimum, minimum + 1, minimum + 2)]
                            nouvelle_valeur = self.changer_parametre(texte)
                            if nouvelle_valeur in ("", "<"):
                                self.afficher_parametres(partie_en_cours=partie_en_cours)
                                return
                            elif nouvelle_valeur in ("a", "auto"):
                                self._nouveau_parametre_nombre_de_coups_maximum = "auto"
                                self.afficher(
                                    ("Nombre de coups maximum changé à {0}, "
                                     "les modifications prendront effet à la prochaine partie.").format(nouvelle_valeur))
                            else:
                                try:
                                    nouvelle_valeur = int(float(nouvelle_valeur))
                                except ValueError:
                                    self.afficher_erreur("Entrée invalide.")
                                    recommencer2 = True
                                    continue
                                if nouvelle_valeur >= self.grille.nombre_de_cases_occupees():  # On veut que le nombre
                                    # de coups soit au moins
                                    # égal au nombre de cases occupées
                                    self._nouveau_parametre_nombre_de_coups_maximum = nouvelle_valeur
                                    self.afficher(
                                        ("Nombre de coups maximum changé à {0}, "
                                         "les modifications prendront effet à la prochaine partie.").format(nouvelle_valeur))
                                else:
                                    self.afficher_erreur("Nombre de coups insuffisant.")
                                    recommencer2 = True
                                    continue
                        elif entree == 3:  # "Temps maximum"
                            minimum = 1
                            texte = ["Nouvelle valeur (auto, {0}, {1}, {2}, ...) : ".format(minimum, minimum + 1, minimum + 2)]
                            nouvelle_valeur = self.changer_parametre(texte)
                            if nouvelle_valeur in ("", "<"):
                                self.afficher_parametres(partie_en_cours=partie_en_cours)
                                return
                            elif nouvelle_valeur in ("a", "auto"):
                                self._nouveau_parametre_temps_maximum = "auto"
                                self.afficher(
                                    ("Temps réglé de manière automatique ({0} s), "
                                    "les modifications prendront effet à la prochaine partie.").format(self.temps_maximum()))
                            else:
                                try:
                                    nouvelle_valeur = int(float(nouvelle_valeur))
                                except ValueError:
                                    self.afficher_erreur("Entrée invalide.")
                                    recommencer2 = True
                                    continue
                                if nouvelle_valeur > 0:
                                    self._nouveau_parametre_temps_maximum = nouvelle_valeur
                                    self.afficher(
                                        ("Temps maximum changé à {0}, "
                                        "les modifications prendront effet à la prochaine partie.").format(nouvelle_valeur))
                                else:
                                    self.afficher_erreur("Temps insuffisant.")
                                    recommencer2 = True
                                    continue
                        else:  # "Taille grille"
                            texte = ["\nAvec quelle taille de grille souhaitez-vous jouer? (nombre entre 6 et 26)\n"]
                            nouvelle_valeur = self.changer_parametre(texte)
                            if nouvelle_valeur in ("", "<"):
                                self.afficher_parametres(partie_en_cours=partie_en_cours)
                                return
                            try:  # On teste si la ligne suivante provoque une erreur
                                nouvelle_valeur = int(float(
                                    nouvelle_valeur))  # Le "float" permet d'accepter des valeurs comme 5.0 ou 2.3e1 (23)
                            except ValueError:  # Si une erreur de valeur est signalée
                                self.afficher_erreur("Erreur, vous devez entrer un nombre")
                            if 6 <= nouvelle_valeur <= 26:
                                cote = nouvelle_valeur
                                self._nouvelle_taille_grille = cote
                                self.afficher(
                                    ("Taille de la grille changée à {0}, "
                                    "les modifications prendront effet à la prochaine partie.").format(cote))
                            elif nouvelle_valeur < 6:
                                self.afficher_erreur(
                                    "La grille doit avoir une taille minimum de 6 cases pour pouvoir placer des bateaux")
                                recommencer2 = True
                                continue
                            else:
                                self.afficher_erreur("La grille est trop grande, le maximum est 26")
                                recommencer2 = True
                                continue
                else:
                    self.afficher_erreur()
                    recommencer = True
                    continue
        self.afficher_parametres(partie_en_cours=partie_en_cours)

    def actualiser_parametres(self):
        """
        Change la valeur des paramètres par la valeur des nouveaux paramètres choisis,
        cette fonction est appelée au début d'une partie.

        :return: "None"
        """
        self.difficulte = self._nouvelle_difficulte
        self._parametre_nombre_de_coups_maximum = self._nouveau_parametre_nombre_de_coups_maximum
        self._parametre_temps_maximum = self._nouveau_parametre_temps_maximum
        self.grille.set_taille(self._nouvelle_taille_grille)

    def afficher_menu(self, partie_en_cours=False):
        """
        Affiche le menu.

        :return: "None"
        """
        self.grille_visible = False
        sous_titre = "       Menu       "
        texte = []
        if partie_en_cours:
            texte.append("Continuer      ")
        texte.extend(("Nouvelle partie",
                      "Paramètres     ",
                      "Quitter        "))
        for i in range(len(texte)):
            texte[i] = str(i + 1) + ".  " + texte[i]  # On ajoute un numéro devant chaque élément du menu
        x, y = 0, 40
        recommencer = True
        while recommencer:
            recommencer = False
            self.effacer_tout()  # On efface l'écran
            self.afficher_titre()
            print("\n" + sous_titre)
            self.tortue_elements_permanents.ecrire(sous_titre, (x, y), alignement="center",
                                                   fonte=("Arial", self.TAILLE_POLICE_DEFAUT, "bold"))
            for i, ligne in enumerate(texte):
                print(ligne)
                self.tortue_elements_permanents.ecrire(ligne, (x, y - 40 - i * 20), alignement="center",
                                                       fonte=("Arial", self.TAILLE_POLICE_DEFAUT, "normal"))
            entree = chaine_nettoyee(self.recevoir_entree(">>> "))
            if entree in ("", "<"):  # Si l'entrée est revenir en arrière
                if partie_en_cours:
                    self.dessiner_tout()  # On continue la partie
                else:
                    self.rejouer()
            else:
                try:
                    entree = int(entree)  # On convertit l'entrée en nombres, si ça ne marche pas, on affiche une erreur
                except ValueError:
                    self.afficher_erreur("Entrée invalide.")  # On affiche une erreur et on recommence
                    recommencer = True
                    continue

                if partie_en_cours:  # Si on a rajouté une ligne au début, on enlève 1 à "entree" pour avoir moins de conditions
                    entree -= 1
                if entree == 0:  # "Continuer"
                    self.dessiner_tout()
                elif entree == 1:  # "Nouvelle partie"
                    if partie_en_cours:
                        if not self.confirmer_question(
                                "Êtes-vous sûr(e) de vouloir recommencer? Votre partie n'est pas finie. o/n"):
                            recommencer = True
                            continue  # On recommence la boucle
                    self.rejouer()
                elif entree == 2:  # "Paramètres"
                    self.afficher_parametres(partie_en_cours=partie_en_cours)
                    return
                elif entree == 3:  # "Quitter"
                    if self.confirmer_quitter():
                        exit(0)
                    else:
                        self.actualiser()
                        recommencer = True
                        continue
                else:  # Erreur
                    self.afficher_erreur("Entrée invalide.")
                    recommencer = True
                    continue

    def afficher_coups_restants(self):
        """
        Affiche le nombre de coups restants pour l'utilisateur.

        :return: "None"
        """
        self.tortue_elements_provisoires.ecrire("Coups restants : " + str(self.coups_restants()), (-330, 295), "left",
                                                ("Arial", self.TAILLE_POLICE_DEFAUT, "normal"))

    def afficher_temps_restant(self):
        """
        Affiche le temps restant avant la fin de la partie.

        :return: "None"
        """
        texte = "Temps restant : {0} s".format(int(round(self.temps_restant())))
        print(texte)
        self.tortue_elements_provisoires.ecrire(texte, (-330, 275), "left",
                                                ("Arial", self.TAILLE_POLICE_DEFAUT, "normal"))

    def afficher_erreur(self, message="Une erreur s'est produite."):
        """
        Indique à l'utilisateur qu'une erreur s'est produite.

        :return: "None"
        """
        self.tortue_erreurs.clear()
        self.afficher(message, tortue=self.tortue_erreurs)

    @staticmethod
    def recevoir_entree(texte_a_afficher=""):
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
        self.afficher(question, fin="", numero_ligne=1, tortue=self.tortue_questions)
        entree = self.recevoir_entree("\n>>> ")
        entree = chaine_nettoyee(entree)
        if entree in ("oui", "o"):
            return True
        return False

    def confirmer_quitter(self):
        """
        Demande la confirmation à l'utilisateur si il veut réellement quitter.

        :return: Booléen indiquant si l'utilisateur veut quitter.
        """
        return self.confirmer_question("\nÊtes-vous sûr(e) de vouloir quitter? o/n")

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
                self.afficher_erreur("Entrée invalide.")

    def rejouer(self):
        """
        Démarre une nouvelle partie

        :return: "None"
        """
        self.actualiser_parametres()
        self.nombre_de_coups = 0
        if not self.grille.placer_bateaux():
            self.afficher(
                "Impossible de placer les bateaux, la grille est peut-être trop petite par rapport au nombre de bateaux.")
            self.afficher_menu(partie_en_cours=False)
            return
        self.temps_depart = time.time()
        self.dessiner_tout()

    def actualiser(self, retour_tir="aucun retour", cases=None):
        """
        Actualise l'écran.

        :param retour_tir: retour du dernier tir
        :param cases: liste de cases à actualiser
        :return: "None"
        """
        self.tortue_elements_provisoires.clear()
        self.tortue_questions.clear()
        self.tortue_erreurs.clear()
        self.tortue_questions.screen.update()
        if retour_tir != "aucun retour":
            self.afficher_retour_tir(retour_tir, cases)
        self.dessiner_grille_console()
        if cases is not None:
            for case in cases:
                self.tortue_elements_permanents.dessiner_case(case)
        self.tortue_elements_permanents.screen.update()
        self.afficher_coups_restants()
        self.afficher_temps_restant()
        self.tortue_elements_provisoires.dessintextenombrebateaux(self.grille, (-300, -175))

    def dessiner_tout(self):
        """
        Dessine la grille en entier avec la tortue et dans la console et affiche différentes informations.

        C'est ici que les éléments à l'écran ne changeant pas, comme le fond d'écran, sont dessinés.
        :return: "None"
        """
        self.grille_visible = True
        self.effacer_tout()
        self.tortue_elements_permanents.dessinfond()
        self.tortue_elements_permanents.dessiner_grille(self.grille.cases)
        self.tortue_elements_permanents.dessinbateaux(self.grille, (-300, -175))
        self.actualiser()

    def ajouter_espacement_avant(self, nombre=None):
        """
        Ajoute un espacement avant la grille pour aligner les nombres sur la droite.

        :param nombre: nombre qui doit être aligné
        :return: "None"
        """
        espacement_total = decimales(self.grille.taille())
        if nombre is None:
            espacement = espacement_total
        else:
            espacement = espacement_total - decimales(nombre)
        print(" " * espacement, end="")  # Ajoute un espacement pour aligner les nombres à droite

    def dessiner_premiere_ligne_console(self):
        """
        Dessine la ligne de numérotation des colonnes de la grille.

        Exemple: _A_B_C_D_E_F_G_H_I_J_
        :return: "None"
        """
        self.ajouter_espacement_avant()
        for index_x in range(self.grille.taille()):
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
        if index_x == self.grille.taille() - 1:
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
        for index_y in range(self.grille.taille()):
            for index_x in range(self.grille.taille()):
                if index_y == 0 and index_x == 0:
                    self.dessiner_premiere_ligne_console()

                if index_x == 0:
                    self.ajouter_espacement_avant(index_y + 1)
                    print(str(index_y + 1), end="")

                self.dessiner_case_console(index_y, index_x)

    @staticmethod
    def _effacer_tout_console():
        """
        Fonction multi-plateforme permettant d'effacer le contenu de la console.

        :return: "None"
        """
        if platform == "win32":  # La commande dépend du système d'exploitation
            _ = os.system("cls")  # Le "_" avant le signe "=" sert à récupérer le retour de la fonction pour empêcher
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

    def afficher_retour_tir(self, retour, cases_affectees):
        """
        Affiche un message à l'écran en fonction du retour de la fonction de tir

        :param retour: retour de la fonction de tir
        :param cases_affectees: cases modifiées par le tir (incl. cases coulées par tir sur autre case)
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
                type_bateau = cases_affectees[0].bateau().TYPE  # On récupère le type du bateau touché
                type_bateau = type_bateau[0].upper() + type_bateau[1:len(type_bateau)]  # On met la première lettre en majuscules
                self.afficher(type_bateau + " coulé")
            self.nombre_de_coups += 1
        else:
            self.afficher_erreur("Case entrée invalide")

    def avancer_d_un_tour(self, entree):
        """
        Fonction permettant au jeu d'avancer d'un tour.

        Elle peut être passée à "turtle.Turtle.screen.onclick", car elle commence par les arguments "x" et "y"
        :param entree: entrée de l'utilisateur dans la console
        :return: booléen indiquant si le jeu doit continuer
        """
        if chaine_nettoyee(entree) in ("quitter", "q"):  # Si l'utilisateur veut quitter
            self.actualiser()
            if self.confirmer_quitter():
                exit(0)
            else:
                self.actualiser()
        elif chaine_nettoyee(entree) in ("", "<", "menu", "m"):
            self.afficher_menu(partie_en_cours=True)
        elif chaine_nettoyee(entree) in ("parametres", "paramÈtres", "paramètres", "p"):
            self.afficher_parametres(partie_en_cours=True)
        else:
            retour, cases = self.grille.tirer(
                entree)  # On tire sur la case et on enregistre le retour de la méthode et les cases affectées
            self.actualiser(retour, cases)

            if self.joueur_a_gagne():
                self.afficher("Vous avez gagné, bravo!", numero_ligne=2)
                self.afficher("Tapez \"m\", \"menu\" ou la touche entrée pour accéder au menu.", numero_ligne=3)
                choix = chaine_nettoyee(self.recevoir_entree("\n>>> "))
                if choix in ("m", "menu", ""):
                    self.afficher_menu()
                    return
                else:
                    if self.demander_rejouer():
                        self.rejouer()
                        return
                    exit(0)
            elif self.joueur_a_perdu():
                self.afficher("Vous avez perdu!", numero_ligne=1)
                self.afficher("Tapez \"m\", \"menu\" ou la touche entrée pour accéder au menu.", numero_ligne=3)
                choix = chaine_nettoyee(self.recevoir_entree("\n>>> "))
                if choix in ("m", "menu", ""):
                    self.afficher_menu()
                    return
                else:
                    if self.demander_rejouer():
                        self.rejouer()
                        return
                    exit(0)
                if self.demander_rejouer():
                    self.rejouer()

    def boucle_des_evenements(self):
        """
        Démarre la boucle des évènements.

        Demande à l'utlisateur où il veut tirer et tire sur la case.
        :return: "None"
        """
        while True:
            entree = self.recevoir_entree("\n>>> ")  # Équivalent à "raw_input("\n>>> ")", mais compatible avec python 3
            self.avancer_d_un_tour(entree)
