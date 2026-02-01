import streamlit as st
from datetime import datetime
import pandas as pd
import os

# --- CONFIGURACIÓN DE DISEÑO PROFESIONAL ---
st.set_page_config(page_title="Executive Life Dashboard", layout="wide", page_icon="👔")

# Inyección de CSS para mejorar la estética
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1f2937; padding: 20px; border-radius: 15px; border: 1px solid #374151; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #3b82f6; color: white; border: none; }
    .stButton>button:hover { background-color: #2563eb; border: none; }
    div[data-testid="stExpander"] { border-radius: 15px; border: 1px solid #374151; background-color: #1f2937; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DATOS ---
DB_FILE = "sistema_datos_v2.txt"
def cargar_datos():
    if not os.path.exists(DB_FILE): return {"puntos": "0", "racha": "0", "ultima_racha": "None"}
    datos = {}
    with open(DB_FILE, "r") as f:
        for linea in f:
            if ":" in linea: k, v = linea.strip().split(":", 1); datos[k] = v
    return datos

def guardar_dato(clave, valor):
    datos = cargar_datos(); datos[clave] = str(valor)
    with open(DB_FILE, "w") as f:
        for k, v in datos.items(): f.write(f"{k}:{v}\n")

# --- LÓGICA DE TIEMPO ---
ahora = datetime.now()
hoy_str = ahora.strftime("%Y-%m-%d")
dia_nombre = ahora.strftime('%A')
hora_decimal = ahora.hour + ahora.minute/60
dias_es = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}

# --- HEADER: SCOREBOARD ---
datos = cargar_datos()
st.title(f"🚀 {dias_es.get(dia_nombre)} | Status del Sistema")

c1, c2, c3 = st.columns(3)
with c1: st.metric("🔥 Racha", f"{datos.get('racha')} Días")
with c2: st.metric("⭐ Nivel", f"{int(datos.get('puntos', 0)) // 1000 + 1}")
with c3: st.metric("💰 Score", f"{datos.get('puntos')} XP")

if st.button("✨ REGISTRAR VICTORIA DIARIA"):
    if datos.get("ultima_racha") != hoy_str:
        guardar_dato("racha", int(datos.get("racha", 0)) + 1)
        guardar_dato("puntos", int(datos.get("puntos", 0)) + 150)
        guardar_dato("ultima_racha", hoy_str)
        st.balloons(); st.rerun()

st.divider()

# --- CUERPO PRINCIPAL ---
col_main, col_side = st.columns([2, 1])

with col_main:
    # 1. MONITOR DINÁMICO
    st.subheader("🎯 Foco Actual")
    def obtener_status():
        if dia_nombre in ["Saturday", "Sunday"]:
            if 9 <= hora_decimal < 14: return "📚 UNIVERSIDAD (MODO BESTIA)", "#FACC15"
            if 14 <= hora_decimal < 19: return "🔓 LIBERTAD CREATIVA / PROYECTOS", "#4ADE80"
            return "🌙 RECARGA DE ENERGÍA", "#60A5FA"
        else:
            if 6.5 <= hora_decimal < 15: return "💼 EJECUCIÓN PROFESIONAL", "#3B82F6"
            if 16.5 <= hora_decimal < 18.5: return "🎓 MEJORA ACADÉMICA", "#F97316"
            if 19 <= hora_decimal < 21: return "🏋️ POTENCIA FÍSICA", "#EF4444"
            return "😴 MODO REPARACIÓN", "#94A3B8"

    texto, color = obtener_status()
    st.markdown(f"<h2 style='color:{color}; background-color:rgba(0,0,0,0.2); padding:20px; border-radius:15px; border-left: 10px solid {color};'>{texto}</h2>", unsafe_allow_html=True)

    # 2. DECISOR DE ENERGÍA
    st.markdown("### 🆘 Decision Helper")
    with st.expander("¿No sabes qué hacer?"):
        energia = st.select_slider("Energía:", options=["Low", "Medium", "High", "Ultra"])
        if st.button("Ejecutar Plan"):
            planes = {"Low": "Inglés (Podcast) + Inversiones.", "Medium": "Mantenimiento o Tarea Uni.", "High": "Programación 1h.", "Ultra": "Tesis o Código Complejo."}
            st.info(planes[energia])

with col_side:
    st.subheader("🛠️ Lifecycle Management")
    manto = {"Corte Pelo": 21, "Carro": 120, "Dentista": 180}
    for t, f in manto.items():
        val = datos.get(f"manto_{t}", "None")
        if val != "None":
            dias = (ahora - datetime.strptime(val, "%Y-%m-%d")).days
            pct = min(dias / f, 1.0)
            st.write(f"**{t}** ({int(pct*100)}%)")
            st.progress(pct)
            if st.button(f"Reset {t}", key=t): guardar_dato(f"manto_{t}", "None"); st.rerun()
        else:
            if st.button(f"Marcar {t} Hecho"): guardar_dato(f"manto_{t}", hoy_str); st.rerun()

# 4. MAPA VISUAL AL FINAL
with st.expander("📅 Master Schedule"):
    st.table(pd.DataFrame({"HORA": ["Mañana", "Tarde", "Noche"], "L-V": ["Trabajo", "Uni", "Gym/Prog"], "S-D": ["Uni", "Proyectos", "Gym"]}))
