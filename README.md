# 🧠 HCB PROTOCOL — Sistema de Acompanhamento Fisioterapêutico

> **Este aplicativo só opera vinculado ao HCB Protocol.**
> Sem a cápsula Alma carregada, a sessão não tem continuidade cognitiva garantida.

---

## O que é o HCB Protocol?

O **Human Context Bus (HCB)** é um sistema de continuidade cognitiva que transporta **LOGOS** (razão estruturante) entre instâncias independentes de IA.

Em linguagem simples: é um protocolo que faz a IA **te conhecer de verdade** antes de começar a trabalhar — sem precisar recalibrar do zero em cada sessão.

### Como funciona

O HCB opera em 3 camadas, sempre nesta ordem:

| Camada | Nome | Conteúdo | Permanência |
|--------|------|----------|-------------|
| 1️⃣ | **Alma** | Identidade, estilo, valores, limitações físicas | Alta — só muda se você mudar |
| 2️⃣ | **HCB Protocol** | Regras do sistema, estrutura, princípios | Alta — só muda se o protocolo evoluir |
| 3️⃣ | **Gaveta Projeto** | Contexto específico, estado atual, histórico | Média — evolui com o projeto |

### Por que JSON?

IAs são treinadas massivamente em JSON. O formato garante:
- Estrutura semântica clara
- Alta densidade de informação
- Compatibilidade universal (qualquer IA lê JSON)
- Validação automática de sintaxe

---

## Este Aplicativo

**HCB Fisio Acompanhamento** é uma ferramenta de registro clínico desenvolvida dentro do protocolo HCB para acompanhar sessões de fisioterapia com:

- ✅ Registro de procedimentos realizados (Magnetismo, Eletrodo, Piscina, Massagem, etc.)
- ✅ Observações personalizadas por sessão
- ✅ Lógica de prioridade automática (Dia do Tribunal / Piscina)
- ✅ Geração e salvamento de relatórios
- ✅ Integração com Google Drive
- ✅ Acesso remoto via browser (PC e celular)

---

## Como usar

### 1. Pré-requisitos

```bash
pip install streamlit google-auth google-auth-oauthlib google-api-python-client
```

### 2. Configurar Google Drive (opcional)

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto e ative a **Google Drive API**
3. Gere credenciais OAuth 2.0 e baixe o `credentials.json`
4. Coloque o arquivo na raiz do projeto

### 3. Executar localmente

```bash
streamlit run app.py
```

### 4. Deploy no Streamlit Cloud

1. Suba o repositório no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte o repositório e configure os secrets do Google Drive

---

## Vinculação obrigatória ao HCB Protocol

Este app foi construído dentro do protocolo HCB. Para uso correto:

1. **Carregue a Alma** (cápsula de identidade do usuário) no início de cada sessão com IA
2. **Carregue o HCB Protocol** em seguida
3. **Carregue a Gaveta Projeto** com o contexto atual

Sem esse carregamento, a IA opera sem continuidade cognitiva — o que vai contra os princípios do protocolo.

---

## Estrutura do Projeto

```
📁 hcb-fisio/
├── app.py                  # Aplicativo principal Streamlit
├── README.md               # Este arquivo
├── requirements.txt        # Dependências
├── credentials.json        # Credenciais Google Drive (não versionar!)
├── HCB_Protocol.json       # Protocolo HCB v1.0
├── Perfil Usuário.json     # Cápsula Alma
└── Pasta Criada na nuvem   # Relatórios locais (fallback)
```

---

## Princípios do HCB aplicados aqui

| Princípio | Como se aplica |
|-----------|----------------|
| **Modularidade**    | Cada sessão de fisio = gaveta independente |
| **Continuidade**    | Histórico preservado entre sessões |
| **Transparência**   | Usuário vê o que foi registrado |
| **Respeito físico** | Interface adaptada para uso com limitações |
| **Persistência**    | LOGOS sobrevive mudanças de dispositivo/plataforma |

---

## Licença e Protocolo

**HCB Protocol v1.0 — PRODUCTION**
Desenvolvido através de engenharia cognitiva iterativa.
Criado em: 2026-02-03

> *"Construir não é fácil, amigo. Devagar, mas vamos!"*
