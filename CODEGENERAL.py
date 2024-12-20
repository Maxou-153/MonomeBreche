import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import threading
import time
import random

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
        # Ne pas initialiser GyroscopeApp ici, cela concerne uniquement l'onglet Gyroscope.
        pass

    def init_gyroscope_tab(self, frame):
        GyroscopeApp(frame)

    def init_piquet_tab(self, frame):
        CompteurPiquets(frame)

    def init_verin_tab(self, frame):
        label = tk.Label(frame, text="Contrôle des Vérins", font=("Arial", 16))
        label.pack(pady=10)

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
