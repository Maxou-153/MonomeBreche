import random

# Classe principale Capteur
class Capteur:
    def __init__(self, nom, unite):
        self.nom = nom
        self.unite = unite

    def lire_valeur(self):
        # Méthode à surcharger dans chaque sous-classe
        raise NotImplementedError("Cette méthode doit être surchargée.")

# Classe pour les capteurs avec des valeurs continues
class CapteurContinu(Capteur):
    def __init__(self, nom, unite, min_valeur, max_valeur):
        super().__init__(nom, unite)
        self.min_valeur = min_valeur
        self.max_valeur = max_valeur

    def lire_valeur(self):
        # Retourne une valeur aléatoire dans la plage définie pour la simulation
        return round(random.uniform(self.min_valeur, self.max_valeur), 2)

# Classe pour les capteurs TOR (Tout Ou Rien)
class CapteurTOR(Capteur):
    def __init__(self, nom):
        super().__init__(nom, "TOR")

    def lire_valeur(self):
        # Simule un interrupteur (True ou False)
        return random.choice([True, False])

# Création des 13 capteurs
capteurs = [
    CapteurContinu("Vitesse de la prise de force", "tr/min", 0, 540),
    CapteurContinu("Débit d'huile", "m3/s", 0, 0.02),
    CapteurContinu("Pression d'huile", "Bar", 0, 250),
    CapteurContinu("Compte tour de roue pour espacement piquets", "tr", 0, 1000),
    CapteurContinu("Présence de piquets dans le guide", "Unité", 0, 50),
    CapteurContinu("Compteur de piquets quand chargement", "Unité", 0, 100),
    CapteurContinu("Gyroscope/Accéléromètre", "°", -90, 90),
    CapteurTOR("Fin de course pour guide"),
    CapteurTOR("Fin de course pour tarrière Z/X"),
    CapteurContinu("Vitesse rotation tarière", "tr/min", 0, 1000),
    CapteurContinu("Vitesse enfoncement tarière (pression)", "N", 0, 10000),
    CapteurContinu("Jauge dans le guide pour enfoncement", "cm", 0, 200),
    CapteurContinu("Pression sangle trémie", "Bar", 0, 10),
    CapteurContinu("Jauge capacité trémie", "%", 0, 100),
]

# Simulation pour lire la valeur des capteurs
def simuler_capteurs():
    for capteur in capteurs:
        valeur = capteur.lire_valeur()
        print(f"{capteur.nom} : {valeur} {capteur.unite}")

# Exécuter la simulation
simuler_capteurs()
