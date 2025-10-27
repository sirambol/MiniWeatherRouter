import numpy as np
import networkx as nx
from utils import haversine
from boat_model import boat_speed

def create_grid(lat_min, lat_max, lon_min, lon_max, resolution=1.0):
    """
    Crée une grille 2D pour la navigation.
    Args:
        lat_min, lat_max, lon_min, lon_max : limites du domaine
        resolution : pas en degrés
    Returns:
        lat2d, lon2d : grilles 2D de coordonnées
    """
    lats = np.arange(lat_min, lat_max + resolution, resolution)
    lons = np.arange(lon_min, lon_max + resolution, resolution)
    lon2d, lat2d = np.meshgrid(lons, lats)
    return lat2d, lon2d

def wind_angle_to_course(u, v, course_deg):
    """
    Calculer l'angle du vent relatif au bateau (en degrés)
    u, v : composantes du vent (m/s)
    course_deg : cap du bateau en degrés (0=nord, 90=est)
    Retour : angle du vent relatif (0=vent de face, 180=vent arrière)
    """
    # relevé origine vent
    wind_dir_deg = (np.arctan2(u, v) * 180 / np.pi+180) % 360
    # angle relatif
    angle = (wind_dir_deg - (course_deg)) % 360
    if angle > 180:
        angle = 360 - angle
    return angle

def build_graph(lat2d, lon2d, u_wind, v_wind, resolution_deg=1.0):
    """
    Crée un graphe NetworkX où les noeuds = cellules de la grille
    et les arêtes sont pondérées par le temps de trajet (en heures)
    """
    nlat, nlon = lat2d.shape
    G = nx.DiGraph()

    for i in range(nlat):
        for j in range(nlon):
            node = (i,j)
            G.add_node(node, lat=lat2d[i,j], lon=lon2d[i,j])

            # voisins 8-connectivité
            for di in [-1,0,1]:
                for dj in [-1,0,1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i+di, j+dj
                    if 0 <= ni < nlat and 0 <= nj < nlon:
                        # distance en milles nautiques
                        dist = haversine(lat2d[i,j], lon2d[i,j],
                                            lat2d[ni,nj], lon2d[ni,nj])

                        # direction du déplacement (cap en degrés)
                        dy = lat2d[ni,nj] - lat2d[i,j]
                        dx = lon2d[ni,nj] - lon2d[i,j]
                        course_deg = (np.degrees(np.arctan2(dx, dy))) % 360

                        # angle du vent relatif
                        angle_rel = wind_angle_to_course(u_wind[i,j], v_wind[i,j], course_deg)

                        # vitesse du bateau selon la polaire
                        speed = boat_speed(angle_rel, np.sqrt(u_wind[i,j]**2+ v_wind[i,j]**2))  # en noeuds

                        # temps de trajet (heures)
                        time_h = dist / speed if speed > 0 else np.inf

                        # ajouter l’arête
                        G.add_edge(node, (ni,nj), weight=time_h)
    return G


def compute_route_metrics_simple(path, lat2d, lon2d, u_wind, v_wind, boat_speed_fn):
    """
    Pour chaque noeud du chemin, calcule :
        - vitesse du bateau (noeuds)
        - angle relatif au vent (degrés)
    Utilise directement les valeurs u/v de la grille.
    """
    speeds = []
    angles = []
    course_deg_list = []
    wind_speed_list = []
    wind_dir_list = []
    u_local_list = []
    v_local_list = []

    for idx, (i,j) in enumerate(path):
        u_local = u_wind[i,j]
        v_local = v_wind[i,j]
        u_local_list.append(u_local)
        v_local_list.append(v_local)

        # Calcul du cap vers le prochain point
        if idx < len(path)-1:
            ni, nj = path[idx+1]
            dy = lat2d[ni,nj] - lat2d[i,j]
            dx = lon2d[ni,nj] - lon2d[i,j]
            course_deg = (np.degrees(np.arctan2(dx, dy))) % 360
        else:
            course_deg = 0  # dernier point

        angle_rel = wind_angle_to_course(u_local, v_local, course_deg)
        wind_speed = np.sqrt(u_local**2 + v_local**2)
        wind_dir = (np.arctan2(u_local, v_local) * 180/np.pi) % 360
        speed = boat_speed_fn(angle_rel, wind_speed)

        speeds.append(speed)
        angles.append(angle_rel)
        course_deg_list.append(course_deg)
        wind_speed_list.append(wind_speed)
        wind_dir_list.append(wind_dir)

    return speeds, angles, course_deg_list, wind_speed_list, wind_dir_list, u_local_list, v_local_list
