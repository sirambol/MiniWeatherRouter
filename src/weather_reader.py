"""
weather_reader.py

Module pour charger les fichiers GRIB et préparer les données de vent
(u10, v10) sur une grille pour le routage.
"""

import numpy as np
import xarray as xr
from pathlib import Path
from datetime import datetime, timezone
from typing import List


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
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Le fichier GRIB n'existe pas: {path}")
    
    try:
        ds = xr.open_dataset(
            path, 
            engine="cfgrib"
        )
        vars_to_keep = [v for v in fields if v in ds.variables]
        ds = ds[vars_to_keep]

        if 'time' not in ds.dims:
            if 'valid_time' in ds.variables:
                time_val = np.datetime64(ds['valid_time'].item())
            else:
                time_val = np.datetime64(datetime.now(timezone.utc))
            ds = ds.expand_dims(time=[time_val])

        return ds
    
    except Exception as e:
        raise RuntimeError(f"Erreur lors de la lecture du fichier GRIB {path}: {e}")
    


def load_multiple_gribs(paths: list, fields: list = ["u10","v10"]) -> xr.Dataset:
    """
    Charge et concatène plusieurs fichiers GRIB le long de la dimension 'time'.

    Args:
        paths (list): chemins vers les fichiers GRIB
        fields (list): variables à charger

    Returns:
        xr.Dataset
    """

    datasets = []

    for path in paths:
        ds = load_grib_file(path, fields=fields)
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

    lat_slice = slice(lat_max, lat_min) if ds[lat_name][0] > ds[lat_name][-1] else slice(lat_min, lat_max)
    lon_slice = slice(lon_min, lon_max)

    ds_subset = ds.sel(
        {lat_name: lat_slice,
         lon_name: lon_slice}
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