import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time

class CapteurPTO:
    def __init__(self, rpm_initial=2000):
        self.rpm = rpm_initial

    def set_rpm(self, rpm):
        self.rpm = rpm

    def get_rpm(self):
        return self.rpm

def update_graph(rpm_history, time_history):
    line.set_data(time_history, rpm_history)
    ax.set_xlim(0, max(1, len(time_history)))
    ax.set_ylim(1400, 2600)  # Plage de régime de 1400 à 2600 RPM
    plt.draw()
    plt.pause(0.01)  # Pause pour permettre le rafraîchissement du graphique

def change_mode(mode):
    if mode == 1:
        sensor.set_rpm(np.random.uniform(1500, 1800))  # Mode 1: 1500 à 1800 RPM
    elif mode == 2:
        sensor.set_rpm(np.random.uniform(1800, 2100))  # Mode 2: 1800 à 2100 RPM
    elif mode == 3:
        sensor.set_rpm(np.random.uniform(2100, 2400))  # Mode 3: 2100 à 2400 RPM
    elif mode == 4:
        sensor.set_rpm(np.random.uniform(2400, 2500))  # Mode 4: 2400 à 2500 RPM

def reset_rpm(event):
    average_rpm = (1500 + 2500) / 2  # Moyenne de la prise de force
    sensor.set_rpm(average_rpm)  # Remet le régime à la moyenne

def simulate_rpm(duree):
    start_time = time.time()
    rpm_history = []
    time_history = []

    while time.time() - start_time < duree:
        current_time = time.time() - start_time
        rpm = sensor.get_rpm()
        rpm_history.append(rpm)
        time_history.append(current_time)

        update_graph(rpm_history, time_history)

        time.sleep(1)  # Met à jour toutes les secondes

    plt.ioff()  # Désactive le mode interactif
    plt.show()  # Affiche le graphique final

# Initialisation du capteur avec un régime initial
sensor = CapteurPTO(rpm_initial=2000)

# Création de la figure et des axes
plt.ion()  # Active le mode interactif pour le graphique
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
line, = ax.plot([], [], label='Régime (RPM)', color='blue')
ax.set_xlim(0, 10)
ax.set_ylim(1400, 2600)  # Plage de régime de 1400 à 2600 RPM
ax.set_xlabel('Temps (s)')
ax.set_ylabel('Régime (RPM)')
ax.set_title('Simulation de la Prise de Force (PTO) du Tracteur')
ax.grid(True)
ax.legend()

# Création des boutons pour changer de mode
axmode1 = plt.axes([0.1, 0.05, 0.1, 0.075])
button_mode1 = Button(axmode1, 'Mode 1')
button_mode1.on_clicked(lambda event: change_mode(1))

axmode2 = plt.axes([0.25, 0.05, 0.1, 0.075])
button_mode2 = Button(axmode2, 'Mode 2')
button_mode2.on_clicked(lambda event: change_mode(2))

axmode3 = plt.axes([0.4, 0.05, 0.1, 0.075])
button_mode3 = Button(axmode3, 'Mode 3')
button_mode3.on_clicked(lambda event: change_mode(3))

axmode4 = plt.axes([0.55, 0.05, 0.1, 0.075])
button_mode4 = Button(axmode4, 'Mode 4')
button_mode4.on_clicked(lambda event: change_mode(4))

# Création du bouton pour réinitialiser le RPM
axreset = plt.axes([0.7, 0.05, 0.1, 0.075])
button_reset = Button(axreset, 'Reset RPM')
button_reset.on_clicked(reset_rpm)

# Lancer la simulation de RPM pour une durée de 60 secondes
simulate_rpm(60)
