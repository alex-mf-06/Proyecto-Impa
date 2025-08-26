import tkinter as tk
from tkinter import messagebox
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

# Buscar cliente y mostrar historial
def buscar_cliente():
    nombre = entry_nombre.get().strip()
    if nombre not in clientes:
        messagebox.showerror("Error", "El cliente no existe.")
        return
    
    historial = clientes[nombre]
    texto = f"Historial de {nombre}:\n"
    for s in historial:
        texto += f"- {s['servicio']} | ${s['precio']:.2f} | {s['fecha']}\n"

    messagebox.showinfo("Historial", texto)

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
        messagebox.showinfo("Informe Semanal", "No hubo servicios en los últimos 7 días.")
        return

    informe = "\n".join(servicios_semana)
    informe += f"\n\nTOTAL SEMANAL: ${total:.2f}"

    # Guardar informe en archivo
    with open("informe_semanal.txt", "w", encoding="utf-8") as f:
        f.write(informe)

    messagebox.showinfo("Informe Semanal", informe)

# Limpiar los campos de entrada
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_servicio.delete(0, tk.END)
    entry_precio.delete(0, tk.END)

# Interfaz Tkinter
root = tk.Tk()
root.title("Gestión de Clientes")
root.geometry("400x350")

tk.Label(root, text="Nombre del Cliente:").pack()
entry_nombre = tk.Entry(root)
entry_nombre.pack()

tk.Label(root, text="Servicio:").pack()
entry_servicio = tk.Entry(root)
entry_servicio.pack()

tk.Label(root, text="Precio:").pack()
entry_precio = tk.Entry(root)
entry_precio.pack()

tk.Button(root, text="Registrar Cliente", command=registrar_cliente).pack(pady=5)
tk.Button(root, text="Agregar Servicio", command=agregar_servicio).pack(pady=5)
tk.Button(root, text="Buscar Cliente", command=buscar_cliente).pack(pady=5)
tk.Button(root, text="Informe Semanal", command=informe_semanal).pack(pady=5)

root.mainloop()