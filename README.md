# Painel Exploratório - Statlog Heart Disease

Projeto da disciplina de Estatística e Probabilidade: análise exploratória de dados com Pandas e dashboard interativo com Streamlit.

**Autores:** Nome do integrante 1 e Nome do integrante 2
**Disciplina:** Estatística e Probabilidade
**Instituição:** Nome da instituição
**Professor(a):** Nome do(a) professor(a)

## Sobre o projeto

O projeto reúne duas partes:

1. **Análise exploratória** (`analise_exploratoria.ipynb`): carregamento, inspeção e tratamento dos dados, estatísticas descritivas, distribuições, correlações e probabilidades.
2. **Dashboard interativo** (`dashboard.py`): painel com filtros que permite explorar os dados de forma independente.

## Conjunto de dados

- **Nome:** Statlog (Heart)
- **Fonte:** UCI Machine Learning Repository
- **Tamanho:** 270 registros e 14 variáveis, sem valores ausentes
- **Conteúdo:** atributos clínicos de pacientes e a indicação de presença ou ausência de doença cardíaca

| Coluna original | Nome no projeto | Descrição |
|---|---|---|
| age | Idade | Idade em anos |
| sex | Sexo | Feminino ou masculino |
| cp | Tipo de dor | Tipo de dor no peito |
| trestbps | Pressão | Pressão arterial em repouso (mm Hg) |
| chol | Colesterol | Colesterol sérico (mg/dl) |
| fbs | Glicemia alta | Glicemia em jejum acima de 120 mg/dl |
| restecg | ECG repouso | Resultado do eletrocardiograma em repouso |
| thalach | Freq. máxima | Frequência cardíaca máxima atingida (bpm) |
| exang | Angina exercício | Angina induzida por exercício |
| oldpeak | Oldpeak | Depressão do segmento ST induzida pelo exercício |
| slope | Inclinação ST | Inclinação do segmento ST no pico do exercício |
| ca | Vasos | Número de vasos principais coloridos por fluoroscopia (0 a 3) |
| thal | Cintilografia | Resultado da cintilografia com tálio |
| target | Doença | Ausente ou presente |

O arquivo original traz as categorias como números. Os rótulos usados no projeto foram definidos a partir da documentação do conjunto de dados.

## Tratamento dos dados

- Verificação de valores ausentes e linhas duplicadas.
- Renomeação das colunas e substituição dos códigos numéricos por rótulos.
- Criação da faixa etária e de uma coluna numérica (0 ou 1) para a variável alvo.
- Identificação de valores atípicos pelo critério do IQR (1,5 vezes a amplitude interquartil). Os registros são mantidos e marcados em uma coluna, e o dashboard permite excluí-los por meio de um filtro.

## Funcionalidades do dashboard

- **Filtros** na barra lateral: variáveis numéricas (faixas de valores), variáveis categóricas (seleção múltipla) e exclusão de valores atípicos.
- **Indicadores** que acompanham os filtros: número de registros, idade média e proporção com presença da doença.
- **Distribuições:** histograma e boxplot de uma variável numérica à escolha, separados por presença da doença, com tabela de estatísticas descritivas.
- **Relações:** gráfico de dispersão entre duas variáveis numéricas, reta de regressão opcional e mapa de calor de correlação (Pearson ou Spearman).
- **Categorias:** contagem por categoria e proporção com presença da doença em cada categoria.
- **Registros:** tabela com os dados filtrados e download em CSV.

## Estrutura do repositório

```
.
├── analise_exploratoria.ipynb
├── dashboard.py
├── Heart_disease_statlog.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Como executar

É necessário ter o Python 3.9 ou superior instalado.

1. Clone o repositório e entre na pasta:

   ```
   git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
   cd NOME-DO-REPOSITORIO
   ```

2. (Opcional) Crie e ative um ambiente virtual:

   ```
   python -m venv .venv
   ```

   No Windows: `.venv\Scripts\activate`
   No Linux ou macOS: `source .venv/bin/activate`

3. Instale as dependências:

   ```
   pip install -r requirements.txt
   ```

4. Para a análise exploratória, abra `analise_exploratoria.ipynb` no Jupyter ou no VS Code e execute as células em ordem.

5. Para o dashboard, execute dentro da pasta do projeto:

   ```
   streamlit run dashboard.py
   ```

   O painel abre no navegador, normalmente em `http://localhost:8501`.

## Tecnologias

Python, Pandas, NumPy, Matplotlib, Seaborn e Streamlit.

## Referência

Statlog (Heart). UCI Machine Learning Repository. Consulte a página do conjunto de dados no repositório para a licença e a citação oficial.
