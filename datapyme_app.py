import streamlit as st
import pandas as pd

# Cargar el archivo Excel
df = pd.read_excel("DataFlores_Organizado.xlsx")

# Sidebar
seccion = st.sidebar.radio("Menú", ["Inicio", "Ventas", "Inventario", "Clientes"])

# Título principal
st.markdown("## 🌸 DataPYME Flores – Panel de Análisis Comercial")
# INICIO
if seccion == "Inicio":
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de ventas", f"${df['total_venta'].sum():,}")
    col2.metric("Inventario disponible", f"{df['unidades_vendidas'].sum():,} tallos")
    col3.metric("Clientes frecuentes", df['cliente'].nunique())

    st.subheader("🔔 Alertas Detalladas")

    # 1. ALERTA – Cajas sobrantes (simulamos cajas con muchas unidades)
    st.markdown("### 📦 Cajas sobrantes")
    sobrantes = df[df["cajas_vendidas"] > 10].groupby("tipo_flor")["cajas_vendidas"].sum().reset_index()
    st.bar_chart(sobrantes.set_index("tipo_flor"))

    # 2. ALERTA – Clientes inactivos (clientes con pocas compras)
    st.markdown("### 💤 Clientes inactivos")
    inactivos = df.groupby("cliente")["total_venta"].sum().reset_index()
    inactivos = inactivos[inactivos["total_venta"] < inactivos["total_venta"].quantile(0.25)]
    st.bar_chart(inactivos.set_index("cliente"))

    # 3. ALERTA – Ventas bajas (flores con menor ingreso)
    st.markdown("### 📉 Ventas bajas por flor")
    ventas_bajas = df.groupby("tipo_flor")["total_venta"].sum().reset_index()
    ventas_bajas = ventas_bajas.sort_values("total_venta").head(5)
    st.bar_chart(ventas_bajas.set_index("tipo_flor"))

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
