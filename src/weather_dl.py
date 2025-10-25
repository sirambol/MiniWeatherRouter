import os
import requests
from datetime import datetime, timezone
from pathlib import Path
from typing import List

def download_gfs_data(
    date: str = None,
    run_hour: str = "00",
    forecast_hours: List[str] = None,
    resolution: str = "0p50",
    out_dir: str = "../data/raw"
) -> List[str]:
    """
    Télécharge un ou plusieurs fichiers GFS GRIB2 depuis NOAA NOMADS.

    Args:
        date (str): Date du run au format 'YYYYMMDD'. Par défaut = aujourd'hui UTC.
        run_hour (str): Heure du run ('00','06','12','18')
        forecast_hours (List[str]): Liste des échéances ('000','006',...)
        resolution (str): Résolution du modèle ('0p25','0p50','1p00')
        out_dir (str): Dossier de sortie
    Returns:
        List[str]: Liste des chemins des fichiers téléchargés
    """

    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y%m%d")

    if forecast_hours is None:
        forecast_hours = ["000", "006", "012", "018"]  # par défaut 4 premières échéances

    os.makedirs(out_dir, exist_ok=True)

    base_url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{date}/{run_hour}/atmos"
    downloaded_files = []

    for fhr in forecast_hours:
        filename = f"gfs.t{run_hour}z.pgrb2.{resolution}.f{fhr}"
        file_path = Path(out_dir) / filename

        if file_path.exists():
            print(f"Fichier déjà présent : {file_path}")
            downloaded_files.append(str(file_path))
            continue

        url = f"{base_url}/{filename}"
        print(f"Téléchargement : {filename}")
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Fichier enregistré : {file_path}")
            downloaded_files.append(str(file_path))
        except requests.RequestException as e:
            print(f"Erreur téléchargement {filename} : {e}")

    return downloaded_files


if __name__ == "__main__":
    # Exemple d'utilisation
    paths = download_gfs_data()
    print("Fichiers disponibles :", paths)
