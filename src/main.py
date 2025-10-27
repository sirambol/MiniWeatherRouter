import json
from config import DATA_DIR, RUN_HOUR, FORECAST_HOURS, RESOLUTION
from weather_dl import download_ecmwf_wind
from weather_reader import load_grib_file, subset_domain, extract_wind
from config import LAT_MIN, LAT_MAX, LON_MIN, LON_MAX
import xarray as xr
from visualization import plot_wind_map

def load_user_config(path: str = "user_config.json"):
    """
    Charge les paramètres user depuis JSON
    """
    try:
        with open(path) as f:
            cfg = json.load(f)
            return cfg
    except FileNotFoundError:
        print(f"{path} non trouvé, utilisation valeurs par défaut")
        return {}

def main():
    print("=== Mini Weather Router ===\n")

    # Télécharger grib
    print("Téléchargement des données ECMWF pour le vent...")
    grib_file = download_ecmwf_wind(
        start_date="2025-10-21",
        area=[LAT_MAX, LON_MIN, LAT_MIN, LON_MAX],
        out_dir="data/raw",
        filename="era5_wind_2025-10-21.grib"
    )
    print(f"Fichier téléchargé : {grib_file}\n")

    # Charger GRIB
    print("Lecture du fichier GRIB...")
    ds = load_grib_file(grib_file)
    print(ds)
    print("\n")

    # Restreindre au domaine souhaité
    print("Découpage du domaine...")
    ds_subset = subset_domain(ds, LAT_MIN, LAT_MAX, LON_MIN, LON_MAX)
    print(ds_subset)
    print("\n")

    # Extraire composantes du vent
    print("Extraction du vent (u, v, speed, direction)...")
    wind = extract_wind(ds_subset)

    # Résultats
    print("=== Résumé ===")
    print("Dimensions u10 :", wind['u'].shape)
    print("Latitudes :", wind['lat'].values)
    print("Longitudes :", wind['lon'].values)
    print("Vitesse du vent (m/s) :", wind['speed'].values)
    print("Direction du vent :", wind['direction'].values)

    print("\nDonnées prêtes pour l'algorithme de routage !")

    plot_wind_map(wind)
    

if __name__ == "__main__":
    main()
