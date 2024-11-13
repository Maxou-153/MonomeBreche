import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import time

class CapteurDebitHuile:
    def __init__(self, impulsions_par_litre=450, precision=0.03, debit_min=1, debit_max=100):
        """
        Initialise un capteur de débit d'huile basé sur une turbine.
        
        :param impulsions_par_litre: Nombre d'impulsions par litre générées par le capteur.
        :param precision: Niveau de précision du capteur (en pourcentage du débit mesuré).
        :param debit_min: Débit minimum mesuré par le capteur (L/min).
        :param debit_max: Débit maximum mesuré par le capteur (L/min).
        """
        self.impulsions_par_litre = impulsions_par_litre
        self.precision = precision
        self.debit_min = debit_min
        self.debit_max = debit_max

    def calculer_debit(self, vitesse_pompe):
        """
        Calcule le débit en fonction de la vitesse de la pompe.
        
        :param vitesse_pompe: Vitesse de la pompe (rpm).
        :return: Débit d'huile calculé (L/min).
        """
        debit = ((vitesse_pompe - 500) / (3000 - 500)) * (self.debit_max - self.debit_min) + self.debit_min
        return debit

    def mesurer_debit(self, vitesse_pompe):
        """
        Simule la mesure du débit d'huile à partir de la vitesse de la pompe.
        
        :param vitesse_pompe: Vitesse de la pompe (rpm).
        :return: Débit d'huile mesuré (litres par minute).
        """
        debit_theorique = self.calculer_debit(vitesse_pompe)
        bruit = np.random.normal(0, self.precision * debit_theorique)
        debit_mesure = np.clip(debit_theorique + bruit, self.debit_min, self.debit_max)
        return debit_mesure

def simuler_capteur_dans_le_temps(capteur, duree):
    """
    Simule les mesures du capteur pendant une durée donnée avec un débit mesuré modifiable par un curseur.
    
    :param capteur: Instance du capteur de débit d'huile.
    :param duree: Durée de la simulation en secondes.
    """
    t = []
    mesures_debit = []
    start_time = time.time()

    # Création de la figure et des axes
    plt.ion()  # Active le mode interactif pour le graphique
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.35)  # Ajustement pour le curseur et le bouton
    line, = ax.plot([], [], label='Débit mesuré (L/min)', color='blue')
    ax.set_xlim(0, duree)
    ax.set_ylim(0, capteur.debit_max + 10)
    ax.set_xlabel('Temps (s)')
    ax.set_ylabel('Débit (L/min)')
    ax.set_title('Simulation du Débit d\'huile Mesuré par le Capteur à Turbine')
    ax.grid(True)
    ax.legend()

    # Initialisation du débit mesuré à 50 L/min
    debit_mesure = 50
    mesures_debit.append(debit_mesure)  # Ajout de la valeur initiale
    t.append(0)  # Temps initial

    # Création du curseur
    axcolor = 'lightgoldenrodyellow'
    ax_debit = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
    slider_debit = Slider(ax_debit, 'Débit Mesuré (L/min)', 1, 100, valinit=debit_mesure)

    # Création du bouton
    ax_button = plt.axes([0.2, 0.05, 0.15, 0.05])  # Position du bouton
    button_reset = Button(ax_button, 'Reset Débit', color='lightcoral', hovercolor='lightpink')

    # Fonction pour réinitialiser le débit à 50
    def reset_debit(event):
        slider_debit.set_val(50)

    button_reset.on_clicked(reset_debit)  # Lier la fonction au clic sur le bouton

    while time.time() - start_time < duree:
        # Générer une vitesse de pompe aléatoire entre 500 et 3000 rpm
        vitesse_pompe = np.random.uniform(500, 3000)  # Vitesse de la pompe en rpm

        # Mesurer le débit avec la valeur du curseur
        debit_mesure = slider_debit.val
        mesures_debit.append(debit_mesure)  # Ajoute la valeur du curseur
        t.append(time.time() - start_time)  # Temps écoulé
        
        # Mise à jour du graphique
        line.set_data(t, mesures_debit)
        ax.set_xlim(0, max(duree, len(t)))  # Met à jour l'axe des x si nécessaire
        ax.set_ylim(0, capteur.debit_max + 10)  # Met à jour l'axe des y si nécessaire
        plt.draw()
        plt.pause(1)  # Pause pour permettre la mise à jour du graphique

        print(f"Vitesse de la pompe: {vitesse_pompe:.2f} rpm, Débit mesuré: {debit_mesure:.2f} L/min")

    plt.ioff()  # Désactive le mode interactif
    plt.show()  # Affiche le graphique final

    return t,
    mesures_debit

# Initialisation du capteur avec un nombre d'impulsions par litre et une précision
capteur = CapteurDebitHuile(impulsions_par_litre=450, precision=0.03, debit_min=1, debit_max=100)

# Simuler le capteur pour une durée de 60 secondes avec un débit mesuré modifiable par un curseur
temps_simulation, mesures = simuler_capteur_dans_le_temps(capteur, 60)
