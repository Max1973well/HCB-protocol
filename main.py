import json
import os
from datetime import datetime

import streamlit as st


TRANSPORTE_IDA = "Ida Transporte"
TRANSPORTE_VOLTA = "Volta Transporte"
ATIVIDADE_HIDRO = "Hidroginástica"
STATUS_MEDICACAO = ["feito", "atrasado", "nao_administrado"]
PASTA_DADOS = "04_RELATORIOS_GERADOS"
ARQUIVO_DB = os.path.join(PASTA_DADOS, "dados_v1.json")
ARQUIVO_DB_BACKUP = os.path.join(PASTA_DADOS, "dados_v1.backup.json")


st.set_page_config(
    page_title="HCB Fisio",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if "modo_acessivel" not in st.session_state:
    st.session_state.modo_acessivel = True

st.toggle(
    "Modo de alta acessibilidade visual (WCAG)",
    key="modo_acessivel",
    help="Aumenta contraste, destaca foco de teclado e melhora legibilidade para baixa visão.",
)


st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(180deg, #22324a 0%, #1d2c44 100%);
        color: #f4f7fb;
        font-size: 1.08rem;
    }
    .hcb-title {
        text-align: center; font-family: 'Courier New', monospace; font-size: 2.15rem;
        font-weight: bold; color: #4ef0c9; text-shadow: 0 0 20px #00d4aa55;
        padding: 1rem 0 0.2rem 0; letter-spacing: 3px;
    }
    .hcb-subtitle {
        text-align: center; font-family: 'Courier New', monospace; font-size: 0.95rem;
        color: #bdd9cd; letter-spacing: 1px; margin-bottom: 1.5rem;
    }
    .visor {
        background: linear-gradient(135deg, #1b3959, #1e4a42); border: 1px solid #4ef0c966;
        border-radius: 8px; padding: 0.8rem 1rem; font-family: 'Courier New', monospace;
        font-size: 1rem; color: #bfffe9; text-align: center; margin-bottom: 1.5rem;
        box-shadow: 0 0 15px #00d4aa22;
    }
    .section-label {
        font-family: 'Courier New', monospace; font-size: 0.95rem; color: #d3e6ff;
        letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.6rem; font-weight: bold;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00d4aa, #00a888) !important;
        color: #0a1628 !important; font-family: 'Courier New', monospace !important;
        font-weight: bold !important; letter-spacing: 2px !important; border: none !important;
        border-radius: 8px !important; padding: 0.85rem 2rem !important; font-size: 1.05rem !important;
        width: 100% !important; transition: all 0.3s !important; box-shadow: 0 4px 15px #00d4aa44 !important;
    }
    .stCheckbox label {
        color: #eef5ff !important; font-family: 'Courier New', monospace !important;
        font-size: 1.05rem !important; font-weight: 600 !important;
    }
    .stTextArea > div > div > textarea {
        background-color: #223a5a !important; color: #f6fbff !important;
        border: 2px solid #6f98c7 !important; border-radius: 8px !important;
        font-family: 'Courier New', monospace !important; font-size: 1.02rem !important;
    }
    .historico-item {
        background: #1b3351; border-left: 4px solid #4ef0c9; border-radius: 0 6px 6px 0;
        padding: 0.6rem 0.8rem; margin: 0.4rem 0; font-family: 'Courier New', monospace;
        font-size: 0.95rem; color: #d6ecff;
    }
    .msg-success {
        background: #1b4a34; border: 1px solid #6cffd6; border-radius: 6px; padding: 0.8rem;
        color: #d7fff4; font-family: 'Courier New', monospace; font-size: 0.98rem;
        text-align: center; margin-top: 0.5rem;
    }
    .stCaption, .stMarkdown p, .stTextInput label, .stTextArea label, .stDateInput label, .stTimeInput label, .stSelectbox label {
        font-size: 1rem !important;
        color: #e6f1ff !important;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)

if st.session_state.modo_acessivel:
    st.markdown(
        """
<style>
    /* Camada adicional de acessibilidade visual (WCAG AA orientativo) */
    .stApp {
        background: #1c2c45 !important;
        color: #ffffff !important;
    }
    .stMarkdown, .stCaption, .stText, .stAlert, p, label, span {
        color: #ffffff !important;
    }
    .stButton > button {
        min-height: 48px !important;
        font-size: 1.1rem !important;
        border: 2px solid #d8fff1 !important;
    }
    .stCheckbox label, .stRadio label, .stSelectbox label, .stDateInput label, .stTimeInput label, .stTextInput label, .stTextArea label {
        font-size: 1.08rem !important;
        font-weight: 700 !important;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] > div, .stDateInput input, .stTimeInput input {
        border: 2px solid #9ec7ff !important;
        background-color: #213a5a !important;
        color: #ffffff !important;
    }
    /* Foco de teclado bem visível */
    button:focus, input:focus, textarea:focus, [role="combobox"]:focus, [tabindex]:focus {
        outline: 3px solid #ffe083 !important;
        outline-offset: 2px !important;
    }
    /* Reduz animações para pessoas sensíveis a movimento */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation: none !important;
            transition: none !important;
            scroll-behavior: auto !important;
        }
    }
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
    base_vazia = {"versao": "1.2", "registros": []}
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


def montar_bloco_agenda(agenda_itens: list) -> str:
    if not agenda_itens:
        return "AGENDA MÉDICA:\n  • —"
    linhas = ["AGENDA MÉDICA:"]
    for item in agenda_itens:
        linhas.append(
            f"  • {item['data']} {item['hora']} | {item['tipo']} | {item['local']} | {item['anotacoes']}"
        )
    return "\n".join(linhas)


def montar_bloco_medicacoes(medicacoes: list) -> str:
    if not medicacoes:
        return "MEDICAÇÕES:\n  • —"
    linhas = ["MEDICAÇÕES:"]
    for med in medicacoes:
        linhas.append(
            f"  • {med['medicamento']} {med['dose']} | previsto {med['horario_previsto']} | "
            f"realizado {med['horario_realizado']} | status {med['status']} | motivo: {med['motivo']}"
        )
    return "\n".join(linhas)


if "historico" not in st.session_state:
    st.session_state.historico = carregar_historico_sessao()
if "agenda_count" not in st.session_state:
    st.session_state.agenda_count = 1
if "med_count" not in st.session_state:
    st.session_state.med_count = 1


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

st.markdown('<div class="section-label">► AGENDA DE ACOMPANHAMENTO MÉDICO</div>', unsafe_allow_html=True)
for i in range(st.session_state.agenda_count):
    st.markdown(f"**Compromisso {i + 1}**")
    col_a, col_b = st.columns(2)
    with col_a:
        st.date_input("Data", key=f"agenda_data_{i}")
        st.text_input("Tipo", value="consulta", key=f"agenda_tipo_{i}")
    with col_b:
        st.time_input("Hora", key=f"agenda_hora_{i}")
        st.text_input("Local", value="—", key=f"agenda_local_{i}")
    st.text_area("Anotações", key=f"agenda_anot_{i}", height=80)
if st.button("➕ Adicionar compromisso de agenda"):
    st.session_state.agenda_count += 1
    st.rerun()

st.markdown("---")
st.markdown('<div class="section-label">► MEDICAÇÕES</div>', unsafe_allow_html=True)
for i in range(st.session_state.med_count):
    st.markdown(f"**Medicação {i + 1}**")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.text_input("Medicamento", key=f"med_nome_{i}")
        st.text_input("Dose", key=f"med_dose_{i}", value="—")
        st.time_input("Horário Previsto", key=f"med_prev_{i}")
    with col_m2:
        st.time_input("Horário Realizado", key=f"med_real_{i}")
        st.selectbox("Status", STATUS_MEDICACAO, key=f"med_status_{i}")
        st.text_input("Motivo (se não administrado)", key=f"med_motivo_{i}", value="—")
if st.button("➕ Adicionar medicação"):
    st.session_state.med_count += 1
    st.rerun()

st.markdown("---")

if st.button("⬡ GERAR RELATÓRIO HCB"):
    data_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    nome_arquivo = f"Relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    obs_txt = obs.strip() if obs and obs.strip() else "—"
    agenda_itens = []
    medicacoes = []

    for i in range(st.session_state.agenda_count):
        tipo = st.session_state.get(f"agenda_tipo_{i}", "").strip()
        local = st.session_state.get(f"agenda_local_{i}", "").strip()
        anot = st.session_state.get(f"agenda_anot_{i}", "").strip()
        data = st.session_state.get(f"agenda_data_{i}")
        hora = st.session_state.get(f"agenda_hora_{i}")
        if tipo or local != "—" or anot:
            agenda_itens.append(
                {
                    "data": data.strftime("%d/%m/%Y"),
                    "hora": hora.strftime("%H:%M"),
                    "tipo": tipo if tipo else "consulta",
                    "local": local if local else "—",
                    "anotacoes": anot if anot else "—",
                }
            )

    for i in range(st.session_state.med_count):
        nome = st.session_state.get(f"med_nome_{i}", "").strip()
        if not nome:
            continue
        status = st.session_state.get(f"med_status_{i}", "feito")
        motivo = st.session_state.get(f"med_motivo_{i}", "").strip() or "—"
        if status == "nao_administrado" and motivo == "—":
            st.warning("Informe o motivo da medicação não administrada.")
            st.stop()
        med_prev = st.session_state.get(f"med_prev_{i}")
        med_real = st.session_state.get(f"med_real_{i}")
        medicacoes.append(
            {
                "medicamento": nome,
                "dose": st.session_state.get(f"med_dose_{i}", "—").strip() or "—",
                "horario_previsto": med_prev.strftime("%H:%M"),
                "horario_realizado": med_real.strftime("%H:%M"),
                "status": status,
                "motivo": motivo,
            }
        )

    bloco_agenda = montar_bloco_agenda(agenda_itens)
    bloco_medicacoes = montar_bloco_medicacoes(medicacoes)

    if "dia do tribunal" in obs_txt.lower():
        conteudo = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HCB PROTOCOL — RELATÓRIO FISIO
DATA: {data_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠ OBSERVAÇÃO PRIORITÁRIA: DIA DO TRIBUNAL
TRANSPORTE: {TRANSPORTE_IDA} | {TRANSPORTE_VOLTA}
OBSERVAÇÕES: {obs_txt}
{bloco_agenda}
{bloco_medicacoes}
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
{bloco_agenda}
{bloco_medicacoes}
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
{bloco_agenda}
{bloco_medicacoes}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HCB Protocol v1.2 — PRODUCTION
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
            "agenda": agenda_itens,
            "medicacoes": medicacoes,
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
    "HCB PROTOCOL v1.2 — PRODUCTION &nbsp;|&nbsp; VINCULADO AO HCB SYSTEM"
    "</div>",
    unsafe_allow_html=True,
)
