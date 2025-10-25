import json
from pathlib import Path
from weather_dl import download_gfs_data
from config import DATA_DIR, RUN_HOUR, FORECAST_HOURS, RESOLUTION

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

    print("Initialisation des données")
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
        print(" -", p)

if __name__ == "__main__":
    main()