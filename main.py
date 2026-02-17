import streamlit as st
from datetime import datetime
import os
import json

# ─────────────────────────────────────────
# CONFIG PÁGINA
# ─────────────────────────────────────────
st.set_page_config(
    page_title="HCB Fisio",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────
# ESTILOS HCB PLATINUM
# ─────────────────────────────────────────
st.markdown("""
<style>
    /* Fundo geral */
    .stApp {
        background-color: #1a1a2e;
        color: #E5E4E2;
    }

    /* Título principal */
    .hcb-title {
        text-align: center;
        font-family: 'Courier New', monospace;
        font-size: 1.8rem;
        font-weight: bold;
        color: #00d4aa;
        text-shadow: 0 0 20px #00d4aa55;
        padding: 1rem 0 0.2rem 0;
        letter-spacing: 3px;
    }

    .hcb-subtitle {
        text-align: center;
        font-family: 'Courier New', monospace;
        font-size: 0.75rem;
        color: #5a8a7a;
        letter-spacing: 2px;
        margin-bottom: 1.5rem;
    }

    /* Visor status */
    .visor {
        background: linear-gradient(135deg, #0d2137, #0a3d2e);
        border: 1px solid #00d4aa44;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        color: #00d4aa;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 15px #00d4aa22;
    }

    /* Cards de seção */
    .section-card {
        background: #16213e;
        border: 1px solid #2a3a5e;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 0.8rem 0;
    }

    .section-label {
        font-family: 'Courier New', monospace;
        font-size: 0.7rem;
        color: #5a7a9a;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }

    /* Botão principal */
    .stButton > button {
        background: linear-gradient(135deg, #00d4aa, #00a888) !important;
        color: #0a1628 !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
        letter-spacing: 2px !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.7rem 2rem !important;
        font-size: 0.9rem !important;
        width: 100% !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 15px #00d4aa44 !important;
    }

    .stButton > button:hover {
        box-shadow: 0 6px 25px #00d4aa88 !important;
        transform: translateY(-1px) !important;
    }

    /* Checkboxes */
    .stCheckbox label {
        color: #b0c4d8 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.9rem !important;
    }

    /* Text input */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #0d1f33 !important;
        color: #E5E4E2 !important;
        border: 1px solid #2a4a6e !important;
        border-radius: 6px !important;
        font-family: 'Courier New', monospace !important;
    }

    /* Divider */
    hr {
        border-color: #2a3a5e !important;
        margin: 1rem 0 !important;
    }

    /* Histórico */
    .historico-item {
        background: #0d1f33;
        border-left: 3px solid #00d4aa;
        border-radius: 0 6px 6px 0;
        padding: 0.6rem 0.8rem;
        margin: 0.4rem 0;
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
        color: #8ab4c8;
    }

    /* Sucesso/erro */
    .msg-success {
        background: #0a2e1a;
        border: 1px solid #00d4aa;
        border-radius: 6px;
        padding: 0.7rem;
        color: #00d4aa;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        text-align: center;
        margin-top: 0.5rem;
    }

    .msg-error {
        background: #2e0a0a;
        border: 1px solid #ff4444;
        border-radius: 6px;
        padding: 0.7rem;
        color: #ff8888;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        text-align: center;
        margin-top: 0.5rem;
    }

    /* Esconder elementos Streamlit padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# GOOGLE DRIVE (opcional)
# ─────────────────────────────────────────
def salvar_drive(conteudo: str, nome_arquivo: str) -> bool:
    """Tenta salvar no Google Drive via st.secrets."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaInMemoryUpload

        creds_dict = dict(st.secrets["google_drive"])
        creds = service_account.Credentials.from_service_account_info(
            creds_dict,
            scopes=["https://www.googleapis.com/auth/drive.file"]
        )
        service = build("drive", "v3", credentials=creds)

        folder_id = st.secrets.get("drive_folder_id", None)
        file_metadata = {"name": nome_arquivo}
        if folder_id:
            file_metadata["parents"] = [folder_id]

        media = MediaInMemoryUpload(
            conteudo.encode("utf-8"),
            mimetype="text/plain"
        )
        service.files().create(
            body=file_metadata,
            media_body=media
        ).execute()
        return True
    except Exception:
        return False


def salvar_local(conteudo: str, nome_arquivo: str) -> str:
    """Salva localmente como fallback."""
    pasta = "04_RELATORIOS_GERADOS"
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return caminho


# ─────────────────────────────────────────
# ESTADO DA SESSÃO
# ─────────────────────────────────────────
if "historico" not in st.session_state:
    st.session_state.historico = []

# ─────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────
st.markdown('<div class="hcb-title">⬡ HCB FISIO</div>', unsafe_allow_html=True)
st.markdown('<div class="hcb-subtitle">HUMAN CONTEXT BUS — ACOMPANHAMENTO FISIOTERAPÊUTICO</div>', unsafe_allow_html=True)

# Visor status
hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
st.markdown(f'<div class="visor">◉ SISTEMA HCB ATIVO &nbsp;|&nbsp; {hora_atual}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
# FORMULÁRIO PRINCIPAL
# ─────────────────────────────────────────
st.markdown('<div class="section-label">► PROCEDIMENTOS DA SESSÃO</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

procedimentos = {}
itens_col1 = ["Ida Táxi", "Magnetismo", "Eletrodo", "Massagem"]
itens_col2 = ["Piscina", "Gelo", "Volta Táxi", "Outros"]

with col1:
    for item in itens_col1:
        procedimentos[item] = st.checkbox(item, key=f"check_{item}")

with col2:
    for item in itens_col2:
        procedimentos[item] = st.checkbox(item, key=f"check_{item}")

st.markdown("---")

# Campo de observações
st.markdown('<div class="section-label">► OBSERVAÇÕES DA SESSÃO</div>', unsafe_allow_html=True)
obs = st.text_area(
    label="obs",
    placeholder="Digite observações, intercorrências, estado do paciente...",
    height=100,
    label_visibility="collapsed"
)

st.markdown("---")

# ─────────────────────────────────────────
# BOTÃO GERAR RELATÓRIO
# ─────────────────────────────────────────
if st.button("⬡ GERAR RELATÓRIO HCB"):

    data_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    nome_arquivo = f"Relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    # Lógica de prioridade
    if obs and "dia do tribunal" in obs.lower():
        conteudo = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HCB PROTOCOL — RELATÓRIO FISIO
DATA: {data_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠ OBSERVAÇÃO PRIORITÁRIA: DIA DO TRIBUNAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

    elif procedimentos.get("Piscina"):
        conteudo = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HCB PROTOCOL — RELATÓRIO FISIO
DATA: {data_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ATIVIDADE PRINCIPAL: PISCINA
NOTA: Outros procedimentos anulados pela prioridade Piscina.
OBSERVAÇÕES: {obs if obs else '—'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

    else:
        selecionados = [item for item, val in procedimentos.items() if val]
        if not selecionados:
            st.warning("Selecione ao menos um procedimento.")
            st.stop()

        conteudo = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HCB PROTOCOL — RELATÓRIO FISIO
DATA: {data_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROCEDIMENTOS REALIZADOS:
{chr(10).join(f'  • {p}' for p in selecionados)}

OBSERVAÇÕES: {obs if obs else '—'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HCB Protocol v1.0 — PRODUCTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

    # Tentar salvar no Drive, fallback local
    drive_ok = salvar_drive(conteudo, nome_arquivo)

    if drive_ok:
        st.markdown('<div class="msg-success">✓ Relatório salvo no Google Drive com sucesso.</div>', unsafe_allow_html=True)
    else:
        caminho = salvar_local(conteudo, nome_arquivo)
        st.markdown(f'<div class="msg-success">✓ Relatório salvo localmente: {caminho}</div>', unsafe_allow_html=True)

    # Adicionar ao histórico da sessão
    st.session_state.historico.append({
        "hora": datetime.now().strftime("%H:%M:%S"),
        "arquivo": nome_arquivo,
        "drive": drive_ok
    })

    # Mostrar prévia
    with st.expander("► Ver relatório gerado"):
        st.code(conteudo, language=None)

# ─────────────────────────────────────────
# HISTÓRICO DA SESSÃO
# ─────────────────────────────────────────
if st.session_state.historico:
    st.markdown("---")
    st.markdown('<div class="section-label">► HISTÓRICO DA SESSÃO</div>', unsafe_allow_html=True)
    for item in reversed(st.session_state.historico):
        icone = "☁" if item["drive"] else "💾"
        st.markdown(
            f'<div class="historico-item">{icone} {item["hora"]} — {item["arquivo"]}</div>',
            unsafe_allow_html=True
        )

# ─────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center; font-family: Courier New; font-size: 0.65rem; color: #2a4a5e; letter-spacing: 2px;">'
    'HCB PROTOCOL v1.0 — PRODUCTION &nbsp;|&nbsp; VINCULADO AO HCB SYSTEM'
    '</div>',
    unsafe_allow_html=True
)
