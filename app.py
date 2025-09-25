import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# --- Título y descripción de la aplicación ---
st.title("Simulador de Reclutamiento de Pacientes")
st.markdown("Esta aplicación realiza una simulación de Montecarlo basada en datos de reclutamiento que usted proporcione. La aplicación calcula la distribución de probabilidad a partir de sus datos y luego ejecuta la simulación.")

st.markdown("---")

# --- 1. Obtener la configuración de la simulación del usuario ---
st.header("Configuración de la simulación")

# Usar st.number_input para un control numérico
num_centros_simulacion = st.number_input("Ingrese el número de centros para la simulación:", min_value=1, value=10, step=1, help="Este es el número de centros que se considerarán en la simulación.")
meta = st.number_input("Ingrese la meta de pacientes total para el estudio:", min_value=0, value=100, step=1, help="Este es el número de pacientes que se espera alcanzar o superar.")

st.markdown("---")
# --- Cambio de etiqueta solicitado ---
st.write("### Defina la distribución de probabilidad con sus datos")
st.info("Ingrese la cantidad de pacientes que espera reclutar cada centro. El sistema calculará las probabilidades automáticamente.")

# --- Lógica para la entrada dinámica y la suma en tiempo real ---
pacientes_ejemplo = []
st.subheader("Ingrese los pacientes por cada centro:")
sum_pacientes = 0
for i in range(int(num_centros_simulacion)):
    # st.number_input para cada centro con una clave única
    paciente_por_centro = st.number_input(
        f"Pacientes para el Centro {i + 1}:",
        min_value=0,
        value=10,
        step=1,
        key=f'paciente_{i}'
    )
    pacientes_ejemplo.append(paciente_por_centro)
    sum_pacientes += paciente_por_centro

# --- Muestra la suma total de pacientes de forma destacada ---
st.markdown(
    f"""
    <div style="background-color:#f0f8ff; padding:15px; border-radius:10px; 
                text-align:center; border: 2px solid #007acc; margin-top:20px;">
        <h3 style="color:#007acc; margin:0;">🔹 Suma total de pacientes ingresados</h3>
        <h2 style="color:#333; margin:5px 0 0 0;">{sum_pacientes}</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Lógica para calcular las probabilidades a partir de la entrada ---
pacientes_posibles = []
probabilidades_list = []
suma_validada = False
try:
    if not pacientes_ejemplo or sum(pacientes_ejemplo) == 0:
        st.warning("Por favor, ingrese un número de pacientes para cada centro.")
    else:
        conteo_pacientes = Counter(pacientes_ejemplo)
        total_pacientes_ejemplo = len(pacientes_ejemplo)
        
        pacientes_posibles = sorted(conteo_pacientes.keys())
        probabilidades_list = [conteo_pacientes[p] / total_pacientes_ejemplo for p in pacientes_posibles]
        
        if abs(sum(probabilidades_list) - 1.0) > 1e-6:
            st.error("Error en el cálculo de probabilidades. Revise sus datos.")
        else:
            st.success("Distribución de probabilidad calculada con éxito. ¡Listo para simular!")
            st.write(f"**Pacientes posibles:** `{pacientes_posibles}`")
            st.write(f"**Probabilidades calculadas:** `{np.round(probabilidades_list, 2)}`")
            suma_validada = True

except (ValueError, IndexError):
    st.error("Error: Revise el formato de los datos ingresados. Deben ser números enteros.")

# --- Lógica de la simulación, solo se ejecuta si los datos son válidos y el botón es presionado ---
if suma_validada and st.button("Ejecutar Simulación"):
    
    # --- 2. Realizar las simulaciones ---
    num_simulaciones = 100000
    resultados_totales = []

    for _ in range(num_simulaciones):
        reclutamiento_por_centro = np.random.choice(
            a=pacientes_posibles, 
            size=int(num_centros_simulacion), 
            p=probabilidades_list
        )
        total_pacientes_simulacion = sum(reclutamiento_por_centro)
        resultados_totales.append(total_pacientes_simulacion)

    # --- 3. Analizar los resultados y mostrarlos ---
    st.markdown("---")
    st.header("Resultados de la Simulación")
    
    media_pacientes = np.mean(resultados_totales)
    st.success(f"**Número esperado de pacientes (media):** {media_pacientes:.2f}")

    probabilidad_exito = sum(np.array(resultados_totales) >= meta) / num_simulaciones
    st.success(f"**Probabilidad de alcanzar o superar la meta de {meta} pacientes:** {probabilidad_exito:.2%}")

    # --- 4. Visualizar la distribución ---
    st.subheader("Visualización de la distribución de resultados")
    fig, ax = plt.subplots()
    ax.hist(resultados_totales, bins=range(min(resultados_totales), max(resultados_totales) + 2), edgecolor='black', alpha=0.7)
    ax.set_title('Distribución de los resultados de la simulación de Montecarlo')
    ax.set_xlabel('Número total de pacientes')
    ax.set_ylabel('Frecuencia de las simulaciones')
    
    ax.axvline(media_pacientes, color='red', linestyle='dashed', linewidth=2, label=f'Media: {media_pacientes:.2f}')
    ax.axvline(meta, color='green', linestyle='solid', linewidth=2, label=f'Meta: {meta}')
    ax.legend()
    st.pyplot(fig)
