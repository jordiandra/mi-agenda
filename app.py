import streamlit as st
from datetime import datetime
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Master Planner 2026", layout="wide", page_icon="🚀")

# --- FUNCIONES DE BASE DE DATOS SIMPLE ---
FILE_DB = "registro_manto.txt"
def cargar_fechas():
    if not os.path.exists(FILE_DB): return {}
    with open(FILE_DB, "r") as f:
        return {linea.split(":")[0]: linea.split(":")[1].strip() for linea in f.readlines()}

def guardar_fecha(tarea):
    fechas = cargar_fechas()
    fechas[tarea] = datetime.now().strftime("%Y-%m-%d")
    with open(FILE_DB, "w") as f:
        for t, d in fechas.items(): f.write(f"{t}:{d}\n")

# --- LÓGICA DE TIEMPO ---
ahora = datetime.now()
dia_nombre = ahora.strftime('%A')
hora = ahora.hour + ahora.minute/60
dias_es = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}

st.title(f"📊 Mi Centro de Mando: {dias_es.get(dia_nombre)}")

# --- COLUMNA IZQUIERDA: RUTINA Y FOCO ---
col1, col2 = st.columns([2, 1])

with col1:
    if dia_nombre in ["Saturday", "Sunday"]:
        st.header("🏠 Fin de Semana: Enfoque y Avance")
        st.info("📌 09:00 - 14:00 | UNIVERSIDAD (Carga Pesada)")
        
        # EL BOTÓN DE PÁNICO (Para cuando sobra tiempo)
        st.divider()
        st.subheader("🆘 ¿Te sobra tiempo? Botón de Pánico")
        energia = st.select_slider("Nivel de batería mental:", options=["Agotado", "Bajo", "Normal", "Full"])
        
        if st.button("Generar Plan de Emergencia"):
            if energia == "Agotado": st.success("🍵 Solo Inglés (15 min) e Inversiones (lectura). Luego descansa.")
            elif energia == "Bajo": st.info("🚗 Tarea física: Limpieza o revisar el carro.")
            elif energia == "Normal": st.warning("📚 Adelanta 1 hora de Universidad o Tesis.")
            elif energia == "Full": st.error("💻 ¡DALE! 2 horas de Programación pura.")
            
    else:
        st.header("💼 Rutina Lunes-Viernes")
        st.markdown(f"""
        * **06:30 - 15:00:** Trabajo 💼
        * **15:00 - 16:30:** Traslado / Almuerzo / **INGLÉS** 🇬🇧
        * **16:30 - 18:30:** Universidad 🎓
        * **19:00 - 21:00:** GYM 🏋️ (Lunes y Miércoles) / Programación (Otros días)
        * **22:00:** DORMIR 😴
        """)

# --- COLUMNA DERECHA: ALERTAS Y MANTENIMIENTO ---
with col2:
    st.header("🛠️ Mantenimiento")
    fechas_historial = cargar_fechas()
    tareas_manto = {"Corte de Cabello": 21, "Dentista": 180, "Servicio Carro": 120}

    for tarea, dias_limite in tareas_manto.items():
        ultima = fechas_historial.get(tarea)
        if ultima:
            dias_pasados = (ahora - datetime.strptime(ultima, "%Y-%m-%d")).days
            if dias_pasados >= dias_limite: st.error(f"⚠️ {tarea}: Toca ya!")
            else: st.success(f"✅ {tarea}: OK")
        else: st.warning(f"❓ {tarea}: Sin registro")
        
        if st.button(f"Hecho: {tarea}"):
            guardar_fecha(tarea)
            st.rerun()

# --- VALIDACIÓN DE SUEÑO ---
if hora >= 22:
    st.error("❗ ¡ALERTA DE SUEÑO! Apaga todo y ve a dormir. Mañana trabajas a las 06:30.")
