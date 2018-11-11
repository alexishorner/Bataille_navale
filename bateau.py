from case import *
from fonctions import *


class AbstractBateau:
    """
    Classe permettant de créer des bateaux. Elle sert de base pour les classe de chaque type de bateau.

    Le mot "Abstract" dans son nom indique qu'elle n'est pas conçue pour être utilisée de manière directe.
    """
    TAILLE = None  # l'attribut "TAILLE" est défini en dehors du constructeur, car chaque bateau d'un même type a la même taille
    TYPE = None  # le type est lui aussi commun à tous les bateaux d'une même classe
    def __init__(self, cases=None):
        """
        constructeur de la classe "AbstractBateau"

        ATTENTION : comme suggéré par le caractère "_" dans le nom de l'attribut "_cases", il ne faut jamais modifier cet attribut directement.
        Pour modifier la valeur de cet attribut il faut absolument utiliser la méthode "setCases(self, cases)".

        :param cases: tuple contenant les cases occupées par le _bateau
        """
        self._cases = list(cases)

    def set_cases(self, cases):
        """
        Méthode permettant de modifier la valeur de "_cases".

        Il vérifie que le nombre et l'alignement des cases est valide
        et que
        :return: booléen informant sur le succès de l'opération
        """
        if len(cases) == self.__class__.TAILLE and sont_alignees(cases):  # le "self.__class__.TAILLE" permet d'accéder à la taille du bateau,
                                                                         # y compris avec les classes héritant de "AbstractBateau".
            for case in cases:
                if case._bateau is not None:  # vérifie qu'un autre bateau n'est pas déjà présent sur une des nouvelles cases
                    return False  # renvoie "False" car un bateau est déjà présent

            for case in self._cases:
                case.set_bateau(None)  # enlève le bateau des anciennes cases

            self._cases = cases
            for case in self._cases:
                case.set_bateau(self)  # ajoute le bateau aux nouvelles cases
            return True  # renvoie "True", car les cases ont bien été remplacées
        else:
            return False  # renvoie "False", car l'opération a échoué

    def est_coule(self):
        """
        Méthode définissant si un bateau est coulé.

        :return: booléen égal à "True" si le _bateau est coulé, et "False" sinon
        """
        for case in self._cases:
            if case.etat != Etat.touche or case.etat != Etat.coule:
                return False
        return True

    def recevoir_tir(self, case):
        """
        Méthode appelée lorsque le joueur tire sur une case appartenant au bateau.

        :return: booléen informant si le tir a été effectué avec succès ou non
        """
        if case in self._cases:  # si la case est une case du bateau
            if not self.est_coule():  # si le bateau n'est pas coulé
                case.etat = Etat.touche  # le bateau est touché en cette case
                if self.est_coule():
                    for chaqueCase in self._cases:
                        chaqueCase.etat = Etat.coule  # si le bateau est coulé, on change l'état de chaque case
            return True
        else:
            return False


class Torpilleur(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des torpilleurs.
    """
    TAILLE = 2  # la taille et le type sont redéfini pour chaque classe héritant de "AbstractBateau"
    TYPE = "torpilleur"

    def __init__(self, cases=None):
        super().__init__(cases)  # appelle le constructeur de la classe "AbstractBateau"


class SousMarin(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des sous-marins.
    """
    TAILLE = 3  # la taille et le type sont redéfini pour chaque classe héritant de "AbstractBateau"
    TYPE = "sous-marin"

    def __init__(self, cases=None):
        super().__init__(cases)  # appelle le constructeur de la classe "AbstractBateau"


class ContreTorpilleur(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des contre-torpilleurs.
    """
    TAILLE = 3  # la taille et le type sont redéfini pour chaque classe héritant de "AbstractBateau"
    TYPE = "contre-torpilleur"

    def __init__(self, cases=None):
        super().__init__(cases)  # appelle le constructeur de la classe "AbstractBateau"


class Croiseur(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des croiseurs.
    """
    TAILLE = 4  # la taille et le type sont redéfini pour chaque classe héritant de "AbstractBateau"
    TYPE = "croiseur"

    def __init__(self, cases=None):
        super().__init__(cases)  # appelle le constructeur de la classe "AbstractBateau"


class PorteAvions(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des porte-avions.
    """
    TAILLE = 5  # la taille et le type sont redéfini pour chaque classe héritant de "AbstractBateau"
    TYPE = "porte-avions"

    def __init__(self, cases=None):
        super().__init__(cases)  # appelle le constructeur de la classe "AbstractBateau"
