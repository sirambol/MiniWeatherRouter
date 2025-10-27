import numpy as np

def boat_speed(angle_deg: float) -> float:
    """
    Polaire simplifiée : vitesse du bateau selon l'angle du vent apparent
    angle_deg : angle vent → bateau (0=vent de face, 180=vent arrière)
    Retour : vitesse du bateau en noeuds
    """
    if angle_deg < 0:  # normaliser
        angle_deg += 360
    if 0 <= angle_deg <= 30:
        return 0.0  # près du vent
    elif 30 < angle_deg <= 60:
        return 4.0  # près
    elif 60 < angle_deg <= 100:
        return 6.0  # travers 
    elif 100 < angle_deg <= 140:
        return 7.0  # largue
    elif 140 < angle_deg <= 165:
        return 8.0  # portant (spi)
    elif 165 < angle_deg <= 180:
        return 6.0  # vent arrière
    else:
        # symétrie
        return boat_speed(360 - angle_deg)
