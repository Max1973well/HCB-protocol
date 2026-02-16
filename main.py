import streamlit as st
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="HCB Protocolo", layout="centered")

# --- ESTILO VISUAL (ESMERALDA, PLATINA E OCEANO) ---
st.markdown("""
    <style>
    .stApp { background-color: #E5E4E2; }
    .visor {
        background-color: #B0E0E6;
        color: #005F6B;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        border: 4px inset #A9A9A9;
    }
    div.stButton > button {
        background-color: #2E8B57;
        color: white;
        font-weight: bold;
        width: 100%;
        height: 3em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="visor">HCB PROTOCOL SYSTEM</div>', unsafe_allow_html=True)

# --- CAMPOS DO SISTEMA ---
st.write("### Procedimentos")
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

st.write("---")
obs = st.text_input("Observações", placeholder="Suas observações aqui...")

# --- LÓGICA DE IMPRESSÃO ---
if st.button("GERAR RELATÓRIO"):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    if "dia do tribunal" in obs.lower():
        txt = f"HCB PROTOCOL\nDATA: {agora}\nFOCO: DIA DO TRIBUNAL\nOBS: {obs}"
    elif pis:
        txt = f"HCB PROTOCOL\nDATA: {agora}\nPROCEDIMENTO: PISCINA\n(Outros itens ignorados)"
    else:
        selecionados = []
        if ida: selecionados.append("Ida Táxi")
        if mag: selecionados.append("Magnetismo")
        if ele: selecionados.append("Eletrodo")
        if mas: selecionados.append("Massagem")
        if gel: selecionados.append("Gelo")
        if vol: selecionados.append("Volta Táxi")
        if out: selecionados.append("Outros")
        
        lista = ", ".join(selecionados) if selecionados else "Nenhum item"
        txt = f"HCB PROTOCOL\nDATA: {agora}\nITENS: {lista}\nOBS: {obs}"

    st.info("Relatório Gerado:")
    st.code(txt)
    st.download_button("BAIXAR RELATÓRIO (.TXT)", txt, file_name=f"relatorio_hcb_{datetime.now().strftime('%d%m%Y')}.txt")
