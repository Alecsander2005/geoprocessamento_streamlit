
import json
import math
import random
from pathlib import Path

import folium
import streamlit as st
from shapely.geometry import Point, Polygon, mapping
from streamlit_folium import st_folium


st.set_page_config(
    page_title="GeoProcessamento",
    page_icon="🗺️",
    layout="wide",
)

OUTPUT_DIR = Path("dados_gerados")
OUTPUT_DIR.mkdir(exist_ok=True)


def random_point(center_lat, center_lon, radius_km):
    """Gera um ponto aleatório dentro de um raio aproximado."""
    radius_deg_lat = radius_km / 111.32
    radius_deg_lon = radius_km / (111.32 * max(math.cos(math.radians(center_lat)), 0.01))

    angle = random.uniform(0, 2 * math.pi)
    distance = math.sqrt(random.uniform(0, 1))

    lat = center_lat + math.sin(angle) * distance * radius_deg_lat
    lon = center_lon + math.cos(angle) * distance * radius_deg_lon

    return lat, lon


def create_points(count, center_lat, center_lon, radius_km):
    features = []

    for i in range(1, count + 1):
        lat, lon = random_point(center_lat, center_lon, radius_km)

        point = Point(lon, lat)

        feature = {
            "type": "Feature",
            "geometry": mapping(point),
            "properties": {
                "id": i,
                "nome": f"Ponto {i}",
                "categoria": random.choice(
                    ["Residencial", "Comercial", "Industrial", "Rural"]
                ),
                "valor": round(random.uniform(1000, 500000), 2),
                "populacao": random.randint(50, 10000),
            },
        }

        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features,
    }


def create_polygons(count, center_lat, center_lon, radius_km):
    features = []

    for i in range(1, count + 1):
        lat, lon = random_point(center_lat, center_lon, radius_km)

        size = random.uniform(0.002, 0.008)

        coordinates = [
            [lon - size, lat - size],
            [lon + size, lat - size],
            [lon + size, lat + size],
            [lon - size, lat + size],
            [lon - size, lat - size],
        ]

        polygon = Polygon(coordinates)

        feature = {
            "type": "Feature",
            "geometry": mapping(polygon),
            "properties": {
                "id": i,
                "nome": f"Área {i}",
                "categoria": random.choice(
                    ["Zona A", "Zona B", "Zona C", "Zona D"]
                ),
                "area_estimada_m2": random.randint(500, 50000),
                "populacao": random.randint(100, 15000),
            },
        }

        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features,
    }


def save_geojson(data):
    file_path = OUTPUT_DIR / "dados_geoprocessamento.geojson"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    return file_path


def create_map(data, center_lat, center_lon):
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        control_scale=True,
    )

    for feature in data["features"]:
        geometry_type = feature["geometry"]["type"]
        properties = feature["properties"]

        popup_html = "<b>Dados geográficos</b><br>"
        for key, value in properties.items():
            popup_html += f"<b>{key}:</b> {value}<br>"

        if geometry_type == "Point":
            lon, lat = feature["geometry"]["coordinates"]

            folium.CircleMarker(
                location=[lat, lon],
                radius=6,
                popup=folium.Popup(popup_html, max_width=350),
                tooltip=properties.get("nome", "Ponto"),
                fill=True,
            ).add_to(m)

        elif geometry_type == "Polygon":
            coords = feature["geometry"]["coordinates"][0]
            lat_lon = [[lat, lon] for lon, lat in coords]

            folium.Polygon(
                locations=lat_lon,
                popup=folium.Popup(popup_html, max_width=350),
                tooltip=properties.get("nome", "Área"),
                fill=True,
            ).add_to(m)

    return m


st.title("🗺️ Gerador de Dados de Geoprocessamento")
st.caption("Gere dados espaciais, exporte em GeoJSON e visualize tudo no mapa.")

with st.sidebar:
    st.header("Configuração")

    geometry_type = st.selectbox(
        "Tipo de geometria",
        ["Pontos", "Polígonos"],
    )

    count = st.number_input(
        "Quantidade de registros",
        min_value=1,
        max_value=10000,
        value=100,
        step=10,
    )

    st.subheader("Localização")

    center_lat = st.number_input(
        "Latitude central",
        value=-7.1195,
        format="%.6f",
    )

    center_lon = st.number_input(
        "Longitude central",
        value=-34.8450,
        format="%.6f",
    )

    radius_km = st.slider(
        "Raio de geração (km)",
        min_value=1.0,
        max_value=100.0,
        value=20.0,
        step=1.0,
    )

    generate = st.button(
        "🚀 Gerar dados",
        use_container_width=True,
        type="primary",
    )


if generate:
    if geometry_type == "Pontos":
        geojson_data = create_points(
            count,
            center_lat,
            center_lon,
            radius_km,
        )
    else:
        geojson_data = create_polygons(
            count,
            center_lat,
            center_lon,
            radius_km,
        )

    st.session_state["geojson"] = geojson_data
    st.session_state["center"] = (center_lat, center_lon)

if "geojson" not in st.session_state:
    st.info("Configure os parâmetros no menu lateral e clique em **Gerar dados**.")
    st.stop()


geojson_data = st.session_state["geojson"]
map_center = st.session_state["center"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Registros", len(geojson_data["features"]))

with col2:
    st.metric("Formato", "GeoJSON")

with col3:
    st.metric("Geometrias", geojson_data["features"][0]["geometry"]["type"])


st.subheader("Visualização no mapa")

map_object = create_map(
    geojson_data,
    map_center[0],
    map_center[1],
)

st_folium(
    map_object,
    width=None,
    height=650,
    returned_objects=[],
)


st.subheader("Dados GeoJSON")

json_text = json.dumps(
    geojson_data,
    ensure_ascii=False,
    indent=2,
)

st.download_button(
    "⬇️ Baixar GeoJSON",
    data=json_text,
    file_name="dados_geoprocessamento.geojson",
    mime="application/geo+json",
)

with st.expander("Ver GeoJSON"):
    st.code(json_text, language="json")
