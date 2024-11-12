import streamlit as st
import pandas as pd
import altair as alt

st.sidebar.title("Filtros para dar mas comodidad")
st.markdown("# Accidentes de autos entre 2010-2018")
st.sidebar.image("Auto_accidentes.jpg")
ruta_csv = "ped_crashes.csv"

# Cargar datos desde el archivo CSV
try:
    # Especificar explícitamente el delimitador como coma
    datos = pd.read_csv(ruta_csv, )
    
    
    st.write("Datos cargados correctos :", datos)
    
    # esto es la barra lateral y seleccionamos graph de lineas o barra
    tipo_grafico = st.sidebar.selectbox("Selecciona el tipo de gráfico", ["Líneas", "Barras"])

    # Selección de la columna para filtrar en la barra lateral
    columna_filtro = st.sidebar.selectbox("Selecciona una columna para filtrar", datos.columns)
    valores_unicos = datos[columna_filtro].unique()
    filtro_seleccion = st.sidebar.multiselect("Selecciona valores para filtrar", valores_unicos)
    
    # Aplicar el filtro
    if filtro_seleccion:
        datos_filtrados = datos[datos[columna_filtro].isin(filtro_seleccion)]
    else:
        datos_filtrados = datos

    # Selección de columnas para los ejes en la barra lateral
    columna_eje_x = st.sidebar.selectbox("Selecciona la columna para el eje X", datos.columns)
    columna_eje_y = st.sidebar.selectbox("Selecciona la columna para el eje Y", datos.columns)

    # Generar el gráfico en función de la selección
    if tipo_grafico == "Líneas":
        grafico = alt.Chart(datos_filtrados).mark_line().encode(
            x=columna_eje_x,
            y=columna_eje_y
        )
    else:  # Opción "Barras"
        grafico = alt.Chart(datos_filtrados).mark_bar().encode(
            x=columna_eje_x,
            y=columna_eje_y
        )
    
    # Mostrar el gráfico en Streamlit
    st.altair_chart(grafico, use_container_width=True)

except FileNotFoundError:
    st.error("No se encontró el archivo en la ruta especificada. Por favor, verifica la ruta e inténtalo de nuevo.")
except Exception as e:
    st.error(f"Hubo un error al leer el archivo: {e}")
