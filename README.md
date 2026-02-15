# 🧠 Modelo de Machine Learning para Análise de Risco de Defasagem

## Datathon – Fase 5 | Associação Passos Mágicos

[![Python](https://img.shields.io/badge/Python-3.9-blue)]()
![Status](https://img.shields.io/badge/Status-Concluído-success)

---

## 📋 Sobre o Projeto

Este projeto foi desenvolvido no contexto do **Datathon – Fase 5**, promovido pela Pós-Tech em Data Analytics, utilizando a base de dados educacionais da Associação **Passos Mágicos**.

A proposta consiste em realizar uma análise exploratória e preditiva sobre indicadores educacionais e psicossociais de alunos em situação de vulnerabilidade social, com o objetivo de:

* Identificar padrões de defasagem
* Analisar evolução de desempenho ao longo dos anos
* Construir um modelo preditivo de risco
* Apoiar decisões estratégicas da instituição

---

## 🏥 Contexto do Problema

A Associação Passos Mágicos atua há mais de 30 anos transformando a vida de crianças e jovens por meio da educação.

O desafio proposto no Datathon envolve analisar dados educacionais dos anos de:

* 2022
* 2023
* 2024

Os indicadores analisados incluem:

* **IAN** – Índice de Adequação de Nível
* **IDA** – Índice de Desempenho Acadêmico
* **IEG** – Índice de Engajamento
* **IAA** – Índice de Autoavaliação
* **IPS** – Índice Psicossocial
* **IPP** – Índice Psicopedagógico
* **IPV** – Índice de Ponto de Virada
* **INDE** – Índice Global do Aluno

O objetivo central foi responder às dores de negócio e desenvolver um modelo capaz de prever o risco de defasagem antes que ele aconteça.

---

## 🎯 Objetivos do Projeto

### 🔎 Análise Exploratória

* Avaliar a evolução do IAN ao longo do tempo
* Identificar tendências no IDA
* Verificar relação entre engajamento (IEG) e desempenho (IDA/IPV)
* Analisar coerência entre autoavaliação (IAA) e desempenho real
* Investigar padrões psicossociais (IPS) associados à queda de desempenho
* Avaliar multidimensionalidade dos indicadores

### 🤖 Modelagem Preditiva

* Criar variável target de risco de defasagem
* Realizar feature engineering
* Separar dados em treino e teste
* Treinar modelo de **Perceptron de Múltiplas Camadas (MLPClassifier)**
* Avaliar métricas de desempenho
* Gerar probabilidade de risco para cada aluno

---

## 🧪 Metodologia

A modelagem seguiu as seguintes etapas:

### 1️⃣ Pré-processamento

* Tratamento de valores ausentes
* Padronização com `StandardScaler`
* Seleção de variáveis relevantes

### 2️⃣ Feature Engineering

* Criação de variável binária de risco
* Combinação de indicadores multidimensionais
* Normalização dos dados

### 3️⃣ Separação dos Dados

* `train_test_split`
* Estratificação da variável target

### 4️⃣ Modelagem

Foi utilizado:

```python
MLPClassifier(hidden_layer_sizes=(100, 50),
              activation='relu',
              solver='adam',
              max_iter=500,
              random_state=42)
```

Modelo baseado em rede neural artificial (Perceptron Multicamadas).

### 5️⃣ Avaliação

* Accuracy
* Precision
* Recall
* F1-Score
* Matriz de Confusão
* Análise de probabilidade de risco

---

## 📊 Principais Insights Analíticos

* Alunos com **baixo IEG + baixo IPS** apresentam maior probabilidade de queda no IDA.
* Existe correlação moderada entre IAA e desempenho real.
* O IPV é fortemente influenciado por engajamento contínuo.
* A combinação **IDA + IEG + IPS** é um forte preditor do INDE.
* Padrões psicossociais antecedem quedas acadêmicas.

---

## 🚀 Aplicação no Streamlit

Foi desenvolvida uma aplicação em **Streamlit** para permitir que a Passos Mágicos:

* Insira indicadores do aluno
* Obtenha probabilidade de risco
* Visualize classificação preditiva
* Apoie tomada de decisão pedagógica

Deploy realizado via Streamlit Community Cloud.

---

## 📈 Estrutura do Projeto

A organização segue o padrão **Cookiecutter Data Science**, adaptado ao Datathon:

```
├── .streamlit/
│   └── config.toml
├── data/
│   ├── raw/
│   ├── processed/
│   ├── interim/
│   └── external/
├── docs/
├── models/
│   └── modelo_risco_defasagem_mlp.joblib
├── notebooks/
│   └── Perceptron de múltiplas camadas.ipynb
├── references/
│   └── POSTECH - DTAT - Datathon - Fase 5.pdf
├── reports/
├── app.py
├── requirements.txt
└── README.md
```

---

## 📘 Documentação

A documentação técnica inclui:

* Explicação das variáveis
* Pipeline de modelagem
* Estratégia de validação
* Justificativa da escolha do modelo MLP

---

## 👨‍💻 Equipe

* [Elton José Araujo Silva](https://www.linkedin.com/in/elton-araujo-silva/)
* [Leonardo Fajoli Formigon](https://www.linkedin.com/in/leonardo-formigon-63052320b/)
* [Lucas Augusto Fernandes de Lira](https://www.linkedin.com/in/lucas--lira-/)
* [Mariana Domingues Brandão](https://www.linkedin.com/in/maridbrandao)
* [Ricardo Vieira Viana](https://www.linkedin.com/in/ricardvviana)
---

## 📌 Conclusão

O modelo desenvolvido permite:

* Antecipar risco de defasagem
* Apoiar decisões pedagógicas
* Identificar padrões críticos
* Gerar impacto social real

O projeto combina **análise estatística, storytelling e Machine Learning aplicado ao terceiro setor**, reforçando o papel da ciência de dados como ferramenta de transformação social.

---

## 📜 Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.