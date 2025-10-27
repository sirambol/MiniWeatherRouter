import os
import requests
from datetime import datetime, timezone
from pathlib import Path
from typing import List
import cdsapi

def download_ecmwf_wind(
        start_date: str = None,
        end_date: str = None,
        area: List[float] = None,
        out_dir: str = "data/raw",
        filename: str = "ecmwf_wind.grib"
) -> Path:
    """
    Télécharge les données de vent ECMWF via CDSAPI (ERA5, 10m u/v).

    Args:
        start_date (str): Date début ('YYYY-MM-DD'). Par défaut = aujourd'hui.
        end_date (str): Date fin. Par défaut = start_date.
        area (List[float]): [North, West, South, East]. Par défaut = zone Atlantique Nord.
        out_dir (str): Répertoire de sauvegarde.
        filename (str): Nom du fichier de sortie.

    Returns:
        Path: Chemin vers le fichier téléchargé.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok = True)
    file_path = out_dir / filename

    if file_path.exists():
        print(f"Fichier déjà présent : {file_path}")
        return file_path
    
    if start_date is None:
        start_date = datetime.date.today().strftime("%Y-%m-%d")
    if end_date is None:
        end_date = start_date
    if area is None:
        # Zone Atlantique Nord approximative
        area = [50, -30, 35, -5]  # [N, W, S, E]

    c = cdsapi.Client()

    print(f"Téléchargement ECMWF ERA5 : {file_path}")
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'variable': ['10m_u_component_of_wind', '10m_v_component_of_wind'],
            'year': start_date[:4],
            'month': start_date[5:7],
            'day': start_date[8:10],
            'time': [
                '00:00', '06:00', '12:00', '18:00'
            ],
            'format': 'grib',
            'area': area
        },
        str(file_path)
    )
    print("Téléchargement terminé !")
    return file_path


def download_grib(url: str, save_dir: str = "data/raw") -> Path:
    """
    Télécharge un fichier GRIB depuis une URL et le sauvegarde localement.

    Args:
        url (str): URL du fichier GRIB.
        save_dir (str): Répertoire où sauvegarder le fichier. Créé si inexistant.

    Returns:
        Path: Chemin vers le fichier téléchargé.
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    filename = url.split("/")[-1]
    file_path = save_dir / filename

    print(f"Téléchargement de {url} vers {file_path} ...")

    with requests.get(url, stream=True) as r:
        r.raise_for_status()  # lève une erreur si le téléchargement échoue
        total_size = int(r.headers.get('content-length', 0))
        chunk_size = 1024 * 1024  # 1 MB

        with open(file_path, 'wb') as f:
            downloaded = 0
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:  # filtre les keep-alive
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = downloaded / total_size * 100 if total_size else 0
                    print(f"\rTéléchargé: {percent:.1f}%", end="")

    print("\nTéléchargement terminé !")
    return file_path

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
    paths = download_ecmwf_wind()
    print("Fichiers disponibles :", paths)
