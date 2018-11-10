from case import *
class AbstractBateau:
    """
    Classe de base permettant de créer des objets de type AbstractBateau. Les classes de bateaux de chaque type héritent de cette classe.
    """
    def __init__(self, cases = None):
        """
        Constructeur de la classe AbstractBateau, il est appelé lors de la création d'un objet de type AbstractBateau.
        Il sert à initialiser les attributs de la classe.

        ATTENTION : comme suggéré par le caractère "_" dans le nom de l'attribut "_case", il ne faut jamais modifier cet attribut directement.
        Pour modifier la valeur de cet attribut il faut absolument utiliser la méthode "setCases(self, cases)".

        :param cases: tuple contenant les cases occupées par le _bateau
        """
        self._cases = tuple(cases)
        self.taille = None


    def setCases(self, cases):
        """
        Mutateur permettant de modifier la valeur de _cases.
        :return: booléen informant sur le succès de l'opération
        """
        if len(cases) == self.taille and :
            for case in self._cases:
                case._bateau = None
            self._cases = cases
            for case in self._cases:
                case.setBateau(self)
            return True
        else:
            return False


    def estCoule(self):
        """
        Méthode définissant si un _bateau est coulé.
        :return: booléen égal à "True" si le _bateau est coulé, et "False" sinon
        """
        for case in self._cases:
            if case.etat != Etat.touche or case.etat != Etat.coule:
                return False
        return True

    def recevoirTir(self, case):
        """
        Méthode appelée lorsque le joueur tire sur une case appartenant au _bateau.
        :return: booléen informant si le tir a été effectué avec succès ou non
        """
        if case in self._cases:
            if case.etat != Etat.coule:
                case.etat = Etat.touche
                if self.estCoule():
                    case.etat = Etat.coule
            return True
        else:
            return False


class Torpilleur(AbstractBateau):
    """
    Classe permettant de créer des torpilleurs.
    """
    def __init__(self, cases = None):
        AbstractBateau.__init__(cases)
        self.type = "torpilleur"
        self.taille = 2
