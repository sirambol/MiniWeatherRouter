import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    """
    Distance entre deux points (lat/lon) en km
    """
    R = 6371.0  # rayon de la Terre en km
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)

    a = np.sin(dphi/2.0)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlambda/2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c/1.852

def find_closest_node(lat2d, lon2d, lat_pt, lon_pt):
    """
    Retourne l'indice (i,j) du noeud le plus proche d'un point (lat_pt, lon_pt)
    """
    dist2 = (lat2d - lat_pt)**2 + (lon2d - lon_pt)**2
    i,j = np.unravel_index(np.argmin(dist2), lat2d.shape)
    return (i,j)

