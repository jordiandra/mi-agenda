import streamlit as st
from datetime import datetime
import pandas as pd

# Configuración Estética
st.set_page_config(page_title="UltraPlanner 2026", layout="wide", page_icon="📈")

# Estilo CSS personalizado para mejorar la interfaz
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA CORE ---
ahora = datetime.now()
dia_nombre = ahora.strftime('%A')
hora = ahora.hour + ahora.minute/60

# Diccionario de Actividades
dias_es = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}

st.title(f"⚡ Sistema de Optimización: {dias_es.get(dia_nombre)}")

# --- SIDEBAR: ESTADO DE SALUD Y LOGÍSTICA ---
st.sidebar.header("🛠️ Logística y Mantenimiento")
with st.sidebar:
    corte = st.slider("Días desde último corte de cabello", 0, 30, 10)
    carro = st.slider("Meses desde servicio al carro", 0, 12, 2)
    dentista = st.checkbox("Cita dental este semestre")
    
    if corte > 20: st.error("💇‍♂️ ¡Toca ir al peluquero este sábado!")
    if carro > 4: st.warning("🚗 Revisa el aceite y niveles.")

# --- PANEL PRINCIPAL: ¿QUÉ HACER AHORA? ---
st.header("🎯 Foco Actual")

def determinar_estado():
    if 6.5 <= hora < 15: return "💼 TRABAJO: Concentración máxima.", "blue"
    if 15 <= hora < 16.5: return "🍴 ALMUERZO + 🎧 INGLÉS (Escucha un Podcast)", "green"
    if 16.5 <= hora < 18.5: return "🎓 UNIVERSIDAD: Tareas y Estudio", "orange"
    if 19 <= hora < 21:
        if dia_nombre in ["Monday", "Wednesday", "Saturday", "Sunday"]:
            return "🏋️ GYM: Dale con todo.", "red"
        return "💻 PROGRAMACIÓN / TESIS: Avance técnico.", "purple"
    if hora >= 22: return "😴 HORA DE DORMIR: Apaga pantallas.", "gray"
    return "⏳ TIEMPO LIBRE: Elige un proyecto abajo.", "normal"

mensaje, color = determinar_estado()
st.subheader(f":{color}[{mensaje}]")

# --- VISUALIZACIÓN SEMANAL ---
st.divider()
st.subheader("📅 Tu Mapa de Calor Semanal")

datos_semana = {
    "Día": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
    "Mañana": ["Trabajo", "Trabajo", "Trabajo", "Trabajo", "Trabajo", "Universidad", "Universidad"],
    "Tarde": ["Univ", "Univ", "Univ", "Univ", "Univ", "Libre/Manto", "Libre/Manto"],
    "Noche": ["Gym", "Prog", "Gym", "Inv", "Social", "Gym", "Gym"]
}
df = pd.DataFrame(datos_semana)
st.table(df)

# --- SISTEMA ANTIDESESPERACIÓN (Fines de Semana) ---
if dia_nombre in ["Saturday", "Sunday"]:
    st.info("💡 Es fin de semana. Tienes más tiempo, úsalo con inteligencia.")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Carga Universitaria", value="5 Horas", delta="Fijo")
        if st.button("Iniciar Bloque Uni"):
            st.write("⏱️ Cronómetro iniciado. Terminas a las 2:00 PM.")
            
    with col2:
        st.metric(label="Proyectos", value="Programación", delta="Prioridad")
        st.write("Si terminaste la Uni, abre VS Code.")
        
    with col3:
        st.metric(label="Inversiones", value="Portafolio", delta="Domingo")
        st.write("Revisa tendencias y balance de mes.")

# --- FOOTER ---
if hora > 22.1:
    st.error("❗ Ya es tarde. Estás robándole energía al 'tú' de mañana. ¡Ve a dormir!")