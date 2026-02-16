import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

# --- Configurações de Cores HCB ---
COR_PLATINA = "#E5E4E2"
COR_ESMERALDA = "#2E8B57"
COR_VISOR = "#B0E0E6"
COR_FONTE = "#005F6B"


def gerar_relatorio():
    # Criar pasta automaticamente se não existir
    pasta = "04_RELATORIOS_GERADOS"
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    data_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    obs = entrada_obs.get()

    # Lógica de Prioridade
    if "dia do tribunal" in obs.lower():
        conteudo = f"RELATÓRIO HCB - DATA: {data_str}\nOBSERVAÇÃO PRIORITÁRIA: DIA DO TRIBUNAL"
    elif check_vars["Piscina"].get():
        conteudo = f"RELATÓRIO HCB - DATA: {data_str}\nATIVIDADE: PISCINA (Outros procedimentos anulados)"
    else:
        selecionados = [item for item, var in check_vars.items() if var.get()]
        conteudo = f"RELATÓRIO HCB - DATA: {data_str}\nPROCEDIMENTOS: {', '.join(selecionados)}\nOBS: {obs}"

    # Salvar o TXT
    nome_arq = f"{pasta}/Relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(nome_arq, "w", encoding="utf-8") as f:
        f.write(conteudo)

    messagebox.showinfo("Imprimir", "Relatório enviado para a pasta 04!")


def limpar_placeholder(event):
    if entrada_obs.get() == "Suas observações aqui...":
        entrada_obs.delete(0, tk.END)
        entrada_obs.config(fg="black")


# --- Interface ---
janela = tk.Tk()
janela.title("HCB PROTOCOL - PLATINUM")
janela.geometry("400x650")
janela.configure(bg=COR_PLATINA)

# Visor Azul
visor = tk.Label(janela, text="HCB SYSTEM READY", bg=COR_VISOR, fg=COR_FONTE,
                 font=("Courier New", 14, "bold"), pady=15, relief="sunken", borderwidth=5)
visor.pack(fill="x", padx=20, pady=20)

# Lista de Checkboxes
itens = ["Ida Táxi", "Magnetismo", "Eletrodo", "Massagem", "Piscina", "Gelo", "Volta Táxi", "Outros"]
check_vars = {}

frame_checks = tk.Frame(janela, bg=COR_PLATINA)
frame_checks.pack(pady=10)

for item in itens:
    var = tk.BooleanVar()
    cb = tk.Checkbutton(frame_checks, text=item, variable=var, bg=COR_PLATINA,
                        font=("Arial", 11), activebackground=COR_ESMERALDA)
    cb.pack(anchor="w")
    check_vars[item] = var

# Caixa de Observações
entrada_obs = tk.Entry(janela, font=("Arial", 12), bg="#F0F0F0", fg="grey", borderwidth=2)
entrada_obs.insert(0, "Suas observações aqui...")
entrada_obs.bind("<FocusIn>", limpar_placeholder)
entrada_obs.pack(pady=20, padx=30, fill="x")

# Botão Esmeralda Metálico
btn_imprimir = tk.Button(janela, text="IMPRIMIR RELATÓRIO", command=gerar_relatorio,
                         bg=COR_ESMERALDA, fg="white", font=("Arial", 12, "bold"),
                         relief="raised", borderwidth=5, pady=10)
btn_imprimir.pack(pady=20)

janela.mainloop()
