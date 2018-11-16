# Attention les noms de variables ne contiennent pas d'accent, ce qui peut changer leur signification (par ex : côté devient cote)
from enumerations import *
import turtle


class Tortue(turtle.Turtle):
    """
    Cette classe permet de customiser la tortue fournie par le module "turtle".
    """
    COULEUR = "white"  # couleur de l'intértieur des cases

    def __init__(self):
        """
        constructeur de la classe "Tortue"
        """
        super().__init__()
        self.hideturtle()  # cache la tortue
        self.screen.tracer(0, 0)  # rend le dessin instantané, mais l'écran doit être rafraîchit manuellement en appelant "self.screen.update()"
        self.fillcolor(self.__class__.COULEUR)

    def _dessiner_forme(self, chemin, ferme=True):
        """
        Dessine une forme à l'écran.

        :param chemin: liste de points décrivant le chemin suivit par le stylo
        :param ferme: booléen indiquant si le style doit fermer la forme en reliant le premier et dernier point.
        :return: "None"
        """
        self.up()
        self.goto(chemin[0])
        self.down()
        self.begin_fill()
        for i in range(1, len(chemin)):  # le stylo est déjà à "chemin[0]", donc on commence à 1
            self.goto(chemin[i])
        if ferme:
            self.goto(chemin[0])
        self.end_fill()

    def dessiner_case(self, case):
        """
        Affiche une case à l'écran.

        Le dessin au centre de la case dépend de son état.
        :param case: case à dessiner
        :return: "None"
        """
        self._dessiner_forme(case.carre())
        self._dessiner_etat(case)
        self.screen.update()  # on actualise l'écran pour afficher les changements

    def _dessiner_etat(self, case):
        """
        Dessine l'état de la case.
        :param case: case dont il faut dessiner l'état
        :return: "None"
        """
        if case.etat == Etat.DANS_L_EAU:
            self._dessiner_dans_l_eau(case.milieu())
        elif case.etat == Etat.TOUCHE:
            self._dessiner_touche(case.milieu())
        elif case.etat == Etat.COULE:
            self._dessiner_coule(case.milieu())

    def _dessiner_dans_l_eau(self, position):
        self.up()
        self.goto(position)
        self.down()
        self.write("O")
        # TODO: définir l'image à dessiner

    def _dessiner_touche(self, position):
        self.up()
        self.goto(position)
        self.down()
        self.write("+")
        # TODO: définir l'image à dessiner

    def _dessiner_coule(self, position):
        self.up()
        self.goto(position)
        self.down()
        self.write("X")
        # TODO: définir l'image à dessiner


class Afficheur:
    """
    Cette classe permet de dessiner les objets à l'écran. Elle utilise un objet "Tortue" ou la console pour dessiner à l'écran.
    """
    def __init__(self, grille):
        """
        constructeur de la classe "Stylo"

        :param grille: grille de jeu à afficher
        :raises: cette méthode lève l'exception "LookupError" lorsque le mode est invalide
        """
        self.grille = grille
        self.tortue = Tortue()

    def dessiner_grille_console(self):
        for i in range(len(self.grille.cases)):
            for j in range(len)
        # TODO: définir un moyen de dessiner la grille dans la console
