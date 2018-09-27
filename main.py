#Ce fichier est l'endroit où le programme commence.
from tkinter import *
import fenetreprincipale


fenetre = fenetreprincipale.FenetrePrincipale(master=Tk()) #Crée une fenêtre
fenetre.mainloop() #La fenêtre principale entre la boucle des événements, c.-à-d. qu'elle commence à recevoir les entrées de l'utilisateur
