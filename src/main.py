import json
from pathlib import Path
from weather_dl import download_gfs_data
from config import DATA_DIR, RUN_HOUR, FORECAST_HOURS, RESOLUTION
from weather_reader import load_grib_file, load_multiple_gribs

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
    """
    Entry point for Mini Weather Router
    Télécharge fichier grib
    """

    """     print("Initialisation des données")
    user_cfg = load_user_config()

    run_hour = user_cfg.get("run_hour", RUN_HOUR)
    forecast_hours = user_cfg.get("forecast_hours", FORECAST_HOURS)
    resolution = user_cfg.get("resolution", RESOLUTION)

    # Téléchargement des fichiers GRIB
    paths = download_gfs_data(
        run_hour=run_hour,         
        forecast_hours=forecast_hours,
        resolution=resolution,
        out_dir=DATA_DIR
    )

    print("Téléchargements effectués:")
    for p in paths:
        print(" -", p) """

    """     
    ds = load_grib_file("./data/raw/gfs.t06z.pgrb2.0p25.f006")
    print(ds) 
    """

    paths = [
    "data/raw/gfs.t06z.pgrb2.0p25.f006",
    "data/raw/gfs.t06z.pgrb2.0p25.f012",
    "data/raw/gfs.t06z.pgrb2.0p25.f018"
]

    ds_multi = load_multiple_gribs(paths, fields=["u10","v10"], step_type="instant")
    print(ds_multi)



if __name__ == "__main__":
    main()