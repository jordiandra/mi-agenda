import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os

# --- CONFIGURACIÓN DE NIVEL PROFESIONAL ---
st.set_page_config(page_title="Personal ERP & Life Planner", layout="wide", page_icon="⚙️")

# --- GESTIÓN DE DATOS (PERSISTENCIA) ---
DB_FILE = "sistema_datos.txt"

def cargar_datos():
    if not os.path.exists(DB_FILE):
        return {"puntos": "0", "racha": "0", "ultima_racha": "None"}
    datos = {}
    with open(DB_FILE, "r") as f:
        for linea in f:
            if ":" in linea:
                k, v = linea.strip().split(":", 1)
                datos[k] = v
    return datos

def guardar_dato(clave, valor):
    datos = cargar_datos()
    datos[clave] = str(valor)
    with open(DB_FILE, "w") as f:
        for k, v in datos.items():
            f.write(f"{k}:{v}\n")

# --- LÓGICA DE TIEMPO Y CALENDARIO ---
ahora = datetime.now()
hoy_str = ahora.strftime("%Y-%m-%d")
dia_nombre = ahora.strftime('%A')
hora_decimal = ahora.hour + ahora.minute/60
dias_es = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
    "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
}

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%); }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA: GAMIFICACIÓN ---
datos = cargar_datos()
st.title(f"🚀 Dashboard de Alto Rendimiento | {dias_es.get(dia_nombre)}")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("🔥 Racha Actual", f"{datos.get('racha')} Días")
with c2:
    st.metric("🏆 Score Total", f"{datos.get('puntos')} pts")
with c3:
    if st.button("✅ REGISTRAR VICTORIA DIARIA"):
        if datos.get("ultima_racha") != hoy_str:
            guardar_dato("racha", int(datos.get("racha", 0)) + 1)
            guardar_dato("puntos", int(datos.get("puntos", 0)) + 100)
            guardar_dato("ultima_racha", hoy_str)
            st.balloons()
            st.rerun()
        else:
            st.toast("¡Ya ganaste tus puntos de hoy!")

st.divider()

# --- COLUMNA PRINCIPAL (OPERACIONES) Y LATERAL (ACTIVOS) ---
col_main, col_side = st.columns([2, 1])

with col_main:
    # 1. MONITOR DE ACTIVIDAD EN TIEMPO REAL
    st.subheader("🎯 Estado del Sistema (Tiempo Real)")
    
    def obtener_bloque():
        if dia_nombre in ["Saturday", "Sunday"]:
            if 9 <= hora_decimal < 14: return "📚 UNIVERSIDAD (CARGA ALTA)", "warning"
            if 14 <= hora_decimal < 19: return "🔓 TIEMPO FLEXIBLE / PROYECTOS", "success"
            if 19 <= hora_decimal < 21: return "🏋️ GYM / ENTRENAMIENTO", "error"
            return "🌙 DESCANSO / PLANIFICACIÓN", "info"
        else:
            if 6.5 <= hora_decimal < 15: return "💼 TRABAJO PROFESIONAL", "info"
            if 15 <= hora_decimal < 16.5: return "🇬🇧 INGLÉS + NUTRICIÓN", "success"
            if 16.5 <= hora_decimal < 18.5: return "🎓 UNIVERSIDAD (ESTUDIO)", "warning"
            if 19 <= hora_decimal < 21: return "🏋️ GYM / PROGRAMACIÓN", "error"
            return "😴 MODO REPARACIÓN (SUEÑO)", "info"

    msg, tipo = obtener_bloque()
    if tipo == "info": st.info(msg)
    elif tipo == "success": st.success(msg)
    elif tipo == "warning": st.warning(msg)
    elif tipo == "error": st.error(msg)

    # 2. BOTÓN DE PÁNICO (SELECTOR DE ENERGÍA)
    st.divider()
    st.subheader("🆘 Algoritmo de Decisión (Huecos Libres)")
    energia = st.select_slider("Nivel de Batería Mental:", options=["Baja", "Media", "Alta", "Máxima"])
    
    if st.button("Calcular Tarea Óptima"):
        dict_tareas = {
            "Baja": "Revisión de Inversiones (Lectura) o Mantenimiento de Carro.",
            "Media": "15 min de Inglés y 45 min de Tareas de Universidad.",
            "Alta": "Bloque de 1 hora de Programación o Tesis.",
            "Máxima": "Sesión intensiva de Programación (Foco profundo)."
        }
        st.write(f"⚙️ **Recomendación:** {dict_tareas[energia]}")

    # 3. MAPA SEMANAL (EXPANDIBLE)
    with st.expander("📅 Ver Hoja de Ruta Semanal"):
        df_mapa = pd.DataFrame({
            "BLOQUE": ["Mañana", "Tarde 1", "Tarde 2", "Noche", "Cierre"],
            "LUN-VIE": ["Trabajo", "Inglés", "Universidad", "Gym/Prog", "Dormir"],
            "SÁB-DOM": ["Univ (Alta)", "Inversiones", "Proyectos", "Gym", "Plan"]
        })
        st.table(df_mapa)

with col_side:
    st.subheader("🛠️ Mantenimiento de Activos")
    # {Tarea: [Frecuencia Días, Criticidad 1-5]}
    activos = {
        "Corte de Cabello": [21, 2],
        "Servicio Carro": [120, 5],
        "Dentista": [180, 4],
        "Cita Médica": [365, 3]
    }
    
    for tarea, specs in activos.items():
        frec, crit = specs
        ultima_vez = datos.get(f"manto_{tarea}")
        
        if ultima_vez and ultima_vez != "None":
            dt_ultima = datetime.strptime(ultima_vez, "%Y-%m-%d")
            dias_transcurridos = (ahora - dt_ultima).days
            uso = min(dias_transcurridos / frec, 1.0)
            
            st.write(f"**{tarea}** (Crit: {crit})")
            st.progress(uso)
            
            if uso >= 1.0:
                st.error("⚠️ CRÍTICO: Realizar hoy")
            elif uso >= 0.8:
                st.warning("⏳ Próximo a vencer")
            
            c_a, c_b = st.columns(2)
            with c_a:
                if st.button("Reset", key=f"re_{tarea}"):
                    guardar_dato(f"manto_{tarea}", "None")
                    st.rerun()
        else:
            st.info(f"Pendiente: {tarea}")
            if st.button("Marcar Hecho", key=f"do_{tarea}"):
                guardar_dato(f"manto_{tarea}", hoy_str)
                st.rerun()

# --- FOOTER: ALERTA DE SALUD ---
if hora_decimal >= 22 or hora_decimal < 5:
    st.sidebar.error("🚨 MODO SUEÑO REQUERIDO: Tu rendimiento de mañana depende de tu descanso hoy.")
