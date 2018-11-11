# Attention les noms de variables ne contiennent pas d'accent, ce qui peut changer leur signification (par ex : côté devient cote)
from enumerations import *
import turtle


class Stylo:
    """
    Cette classe permet de dessiner les objets à l'écran. Elle hérite de "turtle.Turtle".
    """
    def __init__(self, mode=Mode.tortue):
        """
        constructeur de la classe "Stylo"

        :param mode: mode de dessin, il peut être une chaîne de caractères parmi "tortue" et "console" ou un nombre entre 0 et 1
        :raises: cette méthode lève l'exception "LookupError" lorsque le mode est invalide
        """
        modes = {"tortue":Mode.tortue, "t":Mode.tortue, "console":Mode.console, "c":Mode.console}
        if mode in modes:  # si le mode est une chaîne de caractères contenue dans "modes"
            mode = modes[mode]
        if mode != Mode.tortue and mode != Mode.console:
            e = LookupError()
            valAttendues = str(list(modes.keys()).extend([0, 1]))
            e.args = ("Paramètre \"mode\" invalide." + "Valeur reçue : " + str(mode) + "Les valeurs attendues sont : " + valAttendues,)
            raise e
        self._mode = mode
        if mode == Mode.tortue:
            self.tortue = turtle.Turtle()
            self.tortue.hideturtle()  # cache la tortue
            self.tortue.screen.tracer(0, 0)  # rend le dessin instantané, mais l'écran doit être rafraîchit manuellement en appelant "self.screen.update()"

    def dessinerCase(self, case):
        """
        Affiche une case à l'écran.

        Le signe dessiné au centre de la case dépend de son état.
        :param case: case à dessiner
        :return: "None"
        """
        self.dessinerForme(case.carre())

    def dessinerForme(self, chemin, ferme=True):
        """
        Dessine une forme à l'écran.

        :param chemin: liste de points décrivant le chemin suivit par le stylo
        :param ferme: booléen indiquant si le style doit fermer la forme en reliant le premier et dernier point.
        :return: "None"
        """
        if self._mode == Mode.tortue:
            self.tortue.up()
            self.tortue.goto(chemin[0])
            self.tortue.down()
            for i in range(1, len(chemin)):  # le stylo est déjà à "chemin[0]", donc on commence à 1
                self.tortue.goto(chemin[i])
            if ferme:
                self.tortue.goto(chemin[0])

    def dessinerEtat(self, case):

