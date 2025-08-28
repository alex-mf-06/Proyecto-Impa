import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import os
from datetime import datetime, timedelta

# Archivo donde se guardan los datos
ARCHIVO = "clientes.json"

# Cargar datos guardados o iniciar vacío
if os.path.exists(ARCHIVO):
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        clientes = json.load(f)
else:
    clientes = {}

# Guardar clientes en JSON
def guardar_datos():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)

# Registrar cliente con primer servicio
def registrar_cliente():
    nombre = entry_nombre.get().strip()
    servicio = entry_servicio.get().strip()
    precio = entry_precio.get().strip()

    if not nombre or not servicio or not precio:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    
    try:
        precio = float(precio)
        if precio <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número positivo.")
        return

    if nombre not in clientes:
        clientes[nombre] = []

    clientes[nombre].append({
        "servicio": servicio,
        "precio": precio,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    guardar_datos()
    messagebox.showinfo("Éxito", f"Cliente '{nombre}' registrado con el servicio.")
    limpiar_campos()

# Agregar servicio a un cliente existente
def agregar_servicio():
    nombre = entry_nombre.get().strip()
    servicio = entry_servicio.get().strip()
    precio = entry_precio.get().strip()

    if nombre not in clientes:
        messagebox.showerror("Error", "El cliente no existe. Regístralo primero.")
        return
    
    if not servicio or not precio:
        messagebox.showerror("Error", "Debes ingresar servicio y precio.")
        return
    
    try:
        precio = float(precio)
        if precio <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un número positivo.")
        return

    clientes[nombre].append({
        "servicio": servicio,
        "precio": precio,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    guardar_datos()
    messagebox.showinfo("Éxito", f"Servicio agregado al cliente '{nombre}'.")
    limpiar_campos()

# Buscar cliente y mostrar historial en área de texto
def buscar_cliente():
    nombre = entry_nombre.get().strip()
    if nombre not in clientes:
        messagebox.showerror("Error", "El cliente no existe.")
        return
    
    historial = clientes[nombre]
    texto = f"Historial de {nombre}:\n"
    for s in historial:
        texto += f"- {s['servicio']} | ${s['precio']:.2f} | {s['fecha']}\n"

    mostrar_texto(texto)

# Generar informe semanal
def informe_semanal():
    ahora = datetime.now()
    semana = ahora - timedelta(days=7)
    total = 0
    servicios_semana = []

    for cliente, servicios in clientes.items():
        for s in servicios:
            fecha = datetime.strptime(s["fecha"], "%Y-%m-%d %H:%M:%S")
            if fecha >= semana:
                total += s["precio"]
                servicios_semana.append(f"{cliente}: {s['servicio']} | ${s['precio']:.2f} | {s['fecha']}")

    if not servicios_semana:
        mostrar_texto("No hubo servicios en los últimos 7 días.")
        return

    informe = "\n".join(servicios_semana)
    informe += f"\n\nTOTAL SEMANAL: ${total:.2f}"

    # Guardar informe en archivo
    with open("informe_semanal.txt", "w", encoding="utf-8") as f:
        f.write(informe)

    mostrar_texto(informe)

# Mostrar resultados en área de texto
def mostrar_texto(texto):
    text_area.config(state="normal")
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, texto)
    text_area.config(state="disabled")

# Limpiar los campos de entrada
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_servicio.delete(0, tk.END)
    entry_precio.delete(0, tk.END)

# Confirmar antes de salir
def confirmar_salida():
    if messagebox.askyesno("Salir", "¿Seguro que quieres salir?"):
        root.destroy()

# Interfaz Tkinter
root = tk.Tk()
root.title("Gestión de Clientes")
root.geometry("500x500")
root.configure(bg="#f0f0f0")

# Frame para entradas
frame_inputs = tk.Frame(root, bg="#f0f0f0")
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Nombre del Cliente:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
entry_nombre = tk.Entry(frame_inputs, width=30)
entry_nombre.grid(row=0, column=1, pady=5)

tk.Label(frame_inputs, text="Servicio:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w")
entry_servicio = tk.Entry(frame_inputs, width=30)
entry_servicio.grid(row=1, column=1, pady=5)

tk.Label(frame_inputs, text="Precio:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w")
entry_precio = tk.Entry(frame_inputs, width=30)
entry_precio.grid(row=2, column=1, pady=5)

# Frame para botones
frame_botones = tk.Frame(root, bg="#f0f0f0")
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Registrar Cliente", command=registrar_cliente, width=20, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_botones, text="Agregar Servicio", command=agregar_servicio, width=20, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_botones, text="Buscar Cliente", command=buscar_cliente, width=20, bg="#FFC107", fg="black").grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_botones, text="Informe Semanal", command=informe_semanal, width=20, bg="#9C27B0", fg="white").grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame_botones, text="Limpiar Campos", command=limpiar_campos, width=20, bg="#FF5722", fg="white").grid(row=2, column=0, columnspan=2, pady=5)

# Área de texto para mostrar resultados
text_area = scrolledtext.ScrolledText(root, width=60, height=12, wrap=tk.WORD, state="disabled", font=("Courier New", 10))
text_area.pack(pady=10)

# Evento al cerrar ventana
root.protocol("WM_DELETE_WINDOW", confirmar_salida)

root.mainloop()
