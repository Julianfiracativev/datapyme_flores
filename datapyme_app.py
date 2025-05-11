import streamlit as st
import pandas as pd

# Cargar el archivo Excel
df = pd.read_excel("DataFlores_Organizado.xlsx")

# Sidebar
seccion = st.sidebar.radio("Menú", ["Inicio", "Ventas", "Inventario", "Clientes"])

# Título principal
st.markdown("## 🌸 DataPYME Flores – Panel de Análisis Comercial")

# SECCIÓN: INICIO
if seccion == "Inicio":
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de ventas", f"${df['total_venta'].sum():,}")
    col2.metric("Inventario disponible", f"{df['unidades_vendidas'].sum():,} tallos")
    col3.metric("Clientes frecuentes", df['cliente'].nunique())

    st.subheader("🔔 Alertas")
    alertas = pd.DataFrame({
        "Tipo": ["Ventas bajas", "Cajas sobrantes", "Clientes inactivos"],
        "Cantidad": [4, 6, 3]
    })
    st.bar_chart(alertas.set_index("Tipo"))

    st.subheader("✅ Ver sugerencias")
    st.success("📌 Aplicar descuento a Rosa Premium")
    st.warning("👮 Revisar cliente: FloralExpress")
    st.error("🔹 Exceso de stock en Orquídea Blanca")
    st.caption("🔗 Conectado a Excel - Simulado")

# SECCIÓN: VENTAS
elif seccion == "Ventas":
    st.subheader("📈 Detalle de Ventas por Flor")
    ventas_por_flor = df.groupby("tipo_flor")["total_venta"].sum().reset_index()
    st.dataframe(ventas_por_flor)
    st.bar_chart(ventas_por_flor.set_index("tipo_flor"))

# SECCIÓN: INVENTARIO
elif seccion == "Inventario":
    st.subheader("📦 Inventario por ciudad (en tallos)")
    inv_por_ciudad = df.groupby("ciudad")["unidades_vendidas"].sum().reset_index()
    st.bar_chart(inv_por_ciudad.set_index("ciudad"))

# SECCIÓN: CLIENTES
elif seccion == "Clientes":
    st.subheader("🧑‍💼 Lista de Clientes")
    st.dataframe(df[["cliente", "ciudad"]].drop_duplicates())
    st.caption(f"Clientes únicos: {df['cliente'].nunique()}")
