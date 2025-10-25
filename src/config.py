"""
Configuration globale pour le projet Mini Weather Router.
Toutes les constantes/modifiables se trouvent ici.
"""

from pathlib import Path

# === Données météo ===
DATA_DIR = Path("./data/raw")  # dossier où sont stockés les fichiers GRIB
RUN_HOUR = "00"                 # Run GFS : 00, 06, 12, 18
FORECAST_HOURS = ["000", "006"] # Échéances à télécharger
RESOLUTION = "0p50"             # Résolution du modèle (0p25, 0p50, 1p00)

# === Domaine géographique ===
DOMAIN = {
    "lat_min": 35.0,
    "lat_max": 50.0,
    "lon_min": -35.0,
    "lon_max": 0.0,
}

# === Paramètres bateau / routage ===
BOAT_POLAR = {
    "close_hauled": 6.0,   # nœuds au près
    "beam_reach": 8.0,     # nœuds au bon plein
    "running": 7.0         # nœuds au portant
}

# === Autres paramètres ===
DEBUG = True

