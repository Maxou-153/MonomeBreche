import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import threading
import time
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Classe principale pour l'interface utilisateur
class InterfacePrincipale:
    def __init__(self, root):
        self.root = root
        self.root.title("Système de Gestion des Capteurs")

        # Création des onglets
        self.tab_control = ttk.Notebook(root)

        self.tabs = {
            "Jauge Enfoncement": self.init_jauge_enfoncement,
            "Pression des Parois": self.init_pressure_tab,
            "Gyroscope": self.init_gyroscope_tab,
            "Piquets": self.init_piquet_tab,
            "Vérins": self.init_verin_tab,
        }

        for tab_name, init_func in self.tabs.items():
            frame = ttk.Frame(self.tab_control)
            self.tab_control.add(frame, text=tab_name)
            init_func(frame)

        self.tab_control.pack(expand=1, fill="both")

    def init_jauge_enfoncement(self, frame):
        JaugeEnfoncement(frame)

    def init_pressure_tab(self, frame):
        Pressure(frame)

    def init_gyroscope_tab(self, frame):
        GyroscopeApp(frame)

    def init_piquet_tab(self, frame):
        CompteurPiquets(frame)

    def init_verin_tab(self, frame):
        label = tk.Label(frame, text="Contrôle des Vérins", font=("Arial", 16))
        label.pack(pady=10)

# Classe pour gérer l'interface graphique liée à la pression des parois
class Pressure:
    def __init__(self, frame):
        self.frame = frame

        # Liste pour stocker les valeurs de pression au fil du temps
        time_values = []
        pressure_values = []

        # Fonction pour mettre à jour la pression, l'affichage et le graphique
        def update_pressure(val):
            # Convertir la valeur du potentiomètre (0-100) en pression (0-3 bars)
            pression = float(val) * 3.0 / 100.0
            
            # Mettre à jour le label de la pression affichée en temps réel
            label_pressure.config(text=f"Pression actuelle : {pression:.2f} bars")
            
            # Ajouter la nouvelle pression et le temps actuel
            current_time = time.time()  # Temps actuel en secondes
            time_values.append(current_time)
            pressure_values.append(pression)
            
            # Limiter les valeurs pour afficher uniquement les 60 dernières secondes (pour un balayage sur 1 minute)
            if len(time_values) > 60:
                time_values.pop(0)
                pressure_values.pop(0)
            
            # Mettre à jour le graphique
            ax.clear()
            ax.plot(time_values, pressure_values, color='blue', lw=2)
            ax.set_ylim(0, 3)  # Plage de pression de 0 à 3 bars
            ax.set_xlabel("Temps (secondes)")
            ax.set_ylabel("Pression (bars)")
            ax.set_title("Évolution de la Pression Sangle Trémie")
            canvas.draw()

        # Fonction pour simuler le changement automatique du potentiomètre
        def auto_change_potentiometer():
            # Simuler la valeur du potentiomètre de manière aléatoire (0-100)
            new_value = random.randint(0, 100)
            
            # Mettre à jour la pression et le graphique avec la nouvelle valeur du potentiomètre
            update_pressure(new_value)
            
            # Relancer la fonction après un délai pour créer un effet de changement automatique
            self.frame.after(1000, auto_change_potentiometer)  # 1 seconde pour mettre à jour la pression

        # Label pour afficher la pression
        label_pressure = tk.Label(self.frame, text="Pression actuelle : 0.00 bars", font=('Helvetica', 14))
        label_pressure.pack(pady=10)

        # Création du graphique avec Matplotlib
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.set_ylim(0, 3)
        ax.set_xlim(0, 60)  # Afficher les 60 dernières secondes
        ax.set_title("Évolution de la Pression Sangle Trémie")
        ax.set_xlabel("Temps (secondes)")
        ax.set_ylabel("Pression (bars)")

        # Affichage du graphique dans le frame de l'onglet
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.get_tk_widget().pack(pady=20)
        canvas.draw()

        # Démarrer la fonction qui change automatiquement la valeur du potentiomètre
        auto_change_potentiometer()


# Classe pour gérer l'interface graphique et simuler l'inclinaison
class GyroscopeApp:
    def __init__(self, frame):
        self.frame = frame
        self.root = frame

        # Labels pour afficher les angles d'inclinaison
        self.x_angle_label = tk.Label(frame, text="Inclinaison X: 0", font=("Arial", 14))
        self.x_angle_label.pack(pady=20)

        self.y_angle_label = tk.Label(frame, text="Inclinaison Y: 0", font=("Arial", 14))
        self.y_angle_label.pack(pady=20)

        # Mise à jour des données en temps réel
        self.update_inclination()

    def update_inclination(self):
        # Simuler les valeurs d'inclinaison (valeurs aléatoires entre -30 et 30 degrés)
        angle_x = random.uniform(-30, 30)
        angle_y = random.uniform(-30, 30)

        # Mettre à jour les labels avec les nouvelles valeurs simulées
        self.x_angle_label.config(text=f"Inclinaison X: {angle_x:.2f}°")
        self.y_angle_label.config(text=f"Inclinaison Y: {angle_y:.2f}°")

        # Appeler cette méthode toutes les 100ms pour une mise à jour en temps réel
        self.root.after(100, self.update_inclination)

# Classe pour la gestion de la jauge d'enfoncement
class JaugeEnfoncement:
    def __init__(self, frame):
        self.frame = frame

        # Variables pour la jauge
        self.enfoncement_valeur = tk.DoubleVar(value=0.0)
        self.enfoncement_en_cours = False
        self.pause = False

        # Interface graphique
        tk.Label(frame, text="Simulation de l'enfoncement", font=("Arial", 16)).pack(pady=10)
        self.label_valeur = tk.Label(frame, text="Valeur actuelle: 0.0 m", font=("Arial", 14))
        self.label_valeur.pack(pady=10)

        self.progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate", maximum=1.0, variable=self.enfoncement_valeur)
        self.progress.pack(pady=20)

        tk.Button(frame, text="Démarrer", command=self.start_auto_enfoncement, font=("Arial", 14), bg="blue", fg="white").pack(pady=5)
        tk.Button(frame, text="Pause", command=self.toggle_pause, font=("Arial", 14), bg="yellow", fg="black").pack(pady=5)
        tk.Button(frame, text="Réinitialiser", command=self.reset_enfoncement, font=("Arial", 14), bg="red", fg="white").pack(pady=5)

    def auto_enfoncement(self):
        for i in range(101):
            if not self.enfoncement_en_cours:
                break
            while self.pause:
                time.sleep(0.1)
            self.enfoncement_valeur.set(i / 100)
            self.label_valeur.config(text=f"Valeur actuelle: {i / 100:.2f} m")
            self.frame.update()
            time.sleep(0.05)

        if self.enfoncement_en_cours:
            messagebox.showinfo("Piquet enfoncé", "Le trou est d'1 mètre.")
            for i in range(100, -1, -1):
                if not self.enfoncement_en_cours:
                    break
                while self.pause:
                    time.sleep(0.1)
                self.enfoncement_valeur.set(i / 100)
                self.label_valeur.config(text=f"Valeur actuelle: {i / 100:.2f} m")
                self.frame.update()
                time.sleep(0.05)

    def start_auto_enfoncement(self):
        if not self.enfoncement_en_cours:
            self.enfoncement_en_cours = True
            threading.Thread(target=self.auto_enfoncement).start()

    def toggle_pause(self):
        self.pause = not self.pause

    def reset_enfoncement(self):
        self.enfoncement_en_cours = False
        self.pause = False
        self.enfoncement_valeur.set(0.0)
        self.label_valeur.config(text="Valeur actuelle: 0.0 m")

# Classe pour le compteur de piquets
class CompteurPiquets:
    def __init__(self, frame):
        self.frame = frame  # Ajouter cette ligne pour définir l'attribut frame
        self.diametre_roue = 0.6
        self.circumference_roue = np.pi * self.diametre_roue
        self.vitesse_m_s = 1
        self.distance_par_piquet = 5
        self.distance_parcourue = 0
        self.compteur_piquets = 0

        # Interface graphique avec Tkinter
        self.label_piquets = tk.Label(frame, text="Piquets posés: 0", font=("Arial", 14))
        self.label_piquets.pack(pady=10)

        self.label_vitesse = tk.Label(frame, text=f"Vitesse: {self.vitesse_m_s} m/s", font=("Arial", 14))
        self.label_vitesse.pack(pady=10)

        self.label_distance = tk.Label(frame, text=f"Distance par piquet: {self.distance_par_piquet} m", font=("Arial", 14))
        self.label_distance.pack(pady=10)

        self.progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate", maximum=self.circumference_roue)
        self.progress.pack(pady=20)

        # Sliders pour ajuster la vitesse et la distance
        self.slider_vitesse = ttk.Scale(frame, from_=0, to=7, orient="horizontal", command=self.update_vitesse)
        self.slider_vitesse.set(self.vitesse_m_s)
        self.slider_vitesse.pack(pady=5)

        self.slider_distance = ttk.Scale(frame, from_=1, to=10, orient="horizontal", command=self.update_distance)
        self.slider_distance.set(self.distance_par_piquet)
        self.slider_distance.pack(pady=5)

        # Démarrer le calcul du compteur de piquets
        self.update_compteur()

    def update_vitesse(self, val):
        self.vitesse_m_s = float(val)
        self.label_vitesse.config(text=f"Vitesse: {self.vitesse_m_s} m/s")

    def update_distance(self, val):
        self.distance_par_piquet = float(val)
        self.label_distance.config(text=f"Distance par piquet: {self.distance_par_piquet} m")

    def update_compteur(self):
        # Calculer la distance parcourue en fonction de la vitesse
        self.distance_parcourue += self.vitesse_m_s * 0.05  # avance de 0.05s

        while self.distance_parcourue >= self.distance_par_piquet:
            self.compteur_piquets += 1
            self.distance_parcourue -= self.distance_par_piquet

        # Mettre à jour la barre de progression et le texte
        self.progress['value'] = self.distance_parcourue
        self.label_piquets.config(text=f"Piquets posés: {self.compteur_piquets}")

        # Appeler cette fonction toutes les 50ms pour animer le compteur
        self.frame.after(50, self.update_compteur)


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfacePrincipale(root)
    root.mainloop()
