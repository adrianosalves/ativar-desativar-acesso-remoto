import subprocess
import tkinter as tk
from tkinter import messagebox
import sys
import ctypes

SERVICE_NAME = "A1Agent"
SERVICE_DISPLAY_NAME = "ALVESNET Suporte Remoto"

COLOR_GREEN = "#22c55e"
COLOR_RED = "#ef4444"
COLOR_ORANGE = "#f97316"
COLOR_GRAY = "#6b7280"
COLOR_BG = "#f0f0f0"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_sc_command(args):
    cmd = "sc " + " ".join(args)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def get_service_status():
    code, stdout, stderr = run_sc_command(["query", SERVICE_NAME])
    if code != 0:
        return "Nao encontrado"

    if "STOPPED" in stdout:
        return "Parado"
    elif "RUNNING" in stdout:
        return "Em execucao"
    elif "START_PENDING" in stdout:
        return "Iniciando"
    elif "STOP_PENDING" in stdout:
        return "Parando"
    return "Desconhecido"

def get_start_type():
    code, stdout, stderr = run_sc_command(["qc", SERVICE_NAME])
    if code != 0:
        return "Nao encontrado"

    if "DISABLED" in stdout:
        return "Desabilitado"
    elif "DEMAND" in stdout:
        return "Manual"
    elif "AUTO" in stdout:
        return "Automatico"
    return "Desconhecido"

def ativar_servico():
    if not is_admin():
        messagebox.showerror(
            "Erro de Permissao",
            "Este programa precisa ser executado como ADMINISTRADOR.\n\n"
            "Clique com o botao direito no arquivo e selecione 'Executar como administrador'."
        )
        return

    status = get_service_status()

    if status == "Em execucao":
        messagebox.showinfo("Info", f"{SERVICE_DISPLAY_NAME} ja esta em execucao!")
        return

    run_sc_command(["config", SERVICE_NAME, "start=demand"])
    code, stdout, stderr = run_sc_command(["start", SERVICE_NAME])

    if code == 0 or "RUNNING" in stdout or "START_PENDING" in stdout:
        messagebox.showinfo("Sucesso", f"{SERVICE_DISPLAY_NAME}: ATIVADO!")
    elif "FALHA 1056" in stdout or "already running" in stdout.lower():
        messagebox.showinfo("Info", f"{SERVICE_DISPLAY_NAME} ja esta em execucao!")
    elif "FALHA 5" in stdout or "Acesso negado" in stdout:
        messagebox.showerror(
            "Erro de Permissao",
            "Execute este programa como ADMINISTRADOR."
        )
    else:
        messagebox.showerror("Erro", f"Falha ao ativar: {stdout}")

    atualizar_status()

def desativar_servico():
    if not is_admin():
        messagebox.showerror(
            "Erro de Permissao",
            "Este programa precisa ser executado como ADMINISTRADOR.\n\n"
            "Clique com o botao direito no arquivo e selecione 'Executar como administrador'."
        )
        return

    status = get_service_status()

    if status == "Parado":
        messagebox.showinfo("Info", f"{SERVICE_DISPLAY_NAME} ja esta parado!")
        return

    code, stdout, stderr = run_sc_command(["stop", SERVICE_NAME])
    run_sc_command(["config", SERVICE_NAME, "start=disabled"])

    if code == 0 or "STOPPED" in stdout or "STOP_PENDING" in stdout:
        messagebox.showinfo("Sucesso", f"{SERVICE_DISPLAY_NAME}: DESATIVADO!")
    elif "FALHA 1052" in stdout or "not stopped" in stdout.lower():
        messagebox.showwarning("Aviso", "Servico esta sendo parado, aguarde...")
    elif "FALHA 5" in stdout or "Acesso negado" in stdout:
        messagebox.showerror(
            "Erro de Permissao",
            "Execute este programa como ADMINISTRADOR."
        )
    else:
        messagebox.showerror("Erro", f"Falha ao desativar: {stdout}")

    atualizar_status()

def atualizar_status():
    status = get_service_status()
    start_type = get_start_type()

    lbl_status.config(text=status)
    lbl_inicio.config(text=start_type)

    if status == "Em execucao":
        lbl_status.config(fg=COLOR_GREEN)
        canvas.delete("all")
        canvas.create_oval(2, 2, 18, 18, fill=COLOR_GREEN, outline=COLOR_GREEN)
    elif status == "Parado":
        lbl_status.config(fg=COLOR_RED)
        canvas.delete("all")
        canvas.create_oval(2, 2, 18, 18, fill=COLOR_RED, outline=COLOR_RED)
    else:
        lbl_status.config(fg=COLOR_ORANGE)
        canvas.delete("all")
        canvas.create_oval(2, 2, 18, 18, fill=COLOR_ORANGE, outline=COLOR_ORANGE)

    if start_type == "Desabilitado":
        lbl_inicio.config(fg=COLOR_RED)
    elif start_type == "Manual":
        lbl_inicio.config(fg=COLOR_GREEN)
    elif start_type == "Automatico":
        lbl_inicio.config(fg=COLOR_ORANGE)
    else:
        lbl_inicio.config(fg=COLOR_GRAY)

def on_ativar():
    ativar_servico()

def on_desativar():
    desativar_servico()

root = tk.Tk()
root.title(f"Gerenciador - {SERVICE_DISPLAY_NAME}")
root.geometry("400x350")
root.configure(bg=COLOR_BG)

# Aviso se não for admin
if not is_admin():
    aviso = tk.Label(
        root,
        text="Execute como Administrador!",
        font=("Arial", 10, "bold"),
        bg=COLOR_RED,
        fg="white",
        padx=10,
        pady=5
    )
    aviso.pack(pady=5, fill=tk.X)

lbl_titulo = tk.Label(
    root,
    text=SERVICE_DISPLAY_NAME,
    font=("Arial", 16, "bold"),
    bg=COLOR_BG
)
lbl_titulo.pack(pady=15)

frame_status = tk.LabelFrame(
    root,
    text="Status do Servico",
    font=("Arial", 11, "bold"),
    bg=COLOR_BG,
    padx=20,
    pady=10
)
frame_status.pack(fill=tk.X, padx=30, pady=5)

canvas = tk.Canvas(frame_status, width=20, height=20, bg=COLOR_BG, highlightthickness=0)
canvas.pack(side=tk.LEFT, padx=(0, 10))
canvas.create_oval(2, 2, 18, 18, fill=COLOR_GRAY, outline=COLOR_GRAY)

lbl_status = tk.Label(
    frame_status,
    text="",
    font=("Arial", 14, "bold"),
    bg=COLOR_BG,
    fg=COLOR_GRAY
)
lbl_status.pack(side=tk.LEFT)

frame_inicio = tk.LabelFrame(
    root,
    text="Inicializacao",
    font=("Arial", 11, "bold"),
    bg=COLOR_BG,
    padx=20,
    pady=10
)
frame_inicio.pack(fill=tk.X, padx=30, pady=5)

lbl_inicio = tk.Label(
    frame_inicio,
    text="",
    font=("Arial", 12),
    bg=COLOR_BG,
    fg=COLOR_GRAY
)
lbl_inicio.pack(side=tk.LEFT)

frame_botoes = tk.Frame(root, bg=COLOR_BG)
frame_botoes.pack(pady=25)

btn_ativar = tk.Button(
    frame_botoes,
    text="[+] ATIVAR",
    width=14,
    font=("Arial", 12, "bold"),
    bg=COLOR_GREEN,
    fg="white",
    command=on_ativar,
    relief="raised",
    bd=3
)
btn_ativar.pack(side=tk.LEFT, padx=10)

btn_desativar = tk.Button(
    frame_botoes,
    text="[X] DESATIVAR",
    width=14,
    font=("Arial", 12, "bold"),
    bg=COLOR_RED,
    fg="white",
    command=on_desativar,
    relief="raised",
    bd=3
)
btn_desativar.pack(side=tk.LEFT, padx=10)

btn_atualizar = tk.Button(
    root,
    text="Atualizar",
    font=("Arial", 10),
    bg=COLOR_GRAY,
    fg="white",
    command=atualizar_status
)
btn_atualizar.pack(pady=10)

atualizar_status()

root.mainloop()