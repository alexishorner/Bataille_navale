# Attention les noms de variables ne contiennent pas d'accent, ce qui peut changer leur signification (par ex : côté devient cote)
from enumerations import *
import turtle


class Stylo(turtle.Turtle):
    """
    Cette classe permet de dessiner les objets à l'écran. Elle hérite de "turtle.Turtle".
    """
    def __init__(self):
        """
        constructeur de la classe "Stylo"
        """
        super().__init__()
        self.hideturtle()  # cache la tortue
        self.screen.tracer(0, 0)  # rend le dessin instantané, mais l'écran doit être rafraîchit manuellement en appelant "self.screen.update()"

    def dessinerCase(self, case):
        """"
        Affiche une case à l'écran.

        Le signe dessiné au centre de la case dépend de son état.
        :param case: case à dessiner
        :return: "None"
        """
        x = case.position[Coord.x]
        y = case.position[Coord.y]
        cote = case.TAILLE
        chemin = [[x, y], [x+cote, y], [x+cote, y+cote], [x, y+cote]]
        self.dessiner()

    def dessiner(self, chemin, ferme=True):
        """
        Dessine une forme à l'écran.

        :param chemin: liste de points décrivant le chemin suivit par le stylo
        :param ferme: booléen indiquant si le style doit fermer la forme en reliant le premier et dernier point.
        :return: "None"
        """
        self.up()
        self.goto(chemin[0])
        self.down()
        for i in range(1, len(chemin)):  # le stylo est déjà à "chemin[0]", donc on commence à 1
            self.goto(chemin[i])
        if ferme:
            self.goto(chemin[0])
