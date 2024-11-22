import os
import fitz  # PyMuPDF
from deep_translator import GoogleTranslator
import tkinter as tk
from tkinter import filedialog, messagebox

# Función para extraer texto de un archivo PDF
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text("text")  # Extracción de solo el texto de cada página
        print("[INFO] Texto extraído del PDF con éxito.")
        return text
    except Exception as e:
        print(f"[ERROR] Error al extraer texto del PDF: {e}")
        return ""

# Función para guardar el texto extraído en un archivo .txt
def save_text_to_txt(text, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"[INFO] Texto guardado exitosamente en {output_path}")
    except Exception as e:
        print(f"[ERROR] Error al guardar el archivo de texto: {e}")

# Función para dividir el texto en partes de menos de 5000 caracteres
def split_text(text, max_length=3000):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

# Función para traducir el texto
def translate_text(text, src='en', dest='es'):
    try:
        translator = GoogleTranslator(source=src, target=dest)
        translated_text = ""
        
        # Dividir el texto en partes si es necesario
        text_parts = split_text(text)
        
        for part in text_parts:
            translated_text += translator.translate(part) + " "
        
        print("[INFO] Texto traducido con éxito.")
        return translated_text.strip()
    except Exception as e:
        print(f"[ERROR] Error al traducir el texto: {e}")
        return ""

# Función para seleccionar el archivo PDF
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

# Función para seleccionar el directorio de salida
def select_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        entry_output_dir.delete(0, tk.END)
        entry_output_dir.insert(0, directory_path)

# Función para iniciar el procesamiento (extracción, traducción y conversión a archivo .txt)
def start_processing():
    pdf_path = entry_file_path.get()
    output_dir = entry_output_dir.get()
    if not pdf_path or not output_dir:
        messagebox.showerror("Error", "Por favor seleccione un archivo PDF y un directorio de salida.")
        return

    # Extracción de texto
    extracted_text = extract_text_from_pdf(pdf_path)
    if not extracted_text:
        messagebox.showerror("Error", "No se pudo extraer texto del PDF.")
        return

    # Guardar el texto extraído en un archivo .txt
    output_txt_path = os.path.join(output_dir, 'Extracted_Output.txt')
    save_text_to_txt(extracted_text, output_txt_path)

    # Traducir el texto
    translated_text = translate_text(extracted_text)
    if not translated_text:
        messagebox.showerror("Error", "No se pudo traducir el texto.")
        return

    # Guardar el texto traducido en un nuevo archivo .txt
    translated_txt_path = os.path.join(output_dir, 'Translated_Output.txt')
    save_text_to_txt(translated_text, translated_txt_path)

    messagebox.showinfo("Completado", f'Texto traducido guardado exitosamente en: {translated_txt_path}')

# Crear la ventana principal
root = tk.Tk()
root.title("Conversor y Traductor de PDF a TXT")

# Crear y colocar los widgets
tk.Label(root, text="Archivo PDF:").grid(row=0, column=0, padx=10, pady=10)
entry_file_path = tk.Entry(root, width=50)
entry_file_path.grid(row=0, column=1, padx=10, pady=10)
btn_select_file = tk.Button(root, text="Seleccionar archivo", command=select_file)
btn_select_file.grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Directorio de salida:").grid(row=1, column=0, padx=10, pady=10)
entry_output_dir = tk.Entry(root, width=50)
entry_output_dir.grid(row=1, column=1, padx=10, pady=10)
btn_select_directory = tk.Button(root, text="Seleccionar directorio", command=select_directory)
btn_select_directory.grid(row=1, column=2, padx=10, pady=10)

btn_start = tk.Button(root, text="Iniciar", command=start_processing)
btn_start.grid(row=2, column=1, padx=10, pady=20)

# Ejecutar la aplicación
root.mainloop()
