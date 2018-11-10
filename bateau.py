from case import *
from fonctions import *
class AbstractBateau:
    """
    Classe permettant de créer des bateaux. Elle sert de base pour les classe de chaque type de bateau.

    Le mot "Abstract" dans son nom indique qu'elle n'est pas conçue pour être utilisée de manière directe.
    """
    def __init__(self, cases=None):
        """
        constructeur de la classe "AbstractBateau"

        ATTENTION : comme suggéré par le caractère "_" dans le nom de l'attribut "_case", il ne faut jamais modifier cet attribut directement.
        Pour modifier la valeur de cet attribut il faut absolument utiliser la méthode "setCases(self, cases)".

        :param cases: tuple contenant les cases occupées par le _bateau
        """
        self._cases = tuple(cases)
        self.type = None
        self.taille = None


    def setCases(self, cases):
        """
        Mutateur permettant de modifier la valeur de _cases.

        Il vérifie que le nombre et l'alignement des cases est valide
        et que
        :return: booléen informant sur le succès de l'opération
        """
        if len(cases) == self.taille and sontAlignees(cases):
            for case in cases:
                if case._bateau is not None: # vérifie qu'un autre bateau n'est pas déjà présent sur une des nouvelles cases
                    return False # renvoie "False" car un bateau est déjà présent

            for case in self._cases:
                case.setBateau(None) # enlève le bateau des anciennes cases

            self._cases = cases
            for case in self._cases:
                case.setBateau(self) # ajoute le bateau aux nouvelles cases
            return True # renvoie "True", car les cases ont bien été remplacées
        else:
            return False # renvoie "False", car l'opération a échoué


    def estCoule(self):
        """
        Méthode définissant si un bateau est coulé.

        :return: booléen égal à "True" si le _bateau est coulé, et "False" sinon
        """
        for case in self._cases:
            if case.etat != Etat.touche or case.etat != Etat.coule:
                return False
        return True

    def recevoirTir(self, case):
        """
        Méthode appelée lorsque le joueur tire sur une case appartenant au bateau.

        :return: booléen informant si le tir a été effectué avec succès ou non
        """
        if case in self._cases: # si la case est une case du bateau
            if not self.estCoule(): # si le bateau n'est pas coulé
                case.etat = Etat.touche # le bateau est touché en cette case
                if self.estCoule():
                    for chaqueCase in self._cases:
                        chaqueCase.etat = Etat.coule # si le bateau est coulé, on change l'état de chaque case
            return True
        else:
            return False


class Torpilleur(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des torpilleurs.
    """
    def __init__(self, cases=None):
        AbstractBateau.__init__(cases)
        self.type = "torpilleur"
        self.taille = 2


class SousMarin(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des sous-marins.
    """
    def __init__(self, cases=None):
        AbstractBateau.__init__(cases)
        self.type = "sous-marin"
        self.taille = 3


class ContreTorpilleur(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des contre-torpilleurs.
    """
    def __init__(self, cases=None):
        AbstractBateau.__init__(cases)
        self.type = "contre-torpilleur"
        self.taille = 3


class Croiseur(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des croiseurs.
    """
    def __init__(self, cases=None):
        AbstractBateau.__init__(cases)
        self.type = "croiseur"
        self.taille = 4


class PorteAvions(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des porte-avions.
    """
    def __init__(self, cases=None):
        AbstractBateau.__init__(cases)
        self.type = "porte-avions"
        self.taille = 5
