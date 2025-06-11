import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Demanda de Transporte em Florianópolis", layout="wide")
st.title("🚌 Análise da Demanda e Vulnerabilidade no Transporte Público")

# Upload da base de dados
uploaded_file = st.file_uploader("Envie a base 'base_unificada_limpa.xlsx'", type="xlsx")
if uploaded_file:
    df = pd.read_excel(uploaded_file, index_col=0)
    df.columns = [
        "Quilometragem", "Passageiros", "Capacidade",
        "Gini", "Remuneração", "PIB_per_capita",
        "Crescimento_PIB", "Desemprego"
    ]
    
    df = df.fillna(df.mean(numeric_only=True))
    df["Eficiência"] = df["Capacidade"] / df["Quilometragem"]
    df["Vulnerabilidade"] = (1 / df["Remuneração"]) + df["Desemprego"]

    st.sidebar.header("Filtros")
    anos = df.index.tolist()
    ano_selecionado = st.sidebar.selectbox("Selecione o ano", anos)

    df_ano = df.loc[[ano_selecionado]]

    st.subheader(f"Indicadores do ano {ano_selecionado}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Passageiros", f"{int(df_ano['Passageiros'].values[0]):,}".replace(",", "."))
    col2.metric("Eficiência", f"{df_ano['Eficiência'].values[0]:.2f}")
    col3.metric("Vulnerabilidade", f"{df_ano['Vulnerabilidade'].values[0]:.2f}")

    st.divider()

    st.subheader("Correlações entre variáveis")
    corr = df.corr().round(2)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    st.divider()

    st.subheader("Vulnerabilidade x Eficiência")
    fig2 = px.scatter(
        df,
        x="Eficiência",
        y="Vulnerabilidade",
        text=df.index,
        color="Passageiros",
        size="Passageiros",
        color_continuous_scale="Viridis",
        labels={"Eficiência": "Eficiência do Transporte", "Vulnerabilidade": "Vulnerabilidade Socioeconômica"},
        title="Quanto menor a eficiência, maior a vulnerabilidade"
    )
    fig2.update_traces(textposition="top center")
    st.plotly_chart(fig2, use_container_width=True)
