# 📂 Estrutura de Projeto e Arquivos de Configuração

Este documento descreve a organização das pastas e a finalidade dos arquivos de configuração encontrados neste repositório.

---

## 🏛️ Estrutura de Pastas (Padrão Cookiecutter Data Science)

Abaixo estão as pastas principais utilizadas para manter o projeto organizado e reprodutível:

### 📊 Dados (`data/`)
* **`raw/`**: Dados originais, imutáveis e em seu estado bruto.
* **`interim/`**: Dados intermediários que passaram por algum processo de limpeza ou transformação.
* **`processed/`**: Conjuntos de dados finais, prontos para serem usados nos modelos de Machine Learning.
* **`external/`**: Dados de fontes externas ou de terceiros usados no projeto.

### 💻 Código e Desenvolvimento
* **`notebooks/`**: Arquivos Jupyter Notebook para análise exploratória, prototipagem e experimentos.
reaproveitáveis.
* **`models/`**: Local para salvar modelos treinados (arquivos .pkl, .h5) e pesos de redes neurais.

### 📝 Documentação e Relatórios
* **`reports/`**: Análises geradas, gráficos, tabelas e apresentações finais para stakeholders.
* **`docs/`**: Documentação técnica do projeto, como manuais e referências de API.
* **`references/`**: Manuais, dicionários de dados e notas de pesquisa.