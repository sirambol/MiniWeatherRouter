"""
weather_reader.py

Module pour charger les fichiers GRIB et préparer les données de vent
(u10, v10) sur une grille pour le routage.
"""

import numpy as np
import xarray as xr
from pathlib import Path
from datetime import datetime, timezone


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
            time_val = datetime.now(timezone.utc)
        
        # Ajouter dimension time si nécessaire
        if 'time' not in ds.dims:
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
    lat_name = 'latitude' if 'latitude' in ds.coords else 'lat'
    lon_name = 'longitude' if 'longitude' in ds.coords else 'lon'

    ds_subset = ds.sel(
        {lat_name: slice(lat_min, lat_max),
         lon_name: slice(lon_min, lon_max)}
    )
    return ds_subset

def compute_wind_speed_direction(u: xr.DataArray, v: xr.DataArray) -> tuple:
    """
    Calcule la vitesse et la direction du vent à partir des composantes u et v.
    """
    speed = np.sqrt(u**2 + v**2)
    # direction : angle du vent d’où il vient (en degrés, 0=Nord, 90=Est)
    direction = (np.arctan2(u, v) * 180 / np.pi) % 360
    return speed, direction


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
    if 'u10' not in ds.variables or 'v10' not in ds.variables:
        raise ValueError("Les variables u10 et v10 doivent être présentes dans le dataset.")

    u = ds['u10']
    v = ds['v10']
    speed, direction = compute_wind_speed_direction(u, v)

    # Ajuster les noms des coordonnées
    lat_name = 'latitude' if 'latitude' in ds.coords else 'lat'
    lon_name = 'longitude' if 'longitude' in ds.coords else 'lon'

    return {
        'u': u,
        'v': v,
        'lat': ds[lat_name],
        'lon': ds[lon_name],
        'speed': speed,
        'direction': direction
    }