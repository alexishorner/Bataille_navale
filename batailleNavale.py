# coding: utf-8
"""
Module de lancement de la bataille navale.
"""
from case import Grille
from interfacegraphique import Afficheur
import bateau

NOMBRE_TORPILLEURS = 1
NOMBRE_SOUS_MARINS = 1
NOMBRE_CONTRE_TORPILLEURS = 1
NOMBRE_CROISEURS = 1
NOMBRE_PORTES_AVIONS = 1


def creer_bateau(classe, nombre):
    """
    Ajoute des bateaux d'un certain type à une liste

    :param classe: Classe des bateaux à créer
    :param nombre: Nombre de bateaux à créer
    :return: bateaux créés
    """
    bateaux = []
    for i in range(nombre):
        bateaux.append(classe())  # classe() appelle le constructeur de la classe
    return bateaux


def creer_bateaux():
    """
    Crée une liste contenant le nombre désiré de chaque type de bateau.

    :return: pas de retour
    """
    bateaux = []
    bateaux.extend(creer_bateau(bateau.Torpilleur, NOMBRE_TORPILLEURS))
    bateaux.extend(creer_bateau(bateau.SousMarin, NOMBRE_SOUS_MARINS))
    bateaux.extend(creer_bateau(bateau.ContreTorpilleur, NOMBRE_CONTRE_TORPILLEURS))
    bateaux.extend(creer_bateau(bateau.Croiseur, NOMBRE_CROISEURS))
    bateaux.extend(creer_bateau(bateau.PorteAvions, NOMBRE_PORTES_AVIONS))
    return bateaux


if __name__ == "__main__":
    bateaux = creer_bateaux()
    grille = Grille(bateaux)
    interface = Afficheur(grille)
    interface.afficher_menu()
    interface.boucle_des_evenements()
