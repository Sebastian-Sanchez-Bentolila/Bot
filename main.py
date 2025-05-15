# Librerías
import streamlit as st
import pytz
from datetime import datetime, timedelta
import pycountry
import plotly.express as px
import pandas as pd
from PIL import Image

# Configuración de la página
st.set_page_config(
    layout="centered",
    page_title="Explorador de Zonas Horarias",
    page_icon="🌍"
)

# --------- JavaScript para detectar el tema del sistema ----------
st.markdown("""
<script>
const detectDarkMode = () => {
    const isDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    window.parent.document.getElementById('stApp').setAttribute('data-theme', isDark ? 'dark' : 'light');
    return isDark;
};
const isDark = detectDarkMode();
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    window.parent.document.getElementById('stApp').setAttribute('data-theme', event.matches ? 'dark' : 'light');
});
</script>
""", unsafe_allow_html=True)

# --------- Paletas de colores ----------
# Paleta "Tierra y Tiempo" (modo claro)
light_theme = {
    "primary_color": "#6A994E",      # Verde musgo
    "secondary_color": "#BC4749",    # Rojo tierra
    "bg_color": "#F0EFEB",           # Fondo claro tierra
    "text_color": "#2B2D42",         # Gris oscuro
    "card_bg": "#FFFBE6",            # Fondo tarjetas tipo amanecer
    "border_color": "#D9D9D9",       # Gris neutro
}

# Paleta "Noche Estrellada" (modo oscuro)
dark_theme = {
    "primary_color": "#83C5BE",      # Verde agua claro
    "secondary_color": "#FFDDD2",    # Rosa claro
    "bg_color": "#1A1A2E",           # Azul oscuro profundo
    "text_color": "#E6E6E6",         # Gris claro
    "card_bg": "#16213E",            # Azul oscuro
    "border_color": "#4A4A4A",       # Gris oscuro
}

# --------- CSS dinámico basado en el tema ----------
st.markdown(f"""
    <style>
    body, .stApp {{
        background-color: {light_theme['bg_color']};
        color: {light_theme['text_color']};
        font-family: 'Segoe UI', sans-serif;
        transition: all 0.3s ease;
    }}
    .stApp[data-theme="dark"] {{
        background-color: {dark_theme['bg_color']};
        color: {dark_theme['text_color']};
    }}
    .main-title {{
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: {light_theme['primary_color']};
        font-weight: 700;
    }}
    .stApp[data-theme="dark"] .main-title {{
        color: {dark_theme['primary_color']};
    }}
    .subtitle {{
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        color: {light_theme['text_color']};
    }}
    .time-display {{
        font-size: 1.4rem;
        padding: 1rem;
        border-radius: 8px;
        background-color: {light_theme['card_bg']};
        margin: 1rem 0;
        border-left: 6px solid {light_theme['primary_color']};
        color: {light_theme['text_color']};
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    .stApp[data-theme="dark"] .time-display {{
        background-color: {dark_theme['card_bg']};
        border-left: 6px solid {dark_theme['primary_color']};
        color: {dark_theme['text_color']};
    }}
    .difference-display {{
        font-size: 1.3rem;
        padding: 1rem;
        border-radius: 8px;
        background-color: {light_theme['card_bg']};
        margin: 1rem 0;
        border-left: 6px solid {light_theme['secondary_color']};
        color: {light_theme['text_color']};
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    .stApp[data-theme="dark"] .difference-display {{
        background-color: {dark_theme['card_bg']};
        border-left: 6px solid {dark_theme['secondary_color']};
        color: {dark_theme['text_color']};
    }}
    .converter-title {{
        font-size: 1.5rem;
        margin: 1.5rem 0 1rem 0;
        color: {light_theme['primary_color']};
    }}
    .stApp[data-theme="dark"] .converter-title {{
        color: {dark_theme['primary_color']};
    }}
    .author-section {{
        padding: 1.5rem;
        border-radius: 8px;
        background-color: {light_theme['card_bg']};
        margin-top: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .stApp[data-theme="dark"] .author-section {{
        background-color: {dark_theme['card_bg']};
    }}
    .footer {{
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        font-size: 0.9rem;
        color: {light_theme['text_color']};
    }}
    .stApp[data-theme="dark"] .footer {{
        color: {dark_theme['text_color']};
    }}
    [data-testid="stExpander"] {{
        background-color: {light_theme['card_bg']};
        border-radius: 8px;
        border: 1px solid {light_theme['border_color']};
    }}
    .stApp[data-theme="dark"] [data-testid="stExpander"] {{
        background-color: {dark_theme['card_bg']};
        border: 1px solid {dark_theme['border_color']};
    }}
    hr {{
        border-color: {light_theme['border_color']};
    }}
    .stApp[data-theme="dark"] hr {{
        border-color: {dark_theme['border_color']};
    }}
    </style>
""", unsafe_allow_html=True)

# --------- Título y cabecera ----------
st.markdown('<h1 class="main-title">🌍 Explorador de Zonas Horarias Mundiales</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Descubre la hora actual en cualquier país y compara zonas horarias</p>', unsafe_allow_html=True)

# --------- Imagen principal ----------
try:
    st.image("src\\reloj.jpg", width=800, caption="Relojes alrededor del mundo muestran diferentes horas")
except:
    pass

# --------- Selección de países ----------
all_countries = sorted([(country.name, country.alpha_2) for country in pycountry.countries], key=lambda x: x[0])
country_names = [name for name, code in all_countries]
country_dict = {name: code for name, code in all_countries}

col1, col2 = st.columns(2)
with col1:
    country1_name = st.selectbox("Selecciona el primer país", options=country_names, index=country_names.index("Argentina"))
with col2:
    country2_name = st.selectbox("Selecciona el segundo país para comparar", options=country_names, index=country_names.index("Spain"))

country1_code = country_dict[country1_name]
country2_code = country_dict[country2_name]

def get_timezone_from_country_code(code):
    try:
        return pytz.country_timezones[code][0]
    except:
        return None

tz1 = get_timezone_from_country_code(country1_code)
tz2 = get_timezone_from_country_code(country2_code)

now_utc = datetime.now(pytz.utc)
if tz1 and tz2:
    local_time1 = now_utc.astimezone(pytz.timezone(tz1))
    local_time2 = now_utc.astimezone(pytz.timezone(tz2))
    
    offset1 = local_time1.utcoffset().total_seconds() / 3600
    offset2 = local_time2.utcoffset().total_seconds() / 3600
    diff = offset2 - offset1

    st.markdown(f'<div class="time-display">🕒 Hora actual en <strong>{country1_name}</strong>: <code>{local_time1.strftime("%H:%M:%S")}</code> ({tz1})</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="time-display">🕒 Hora actual en <strong>{country2_name}</strong>: <code>{local_time2.strftime("%H:%M:%S")}</code> ({tz2})</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="difference-display">🧮 Diferencia horaria: <code>{diff:+.1f} horas</code> {"(misma zona horaria)" if diff == 0 else ""}</div>', unsafe_allow_html=True)

    st.markdown('<div class="converter-title">🔄 Conversor de Hora</div>', unsafe_allow_html=True)

    if f"time_input_{country1_code}" not in st.session_state:
        st.session_state[f"time_input_{country1_code}"] = local_time1.time()

    input_time = st.time_input(
        f"Selecciona una hora en {country1_name}",
        value=st.session_state[f"time_input_{country1_code}"],
        key=f"time_input_{country1_code}"
    )

    current_date = datetime.now().date()
    selected_datetime = datetime.combine(current_date, input_time)
    localized_time = pytz.timezone(tz1).localize(selected_datetime)
    converted_time = localized_time.astimezone(pytz.timezone(tz2))

    st.markdown(f'<div class="time-display">🧭 Hora correspondiente en <strong>{country2_name}</strong>: <code>{converted_time.strftime("%H:%M:%S")}</code></div>', unsafe_allow_html=True)

else:
    st.error("No se pudo obtener la zona horaria de uno o ambos países seleccionados.")

# --------- Mapa Interactivo ----------
country_data = []
for country in pycountry.countries:
    code = country.alpha_2
    name = country.name
    timezones = pytz.country_timezones.get(code)
    if timezones:
        tz = pytz.timezone(timezones[0])
        local_time = now_utc.astimezone(tz)
        utc_offset = local_time.utcoffset().total_seconds() / 3600
        country_data.append({
            "Country": name,
            "Code": code,
            "Timezone": timezones[0],
            "Local Time": local_time.strftime("%H:%M:%S"),
            "UTC Offset (hrs)": utc_offset
        })

df_countries = pd.DataFrame(country_data)

fig = px.choropleth(
    df_countries,
    locations="Code",
    color="UTC Offset (hrs)",
    hover_name="Country",
    hover_data=["Timezone", "Local Time"],
    color_continuous_scale=[
        "#3B1F2B", "#8C593B", "#D9A066", "#F2E394", "#A1C181", "#6A994E"
    ],
    projection="natural earth",
    title="🌐 Zonas Horarias del Mundo"
)

fig.update_layout(
    margin=dict(l=0, r=0, t=40, b=0),
    coloraxis_colorbar=dict(
        title="Diferencia con UTC (horas)",
        ticks="outside",
        tickvals=[-12, -8, -4, 0, 4, 8, 12],
        ticktext=["-12", "-8", "-4", "0", "+4", "+8", "+12"]
    ),
    plot_bgcolor=light_theme['bg_color'],
    paper_bgcolor=light_theme['bg_color'],
    font_color=light_theme['text_color']
)
st.plotly_chart(fig, use_container_width=True)

# --------- Historial ----------
if "historial" not in st.session_state:
    st.session_state.historial = []

current_comparison = (country1_name, country2_name)
if current_comparison not in st.session_state.historial:
    st.session_state.historial.append(current_comparison)

with st.expander("📜 Historial de consultas (últimas 10)"):
    for c1, c2 in st.session_state.historial[-10:]:
        st.markdown(f"- {c1} ↔ {c2}")

# --------- Sobre mí ----------
st.markdown("---")
with st.container():
    st.markdown("## 👨‍💻 Sobre el Autor")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://avatars.githubusercontent.com/u/97362291?v=4", width=150)
    with col2:
        st.markdown("""
        **Estudiante de Ciencia de Datos** | Universidad Nacional Guillermo Brown  
        
        🔧 **Stack técnico:**  
        - Python • Streamlit • Pandas • Plotly • Folium  
        
        🌐 **Enlaces:**  
        [Portfolio](https://sebastian-sanchez-bentolila.netlify.app/) • 
        [LinkedIn](https://www.linkedin.com/in/sebastian-sanchez-bentolila/) • 
        [GitHub](https://github.com/Sebastian-Sanchez-Bentolila)  
        
        📫 **Contacto:** sebastiansb3004@gmail.com  
        
        *"La ciencia de datos es el arte de convertir datos en decisiones."*
        """)

# --------- Pie ----------
st.markdown("---")
st.markdown('<div class="footer">Aplicación desarrollada con ❤️ usando Streamlit y Python</div>', unsafe_allow_html=True)