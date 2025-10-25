#!/bin/bash
# Télécharge un petit fichier GFS (vent 10m, analyse + prévision 6h)
# Domaine : Atlantique Nord (Les Sables → Açores)

mkdir -p ../data/raw

# Exemple : GFS 0.5° (10m wind, 2025-10-25 00Z)
date="20251025"
hour="00"

# URL NOAA NOMADS (GFS 0p50°)
base_url="https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.${date}/${hour}/atmos"
file="gfs.t${hour}z.pgrb2.0p50.f006"

echo "Downloading $file ..."
curl -O ${base_url}/${file}

mv ${file} ../data/raw/
echo "Saved to data/raw/${file}"

