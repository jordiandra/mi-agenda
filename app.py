import streamlit as st
from datetime import datetime, date
import pandas as pd
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Master Planner Pro + Game", layout="wide")

# --- SISTEMA DE PERSISTENCIA (PUNTOS Y MANTENIMIENTO) ---
DB_FILE = "datos_maestros.txt"

def cargar_datos():
    if not os.path.exists(DB_FILE): return {"puntos": 0, "racha": 0, "ultima_racha": ""}
    datos = {}
    with open(DB_FILE, "r") as f:
        for linea in f:
            k, v = linea.strip().split(":")
            datos[k] = v
    return datos

def guardar_dato(clave, valor):
    datos = cargar_datos()
    datos[clave] = valor
    with open(DB_FILE, "w") as f:
        for k, v in datos.items(): f.write(f"{k}:{v}\n")

# --- LÓGICA DE TIEMPO ---
ahora = datetime.now()
hoy_str = ahora.strftime("%Y-%m-%d")
dia_nombre = ahora.strftime('%A')
hora_actual = ahora.hour + ahora.minute/60
dias_es = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}

# --- INTERFAZ DE USUARIO ---
st.title(f"🏆 Nivel de Enfoque: {cargar_datos().get('puntos', 0)} pts")

# --- SISTEMA DE RACHAS ---
datos = cargar_datos()
col_r1, col_r2 = st.columns(2)
with col_r1:
    st.metric("🔥 Racha Actual", f"{datos.get('racha', 0)} Días")
with col_r2:
    if st.button("✅ ¡LOGRÉ MI RUTINA DE HOY!"):
        if datos.get("ultima_racha") != hoy_str:
            nueva_racha = int(datos.get("racha", 0)) + 1
            nuevos_puntos = int(datos.get("puntos", 0)) + 100
            guardar_dato("racha", nueva_racha)
            guardar_dato("puntos", nuevos_puntos)
            guardar_dato("ultima_racha", hoy_str)
            st.balloons()
            st.rerun()
        else:
            st.warning("Ya registraste tu éxito de hoy. ¡Sigue así!")

st.divider()

# --- MAPA DE VIDA ---
ver_tabla = st.checkbox("🔍 Ver Mapa de Vida Completo")
if ver_tabla:
    datos_semana = {
        "HORARIO": ["06:30 - 15:00", "15:00 - 16:30", "16:30 - 18:30", "19:00 - 21:00", "22:00"],
        "LUNES-VIERNES": ["TRABAJO", "INGLÉS / COMIDA", "UNIVERSIDAD", "GYM / PROG", "DORMIR"],
        "SÁBADO-DOMINGO": ["UNIV (CARGA ALTA)", "INVERSIONES / LIBRE", "PROYECTOS / SOCIAL", "GYM", "ORGANIZACIÓN"]
    }
    st.table(pd.DataFrame(datos_semana))

# --- BLOQUE DINÁMICO ---
st.subheader(f"🎯 Actividad para {dias_es.get(dia_nombre)}")
if 6.5 <= hora_actual < 15 and dia_nombre not in ["Saturday", "Sunday"]:
    st.info("💼 Bloque de TRABAJO. Prohibido distracciones.")
elif 16.5 <= hora_actual < 18.5:
    st.warning("🎓 Bloque de UNIVERSIDAD. Foco en tareas.")
elif 19 <= hora_actual < 21:
    st.error("🏋️ Bloque de GYM. ¡A romper fibras!")
else:
    st.success("🔓 TIEMPO LIBRE / FLEXIBLE. Usa el botón de pánico si dudas.")

# --- BOTÓN DE PÁNICO Y MANTENIMIENTO ---
c_panico, c_manto = st.columns([2, 1])

with c_panico:
    st.subheader("🆘 Botón de Pánico")
    energia = st.select_slider("Energía:", options=["Cero", "Baja", "Media", "Alta"])
    if st.button("¿Qué hago?"):
        respuestas = {"Cero": "15 min de Inglés.", "Baja": "Mantenimiento físico (Carro/Limpieza).", "Media": "1h Universidad.", "Alta": "2h Programación/Tesis."}
        st.write(f"✅ **Plan:** {respuestas[energia]}")

with c_manto:
    st.subheader("🛠️ Manto.")
    # Usamos los puntos para "pagar" mantenimientos si quieres o solo registrarlos
    manto_tareas = {"Corte Cabello": 21, "Dentista": 180, "Carro": 120}
    for t, d in manto_tareas.items():
        if st.button(f"Hecho: {t}"):
            st.toast(f"{t} actualizado")
