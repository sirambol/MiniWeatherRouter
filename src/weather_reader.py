"""
weather_reader.py

Module pour charger les fichiers GRIB et préparer les données de vent
(u10, v10) sur une grille pour le routage.
"""

import numpy as np
import xarray as xr
from pathlib import Path


# === Fonctions principales ===

def load_grib_file(path: str, fields: list = ["u10", "v10"], step_type: str = "instant") -> xr.Dataset:
    """
    Charge un fichier GRIB en xarray.Dataset.

    Args:
        path (str): chemin vers le fichier GRIB.
        fields (list): liste des variables à charger, par défaut ['u10','v10'].
        step_type (str): type de pas de temps ('instant', 'avg', 'accum').

    Returns:
        xr.Dataset: dataset contenant les champs spécifiés et les coordonnées lat/lon.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Le fichier GRIB n'existe pas: {path}")
    
    try:
        ds = xr.open_dataset(
            path, 
            engine="cfgrib", 
            filter_by_keys={'typeOfLevel': 'surface', 'stepType': 'instant'}
        )
        vars_to_keep = [v for v in fields if v in ds.variables]
        ds = ds[vars_to_keep]

        return ds
    
    except Exception as e:
        raise RuntimeError(f"Erreur lors de la lecture du fichier GRIB {path}: {e}")
    


def load_multiple_gribs(paths: list, fields: list = ["u10","v10"], step_type: str = "instant") -> xr.Dataset:
    datasets = []

    for path in paths:
        ds = load_grib_file(path, fields=fields, step_type=step_type)
        
        # Créer la dimension 'time' depuis valid_time si disponible
        if 'valid_time' in ds.variables:
            time_val = ds['valid_time'].item()
            
        elif 'forecast_time' in ds.variables:
            time_val = ds['forecast_time'].item()
        else:
            time_val = xr.DataArray([0], dims="time")  # fallback
        
        # Ajouter dimension time si nécessaire
        if 'time' not in ds.dims:
            print(time_val)
            ds = ds.expand_dims(time=time_val)

        datasets.append(ds)

    combined = xr.concat(datasets, dim="time")
    return combined


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
