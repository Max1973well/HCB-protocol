import json
import os
from datetime import datetime

import streamlit as st


TRANSPORTE_IDA = "Ida Transporte"
TRANSPORTE_VOLTA = "Volta Transporte"
ATIVIDADE_HIDRO = "Hidroginástica"
PASTA_DADOS = "04_RELATORIOS_GERADOS"
ARQUIVO_DB = os.path.join(PASTA_DADOS, "dados_v1.json")
ARQUIVO_DB_BACKUP = os.path.join(PASTA_DADOS, "dados_v1.backup.json")


st.set_page_config(
    page_title="HCB Fisio",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
<style>
    .stApp { background-color: #1a1a2e; color: #E5E4E2; }
    .hcb-title {
        text-align: center; font-family: 'Courier New', monospace; font-size: 1.8rem;
        font-weight: bold; color: #00d4aa; text-shadow: 0 0 20px #00d4aa55;
        padding: 1rem 0 0.2rem 0; letter-spacing: 3px;
    }
    .hcb-subtitle {
        text-align: center; font-family: 'Courier New', monospace; font-size: 0.75rem;
        color: #5a8a7a; letter-spacing: 2px; margin-bottom: 1.5rem;
    }
    .visor {
        background: linear-gradient(135deg, #0d2137, #0a3d2e); border: 1px solid #00d4aa44;
        border-radius: 8px; padding: 0.8rem 1rem; font-family: 'Courier New', monospace;
        font-size: 0.85rem; color: #00d4aa; text-align: center; margin-bottom: 1.5rem;
        box-shadow: 0 0 15px #00d4aa22;
    }
    .section-label {
        font-family: 'Courier New', monospace; font-size: 0.7rem; color: #5a7a9a;
        letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0.6rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00d4aa, #00a888) !important;
        color: #0a1628 !important; font-family: 'Courier New', monospace !important;
        font-weight: bold !important; letter-spacing: 2px !important; border: none !important;
        border-radius: 8px !important; padding: 0.7rem 2rem !important; font-size: 0.9rem !important;
        width: 100% !important; transition: all 0.3s !important; box-shadow: 0 4px 15px #00d4aa44 !important;
    }
    .stCheckbox label {
        color: #b0c4d8 !important; font-family: 'Courier New', monospace !important;
        font-size: 0.9rem !important;
    }
    .stTextArea > div > div > textarea {
        background-color: #0d1f33 !important; color: #E5E4E2 !important;
        border: 1px solid #2a4a6e !important; border-radius: 6px !important;
        font-family: 'Courier New', monospace !important;
    }
    .historico-item {
        background: #0d1f33; border-left: 3px solid #00d4aa; border-radius: 0 6px 6px 0;
        padding: 0.6rem 0.8rem; margin: 0.4rem 0; font-family: 'Courier New', monospace;
        font-size: 0.8rem; color: #8ab4c8;
    }
    .msg-success {
        background: #0a2e1a; border: 1px solid #00d4aa; border-radius: 6px; padding: 0.7rem;
        color: #00d4aa; font-family: 'Courier New', monospace; font-size: 0.85rem;
        text-align: center; margin-top: 0.5rem;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)


def salvar_drive(conteudo: str, nome_arquivo: str) -> bool:
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaInMemoryUpload

        creds_dict = dict(st.secrets["google_drive"])
        creds = service_account.Credentials.from_service_account_info(
            creds_dict, scopes=["https://www.googleapis.com/auth/drive.file"]
        )
        service = build("drive", "v3", credentials=creds)

        folder_id = st.secrets.get("drive_folder_id", None)
        file_metadata = {"name": nome_arquivo}
        if folder_id:
            file_metadata["parents"] = [folder_id]

        media = MediaInMemoryUpload(conteudo.encode("utf-8"), mimetype="text/plain")
        service.files().create(body=file_metadata, media_body=media).execute()
        return True
    except Exception:
        return False


def salvar_local(conteudo: str, nome_arquivo: str) -> str:
    os.makedirs(PASTA_DADOS, exist_ok=True)
    caminho = os.path.join(PASTA_DADOS, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)
    return caminho


def carregar_banco_json() -> dict:
    base_vazia = {"versao": "1.1", "registros": []}
    if not os.path.exists(ARQUIVO_DB):
        return base_vazia

    try:
        with open(ARQUIVO_DB, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        if isinstance(dados, dict) and "registros" in dados:
            return dados
    except Exception:
        pass
    return base_vazia


def salvar_banco_json(dados: dict) -> None:
    os.makedirs(PASTA_DADOS, exist_ok=True)
    temp_path = f"{ARQUIVO_DB}.tmp"

    if os.path.exists(ARQUIVO_DB):
        try:
            with open(ARQUIVO_DB, "r", encoding="utf-8") as origem, open(
                ARQUIVO_DB_BACKUP, "w", encoding="utf-8"
            ) as backup:
                backup.write(origem.read())
        except Exception:
            pass

    with open(temp_path, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        arquivo.flush()
        os.fsync(arquivo.fileno())
    os.replace(temp_path, ARQUIVO_DB)


def salvar_registro_json(payload: dict) -> None:
    dados = carregar_banco_json()
    payload["id"] = f"REG-{datetime.now().strftime('%Y%m%d%H%M%S')}-{payload['arquivo']}"
    dados.setdefault("registros", []).append(payload)
    salvar_banco_json(dados)


def carregar_historico_sessao() -> list:
    dados = carregar_banco_json()
    historico = []
    for registro in dados.get("registros", [])[-30:]:
        hora = "?"
        data_hora = registro.get("data_hora", "")
        if len(data_hora) >= 19:
            try:
                hora = datetime.strptime(data_hora, "%d/%m/%Y %H:%M:%S").strftime("%H:%M:%S")
            except ValueError:
                hora = data_hora

        historico.append(
            {
                "hora": hora,
                "arquivo": registro.get("arquivo", "sem_nome.txt"),
                "drive": registro.get("destino") == "google_drive",
            }
        )
    return historico


if "historico" not in st.session_state:
    st.session_state.historico = carregar_historico_sessao()


st.markdown('<div class="hcb-title">⬡ HCB FISIO</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hcb-subtitle">HUMAN CONTEXT BUS — ACOMPANHAMENTO FISIOTERAPÊUTICO</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="visor">◉ SISTEMA HCB ATIVO &nbsp;|&nbsp; {datetime.now().strftime("%d/%m/%Y %H:%M")}</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="section-label">► PROCEDIMENTOS DA SESSÃO</div>', unsafe_allow_html=True)
st.caption(f"{TRANSPORTE_IDA} e {TRANSPORTE_VOLTA} são obrigatórios em toda sessão.")

col1, col2 = st.columns(2)
procedimentos = {
    TRANSPORTE_IDA: True,
    TRANSPORTE_VOLTA: True,
}

itens_col1 = ["Magnetismo", "Eletrodo", "Massagem"]
itens_col2 = [ATIVIDADE_HIDRO, "Gelo", "Outros"]

with col1:
    st.checkbox(TRANSPORTE_IDA, value=True, disabled=True, key="fixo_ida")
    for item in itens_col1:
        procedimentos[item] = st.checkbox(item, key=f"check_{item}")

with col2:
    st.checkbox(TRANSPORTE_VOLTA, value=True, disabled=True, key="fixo_volta")
    for item in itens_col2:
        procedimentos[item] = st.checkbox(item, key=f"check_{item}")

st.markdown("---")
st.markdown('<div class="section-label">► OBSERVAÇÕES DA SESSÃO</div>', unsafe_allow_html=True)
obs = st.text_area(
    label="obs",
    placeholder="Digite observações, intercorrências, estado do paciente...",
    height=100,
    label_visibility="collapsed",
)

st.markdown("---")

if st.button("⬡ GERAR RELATÓRIO HCB"):
    data_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    nome_arquivo = f"Relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    obs_txt = obs.strip() if obs and obs.strip() else "—"

    if "dia do tribunal" in obs_txt.lower():
        conteudo = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HCB PROTOCOL — RELATÓRIO FISIO
DATA: {data_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠ OBSERVAÇÃO PRIORITÁRIA: DIA DO TRIBUNAL
TRANSPORTE: {TRANSPORTE_IDA} | {TRANSPORTE_VOLTA}
OBSERVAÇÕES: {obs_txt}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        selecionados = [TRANSPORTE_IDA, TRANSPORTE_VOLTA]
    elif procedimentos.get(ATIVIDADE_HIDRO):
        conteudo = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HCB PROTOCOL — RELATÓRIO FISIO
DATA: {data_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ATIVIDADE PRINCIPAL: {ATIVIDADE_HIDRO}
TRANSPORTE: {TRANSPORTE_IDA} | {TRANSPORTE_VOLTA}
NOTA: Outros procedimentos anulados pela prioridade {ATIVIDADE_HIDRO}.
OBSERVAÇÕES: {obs_txt}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        selecionados = [TRANSPORTE_IDA, ATIVIDADE_HIDRO, TRANSPORTE_VOLTA]
    else:
        selecionados_sem_transporte = [
            item
            for item, val in procedimentos.items()
            if val and item not in (TRANSPORTE_IDA, TRANSPORTE_VOLTA)
        ]
        if not selecionados_sem_transporte:
            st.warning("Selecione ao menos um procedimento clínico além do transporte obrigatório.")
            st.stop()

        selecionados = [TRANSPORTE_IDA] + selecionados_sem_transporte + [TRANSPORTE_VOLTA]
        conteudo = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HCB PROTOCOL — RELATÓRIO FISIO
DATA: {data_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROCEDIMENTOS REALIZADOS:
{chr(10).join(f'  • {p}' for p in selecionados)}

OBSERVAÇÕES: {obs_txt}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HCB Protocol v1.1 — PRODUCTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

    drive_ok = salvar_drive(conteudo, nome_arquivo)

    if drive_ok:
        st.markdown(
            '<div class="msg-success">✓ Relatório salvo no Google Drive com sucesso.</div>',
            unsafe_allow_html=True,
        )
        destino = "google_drive"
    else:
        caminho = salvar_local(conteudo, nome_arquivo)
        st.markdown(
            f'<div class="msg-success">✓ Relatório salvo localmente: {caminho}</div>',
            unsafe_allow_html=True,
        )
        destino = "local"

    salvar_registro_json(
        {
            "data_hora": data_str,
            "arquivo": nome_arquivo,
            "destino": destino,
            "procedimentos": selecionados,
            "observacoes": obs_txt,
        }
    )

    st.session_state.historico.append(
        {"hora": datetime.now().strftime("%H:%M:%S"), "arquivo": nome_arquivo, "drive": drive_ok}
    )

    with st.expander("► Ver relatório gerado"):
        st.code(conteudo, language=None)

if st.session_state.historico:
    st.markdown("---")
    st.markdown('<div class="section-label">► HISTÓRICO DA SESSÃO</div>', unsafe_allow_html=True)
    for item in reversed(st.session_state.historico):
        icone = "☁" if item["drive"] else "💾"
        st.markdown(
            f'<div class="historico-item">{icone} {item["hora"]} — {item["arquivo"]}</div>',
            unsafe_allow_html=True,
        )

st.markdown("---")
st.markdown(
    '<div style="text-align:center; font-family: Courier New; font-size: 0.65rem; color: #2a4a5e; letter-spacing: 2px;">'
    "HCB PROTOCOL v1.1 — PRODUCTION &nbsp;|&nbsp; VINCULADO AO HCB SYSTEM"
    "</div>",
    unsafe_allow_html=True,
)
