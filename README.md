# 🧠 HCB PROTOCOL — Sistema de Acompanhamento Fisioterapêutico

> Este aplicativo opera vinculado ao HCB Protocol para manter continuidade de contexto clínico.

---

## O que é o HCB Protocol?

O **Human Context Bus (HCB)** é um sistema de continuidade de contexto entre sessões, com foco em consistência operacional e rastreabilidade.

### Camadas do HCB

| Camada | Nome | Conteúdo | Permanência |
|--------|------|----------|-------------|
| 1 | Alma | Identidade, estilo, limites físicos | Alta |
| 2 | HCB Protocol | Regras, estrutura, princípios | Alta |
| 3 | Gaveta Projeto | Estado atual e histórico do caso | Média |

---

## Este aplicativo (estado atual v1.2)

**HCB Fisio Acompanhamento** é um app Streamlit para registro de sessões, com foco em rotina clínica de fisioterapia.

### Funcionalidades atuais

- Registro de procedimentos da sessão
- Substituição de **Piscina** por **Hidroginástica**
- **Transporte obrigatório** em toda sessão:
  - `Ida Transporte`
  - `Volta Transporte`
- Observações clínicas por sessão
- Regra de prioridade:
  - `dia do tribunal`
  - `Hidroginástica` (anula demais procedimentos clínicos)
- Geração de relatório `.txt`
- Salvamento no Google Drive (quando configurado) com fallback local
- Persistência JSON robusta:
  - `dados_v1.json` (base principal)
  - `dados_v1.backup.json` (backup automático)
  - escrita atômica para reduzir risco de corrupção
- Histórico carregado entre sessões/dispositivos
- Módulos de **Agenda médica** e **Medicações** integrados ao relatório e ao JSON

---

## Acessibilidade visual (crucial)

O app inclui um modo dedicado: `Modo de alta acessibilidade visual (WCAG)`.

### O que esse modo faz

- Aumenta contraste de texto e componentes
- Amplia tipografia e áreas clicáveis
- Destaca foco de teclado com contorno visível
- Melhora legibilidade de campos e labels
- Respeita `prefers-reduced-motion` para reduzir animações

> Recomendação: manter este modo ativo para usuários com baixa visão, fadiga ocular ou uso em ambientes clínicos com iluminação variável.

---

## Como usar

### 1. Pré-requisitos

```bash
pip install streamlit google-auth google-api-python-client
```

### 2. Configurar Google Drive (opcional, via `st.secrets`)

No Streamlit Cloud, configure:
- `google_drive` (service account JSON)
- `drive_folder_id` (opcional)

> Se não houver configuração válida do Drive, o app salva localmente em `04_RELATORIOS_GERADOS/`.

### 3. Executar localmente

```bash
streamlit run "01_DESENVOLVIMENTO/O Sistema HCB - Edição de Luxo - Fisio Acompanhamento.py"
```

### 4. Deploy no Streamlit Cloud

1. Subir o repositório no GitHub
2. Criar app no Streamlit Cloud
3. Configurar `secrets` do Google Drive
4. Publicar

---

## Estrutura de dados local

```text
04_RELATORIOS_GERADOS/
├── Relatorio_YYYYMMDD_HHMMSS.txt
├── dados_v1.json
└── dados_v1.backup.json
```

---

## Estrutura sugerida do projeto

```text
hcb-fisio/
├── 01_DESENVOLVIMENTO/
│   └── O Sistema HCB - Edição de Luxo - Fisio Acompanhamento.py
├── README.md
├── requirements.txt
└── 04_RELATORIOS_GERADOS/   # criado automaticamente em runtime
```

---

## Princípios aplicados

| Princípio | Aplicação |
|-----------|-----------|
| Continuidade | Histórico persistente entre sessões |
| Segurança operacional | Transporte obrigatório e regras de prioridade |
| Transparência | Pré-visualização e histórico de relatórios |
| Persistência | JSON principal + backup + escrita atômica |
| Acessibilidade | Uso via navegador (desktop e celular) |

---

## Versão

**HCB Protocol v1.2 — PRODUCTION**
