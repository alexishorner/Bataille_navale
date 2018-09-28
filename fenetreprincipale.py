#Ce fichier contient la classe de la fenêtre principale
from tkinter import * #Ce module permet de faire une interface graphique (une application avec des fenêtres et pas seulement du texte dans la console)


class FenetrePrincipale(Frame):
    """
    Hérite de la classe `Frame`.
    """
    def __init__(self, master=None):
        """
        Constructeur de la classe `FenetrePrincipale`. Il sert à créer
        un objet de type `FenetrePrincipale`. Les différents attributs (variables de la classe)
        sont créés à cet endroit.
        """
        Frame.__init__(self, master)
        self.pack()
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["command"] = self.quit
        self.QUIT.pack({"side": "left"})
