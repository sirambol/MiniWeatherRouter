"""
weather_reader.py

Module pour charger les fichiers GRIB et préparer les données de vent
(u10, v10) sur une grille pour le routage.
"""

import xarray as xr
from pathlib import Path
import numpy as np

# === Fonctions principales ===

def load_grib_file(path: str, fields: list = ["u10", "v10"]) -> xr.Dataset:
    """
    Charge un fichier GRIB en xarray.Dataset.

    Args:
        path (str): chemin vers le fichier GRIB.
        fields (list): liste des variables à charger, par défaut ['u10','v10'].

    Returns:
        xr.Dataset: dataset contenant les champs spécifiés et les coordonnées lat/lon.
    """
    pass  # implémentation à venir


def load_multiple_gribs(paths: list, fields: list = ["u10", "v10"]) -> xr.Dataset:
    """
    Charge et combine plusieurs fichiers GRIB le long de la dimension time.

    Args:
        paths (list): liste de chemins vers les fichiers GRIB.
        fields (list): variables à charger.

    Returns:
        xr.Dataset: dataset combiné avec dimension 'time' pour chaque échéance.
    """
    pass  # implémentation à venir


def subset_domain(ds: xr.Dataset, lat_min: float, lat_max: float,
                  lon_min: float, lon_max: float) -> xr.Dataset:
    """
    Découpe le dataset pour ne garder qu’une sous-région géographique.

    Args:
        ds (xr.Dataset): dataset complet.
        lat_min, lat_max, lon_min, lon_max (float): limites du domaine.

    Returns:
        xr.Dataset: dataset limité au domaine spécifié.
    """
    pass  # implémentation à venir


def extract_wind(ds: xr.Dataset) -> dict:
    """
    Extrait les composantes du vent et éventuellement la vitesse et la direction.

    Args:
        ds (xr.Dataset): dataset contenant les variables u10 et v10.

    Returns:
        dict: {
            'u': xr.DataArray,
            'v': xr.DataArray,
            'lat': xr.DataArray,
            'lon': xr.DataArray,
            'speed': xr.DataArray (optionnel),
            'direction': xr.DataArray (optionnel)
        }
    """
    pass  # implémentation à venir


def compute_wind_speed_direction(u: xr.DataArray, v: xr.DataArray) -> tuple:
    """
    Calcule la vitesse et la direction du vent à partir des composantes u et v.

    Args:
        u (xr.DataArray): composante zonale (Ouest-Est).
        v (xr.DataArray): composante méridienne (Sud-Nord).

    Returns:
        tuple: (speed: xr.DataArray, direction: xr.DataArray)
    """
    pass  # implémentation à venir
