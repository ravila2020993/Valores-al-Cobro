
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta, date

st.set_page_config(page_title="Procesador de Fechas de Pago", layout="centered", page_icon="📆")
st.title("📆 Procesador de Fechas de Pago")

st.markdown("Subí un archivo Excel con columnas de importe y fecha, seleccioná fechas límites y días no laborables. El sistema ajustará automáticamente las fechas.")

uploaded_file = st.file_uploader("📤 Subí tu archivo Excel", type=["xlsx"])

fecha_inicio = st.date_input("📅 Ingresá la fecha de inicio")
fecha_fin = st.date_input("📅 Ingresá la fecha de finalización")

# Selección de días no laborables por calendario
dias_no_laborables = st.multiselect(
    "📌 Seleccioná los días no laborables (uno o varios):",
    options=pd.date_range(start=date.today(), end=date.today() + timedelta(days=365)).to_pydatetime(),
    format_func=lambda x: x.strftime('%Y-%m-%d')
)
dias_no_laborables = set([d.date() for d in dias_no_laborables])

def ajustar_fecha(fecha_original, dias_no_laborables, fecha_inicio):
    if pd.isnull(fecha_original):
        return None
    if fecha_original < fecha_inicio:
        diferencia_dias = (fecha_inicio - fecha_original).days
        if diferencia_dias > 30:
            return None
        else:
            nueva_fecha = fecha_inicio + timedelta(days=2)
    else:
        nueva_fecha = fecha_original + timedelta(days=2)
    while nueva_fecha in dias_no_laborables:
        nueva_fecha += timedelta(days=1)
    return nueva_fecha

def procesar_datos(df, fecha_inicio, fecha_fin, dias_no_laborables):
    importe_col = df.iloc[:, 6]  # Columna G
    fecha_col = df.iloc[:, 7]    # Columna H

    df_procesado = pd.DataFrame()
    df_procesado['Importe'] = importe_col
    df_procesado['Fecha Original'] = pd.to_datetime(fecha_col, errors='coerce').dt.date
    df_procesado['Fecha Ajustada'] = df_procesado['Fecha Original'].apply(
        lambda x: ajustar_fecha(x, dias_no_laborables, fecha_inicio)
    )

    df_filtrado = df_procesado[
        (df_procesado['Fecha Ajustada'].notnull()) & 
        (df_procesado['Fecha Ajustada'] <= fecha_fin)
    ]

    return df_filtrado[['Importe', 'Fecha Ajustada']]

if uploaded_file and fecha_inicio and fecha_fin:
    try:
        df = pd.read_excel(uploaded_file, header=0)

        resultado = procesar_datos(df, fecha_inicio, fecha_fin, dias_no_laborables)

        if not resultado.empty:
            st.success("✅ Procesamiento exitoso")
            st.dataframe(resultado)

            resumen = resultado.groupby('Fecha Ajustada')['Importe'].sum().reset_index()
            resumen = resumen.pivot_table(values='Importe', index=None, columns='Fecha Ajustada', aggfunc='sum')

            output = BytesIO()
            with pd.ExcelWriter(output) as writer:
                resultado.to_excel(writer, sheet_name="Detalle", index=False)
                resumen.to_excel(writer, sheet_name="Acumulado por Fecha", index=False)

            st.download_button("📥 Descargar archivo procesado", data=output.getvalue(), file_name="resultado.xlsx")
        else:
            st.warning("⚠️ No hay datos que cumplan con los criterios.")
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
