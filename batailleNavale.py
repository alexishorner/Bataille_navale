# coding: utf-8
from case import Grille
from interfacegraphique import Afficheur
import bateau

NOMBRE_TORPILLEURS = 1
NOMBRE_SOUS_MARINS = 1
NOMBRE_CONTRE_TORPILLEURS = 1
NOMBRE_CROISEURS = 1
NOMBRE_PORTES_AVIONS = 1


def ajouter_bateau(classe, nombre, liste):
    """
    Ajoute des bateaux d'un certain type à une liste
    :param classe: Classe des bateaux à créer
    :param nombre: Nombre de bateaux à créer
    :param liste: Liste où stocker les bateaux
    :return: "None"
    """
    for i in range(nombre):
        liste.append(classe())  # classe() appelle le constructeur de la classe
        
def ajouter_bateaux(liste):
    ajouter_bateau(bateau.Torpilleur, NOMBRE_TORPILLEURS, liste)
    ajouter_bateau(bateau.SousMarin, NOMBRE_SOUS_MARINS, liste)
    ajouter_bateau(bateau.ContreTorpilleur, NOMBRE_CONTRE_TORPILLEURS, liste)
    ajouter_bateau(bateau.Croiseur, NOMBRE_CROISEURS, liste)
    ajouter_bateau(bateau.PorteAvions, NOMBRE_PORTES_AVIONS, liste)


if __name__ == "__main__":
    grille = Grille()
    interface = Afficheur(grille)
    bateaux = []
    ajouter_bateaux(bateaux)
