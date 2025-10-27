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
    ax.set_title("Vent à 10m - Intensité et direction\nPrévision: {forecast_time}", fontsize=16)

    # Ajouter une colorbar
    norm = mpl.colors.Normalize(vmin=np.min(speed), vmax=np.max(speed))
    sm = mpl.cm.ScalarMappable(cmap='coolwarm', norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical', pad=0.05, aspect=30)
    cbar.set_label("Vitesse du vent (m/s)")

    plt.show()