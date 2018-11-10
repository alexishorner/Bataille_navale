# Attention les noms de variables ne contiennent pas d'accent, ce qui peut changer leur signification (par ex : côté devient cote)
import turtle

class Stylo(turtle.Turtle):
    def dessinerCase(self, case):
        """"
        Dessine une case aux coordonnées coord (les coordonnées vont de 0 à nbreDeCasesCote**2-1,
        c'est en fait l'index de la case dans le tableau grille).
        L'état de la case détermine son apparence
        """
        self.up()
        self.goto(case.position)
        self.setheading()


    def dessiner(self, chemin, ferme):
