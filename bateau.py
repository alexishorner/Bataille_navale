# coding: utf-8
"""
Module contenant des classes relatives aux bateaux.
"""

from case import Etat, Case


class AbstractBateau:
    """
    Classe permettant de créer des bateaux. Elle sert de base pour les classe de chaque type de bateau.

    Le mot "Abstract" dans son nom indique qu'elle n'est pas conçue pour être utilisée de manière directe.
    """
    TAILLE = None   # l'attribut "largeur_pixels" est défini en dehors du constructeur,
                    # car chaque bateau d'un même type a la même taille
    TYPE = None  # le type est lui aussi commun à tous les bateaux d'une même classe
    NOMBRE_RESTANT = None  # nombre de bateaux non coulés par type

    def __init__(self, cases=None):
        """
        constructeur de la classe "AbstractBateau"

        ATTENTION : comme suggéré par le caractère "_" dans le nom de l'attribut "_cases",
        il ne faut jamais modifier cet attribut directement.
        Pour modifier la valeur de cet attribut il faut absolument utiliser la méthode "setCases(self, cases)".

        :param cases: tuple contenant les cases occupées par le _bateau
        """
        self._cases = []
        if cases is not None:
            cases_libres = True
            for case in cases:
                if case.bateau() is not None and case.bateau() is not self:
                    cases_libres = False
            if cases_libres:
                self.set_cases(list(cases))

    def set_cases(self, cases):
        """
        Méthode permettant de modifier la valeur de "_cases".

        Il vérifie que le nombre et l'alignement des cases est valide
        et que celles-ci sont adjacentes.
        :return: booléen informant sur le succès de l'opération
        """
        etait_coule = self.est_coule()
        if not cases:  # Si "cases" est vide ou vaut "None"
            for case in self._cases:
                case.set_bateau(None)
            self._cases = []
        elif len(cases) == self.TAILLE and Case.sont_alignees(cases) and Case.sont_adjacentes(cases):
            # Le "self.__class__.largeur_pixels" permet d'accéder à la taille du bateau,
            # y compris avec les classes héritant de "AbstractBateau".
            # Cette condition vérifie qu'il y a le bon nombre de cases, qu'elle sont alignées et
            # qu'il n'y a pas d'espace les séparant.
            for case in cases:
                if case.bateau() is not None:   # vérifie qu'un autre bateau n'est pas déjà présent
                                                # sur une des nouvelles cases
                    return False  # renvoie "False" car un bateau est déjà présent

            for case in self._cases:
                case.set_bateau(None)  # enlève le bateau des anciennes cases

            self._cases = cases
            for case in self._cases:
                case.set_bateau(self)  # ajoute le bateau aux nouvelles cases
        else:
            return False  # renvoie "False", car l'opération a échoué
        # On regarde si l'état du bateau a changé
        self.__class__.NOMBRE_RESTANT += etait_coule-self.est_coule()
        # Pour plus d'informations regarder méthode "recevoir_tir"
        return True  # renvoie "True", car les cases ont bien été remplacées

    def est_coule(self):
        """
        Méthode définissant si un bateau est coulé.

        :return: booléen égal à "True" si le bateau est coulé, et "False" sinon
        """
        for case in self._cases:
            if case.etat not in (Etat.TOUCHE, Etat.COULE):
                return False
        return True

    def recevoir_tir(self, case):
        """
        Méthode appelée lorsque le joueur tire sur une case appartenant au bateau.

        :return: 1. Etat de la case après l'opération ou "None" si la case a déjà reçu un tir ou
                    "False" si l'opération a échoué
                 2. Cases modifiées
        """
        etait_coule = self.est_coule()
        if case in self._cases:  # si la case est une case du bateau
            if case.etat == Etat.BATEAU_INTACT:  # si la case n'a pas déjà été touchée
                cases_modifiees = [case]
                case.etat = Etat.TOUCHE  # le bateau est touché en cette case
                if self.est_coule():
                    self.NOMBRE_RESTANT -= 1
                    cases_modifiees = self._cases
                    for chaque_case in self._cases:     # On utilise le nom "chaque_case", car "case" est déjà
                                                        # le nom d'un paramètre
                        chaque_case.etat = Etat.COULE  # si le bateau est coulé, on change l'état de chaque case

                        # On regarde si l'état du bateau a changé
                        self.__class__.NOMBRE_RESTANT += etait_coule-self.est_coule()
                        # Note : on a le droit de soustraire des booléens, "True" vaut 1 et "False" 0
                        # Donc si le bateau n'était pas coulé (0) et que maintenant il l'est (1), on a 0-1 = -1,
                        # donc on ajoute -1 (on enlève 1) au nombre de bateaux restants
                return case.etat, cases_modifiees
            return None, None  # La case a déjà reçu un tir
        return False, None  # Il y a eu une erreur


class Torpilleur(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des torpilleurs.
    """
    TAILLE = 2  # la taille et le type sont redéfinis pour chaque classe héritant de "AbstractBateau"
    TYPE = "torpilleur"     # sert à afficher le type du bateau indépendamment du nom de la classe
                            # (contrairement à __class__.__name__.lower())
    NOMBRE_RESTANT = 0

    def __init__(self, cases=None):
        AbstractBateau.__init__(self, cases)  # appelle le constructeur de la classe "AbstractBateau"


class SousMarin(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des sous-marins.
    """
    TAILLE = 3  # la taille et le type sont redéfinis pour chaque classe héritant de "AbstractBateau"
    TYPE = "sous-marin"
    NOMBRE_RESTANT = 0

    def __init__(self, cases=None):
        AbstractBateau.__init__(self, cases)  # appelle le constructeur de la classe "AbstractBateau"


class ContreTorpilleur(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des contre-torpilleurs.
    """
    TAILLE = 3  # la taille et le type sont redéfinis pour chaque classe héritant de "AbstractBateau"
    TYPE = "contre-torpilleur"
    NOMBRE_RESTANT = 0

    def __init__(self, cases=None):
        AbstractBateau.__init__(self, cases)  # appelle le constructeur de la classe "AbstractBateau"


class Croiseur(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des croiseurs.
    """
    TAILLE = 4  # la taille et le type sont redéfinis pour chaque classe héritant de "AbstractBateau"
    TYPE = "croiseur"
    NOMBRE_RESTANT = 0

    def __init__(self, cases=None):
        AbstractBateau.__init__(self, cases)  # appelle le constructeur de la classe "AbstractBateau"


class PorteAvions(AbstractBateau):
    """
    Classe héritant de "AbstractBateau" permettant de créer des porte-avions.
    """
    TAILLE = 5  # la taille et le type sont redéfinis pour chaque classe héritant de "AbstractBateau"
    TYPE = "porte-avions"
    NOMBRE_RESTANT = 0

    def __init__(self, cases=None):
        AbstractBateau.__init__(self, cases)  # appelle le constructeur de la classe "AbstractBateau"
