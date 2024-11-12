import streamlit as st
import pandas as pd
import altair as alt


st.sidebar.header("Ajustes de visualización")
st.title("Visualización de Accidentes de Autos (2010-2018)")
st.sidebar.image("Auto_accidentes.jpg", caption="Análisis de accidentes")

archivo_datos = "ped_crashes.csv"


try:
    
    datos_accidentes = pd.read_csv(archivo_datos)
    st.write("Datos cargados exitosamente:", datos_accidentes.head())
    
    
    opcion_grafico = st.sidebar.radio(
        "Selecciona el tipo de gráfico para visualizar", 
        options=["Líneas", "Barras", "Dispersión", "Violin Plot"]
    )
    
    
    st.markdown(f"## Análisis de Accidentes: {opcion_grafico}")
    
    
    columna_filtro = st.sidebar.selectbox("Elige una columna para filtrar los datos", datos_accidentes.columns)
    valores_opciones = datos_accidentes[columna_filtro].unique()
    seleccion_filtros = st.sidebar.multiselect("Selecciona valores para incluir en el análisis", valores_opciones)
    
    
    if seleccion_filtros:
        datos_filtrados = datos_accidentes[datos_accidentes[columna_filtro].isin(seleccion_filtros)]
    else:
        datos_filtrados = datos_accidentes

    
    st.sidebar.subheader("Resumen de Datos")
    st.sidebar.write(datos_filtrados.describe())

    
    eje_x = st.sidebar.selectbox("Selecciona la variable para el eje X", datos_accidentes.columns)
    eje_y = st.sidebar.selectbox("Selecciona la variable para el eje Y", datos_accidentes.columns)

    
    if opcion_grafico == "Líneas":
        grafico = alt.Chart(datos_filtrados).mark_line(color="blue").encode(
            x=eje_x,
            y=eje_y,
            tooltip=[eje_x, eje_y]
        )
    elif opcion_grafico == "Barras":
        grafico = alt.Chart(datos_filtrados).mark_bar(color="green").encode(
            x=eje_x,
            y=eje_y,
            tooltip=[eje_x, eje_y]
        )
    elif opcion_grafico == "Dispersión":
        grafico = alt.Chart(datos_filtrados).mark_circle(size=75, color="red").encode(
            x=eje_x,
            y=eje_y,
            tooltip=[eje_x, eje_y, columna_filtro]
        )
    elif opcion_grafico == "Violin Plot":
        grafico = alt.Chart(datos_filtrados).transform_density(
            eje_y,
            as_=[eje_y, 'density'],
            groupby=[eje_x]
        ).mark_area(orient='horizontal', color="purple").encode(
            y=eje_x,
            x=alt.X('density:Q', stack='center', title=None),
            color=eje_x
        )

    
    if "año" in datos_accidentes.columns:
        slider_tiempo = alt.binding_range(min=datos_filtrados["año"].min(), max=datos_filtrados["año"].max(), step=1)
        selector_tiempo = alt.selection_single(name="Año", fields=['año'], bind=slider_tiempo)
        grafico = grafico.add_selection(selector_tiempo).transform_filter(selector_tiempo)

    
    st.altair_chart(grafico, use_container_width=True)

    
    @st.cache_data
    def convertir_csv(df):
        return df.to_csv(index=False).encode("utf-8")
    
    
    archivo_csv = convertir_csv(datos_filtrados)
    st.sidebar.download_button(
        label="Descargar datos filtrados como CSV",
        data=archivo_csv,
        file_name="datos_filtrados.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.error("Error: No se pudo encontrar el archivo en la ruta especificada.")
except Exception as error:
    st.error(f"Ocurrió un error al cargar el archivo: {error}")
