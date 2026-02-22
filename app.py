# Importar bibliotecas padrão
import io
import re
import unicodedata
import os
import datetime

# Importar bibliotecas de terceiros
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
import streamlit as st

# Variável de debug
validar_shap = 'n'

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Predição de Risco de Defasagem",
    page_icon="🎓",
    layout="centered"
)

# FUNÇÕES DE PREPARO DE DADOS
def coerce_numeric(s):
    return pd.to_numeric(s, errors="coerce")

def extrair_fase(valor):
    if pd.isna(valor):
        return np.nan
    valor = str(valor).lower()
    if "alfa" in valor:
        return 0
    m = re.search(r"fase\s*(\d+)", valor)
    if m:
        return int(m.group(1))
    return np.nan

def padronizar_genero(df):
    df = df.copy()
    if "genero" in df.columns:
        df["genero"] = df["genero"].astype(str).str.strip().str.lower()
        map_genero = {
            "menino": "masculino", "masculino": "masculino",
            "menina": "feminino", "feminino": "feminino"
        }
        df["genero"] = df["genero"].map(map_genero)
    return df

def padronizar_idade(df):
    df = df.copy()
    if "idade" not in df.columns:
        return df
    s = df["idade"]
    dt = pd.to_datetime(s, errors="coerce")
    idade_from_date = np.where(dt.notna() & (dt.dt.year == 1900) & (dt.dt.month == 1), dt.dt.day, np.nan)
    idade_num = pd.to_numeric(s, errors="coerce")
    idade_final = pd.Series(idade_num, index=df.index)
    mask = idade_final.isna() & ~pd.isna(idade_from_date)
    idade_final.loc[mask] = idade_from_date[mask]
    idade_final = idade_final.where(idade_final.between(6, 30))
    df["idade"] = idade_final.round()
    return df

def tratar_inde_2024(df):
    df = df.copy()
    if "inde_2024" in df.columns:
        tmp = df["inde_2024"].astype(str).str.strip().str.upper()
        tmp = tmp.replace("INCLUIR", np.nan)
        df["inde_2024"] = coerce_numeric(tmp)
    return df

def preparar_base_app(df):
    df = df.copy()
    df = padronizar_genero(df)
    df = padronizar_idade(df)
    df = tratar_inde_2024(df)

    if "fase_ideal" in df.columns:
        df["fase_ideal"] = df["fase_ideal"].apply(extrair_fase)

    # Features extras (Feature Engineering)
    cols_acad = [c for c in ["mat","por","ing"] if c in df.columns]
    if len(cols_acad) >= 2:
        df["media_academica"] = df[cols_acad].mean(axis=1)

    cols_comp = [c for c in ["iaa","ieg","ips","ipp"] if c in df.columns]
    if len(cols_comp) >= 2:
        df["media_comportamental"] = df[cols_comp].mean(axis=1)

    if ("inde_2022" in df.columns) and ("inde_2023" in df.columns):
        df["delta_inde"] = df["inde_2023"] - df["inde_2022"]

    return df

# DEFINIÇÃO DE FUNÇÕES DO APP
def traduzir_nomes_features(lista_nomes_tecnicos):

    """Traduz os nomes técnicos do Pipeline para Português legível."""

    mapa_nomes = {
        'num__idade': 'Idade do Aluno',
        'num__inde_2024': 'Índice INDE (Atual)',
        'num__media_academica': 'Média Acadêmica (Mat, Por, Ing)',
        'num__media_comportamental': 'Média Comportamental (IAA, IEG, IPS, IPP)',
        'num__delta_inde': 'Evolução do INDE (Últimos 2 anos)',
        'num__fase_ideal': 'Fase Ideal',
        'cat__genero_masculino': 'Gênero (Masculino)',
        'cat__genero_feminino': 'Gênero (Feminino)',
        # Adicionadas as traduções para os indicadores avançados:
        'num__ida': 'Indicador de Desemp. Acad. (IDA)',
        'num__ipv': 'Indicador de Ponto de Virada (IPV)',
        'num__n_av': 'Número de Avaliações'
    }
    
    nomes_traduzidos = []

    for nome in lista_nomes_tecnicos:
        if nome in mapa_nomes:
            nomes_traduzidos.append(mapa_nomes[nome])
        else:
            limpo = nome.replace('num__', '').replace('cat__', '').replace('bin__', '').replace('_', ' ').title()
            nomes_traduzidos.append(limpo)
            
    return nomes_traduzidos

@st.cache_resource 
def load_models_and_config():

    """Carrega o modelo treinado e o arquivo de configuração usando caminhos relativos."""
    
    caminho_modelo = os.path.join("models", "modelo_passos_magicos.pkl")
    caminho_config = os.path.join("models", "config_passos_magicos.pkl")
    
    try:
        modelo = joblib.load(caminho_modelo)
        config = joblib.load(caminho_config)
        return modelo, config
        
    except FileNotFoundError:
        st.error(f"Arquivos não encontrados. Certifique-se de que a pasta 'models' existe junto ao app.py e contém os arquivos .pkl.")
        return None, None

@st.cache_resource
def _get_shap_explainer(_classifier):
    return shap.TreeExplainer(_classifier)

def configurar_sidebar():
    with st.sidebar:
        st.header("📌 Sobre o Projeto")
        st.info(
            """
            Aplicativo desenvolvido para o **Datathon FIAP - Fase 5** para prevê o risco de defasagem de alunos da ONG Passos Mágicos.
            """
        )
        st.markdown("---")

        st.subheader("👨‍💻 Equipe de Desenvolvimento")
        
        membros = [
            {"nome": "Elton José Araujo Silva", "link": "https://www.linkedin.com/in/elton-araujo-silva/"},
            {"nome": "Leonardo Fajoli Formigon", "link": "https://www.linkedin.com/in/leonardo-formigon-63052320b/"}, 
            {"nome": "Lucas Augusto Fernandes de Lira", "link": "https://www.linkedin.com/in/lucas--lira-/"},
            {"nome": "Mariana Domingues Brandão", "link": "https://www.linkedin.com/in/maridbrandao"},
            {"nome": "Ricardo Vieira Viana", "link": "https://www.linkedin.com/in/ricardvviana"}

        ]

        for membro in membros:
            st.markdown(f"• [{membro['nome']}]({membro['link']})")
            
        st.markdown("---")
        
        st.subheader("📂 Código Fonte")
        st.markdown("Acesse o repositório completo do projeto:")
        st.link_button("🔗 Ver no GitHub", "https://github.com/RicardViana/fiap-fase5-datathon")

def gerar_explicacao_shap(model, input_df_processed):

    """Gera o gráfico SHAP Waterfall."""
    
    try:
        preprocessor = model.named_steps['prep']
        classifier = model.named_steps['model']

        nome_modelo = type(classifier).__name__
        if nome_modelo == 'LogisticRegression':
            st.info("ℹ️ O gráfico detalhado de explicabilidade (SHAP) é exclusivo para modelos baseados em Árvores de Decisão. O modelo atual em uso é uma Regressão Logística.")
            return None, None

        input_transformed = preprocessor.transform(input_df_processed)
        feature_names_raw = preprocessor.get_feature_names_out()
        feature_names_pt = traduzir_nomes_features(feature_names_raw)

        df_mapeamento = pd.DataFrame({
            'Nome Técnico': feature_names_raw,
            'Nome Traduzido': feature_names_pt,  
            'Valor Inputado': input_transformed[0]
        })

        explainer = _get_shap_explainer(classifier)
        shap_values = explainer(input_transformed)

        if len(shap_values.shape) == 3:
            shap_values_to_plot = shap_values[0, :, 1] 
        else:
            shap_values_to_plot = shap_values[0]

        shap_values_to_plot.feature_names = feature_names_pt

        fig, ax = plt.subplots(figsize=(10, 6))
        shap.plots.waterfall(shap_values_to_plot, show=False, max_display=10)
        
        return plt.gcf(), df_mapeamento
    
    except Exception as e:
        st.error(f"Erro ao gerar explicabilidade SHAP: {e}")
        return None, None

def get_user_input_features():

    """Coleta os dados do usuário"""

    st.header("1. Dados do Aluno")
    col1, col2, col3 = st.columns(3)
    with col1:
        idade = st.number_input("Idade", min_value=6, max_value=30, value=12)

    with col2:
        genero = st.selectbox("Gênero", ["Menino", "Menina"])

    with col3:
        fase = st.selectbox("Fase Ideal", ["Alfa", "Fase 1", "Fase 2", "Fase 3", "Fase 4", "Fase 5", "Fase 6", "Fase 7", "Fase 8"])

    st.markdown("---")
    st.header("2. Notas Acadêmicas")
    st.write("Deixe em branco caso o aluno não possua a nota.")
    col_n1, col_n2, col_n3 = st.columns(3)
    
    with col_n1:
        mat = st.number_input("Matemática (MAT)", min_value=0.0, max_value=10.0, value=None, step=0.1, format="%0.4f")

    with col_n2:
        por = st.number_input("Português (POR)", min_value=0.0, max_value=10.0, value=None, step=0.1, format="%0.4f")

    with col_n3:
        ing = st.number_input("Inglês (ING)", min_value=0.0, max_value=10.0, value=None, step=0.1, format="%0.4f")

    st.markdown("---")
    st.header("3. Indicadores (Comportamental e Geral)")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        iaa = st.number_input("Ind. Autoavaliação (IAA)", min_value=0.0, max_value=10.0, value=None, format="%0.4f")
        ieg = st.number_input("Ind. Engajamento (IEG)", min_value=0.0, max_value=10.0, value=None, format="%0.4f")
        inde_2024 = st.number_input("INDE Atual", min_value=0.0, max_value=10.0, value=None, format="%0.4f")

    with col_i2:
        ips = st.number_input("Ind. Psicossocial (IPS)", min_value=0.0, max_value=10.0, value=None, format="%0.4f")
        ipp = st.number_input("Ind. Psicopedagógico (IPP)", min_value=0.0, max_value=10.0, value=None, format="%0.4f")
        
    with st.expander("Histórico de INDE (Opcional - para calcular evolução)"):
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            inde_2022 = st.number_input("INDE de 2 anos atrás", min_value=0.0, max_value=10.0, value=None, format="%0.4f")
        with col_h2:
            inde_2023 = st.number_input("INDE do ano passado", min_value=0.0, max_value=10.0, value=None, format="%0.4f")

    st.markdown("---")
    st.header("4. Indicadores Avançados")
    with st.expander("Preencha se possuir os dados (Importante para a precisão)"):
        col_adv1, col_adv2, col_adv3 = st.columns(3)
        with col_adv1:
            ida = st.number_input("Ind. Desemp. Acad. (IDA)", min_value=0.0, max_value=10.0, value=None, format="%0.4f")
        with col_adv2:
            ipv = st.number_input("Ponto de Virada (IPV)", min_value=0.0, max_value=10.0, value=None, format="%0.4f")
        with col_adv3:
            n_av = st.number_input("Nº de Avaliações", min_value=0, max_value=50, value=None, step=1)

    # Dicionário Final
    data = {
        'idade': idade,
        'genero': genero,
        'fase_ideal': fase,
        'mat': mat if mat is not None else np.nan,
        'por': por if por is not None else np.nan,
        'ing': ing if ing is not None else np.nan,
        'iaa': iaa if iaa is not None else np.nan,
        'ieg': ieg if ieg is not None else np.nan,
        'ips': ips if ips is not None else np.nan,
        'ipp': ipp if ipp is not None else np.nan,
        'inde_2022': inde_2022 if inde_2022 is not None else np.nan,
        'inde_2023': inde_2023 if inde_2023 is not None else np.nan,
        'inde_2024': str(inde_2024) if inde_2024 is not None else np.nan,
        
        # Variáveis cruciais incluídas no app
        'ida': ida if ida is not None else np.nan,
        'ipv': ipv if ipv is not None else np.nan,
        'n_av': n_av if n_av is not None else np.nan,

    }
    
    return pd.DataFrame(data, index=[0])

# FUNÇÃO PRINCIPAL
def main():
    configurar_sidebar()
    
    # Carregar Modelo e Configs
    model, config = load_models_and_config()

    st.title("🎓 Previsão de Defasagem Educacional")
    st.markdown("Analise o risco do aluno apresentar defasagem educacional (IAN <= 5) com base em seus indicadores.")
    
    if config:
        st.caption(f"🤖 Modelo Ativo: **{config['best_model']}** | 🎚️ Limite (Threshold) de Corte: **{config['threshold']:.2f}**")
    
    st.markdown("---")

    # Input bruto
    raw_input_df = get_user_input_features()

    st.markdown("###")
    
    if st.button("🔍 Realizar Predição", type="primary", use_container_width=True):
        if model is not None and config is not None:
            with st.spinner('Analisando dados...'):
                try:
                    # Aplicar o pré-processamento igualzinho ao Notebook
                    processed_df = preparar_base_app(raw_input_df)

                    # Pegar probabilidades
                    probability = model.predict_proba(processed_df)
                    proba_risco = probability[0][1] # Probabilidade de ser classe 1 (Risco)
                    
                    # Usar o Threshold do config para decidir
                    limiar = config['threshold']
                    
                    st.markdown("---")
                    st.header("Resultado da Análise")

                    if proba_risco >= limiar:
                        st.error("⚠️ **ALTO RISCO DE DEFASAGEM IDENTIFICADO**")
                        st.metric(label="Probabilidade de Risco", value=f"{proba_risco * 100:.1f}%")
                        st.warning("👉 **Recomendação:** Necessário acompanhamento pedagógico e psicossocial intensificado.")

                    else:
                        st.success("✅ **ALUNO NO CAMINHO CERTO (BAIXO RISCO)**")
                        st.metric(label="Probabilidade de Risco", value=f"{proba_risco * 100:.1f}%")
                        st.info("👉 **Recomendação:** Manter acompanhamento padrão para garantir o engajamento.")
                    
                    # 4. Exibição do SHAP
                    st.markdown("---")
                    st.header("Fatores de Influência (Explicabilidade)")
                    st.write("Entenda quais características mais impactaram esta previsão específica.")
                    
                    fig_shap, df_map = gerar_explicacao_shap(model, processed_df)
                    if fig_shap:
                        st.pyplot(fig_shap)
                        
                        st.markdown("""
                        **Legenda:** - **Eixo X:** Pontuação base / Probabilidade.  
                        - **Barras Vermelhas:** Fatores que **aumentam** o risco de defasagem.  
                        - **Barras Azuis:** Fatores que **diminuem** o risco de defasagem.  
                        """)

                    if validar_shap.lower() == 's' and df_map is not None:
                        st.markdown("---")
                        st.header("🕵️‍♀️ Debug: Variáveis")
                        with st.expander("Ver Mapeamento"):
                            st.dataframe(df_map)

                except Exception as e:
                    st.error(f"Ocorreu um erro técnico ao realizar a predição: {e}")

        else:
            st.error("⚠️ O modelo não foi carregado corretamente.")

if __name__ == "__main__":
    main()