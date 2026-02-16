import streamlit as st
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="HCB Protocolo Platinum", layout="centered")

# --- ESTILO VISUAL DE ALTO CONTRASTE ---
st.markdown("""
    <style>
    .stApp { background-color: #E5E4E2; } /* Platina */
    
    .visor {
        background-color: #B0E0E6; /* Azul Oceano */
        color: #000000; /* PRETO para leitura total */
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-family: 'Courier New', monospace;
        font-size: 24px;
        font-weight: bold;
        border: 4px inset #A9A9A9;
        margin-bottom: 20px;
    }
    
    /* Ajustando cor dos textos das perguntas e títulos */
    h3, p, .stCheckbox label {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    
    /* Botão Esmeralda Principal */
    div.stButton > button {
        background-color: #2E8B57;
        color: #FFFFFF;
        font-weight: bold;
        font-size: 20px;
        width: 100%;
        height: 3.5em;
        border-radius: 10px;
        border: 2px solid #1E5D3A;
    }

    /* Caixa de Texto (Observações) */
    .stTextInput input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #2E8B57 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="visor">HCB PROTOCOL SYSTEM</div>', unsafe_allow_html=True)

# --- CORPO DO SISTEMA ---
st.markdown("### 📝 Marque os Procedimentos:")
c1, c2 = st.columns(2)
with c1:
    ida = st.checkbox("Ida Táxi")
    mag = st.checkbox("Magnetismo")
    ele = st.checkbox("Eletrodo")
    mas = st.checkbox("Massagem")
with c2:
    pis = st.checkbox("Piscina")
    gel = st.checkbox("Gelo")
    vol = st.checkbox("Volta Táxi")
    out = st.checkbox("Outros")

st.markdown("---")
obs = st.text_input("Observações:", placeholder="Digite aqui...")

# --- AÇÃO E RESULTADO ---
if st.button("GERAR RELATÓRIO FINAL"):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Lógica Maxwell (Tribunal > Piscina > Outros)
    if "dia do tribunal" in obs.lower():
        txt = f"--- HCB RELATÓRIO ---\nDATA: {agora}\nSTATUS: DIA DO TRIBUNAL\nDETALHES: {obs}"
    elif pis:
        txt = f"--- HCB RELATÓRIO ---\nDATA: {agora}\nPROCEDIMENTO: PISCINA\n(Itens adicionais ignorados)"
    else:
        selecionados = [item for item, var in {
            "Ida Táxi": ida, "Magnetismo": mag, "Eletrodo": ele, 
            "Massagem": mas, "Gelo": gel, "Volta Táxi": vol, "Outros": out
        }.items() if var]
        lista = ", ".join(selecionados) if selecionados else "Nenhum"
        txt = f"--- HCB RELATÓRIO ---\nDATA: {agora}\nITENS: {lista}\nOBS: {obs}"

    # RESUMO NA TELA (LETRA PRETA NO FUNDO BRANCO)
    st.markdown("### 📋 Resumo do Documento:")
    st.code(txt, language="text")
    
    # BOTÃO DE DOWNLOAD BEM GRANDE
    st.download_button(
        label="📥 BAIXAR RELATÓRIO (.TXT)", 
        data=txt, 
        file_name=f"HCB_{datetime.now().strftime('%d%m%Y_%H%M')}.txt",
        mime="text/plain"
    )

st.markdown("---")
st.caption("HCB PLATINUM SERIES - MOBILE READY")
