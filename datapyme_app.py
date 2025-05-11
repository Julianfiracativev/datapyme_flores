import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar el archivo Excel
df = pd.read_excel("DataFlores_Organizado.xlsx")

seccion = st.sidebar.radio("Menú", ["Inicio", "Ventas", "Inventario", "Clientes"])

# PANEL PRINCIPAL
st.markdown("## 🌸 DataPYME Flores – Panel de Análisis Comercial")

if seccion == "Inicio":
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de ventas", f"${df['total_venta'].sum():,}")
    col2.metric("Inventario disponible", f"{df['unidades_vendidas'].sum():,} tallos")
    col3.metric("Clientes frecuentes", df['cliente'].nunique())

    st.subheader("🔔 Alertas Detalladas")

    # Gráfico 1: Cajas sobrantes
    st.markdown("### 📦 Cajas sobrantes")
    cajas_sobrantes = df[df["cajas_vendidas"] > 10].groupby("tipo_flor")["cajas_vendidas"].sum().reset_index()
    fig1 = px.bar(cajas_sobrantes, x="tipo_flor", y="cajas_vendidas", color="tipo_flor", title="Flores con exceso de cajas")
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("🔍 *Estas flores tienen más de 10 cajas vendidas, lo cual podría indicar sobreinventario.*")

    # Gráfico 2: Clientes inactivos
    st.markdown("### 💤 Clientes inactivos")
    inactivos = df.groupby("cliente")["total_venta"].sum().reset_index()
    inactivos = inactivos[inactivos["total_venta"] < inactivos["total_venta"].quantile(0.25)]
    fig2 = px.bar(inactivos, x="cliente", y="total_venta", title="Clientes con compras muy bajas")
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("📉 *Clientes con menor nivel de compras. Puede ser momento de reactivarlos con promociones.*")

    # Gráfico 3: Ventas bajas por flor
    st.markdown("### 📉 Ventas bajas por flor")
    ventas_bajas = df.groupby("tipo_flor")["total_venta"].sum().reset_index().sort_values("total_venta").head(5)
    fig3 = px.bar(ventas_bajas, x="tipo_flor", y="total_venta", color="tipo_flor", title="Top 5 flores con menos ventas")
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("⚠️ *Estas flores tienen bajo rendimiento comercial. Evaluar si mantenerlas o mejorar su promoción.*")

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
