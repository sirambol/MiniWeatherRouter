def boat_speed(angle_deg: float, w_speed: float) -> float:
    """
    Polaire simplifiée : vitesse du bateau selon l'angle du vent apparent
    angle_deg : angle vent-bateau (0=vent de face, 180=vent arrière)
    Retour : vitesse (noeuds)
    """
    if angle_deg < 0:  # normaliser
        angle_deg += 360
    if 0 <= angle_deg <= 30:
        return 0.0  # près du vent
    elif 30 < angle_deg <= 60:
        return 1/3.0*w_speed  # près
    elif 60 < angle_deg <= 100:
        return 1/2.0*w_speed  # travers 
    elif 100 < angle_deg <= 140:
        return 2/3.0*w_speed  # largue
    elif 140 < angle_deg <= 165:
        return 4/5.0*w_speed  # portant (spi)
    elif 165 < angle_deg <= 180:
        return 3/5.0*w_speed  # vent arrière
    else:
        # symétrie
        return boat_speed(360 - angle_deg, w_speed)
