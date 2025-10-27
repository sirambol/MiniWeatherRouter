import json
from config import DATA_DIR, RUN_HOUR, FORECAST_HOURS, RESOLUTION
from weather_dl import download_ecmwf_wind
from weather_reader import load_grib_file, subset_domain, extract_wind
from config import LAT_MIN, LAT_MAX, LON_MIN, LON_MAX
import xarray as xr
from visualization import plot_wind_map, plot_wind_map_with_route, plot_wind_and_route
from routing import build_graph, create_grid, compute_route_metrics_simple
import networkx as nx
from utils import find_closest_node
from boat_model import boat_speed

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

    #plot_wind_map(wind)

    ### Routage
    # Créer la grille
    lat2d, lon2d = create_grid(LAT_MIN, LAT_MAX, LON_MIN, LON_MAX, resolution=1.0)

    # Extraire les composantes du vent
    wind = extract_wind(ds_subset)
    u_wind = wind['u'].values[0,:,:]  # premier pas de temps
    v_wind = wind['v'].values[0,:,:]

    # Construire le graphe
    G = build_graph(lat2d, lon2d, u_wind, v_wind)
    print(f"Graphe créé avec {G.number_of_nodes()} noeuds et {G.number_of_edges()} arêtes")

    # Route la plus courte Dijkstra

    # Points de départ/arrivée
    start_lat, start_lon = 46.5, -1.8   # Les Sables d’Olonne
    end_lat, end_lon = 38.5, -28.6      # Horta, Açores

    start_node = find_closest_node(lat2d, lon2d, start_lat, start_lon)
    end_node = find_closest_node(lat2d, lon2d, end_lat, end_lon)

    # Calcul du chemin le plus rapide
    path = nx.dijkstra_path(G, source=start_node, target=end_node, weight='weight')
    total_time = nx.dijkstra_path_length(G, source=start_node, target=end_node, weight='weight')

    print(f"Chemin trouvé avec {len(path)} étapes, temps total estimé : {total_time:.1f} h")

    path_lats = [lat2d[i,j] for i,j in path]
    path_lons = [lon2d[i,j] for i,j in path]

    speeds, angles, course_deg_list, wind_speed_list, wind_dir_list, u_loc_list, v_loc_list = compute_route_metrics_simple(path, lat2d, lon2d, u_wind, v_wind, boat_speed)

    for idx, (lat, lon, spd, ang, course, w_speed, w_dir, u_loc, v_loc) in enumerate(zip(path_lats, path_lons, speeds, angles, course_deg_list, wind_speed_list, wind_dir_list, u_loc_list, v_loc_list)):
        print(f"Point {idx}: lat={lat:.2f}, lon={lon:.2f}, "
          f"v_bateau={spd:.1f} nds, angle_vent={ang:.1f}°, "
          f"cap={course:.1f}°, vent={w_speed:.1f} m/s à {w_dir:.1f}°, "
          f"vent_u = {u_loc:.1f}, vent_v={v_loc:.1f}")


    #plot_wind_map_with_route(wind, path_lats, path_lons)
    plot_wind_and_route(
        wind=wind,
        path_lats=path_lats,
        path_lons=path_lons,
        u_path = u_loc_list,
        v_path = v_loc_list
    )

if __name__ == "__main__":
    main()
