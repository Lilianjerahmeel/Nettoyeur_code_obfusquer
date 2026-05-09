"""
Point d'entrée principal du nettoyeur de code obfusqué.
Interface graphique Tkinter — deux colonnes :
  Gauche  : fichier source
  Droite  : code nettoyé + rapport
"""

import os
import tkinter as tk
from tkinter import filedialog, scrolledtext

from detector import analyze_script
from decoder  import decode_base64, decode_hex
from cleaner  import clean_code


# ==========================================
# Variables globales de l'interface

current_filepath = None


# ==========================================
# Logique métier

def load_file(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Fichier introuvable : {filepath}")
    if not filepath.endswith('.py'):
        raise ValueError("Le fichier doit être un script Python (.py)")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def build_decoded_map(analysis):
    decoded_map = {}
    for encoded in analysis.get("base64_strings", []):
        decoded = decode_base64(encoded)
        if decoded:
            decoded_map[encoded] = decoded
    for encoded in analysis.get("hex_strings", []):
        decoded = decode_hex(encoded)
        if decoded:
            decoded_map[encoded] = decoded
    return decoded_map


def save_result(cleaned_code, input_filepath):
    os.makedirs("output", exist_ok=True)
    filename    = os.path.basename(input_filepath)
    output_path = os.path.join("output", f"cleaned_{filename}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_code)
    return os.path.abspath(output_path)


def build_report(analysis, decoded_map, original, cleaned, filepath):
    var_base64     = analysis.get("base64_strings", [])
    var_hex      = analysis.get("hex_strings", [])
    var_suspicious     = analysis.get("suspicious_variables", [])
    removed = len(original.splitlines()) - len(cleaned.splitlines())

    lines = [
        "  RAPPORT D'ANALYSE",
        "=" * 50,
        "",
        f"  Fichier           : {os.path.basename(filepath)}",
        f"  Lignes originales : {len(original.splitlines())}",
        f"  Lignes nettoyees  : {len(cleaned.splitlines())}",
        f"  Lignes supprimees : {removed}",
        "",
        "-" * 50,
        "  DETECTIONS",
        "-" * 50,
        f"  Chaines Base64    : {len(var_base64)}",
        f"  Chaines Hex       : {len(var_hex)}",
        f"  Variables suspectes : {len(var_suspicious)}"
    ]

    return "\n".join(lines)

# ==========================================
# Actions des boutons

def on_open_file():
    global current_filepath

    path = filedialog.askopenfilename(
        title="Choisir un script Python",
        filetypes=[("Fichiers Python", "*.py"), ("Tous les fichiers", "*.*")]
    )
    if not path:
        return

    try:
        code = load_file(path)
    except Exception as e:
        set_status(f"ERREUR : {e}")
        return

    current_filepath = path
    filepath_var.set(os.path.basename(path))

    set_text(txt_source, code)
    lbl_lines.config(text=f"{len(code.splitlines())} lignes")

    set_text(txt_cleaned, "")
    set_text(txt_report, "")
    output_var.set("—")
    btn_clean.config(state="normal")
    set_status(f"Fichier charge : {os.path.basename(path)}")


def on_clean():
    global current_filepath

    if not current_filepath:
        return

    try:
        code = load_file(current_filepath)
    except Exception as e:
        set_status(f"ERREUR lecture : {e}")
        return

    set_status("Analyse en cours...")
    window.update_idletasks()

    try:
        analysis    = analyze_script(code)
        decoded_map = build_decoded_map(analysis)
        cleaned     = clean_code(code, decoded_map)
        output_path = save_result(cleaned, current_filepath)
    except Exception as e:
        set_status(f"ERREUR nettoyage : {e}")
        return

    set_text(txt_cleaned, cleaned)
    output_var.set(os.path.basename(output_path))
    set_text(txt_report, build_report(analysis, decoded_map, code, cleaned, current_filepath))
    set_status(f"Nettoyage termine  ->  {output_path}")


# ==========================================
# Helpers interface

def set_text(widget, text):
    widget.config(state="normal")
    widget.delete("1.0", "end")
    widget.insert("1.0", text)
    widget.config(state="disabled")

#pour afficher un message lorsque le code est en cours de traitement
def set_status(message):
    status_var.set(message)


def make_code_area(parent, row, height=None):
    """Crée une zone de texte scrollable avec grid."""
    frame = tk.Frame(parent, bg="#30363d")
    frame.grid(row=row, column=0, sticky="nsew", padx=10, pady=(0, 8))
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    area = scrolledtext.ScrolledText(
        frame,
        font=("Consolas", 10),
        bg="#0d1117", fg="#e6edf3",
        insertbackground="white",
        relief="flat", bd=0,
        wrap=tk.NONE,
        padx=10, pady=8,
    )
    if height:
        area.config(height=height)
    area.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
    return area


# ==========================================
# Construction de la fenêtre

window = tk.Tk()
window.title("Nettoyeur de Code Obfusque")
window.geometry("1300x780")
#window.minsize(600, 580)
window.configure(bg="#0f1117")

# ==========================================
# Titre principal 
title_bar = tk.Frame(window, bg="#1c2128", height=46)
title_bar.pack(fill="x", side="top")
title_bar.pack_propagate(False)

tk.Label(
    title_bar,
    text="NETTOYEUR DE CODE OBFUSQUE",
    fg="#e6edf3", bg="#1c2128",
    font=("Consolas", 12, "bold"),
    padx=16
).pack(side="left", pady=10)

tk.Label(
    title_bar,
    text="Analyse statique  |  Decodage  |  Nettoyage",
    fg="#8b949e", bg="#1c2128",
    font=("Consolas", 9),
).pack(side="left")


# ==========================================
# Corps principal (deux colonnes) 
body = tk.Frame(window, bg="#0f1117")
body.pack(fill="both", expand=True, padx=10, pady=8)
body.columnconfigure(0, weight=1, uniform="col")
body.columnconfigure(1, weight=1, uniform="col")
body.rowconfigure(0, weight=1)

col_left  = tk.Frame(body, bg="#161b22")
col_right = tk.Frame(body, bg="#161b22")
col_left.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
col_right.grid(row=0, column=1, sticky="nsew", padx=(5, 0))


# ==========================================
# Colonne gauche 
col_left.columnconfigure(0, weight=1)
col_left.rowconfigure(2, weight=1)

# En-tête
tk.Label(
    col_left,
    text="  FICHIER SOURCE",
    fg="#58a6ff", bg="#1c2128",
    font=("Consolas", 9, "bold"),
    anchor="w", pady=7
).grid(row=0, column=0, sticky="ew")

# Contrôles : bouton + champ chemin
ctrl_left = tk.Frame(col_left, bg="#161b22")
ctrl_left.grid(row=1, column=0, sticky="ew", padx=10, pady=8)
ctrl_left.columnconfigure(1, weight=1)

btn_open = tk.Button(
    ctrl_left,
    text="Choisir un fichier .py",
    command=on_open_file,
    bg="#58a6ff", fg="#0d1117",
    font=("Consolas", 9, "bold"),
    relief="flat", bd=0, cursor="hand2",
    padx=12, pady=6,
)
btn_open.grid(row=0, column=0)

filepath_var = tk.StringVar(value="Aucun fichier selectionne")
tk.Entry(
    ctrl_left,
    textvariable=filepath_var,
    state="disabled",
    disabledbackground="#21262d",
    disabledforeground="#8b949e",
    font=("Consolas", 9),
    relief="flat", bd=0,
).grid(row=0, column=1, sticky="ew", padx=(10, 0), ipady=6)

# Zone code source
txt_source = make_code_area(col_left, row=2)
txt_source.config(state="disabled")

# Compteur lignes
lbl_lines = tk.Label(col_left, text="", fg="#8b949e", bg="#161b22",
                     font=("Consolas", 8), anchor="e")
lbl_lines.grid(row=3, column=0, sticky="e", padx=12, pady=(0, 4))


# ==========================================
# Colonne droite
col_right.columnconfigure(0, weight=1)
col_right.rowconfigure(2, weight=3)
col_right.rowconfigure(5, weight=1)

# En-tête
tk.Label(
    col_right,
    text="  CODE NETTOYE",
    fg="#3fb950", bg="#1c2128",
    font=("Consolas", 9, "bold"),
    anchor="w", pady=7
).grid(row=0, column=0, sticky="ew")

# Contrôles : bouton + champ chemin output
ctrl_right = tk.Frame(col_right, bg="#161b22")
ctrl_right.grid(row=1, column=0, sticky="ew", padx=10, pady=8)
ctrl_right.columnconfigure(1, weight=1)

btn_clean = tk.Button(
    ctrl_right,
    text="Nettoyer le code",
    command=on_clean,
    bg="#3fb950", fg="#0d1117",
    font=("Consolas", 9, "bold"),
    relief="flat", bd=0, cursor="hand2",
    padx=12, pady=6,
    state="disabled",
)
btn_clean.grid(row=0, column=0)

output_var = tk.StringVar(value="—")
tk.Entry(
    ctrl_right,
    textvariable=output_var,
    state="disabled",
    disabledbackground="#21262d",
    disabledforeground="#3fb950",
    font=("Consolas", 9),
    relief="flat", bd=0,
).grid(row=0, column=1, sticky="ew", padx=(10, 0), ipady=6)

# Zone code nettoyé
txt_cleaned = make_code_area(col_right, row=2)
txt_cleaned.config(state="disabled")

# En-tête rapport
tk.Label(
    col_right,
    text="  RAPPORT D'ANALYSE",
    fg="#e3b341", bg="#1c2128",
    font=("Consolas", 9, "bold"),
    anchor="w", pady=6
).grid(row=3, column=0, sticky="ew", padx=0, pady=(4, 0))

tk.Frame(col_right, bg="#30363d", height=1).grid(
    row=4, column=0, sticky="ew", padx=10)

# Zone rapport
txt_report = make_code_area(col_right, row=5, height=9)
txt_report.config(state="disabled")


# ==========================================
# Barre de statut
status_bar = tk.Frame(window, bg="#1c2128", height=26)
status_bar.pack(fill="x", side="bottom")
status_bar.pack_propagate(False)

status_var = tk.StringVar(value="Pret  -  Selectionnez un fichier .py a analyser")
tk.Label(
    status_bar,
    textvariable=status_var,
    fg="#8b949e", bg="#1c2128",
    font=("Consolas", 8), anchor="w"
).pack(side="left", padx=14)


# ==========================================
# Lancement

window.mainloop()