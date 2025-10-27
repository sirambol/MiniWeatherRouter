# visualization_example.py
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

def plot_wind_map(wind):
    """
    Affiche les données de vent sur une carte style SHOM :
    - Terre jaune, mer bleu
    - Vent sous forme de flèches proportionnelles à l'intensité et orientées selon la direction
    """

    u = wind['u'].values[0,:,:] if wind['u'].ndim == 3 else wind['u'].values
    v = wind['v'].values[0,:,:] if wind['v'].ndim == 3 else wind['v'].values
    lat = wind['lat'].values
    lon = wind['lon'].values
    lon2d, lat2d = np.meshgrid(lon, lat)
    speed = wind['speed'].values[0,:,:] if wind['speed'].ndim == 3 else wind['speed'].values

    # Date de la prévision
    if 'time' in wind['u'].dims:
        forecast_time = np.datetime_as_string(wind['u']['time'].values[0], unit='h')
    else:
        forecast_time = "Date inconnue"

    # Créer la figure
    fig = plt.figure(figsize=(12,10))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Ajouter la mer et la terre
    ax.add_feature(cfeature.LAND, facecolor='lightyellow')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.coastlines(resolution='10m')

    # Grille pour les flèches
    skip = (slice(None, None, 5), slice(None, None, 5))  # flèches toutes les 5 cases pour lisibilité

    colors = ["green", "yellow", "red", "purple"]
    cmap_custom = mpl.colors.LinearSegmentedColormap.from_list("wind_cmap", colors)


    # Flèches de vent (u et v) sur la grille
    q = ax.quiver(
        lon2d[skip], lat2d[skip],
        u[skip], v[skip],
        speed[skip],              # couleur selon intensité
        scale=500,                 # ajuster la taille des flèches
        cmap=cmap_custom,
        width=0.002,
        transform=ccrs.PlateCarree()
    )

    # Ajouter un titre
    ax.set_title(f"Vent à 10m - Intensité et direction\nPrévision: {forecast_time}", fontsize=16)

    # Ajouter une colorbar
    norm = mpl.colors.Normalize(vmin=np.min(speed), vmax=np.max(speed))
    sm = mpl.cm.ScalarMappable(cmap=cmap_custom, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical', pad=0.05, aspect=30)
    cbar.set_label("Vitesse du vent (m/s)")

    plt.show()

def plot_wind_map_with_route(wind, path_lats=None, path_lons=None):
    import numpy as np
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import matplotlib as mpl

    u = wind['u'].values[0,:,:] if wind['u'].ndim == 3 else wind['u'].values
    v = wind['v'].values[0,:,:] if wind['v'].ndim == 3 else wind['v'].values
    speed = wind['speed'].values[0,:,:] if wind['speed'].ndim == 3 else wind['speed'].values

    lat_1d = wind['lat'].values
    lon_1d = wind['lon'].values

    if 'time' in wind['u'].dims:
        forecast_time = np.datetime_as_string(wind['u']['time'].values[0], unit='h')
    else:
        forecast_time = "Date inconnue"

    lon2d, lat2d = np.meshgrid(lon_1d, lat_1d)

    fig = plt.figure(figsize=(12,10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, facecolor='lightyellow')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.coastlines(resolution='10m')

    skip = (slice(None, None, 5), slice(None, None, 5))
    colors = ["green", "yellow", "red", "purple"]
    cmap_custom = mpl.colors.LinearSegmentedColormap.from_list("wind_cmap", colors)

    q = ax.quiver(
        lon2d[skip], lat2d[skip],
        u[skip], v[skip],
        speed[skip],
        scale=500,
        cmap=cmap_custom,
        width=0.002,
        transform=ccrs.PlateCarree()
    )

    # Colorbar
    norm = mpl.colors.Normalize(vmin=np.min(speed), vmax=np.max(speed))
    sm = mpl.cm.ScalarMappable(cmap=cmap_custom, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical', pad=0.05, aspect=30)
    cbar.set_label("Vitesse du vent (m/s)")

    # Ajouter le chemin
    if path_lats is not None and path_lons is not None:
        ax.plot(path_lons, path_lats, color='blue', linewidth=2, marker='o', markersize=3,
                label='Route optimale')

    ax.set_title(f"Vent à 10m - Route optimale\nPrévision : {forecast_time}", fontsize=16)
    ax.legend()

    plt.show()


def plot_route_with_wind(path, lat2d, lon2d, u_wind, v_wind, path_lats, path_lons):
    """
    Affiche la route optimale et les vents locaux (flèches noires).
    """
    # On récupère les composantes du vent aux points du chemin
    u_route = np.array([u_wind[i, j] for i, j in path])
    v_route = np.array([v_wind[i, j] for i, j in path])

    # Création de la figure avec projection PlateCarree
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(10, 6))
    ax.set_title("Route optimale et vents locaux", fontsize=14)

    # Fond de carte façon SHOM
    ax.coastlines(resolution='50m')
    ax.add_feature(cfeature.LAND, facecolor='khaki', edgecolor='black')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')

    # Route optimale (en rouge)
    ax.plot(path_lons, path_lats, color='red', linewidth=2, marker='o', transform=ccrs.PlateCarree(), label='Route optimale')

    # Flèches du vent (en noir)
    ax.quiver(
        path_lons, path_lats, u_route, v_route,
        transform=ccrs.PlateCarree(),
        color='black', scale=80, width=0.004,
        label='Vent local'
    )

    ax.legend()
    plt.show()


def plot_wind_and_route(wind, path_lats, path_lons, u_path, v_path):
    """
    Affiche :
    La carte globale des vents (en haut)
    La route optimale avec les vents locaux (en bas)
    """
    # On récupère u, v et on calcule la vitesse du vent
    u = wind["u"].values[0, :, :] if wind["u"].ndim == 3 else wind["u"].values
    v = wind["v"].values[0, :, :] if wind["v"].ndim == 3 else wind["v"].values
    wind_speed = np.sqrt(u**2 + v**2)

    lat_1d = wind['lat'].values
    lon_1d = wind['lon'].values

    if 'time' in wind['u'].dims:
        forecast_time = np.datetime_as_string(wind['u']['time'].values[0], unit='h')
    else:
        forecast_time = "Date inconnue"

    lon2d, lat2d = np.meshgrid(lon_1d, lat_1d)

    # Création de la figure avec deux sous-cartes
    fig, axes = plt.subplots(
        2, 1,
        figsize=(12, 10),
        subplot_kw={'projection': ccrs.PlateCarree()},
        constrained_layout=True
    )

    # -------------------------------------------------------
    # CARTE GLOBALE DU VENT
    # -------------------------------------------------------
    ax = axes[0]
    ax.set_title("Carte des vents (champ GRIB)", fontsize=14)
    ax.coastlines(resolution='50m')
    ax.add_feature(cfeature.LAND, facecolor='khaki', edgecolor='black')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')

    # Champ de vent (couleur = intensité)
    im = ax.pcolormesh(lon2d, lat2d, wind_speed, cmap="plasma", shading="auto", transform=ccrs.PlateCarree())
    skip = (slice(None, None, 5), slice(None, None, 5))  # échantillonnage des flèches
    ax.quiver(lon2d[skip], lat2d[skip], -u[skip], -v[skip],
              transform=ccrs.PlateCarree(), color='black', scale=500, width=0.002)
    plt.colorbar(im, ax=ax, orientation='vertical', label="Vitesse du vent (m/s)")

    # -------------------------------------------------------
    # ROUTE OPTIMALE AVEC VENTS LOCAUX
    # -------------------------------------------------------
    ax2 = axes[1]
    ax2.set_title("Route optimale et vents locaux", fontsize=14)
    ax2.coastlines(resolution='50m')
    ax2.add_feature(cfeature.LAND, facecolor='khaki', edgecolor='black')
    ax2.add_feature(cfeature.OCEAN, facecolor='lightblue')

    # Route (en rouge)
    ax2.plot(path_lons, path_lats, color='red', linewidth=2, marker='o',
             transform=ccrs.PlateCarree(), label='Route optimale')

    # Flèches noires du vent local
    ax2.quiver(path_lons, path_lats, u_path, v_path,
               transform=ccrs.PlateCarree(),
               color='black', scale=250, width=0.004, label='Vent local')

    ax2.legend(loc="lower right")

    plt.show()
