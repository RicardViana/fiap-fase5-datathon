# 🎓 Datathon FIAP – Fase 5

## 🧠 Modelo Preditivo de Risco de Defasagem Educacional

[![CCDS](https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter)](https://cookiecutter-data-science.drivendata.org/) 
![Python](https://img.shields.io/badge/Python-3.10-blue) 
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

## 📌 1. Introdução

Este projeto foi desenvolvido no contexto do **Datathon – Fase 5** da Pós-Tech em Data Analytics (FIAP | POSTECH).

O desafio consiste em analisar dados educacionais da **Associação Passos Mágicos**, organização com mais de 30 anos de atuação na transformação da vida de crianças e jovens em situação de vulnerabilidade social por meio da educação.

A proposta do trabalho foi:

* Realizar análise exploratória dos indicadores educacionais (2022–2024)
* Responder às dores de negócio apresentadas no briefing
* Construir um modelo preditivo de risco de defasagem
* Desenvolver uma aplicação em Streamlit para uso prático da instituição

---

## 🏫 2. Contexto do Negócio

A Associação Passos Mágicos realiza a **Pesquisa Extensiva do Desenvolvimento Educacional (PEDE)**, que consolida indicadores multidimensionais dos alunos.

O índice global utilizado é o:

### 🔎 Índice de Desenvolvimento Educacional (INDE)

O INDE é composto pelos seguintes indicadores:

| Indicador | Descrição                         |
| --------- | --------------------------------- |
| **IAN**   | Indicador de Adequação de Nível   |
| **IDA**   | Indicador de Aprendizagem |
| **IEG**   | Indicador de Engajamento          |
| **IAA**   | Indicador de Autoavaliação        |
| **IPS**   | Indicador Psicossocial            |
| **IPP**   | Indicador Psicopedagógico         |
| **IPV**   | Indicador de Ponto de Virada      |

As fórmulas oficiais e conceitos estão descritos no documento técnico do PEDE e o dicionário detalhado das variáveis encontra-se no documento oficial 

---

## 🎯 3. Objetivos do Projeto

### 📊 Análise Exploratória

Responder às questões propostas no briefing oficial :

* Perfil de defasagem (IAN)
* Evolução do desempenho acadêmico (IDA)
* Relação entre engajamento (IEG) desempenho (IDA) e ponto de virada (IPV)
* Coerência entre autoavaliação (IAA) desempenho real (IDA) e engajaento (IEG)
* Padrões psicossocial (IPS) que antecedem quedas de desempenho ou engajamento
* Aspectos psicopedagógico (IPP) para confirmar (ou contradizer) a defasagem (IAN)
* Fatores associados ao Ponto de Virada (IPV) ao longo do tempo
* Multidimensionalidade dos indicadores
* Efetividade do programa ao longo das fases (Quartzo, Ágata, Ametista, Topázio)  

---

### 🤖 Modelagem Preditiva

Desenvolver um modelo capaz de:

✔ Identificar risco de defasagem antes da queda do desempenho  
✔ Estimar probabilidade individual de risco de defasagem
✔ Apoiar decisões pedagógicas preventivas  

---

# 🧪 4. Metodologia

## 4.1 Preparação dos Dados e Feature Engineering

A etapa de preparação foi estruturada para garantir consistência, evitar vazamento de informação e aumentar capacidade preditiva.

### 🔹 Padronização e Tratamento

Foram realizadas as seguintes transformações:

* Padronização da variável **gênero**
* Padronização e validação da variável **idade**
* Tratamento da coluna **INDE_2024**
* Extração da **fase numérica** a partir da descrição textual
* Remoção de variáveis com risco de vazamento de informação:

  * `ian`
  * `defasagem`

Essa etapa garantiu integridade estatística e consistência no pipeline.

---

### 🔹 Criação de Novas Variáveis (Feature Engineering)

Foram criadas variáveis estratégicas para capturar padrões multidimensionais:

* `media_academica` → média entre Matemática, Português e Inglês
* `media_comportamental` → média entre IAA, IEG, IPS e IPP
* `delta_inde` → evolução do INDE entre períodos
* `risco_defasagem_atual` → variável target binária

A engenharia de atributos teve como objetivo capturar sinais precoces de risco antes da consolidação da defasagem.

---

## 4.2 Definição da Variável Target

O risco de defasagem foi definido com base no indicador oficial de adequação de nível:

```
IAN <= 5  → Risco de Defasagem
IAN > 5   → Sem Risco
```

A variável `risco_defasagem_atual` foi construída de forma binária para tratar o problema como **classificação supervisionada**.

---

## 4.3 Separação dos Dados

Foi adotada uma estratégia mais robusta do que um simples split aleatório.

### 🔹 Estratégia utilizada:

* **Treino:** Dados de 2022 e 2023
* **Teste Real:** Dados de 2024

Essa abordagem configura um **split temporal**, simulando cenário real de previsão futura.

Além disso:

* Estratificação da variável target
* Padronização via `StandardScaler` quando necessário

Essa decisão aumenta a validade prática do modelo.

---

## 4.4 Modelagem Preditiva

Foram testados diferentes algoritmos de classificação:

* Logistic Regression
* Random Forest
* MLP (Multi-Layer Perceptron)
* XGBoost

### 🔎 Critérios de comparação

Os modelos foram comparados com base em:

* Accuracy
* ROC AUC
* PR AUC

A escolha do modelo final considerou:

* Performance média em validação cruzada
* Estabilidade
* Capacidade de generalização no teste temporal (2024)

O modelo selecionado foi salvo e disponibilizado na aplicação via:

```python
joblib.load("models/modelo_passos_magicos.pkl")
```

O threshold ótimo também foi armazenado em arquivo `.pkl`.

---

## 4.5 Avaliação dos Resultados

A avaliação foi conduzida em múltiplas camadas para garantir robustez.

### 🔹 Validação

* Cross-validation no conjunto de treino
* Teste temporal utilizando 2024 como base real

### 🔹 Métricas utilizadas

* Matriz de Confusão
* Precision
* Recall
* F1-Score
* ROC AUC
* PR AUC

### 🔹 Ajuste de Threshold

Foi realizado ajuste do ponto de corte com base no trade-off entre Precision e Recall, priorizando:

> Minimizar falsos negativos (evitar deixar alunos em risco sem intervenção).

---

## 📊 5. Principais Insights

* Em desenvolvimento

---

## 💻 6. Aplicação em Streamlit

Foi desenvolvida uma aplicação interativa utilizando **Streamlit**.

### 🔹 Funcionalidades:

* Inserção manual dos indicadores do aluno
* Cálculo automático de IDA (quando aplicável)
* Probabilidade de risco de defasagem
* Classificação baseada em threshold otimizado
* Explicabilidade com SHAP (quando aplicável ao modelo)
* Recomendações pedagógicas automáticas

### 🌐 Deploy

Aplicação disponível em:

🔗 [https://fiap-fase5-datathon.streamlit.app/](https://fiap-fase5-datathon.streamlit.app/)

---

## 📂 7. Estrutura do Repositório

```
├── .streamlit/
    ├── config.toml
├── data/
    ├── external/
│   ├── interim/
│   ├── processed/
        ├── Base de Dados PEDE.xlsx
        ├── base_processada.xlsx
        └── idacao_app_passos_magicos.xlsx
│   └── raw/
        └── BASE DE DADOS PEDE 2024 - DATATHON.xlsx
├── docs/
├── models/
│   ├── modelo_passos_magicos.pkl
│   └── config_passos_magicos.pkl
├── notebooks/
│   └── Datathon_FIAP_Fase_5.ipynb
├── references/
│   ├── Dicionário Dados Datathon.pdf
    ├── PEDE_ Pontos importantes.docx
│   └── POSTECH - DTAT - Datathon - Fase 5.pdf
├── reports/
├── .gitignore
├── LICENSE
├── README.md
├── app.py
├── pyproject.toml
└── requirements.txt
```
---

## 📚 8. Documentação Técnica

A documentação completa inclui:

* Dicionário de variáveis
* Fórmulas oficiais dos indicadores
* Critério de definição de risco

---

## 👨‍💻 9. Equipe

* [Elton José Araujo Silva](https://www.linkedin.com/in/elton-araujo-silva/)
* [Leonardo Fajoli Formigon](https://www.linkedin.com/in/leonardo-formigon-63052320b/)
* [Lucas Augusto Fernandes de Lira](https://www.linkedin.com/in/lucas--lira-/)
* [Mariana Domingues Brandão](https://www.linkedin.com/in/maridbrandao)
* [Ricardo Vieira Viana](https://www.linkedin.com/in/ricardvviana)

---

## 🌍 10. Impacto Social

Este projeto demonstra como:

* Ciência de Dados aplicada ao terceiro setor
* Modelos preditivos com interpretabilidade
* Analytics orientado a impacto social

podem auxiliar na transformação educacional de jovens em vulnerabilidade.

---

## 📜 Licença

Este projeto está sob licença MIT.