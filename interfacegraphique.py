# coding: utf8
# Attention les noms de variables ne contiennent pas d'accent, ce qui peut changer leur signification (par ex : côté devient cote)
from case import *
import turtle

# Constantes
largeurCase = 10 #Largeur d'une case en pixels
nbreDeCaseCote = 10 #Nombre de _cases par côté de la grille


# Variables globales (c.à.d. accédées partout dans le programme, y compris à l'intérieur de fonctions)
stylo = turtle.Turtle() #Objet utilisé pour dessiner à l'écran

# Fonctions pour l'affichage
def dessinerCase(case):
    """"
    Dessine une case aux coordonnées coord (les coordonnées vont de 0 à nbreDeCasesCote**2-1,
    c'est en fait l'index de la case dans le tableau grille).
    L'état de la case détermine son apparence
    """
    stylo.up()
    stylo.goto(case.position())
    stylo.setheading()


def dessinerGrille(grille):
