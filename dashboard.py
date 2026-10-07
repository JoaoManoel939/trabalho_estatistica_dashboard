import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

plt.rcParams["figure.max_open_warning"] = 0
st.set_page_config(page_title="Painel - Statlog Heart", layout="wide")

df = pd.read_csv("Heart_disease_statlog.csv")

df = df.rename(columns={
    "age": "Idade",
    "sex": "Sexo",
    "cp": "Tipo de dor",
    "trestbps": "Pressão",
    "chol": "Colesterol",
    "fbs": "Glicemia alta",
    "restecg": "ECG repouso",
    "thalach": "Freq. máxima",
    "exang": "Angina exercício",
    "oldpeak": "Oldpeak",
    "slope": "Inclinação ST",
    "ca": "Vasos",
    "thal": "Cintilografia",
    "target": "Doença",
})

df["Sexo"] = df["Sexo"].map({0: "Feminino", 1: "Masculino"})
df["Glicemia alta"] = df["Glicemia alta"].map({0: "Não", 1: "Sim"})
df["Angina exercício"] = df["Angina exercício"].map({0: "Não", 1: "Sim"})
df["Tipo de dor"] = df["Tipo de dor"].map({
    0: "Angina típica",
    1: "Angina atípica",
    2: "Dor não anginosa",
    3: "Assintomático",
})
df["ECG repouso"] = df["ECG repouso"].map({
    0: "Normal",
    1: "Anormalidade ST-T",
    2: "Hipertrofia ventricular",
})
df["Inclinação ST"] = df["Inclinação ST"].map({0: "Ascendente", 1: "Plano", 2: "Descendente"})
df["Cintilografia"] = df["Cintilografia"].map({1: "Normal", 2: "Defeito fixo", 3: "Defeito reversível"})
df["Vasos"] = df["Vasos"].astype(str)
df["Doença (0/1)"] = df["Doença"]
df["Doença"] = df["Doença"].map({0: "Ausente", 1: "Presente"})
df["Faixa etária"] = pd.cut(
    df["Idade"],
    bins=[20, 40, 50, 60, 70, 80],
    labels=["20-39", "40-49", "50-59", "60-69", "70-79"],
    right=False,
).astype(str)

numericas = ["Idade", "Pressão", "Colesterol", "Freq. máxima", "Oldpeak"]
categoricas = ["Sexo", "Tipo de dor", "Glicemia alta", "ECG repouso", "Angina exercício",
               "Inclinação ST", "Vasos", "Cintilografia", "Faixa etária"]

df["Atípico"] = False
for coluna in numericas:
    q1 = df[coluna].quantile(0.25)
    q3 = df[coluna].quantile(0.75)
    iqr = q3 - q1
    atipico_coluna = (df[coluna] < q1 - 1.5 * iqr) | (df[coluna] > q3 + 1.5 * iqr)
    df["Atípico"] = df["Atípico"] | atipico_coluna

ordem_doenca = ["Ausente", "Presente"]
cores = {"Ausente": "steelblue", "Presente": "tomato"}

st.title("Painel - Statlog Heart Disease")

st.sidebar.header("Filtros")
filtro = pd.Series(True, index=df.index)

for coluna in numericas:
    minimo = df[coluna].min().item()
    maximo = df[coluna].max().item()
    faixa = st.sidebar.slider(coluna, minimo, maximo, (minimo, maximo))
    filtro = filtro & df[coluna].between(faixa[0], faixa[1])

with st.sidebar.expander("Variáveis categóricas"):
    for coluna in categoricas + ["Doença"]:
        opcoes = sorted(df[coluna].unique())
        escolhidas = st.multiselect(coluna, opcoes, default=opcoes)
        filtro = filtro & df[coluna].isin(escolhidas)

if st.sidebar.checkbox("Excluir valores atípicos (critério do IQR)"):
    filtro = filtro & ~df["Atípico"]

dados = df[filtro]

if dados.empty:
    st.warning("Nenhum registro atende aos filtros selecionados.")
    st.stop()

indicador1, indicador2, indicador3 = st.columns(3)
indicador1.metric("Registros", f"{len(dados)} de {len(df)}")
indicador2.metric("Idade média", f"{dados['Idade'].mean():.1f}")
indicador3.metric("Proporção com presença", f"{dados['Doença (0/1)'].mean():.1%}")

aba_distribuicoes, aba_relacoes, aba_categorias, aba_registros = st.tabs(
    ["Distribuições", "Relações", "Categorias", "Registros"]
)

with aba_distribuicoes:
    variavel = st.selectbox("Variável numérica", numericas)
    classes = st.slider("Número de classes", 5, 50, 20)
    esquerda, direita = st.columns(2)
    with esquerda:
        fig, ax = plt.subplots()
        sns.histplot(data=dados, x=variavel, hue="Doença", hue_order=ordem_doenca,
                     palette=cores, bins=classes, ax=ax)
        st.pyplot(fig)
    with direita:
        fig, ax = plt.subplots()
        sns.boxplot(data=dados, x="Doença", y=variavel, hue="Doença", order=ordem_doenca,
                    hue_order=ordem_doenca, palette=cores, legend=False, ax=ax)
        st.pyplot(fig)
    st.dataframe(dados.groupby("Doença")[variavel].describe())

with aba_relacoes:
    esquerda, direita = st.columns(2)
    with esquerda:
        eixo_x = st.selectbox("Eixo X", numericas, index=0)
        eixo_y = st.selectbox("Eixo Y", numericas, index=3)
        mostrar_reta = st.checkbox("Mostrar reta de regressão")
        fig, ax = plt.subplots()
        sns.scatterplot(data=dados, x=eixo_x, y=eixo_y, hue="Doença", hue_order=ordem_doenca,
                        palette=cores, ax=ax)
        if mostrar_reta and len(dados) > 2:
            sns.regplot(data=dados, x=eixo_x, y=eixo_y, scatter=False, color="black", ax=ax)
        st.pyplot(fig)
        st.write(f"Correlação entre as duas variáveis: {dados[eixo_x].corr(dados[eixo_y]):.3f}")
    with direita:
        metodo = st.radio("Coeficiente de correlação", ["pearson", "spearman"], horizontal=True)
        fig, ax = plt.subplots()
        sns.heatmap(dados[numericas + ["Doença (0/1)"]].corr(method=metodo), annot=True,
                    fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
        st.pyplot(fig)

with aba_categorias:
    categoria = st.selectbox("Variável categórica", categoricas)
    ordem_categorias = sorted(dados[categoria].unique())
    proporcao = dados.groupby(categoria)["Doença (0/1)"].agg(["mean", "count"]).reset_index()
    proporcao.columns = [categoria, "Proporção com presença", "Registros"]
    esquerda, direita = st.columns(2)
    with esquerda:
        fig, ax = plt.subplots()
        sns.countplot(data=dados, x=categoria, hue="Doença", order=ordem_categorias,
                      hue_order=ordem_doenca, palette=cores, ax=ax)
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig)
    with direita:
        fig, ax = plt.subplots()
        sns.barplot(data=proporcao, x=categoria, y="Proporção com presença",
                    order=ordem_categorias, color="tomato", ax=ax)
        ax.set_ylim(0, 1)
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig)
    st.dataframe(proporcao)

with aba_registros:
    st.dataframe(dados)
    st.download_button(
        "Baixar registros filtrados (CSV)",
        dados.to_csv(index=False),
        "registros_filtrados.csv",
        "text/csv",
    )
