import tkinter as tk
from tkinter import filedialog, messagebox
import os

def limpiar_txt(input_file, output_file):
    """
    Función para limpiar un archivo de texto eliminando las líneas duplicadas.
    También limpia espacios adicionales, saltos de línea innecesarios y caracteres invisibles.
    """
    try:
        # Abrir el archivo de entrada para leerlo
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Limpiar espacios adicionales y saltos de línea innecesarios
        lines = [line.strip() for line in lines if line.strip()]  # Eliminar líneas vacías y limpiar espacios
        
        # Usar un conjunto para eliminar las líneas duplicadas y mantener el orden
        seen = set()
        lines_unicas = []
        
        for line in lines:
            # Limpiar caracteres invisibles, como tabulaciones, saltos de línea extra
            clean_line = line.replace("\t", " ").strip()
            
            if clean_line.lower() not in seen:  # Comparar sin importar mayúsculas o minúsculas
                seen.add(clean_line.lower())  # Agregar a 'seen' para evitar duplicados
                lines_unicas.append(line)
        
        # Guardar el archivo limpio
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in lines_unicas:
                f.write(line + '\n')
        
        return f"[INFO] El archivo ha sido limpiado y guardado como {output_file}"

    except Exception as e:
        return f"[ERROR] Error al limpiar el archivo: {e}"

# Función para abrir el cuadro de diálogo y seleccionar el archivo de entrada
def seleccionar_origen():
    archivo_origen = filedialog.askopenfilename(title="Selecciona el archivo de entrada", filetypes=[("Text Files", "*.txt")])
    entry_origen.delete(0, tk.END)  # Borrar el contenido anterior
    entry_origen.insert(0, archivo_origen)  # Mostrar la ruta seleccionada

# Función para abrir el cuadro de diálogo y seleccionar la ubicación del archivo de salida
def seleccionar_destino():
    archivo_destino = filedialog.asksaveasfilename(title="Selecciona la ubicación del archivo de salida", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    entry_destino.delete(0, tk.END)  # Borrar el contenido anterior
    entry_destino.insert(0, archivo_destino)  # Mostrar la ruta seleccionada

# Función para ejecutar la limpieza del archivo
def ejecutar_limpieza():
    input_path = entry_origen.get()
    output_path = entry_destino.get()
    
    if not input_path or not output_path:
        messagebox.showwarning("Advertencia", "Por favor, selecciona ambos archivos de origen y destino.")
        return

    # Llamar la función de limpieza
    mensaje = limpiar_txt(input_path, output_path)
    messagebox.showinfo("Resultado", mensaje)

# Crear la ventana principal de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Limpieza de Archivos de Texto")

# Crear widgets
label_origen = tk.Label(ventana, text="Archivo de origen:")
label_origen.grid(row=0, column=0, padx=10, pady=5, sticky="e")

entry_origen = tk.Entry(ventana, width=50)
entry_origen.grid(row=0, column=1, padx=10, pady=5)

boton_origen = tk.Button(ventana, text="Seleccionar", command=seleccionar_origen)
boton_origen.grid(row=0, column=2, padx=10, pady=5)

label_destino = tk.Label(ventana, text="Archivo de destino:")
label_destino.grid(row=1, column=0, padx=10, pady=5, sticky="e")

entry_destino = tk.Entry(ventana, width=50)
entry_destino.grid(row=1, column=1, padx=10, pady=5)

boton_destino = tk.Button(ventana, text="Seleccionar", command=seleccionar_destino)
boton_destino.grid(row=1, column=2, padx=10, pady=5)

boton_limpiar = tk.Button(ventana, text="Limpiar Archivo", command=ejecutar_limpieza)
boton_limpiar.grid(row=2, column=1, padx=10, pady=10)

# Ejecutar la ventana
ventana.mainloop()
