import streamlit as st
import pandas as pd
import altair as alt

# Encabezado de la aplicación y elementos de la barra lateral
st.sidebar.header("Ajustes de visualización")
st.title("Visualización de Accidentes de Autos (2010-2018)")
st.sidebar.image("Auto_accidentes.jpg", caption="Análisis de accidentes")

# Ruta del archivo de datos
archivo_datos = "ped_crashes.csv"

# Intentar cargar los datos
try:
    # Leer datos desde el archivo CSV
    datos_accidentes = pd.read_csv(archivo_datos)
    st.write("Datos cargados exitosamente:", datos_accidentes.head())
    
    # Configuración del tipo de gráfico a mostrar
    opcion_grafico = st.sidebar.radio(
        "Selecciona el tipo de gráfico para visualizar", 
        options=["Líneas", "Barras", "Dispersión", "Violin Plot"]
    )
    
    # Selección de columna para aplicar filtro
    columna_filtro = st.sidebar.selectbox("Elige una columna para filtrar los datos", datos_accidentes.columns)
    valores_opciones = datos_accidentes[columna_filtro].unique()
    seleccion_filtros = st.sidebar.multiselect("Selecciona valores para incluir en el análisis", valores_opciones)
    
    # Aplicar el filtro si hay selección
    if seleccion_filtros:
        datos_filtrados = datos_accidentes[datos_accidentes[columna_filtro].isin(seleccion_filtros)]
    else:
        datos_filtrados = datos_accidentes

    # Elegir columnas para los ejes X e Y
    eje_x = st.sidebar.selectbox("Selecciona la variable para el eje X", datos_accidentes.columns)
    eje_y = st.sidebar.selectbox("Selecciona la variable para el eje Y", datos_accidentes.columns)

    # Crear el gráfico seleccionado por el usuario
    if opcion_grafico == "Líneas":
        grafico = alt.Chart(datos_filtrados).mark_line().encode(
            x=eje_x,
            y=eje_y
        )
    elif opcion_grafico == "Barras":
        grafico = alt.Chart(datos_filtrados).mark_bar().encode(
            x=eje_x,
            y=eje_y
        )
    elif opcion_grafico == "Dispersión":
        grafico = alt.Chart(datos_filtrados).mark_circle(size=75).encode(
            x=eje_x,
            y=eje_y,
            tooltip=[eje_x, eje_y]
        )
    elif opcion_grafico == "Violin Plot":
        grafico = alt.Chart(datos_filtrados).transform_density(
            eje_y,
            as_=[eje_y, 'density'],
            groupby=[eje_x]
        ).mark_area(orient='horizontal').encode(
            y=eje_x,
            x=alt.X('density:Q', stack='center', title=None),
            color=eje_x
        )

    # Mostrar el gráfico en la aplicación
    st.altair_chart(grafico, use_container_width=True)

except FileNotFoundError:
    st.error("Error: No se pudo encontrar el archivo en la ruta especificada.")
except Exception as error:
    st.error(f"Ocurrió un error al cargar el archivo: {error}")
