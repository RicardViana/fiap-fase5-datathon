import streamlit as st
import pandas as pd
import numpy as np
# import tensorflow as tf  <-- Descomente quando tiver o modelo
# import joblib            <-- Descomente quando tiver o modelo
import random # Apenas para simulação visual

# --- Configuração da Página ---
st.set_page_config(
    page_title="Predição de Risco - Passos Mágicos",
    page_icon="🎓",
    layout="centered"
)

# --- CSS para melhorar a aparência (Opcional) ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Cabeçalho ---
st.title("🎓 Passos Mágicos: Sistema de Alerta")
st.markdown("### Ferramenta de Predição de Risco de Defasagem")
st.info("ℹ️ Preencha os indicadores pedagógicos e psicossociais para avaliar o risco do aluno.")
st.divider()

# ==============================================================================
# ⚠️ ÁREA DE CARREGAMENTO DO MODELO (ATUALMENTE EM MODO SIMULAÇÃO)
# ==============================================================================

# QUANDO TIVER O MODELO PRONTO, DESCOMENTE O BLOCO ABAIXO E APAGUE O BLOCO DE SIMULAÇÃO:

"""
@st.cache_resource
def load_assets():
    try:
        model = tf.keras.models.load_model('modelo_passos_magicos.keras')
        scaler = joblib.load('scaler_passos_magicos.pkl')
        return model, scaler
    except Exception as e:
        st.error(f"Erro ao carregar arquivos: {e}")
        return None, None

model, scaler = load_assets()
"""

# --- BLOCO DE SIMULAÇÃO (APAGUE ISSO DEPOIS) ---
model = None 
scaler = None
# ==============================================================================


# --- Formulário de Entrada ---
with st.form("form_predicao"):
    st.subheader("📊 Indicadores do Aluno")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧠 Psicossocial")
        iaa = st.number_input("IAA (Auto Avaliação)", 0.0, 10.0, 7.5, 0.1)
        ieg = st.number_input("IEG (Engajamento)", 0.0, 10.0, 8.0, 0.1)
        ips = st.number_input("IPS (Psicossocial)", 0.0, 10.0, 7.0, 0.1)
        ipp = st.number_input("IPP (Psicopedagógico)", 0.0, 10.0, 7.0, 0.1)

    with col2:
        st.markdown("### 📚 Acadêmico")
        ida = st.number_input("IDA (Aprendizagem)", 0.0, 10.0, 6.5, 0.1)
        ipv = st.number_input("IPV (Ponto de Virada)", 0.0, 10.0, 7.0, 0.1)
        mat = st.number_input("Nota Matemática", 0.0, 10.0, 6.0, 0.1)
        por = st.number_input("Nota Português", 0.0, 10.0, 6.0, 0.1)

    # Botão de submissão
    submit_button = st.form_submit_button("🔍 Calcular Probabilidade de Risco", type="primary")


# --- Lógica de Exibição do Resultado ---
if submit_button:
    
    # 1. Criação do DataFrame com os dados inseridos
    input_data = pd.DataFrame({
        'iaa': [iaa], 'ieg': [ieg], 'ips': [ips], 'ipp': [ipp],
        'ida': [ida], 'mat': [mat], 'por': [por], 'ipv': [ipv]
    })

    # ==========================================================================
    # LÓGICA REAL (DESCOMENTAR DEPOIS)
    # ==========================================================================
    if model is not None and scaler is not None:
        try:
            # input_scaled = scaler.transform(input_data)
            # prediction_prob = model.predict(input_scaled)
            # probability = prediction_prob[0][0]
            pass # Remover esse pass quando descomentar acima
        except Exception as e:
            st.error(f"Erro na predição: {e}")
            probability = 0.0
    
    # ==========================================================================
    # LÓGICA DE SIMULAÇÃO (APAGAR DEPOIS)
    # ==========================================================================
    else:
        # Gera um valor aleatório só para testar o visual
        # Se as notas forem baixas, finge risco alto, senão risco baixo
        media_notas = (iaa + ieg + ida + mat) / 4
        if media_notas < 6.0:
            probability = random.uniform(0.60, 0.95) # Simula Alto Risco
        else:
            probability = random.uniform(0.10, 0.40) # Simula Baixo Risco
            
        st.warning("⚠️ MODO DE SIMULAÇÃO: O modelo ainda não foi carregado. Este resultado é ilustrativo.")
    # ==========================================================================


    # --- EXIBIÇÃO DO DASHBOARD DE RESULTADO ---
    st.divider()
    st.subheader("📋 Resultado da Análise")

    col_metric, col_desc = st.columns([1, 2])

    with col_metric:
        st.metric(label="Probabilidade de Risco", value=f"{probability:.1%}")
        
        # Barra de progresso visual
        st.progress(int(probability * 100))

    with col_desc:
        if probability > 0.5:
            st.error("🚨 **ALTO RISCO IDENTIFICADO**")
            st.markdown(f"""
            O modelo indica uma probabilidade de **{probability:.1%}** deste aluno entrar em defasagem.
            
            **Recomendações Sugeridas:**
            - 🛑 Contato imediato com a família.
            - 🛑 Agendamento com psicopedagogia.
            - 🛑 Reforço escolar nas matérias críticas (Mat/Port).
            """)
        else:
            st.success("✅ **SITUAÇÃO SOB CONTROLE**")
            st.markdown(f"""
            O aluno apresenta indicadores saudáveis, com apenas **{probability:.1%}** de risco calculado.
            
            **Ação:**
            - Manter acompanhamento regular nas atividades do Passos Mágicos.
            """)