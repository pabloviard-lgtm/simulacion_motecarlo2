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
st.write("### Defina la distribución de probabilidad con sus datos")
st.info("Ingrese la cantidad de pacientes que reclutó cada centro en un escenario de ejemplo, separados por comas. El sistema calculará las probabilidades automáticamente.")

# Usar st.text_input para ingresar la lista de pacientes de ejemplo
pacientes_ejemplo_str = st.text_input("Pacientes por centro (ej: 8, 9, 10, 10, 11)", "8, 9, 10, 11, 12, 10, 10, 10, 10, 8")

# --- Lógica para calcular las probabilidades automáticamente ---
pacientes_posibles = []
probabilidades_list = []
suma_validada = False
try:
    pacientes_ejemplo = [int(p.strip()) for p in pacientes_ejemplo_str.split(',')]
    if not pacientes_ejemplo:
        st.warning("Por favor, ingrese al menos un número de paciente de ejemplo.")
    else:
        # Usar Counter para contar la frecuencia de cada número
        conteo_pacientes = Counter(pacientes_ejemplo)
        total_pacientes_ejemplo = len(pacientes_ejemplo)
        
        # Ordenar los pacientes posibles de menor a mayor
        pacientes_posibles = sorted(conteo_pacientes.keys())
        
        # Calcular las probabilidades para cada paciente posible
        probabilidades_list = [conteo_pacientes[p] / total_pacientes_ejemplo for p in pacientes_posibles]
        
        # Validar que la suma de probabilidades es 1.0
        if abs(sum(probabilidades_list) - 1.0) > 1e-6:
            st.error("Error en el cálculo de probabilidades. Revise sus datos.")
        else:
            st.success("Distribución de probabilidad calculada con éxito. ¡Listo para simular!")
            st.write(f"**Pacientes posibles:** `{pacientes_posibles}`")
            st.write(f"**Probabilidades calculadas:** `{np.round(probabilidades_list, 2)}`")
            suma_validada = True

except (ValueError, IndexError):
    st.error("Error: Revise el formato de los datos ingresados. Deben ser números enteros separados por comas.")

# --- Lógica de la simulación, solo se ejecuta si los datos son válidos y el botón es presionado ---
if suma_validada and st.button("Ejecutar Simulación"):
    
    # --- 2. Realizar las simulaciones ---
    num_simulaciones = 100000
    resultados_totales = []

    for _ in range(num_simulaciones):
        reclutamiento_por_centro = np.random.choice(
            a=pacientes_posibles, 
            size=num_centros_simulacion, 
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