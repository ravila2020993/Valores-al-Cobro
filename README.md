# 📆 Procesador de Fechas de Pago

Esta app permite procesar archivos Excel con fechas de cobro y ajustar automáticamente las fechas teniendo en cuenta:

- Una fecha de inicio mínima.
- Días no laborables seleccionables por calendario.
- Una fecha de finalización límite.

---

## 🧩 Cómo usar

1. Subí un archivo `.xlsx` con:
   - La columna **G** con importes.
   - La columna **H** con fechas originales.

2. Elegí:
   - Fecha de inicio.
   - Fecha de fin.
   - Días no laborables.

3. La app ajustará las fechas automáticamente:
   - Si la fecha es anterior a la de inicio, y la diferencia es menor o igual a 30 días, se mueve 2 días adelante.
   - Si no, se suma 2 días.
   - Luego se evita que caiga en días no laborables.

4. Podés descargar el resultado con:
   - Una hoja con el detalle ajustado.
   - Una hoja resumen con el total acumulado por fecha.

---

## 📦 Requisitos

Instalación automática vía `requirements.txt`:

```
streamlit
pandas
openpyxl
```

---

## 🚀 Desplegar en Streamlit Cloud

1. Subí este repositorio a GitHub.
2. En [streamlit.io/cloud](https://streamlit.io/cloud):
   - Elegí el archivo principal: `app_fechas_pago_v3.py`.
   - Verificá que el `requirements.txt` esté presente.

---

## 🧑‍💻 Autor

- Ramiro Ávila — CFO & Consultor Agroindustrial