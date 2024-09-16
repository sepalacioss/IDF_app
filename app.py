# -*- coding: utf-8 -*-
"""
Sebastian Palacios
Análisis de la incertidumbre en procesos de construcción de IDF con llenado de
datos de precipitación y gestadística para la interpolación de los datos
"""
from sodapy import Socrata
import hvplot.pandas
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import folium
import geopandas as gpd
from shapely.geometry import Point


st.set_page_config(page_title="Resultados")

st.sidebar.markdown(
'''
# Elaboración de curvas IDF usando métodos estocásticos y comparación de la incertidumbre
___

A partir de la zona de estudio definida (Cuenca del rio las Ceibas), se obtienen las estaciones que se encuentran dentro del poligono aferente para la construccion de las curvas IDF de cada estacion usando las diferentes ecuaciones referenciadas en el articulo entregable


''')

st.markdown('''
    # Zona de Estudio
    ## Cuenca del río Las Ceibas
    ''')

shp = gpd.read_file("ShapefileCuenca/Cuenca.shp")
map_ = folium.Map(location=[shp.geometry.centroid.y.mean(), shp.geometry.centroid.x.mean()], zoom_start=12)
folium.GeoJson(shp).add_to(map_)
st_data = st_folium(map_,width=750)


st.markdown(
'''
___
## Identificación de las estaciones climatológicas en la zona de estudio
Para identificar las estaciones existentes en la zona de estudio del proyecto se obtienen a partir de la información del IDEAM            
''')

df_cat = pd.read_excel("CNE_IDEAM.xls")
geometry = [Point(lon, lat) for lon, lat in zip(df_cat['Longitud'], df_cat['Latitud'])]
gdf = gpd.GeoDataFrame(df_cat, geometry=geometry, crs='EPSG:4326')
outside_boundary = gpd.sjoin(gdf, shp, how='left', predicate='within')
outside_points_index = outside_boundary[outside_boundary['index_right'].isnull()].index
cleaned_gdf = gdf.drop(outside_points_index)
cleaned_df = cleaned_gdf[['Código','Nombre','Categoría','Latitud','Longitud','Altitud']]
cleaned_df

marker_icons = {'Pluviográfica': 'blue', 'Limnimétrica': 'green', 'Climática Principal': 'red'}

def plot_station(row):
    html = row.to_frame("Estaciones dentro de la Cuenca del Río Las Ceibas").to_html(classes="table table-striped table-hover table-condensed table-responsive")
    popup = folium.Popup(html, max_width=1000)
    category = row['Categoría']
    icon_color = marker_icons.get(category, 'gray')
    folium.Marker(location=[row.Latitud, row.Longitud],
                  icon=folium.Icon(color=icon_color),
                  popup=popup).add_to(map_)

map_ = folium.Map(location=[shp.geometry.centroid.y.mean(), shp.geometry.centroid.x.mean()], zoom_start=12)
folium.GeoJson(shp).add_to(map_)
cleaned_df.apply(plot_station,axis=1)

st_data = st_folium(map_,width=750)

col1,col2 = st.columns(2)
with col1:
    st.image("Categorias_legenda.png")
with col2:
    st.markdown("""
Las estaciones pluviográficas dentro de la cuenca del río Las Ceibas serán consultadas y sus series de tiempo serán graficadas a continuación \n

La estación Climática Principal también reporta información de precipitación.
""")

st.markdown("""___
### Información reportada
Las series de tiempo reportadas por las estaciones consultadas se encuentran graficadas a continuación
""")

AppToken = "BCSpYJsEcMNQtlN5flEoApTw2"
client = Socrata("www.datos.gov.co",
                 AppToken,
                 username="promerol@unal.edu.co",
                 password="24/2Kobe&Gigi")

MEDICIONES = []

for estacion in cleaned_df['Código']:
    ppt_query = client.get(
        dataset_identifier="s54a-sgyg",
        select="fechaobservacion, valorobservado, codigoestacion, nombreestacion",
        where=f"codigoestacion IN ('00{estacion}')",
    )
    df_est = pd.DataFrame.from_records(ppt_query)
    MEDICIONES.append(df_est)

df = pd.concat(MEDICIONES)
df['fechaobservacion'] = pd.to_datetime(df["fechaobservacion"])

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots()
sns.lineplot(data = df, x = 'fechaobservacion', y = 'valorobservado' ,
              hue='nombreestacion', ax = ax)
ax.set_title('Precipitación reportada por las estaciones')
ax.set_ylabel('Precipitación [mm]')

st.pyplot(fig)

st.markdown('''
----
# Para visualizar los resultados obtenidos al descargar toda la información de las estaciones, revisar la sección "Selección de estación" en el costado superior izquierdo

''')

