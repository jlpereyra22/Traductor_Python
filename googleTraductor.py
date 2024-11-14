import os
import PyPDF2
from deep_translator import GoogleTranslator
from fpdf import FPDF
import tkinter as tk
from tkinter import filedialog, messagebox

# Función para extraer texto de un PDF entre dos páginas específicas
def extract_text_from_pdf(pdf_path, start_page, end_page):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(start_page, end_page):
            if page_num < len(reader.pages):
                page = reader.pages[page_num]
                text += page.extract_text()
    return text

# Función para dividir el texto en partes más pequeñas
def split_text(text, max_chars=3000):
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

# Función para traducir texto usando deep-translator
def translate_text(text, src='en', dest='es'):
    translator = GoogleTranslator(source=src, target=dest)
    parts = split_text(text, max_chars=3000)  # Ahora con un tamaño de 3000 caracteres
    translated_text = ""
    for part in parts:
        translated_text += translator.translate(part) + " "  # Añadir un espacio entre las partes traducidas
    return translated_text.strip()  # Eliminar espacios en blanco al final

# Función para crear un PDF a partir de un texto
def create_pdf_from_text(text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, text)
    pdf.ln()
    pdf.output(output_path)

# Función para combinar múltiples PDFs en uno solo
def combine_pdfs(pdf_list, output_path):
    pdf_writer = PyPDF2.PdfWriter()
    for pdf in pdf_list:
        pdf_reader = PyPDF2.PdfReader(pdf)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)
    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

# Función principal que procesa el PDF en partes, traduce cada parte y crea PDFs parciales
def process_pdf(pdf_path, output_dir):
    chunk_size = 10
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    num_pages = len(pdf_reader.pages)
    pdf_chunks = []

    # Procesar el PDF en partes de chunk_size páginas
    for start_page in range(0, num_pages, chunk_size):
        end_page = min(start_page + chunk_size, num_pages)
        chunk_text = extract_text_from_pdf(pdf_path, start_page, end_page)
        
        # Traducción del texto extraído
        translated_text = translate_text(chunk_text)
        
        # Guardar el texto traducido en un PDF
        chunk_pdf_path = os.path.join(output_dir, f'chunk_{start_page // chunk_size + 1}.pdf')
        create_pdf_from_text(translated_text, chunk_pdf_path)
        pdf_chunks.append(chunk_pdf_path)

    # Combinar todos los PDFs parciales en un único PDF final
    final_pdf_path = os.path.join(output_dir, 'CompTIA_Security_plus_translated.pdf')
    combine_pdfs(pdf_chunks, final_pdf_path)
    messagebox.showinfo("Completado", f'PDF final traducido guardado en: {final_pdf_path}')

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

# Función para iniciar el procesamiento del PDF
def start_processing():
    pdf_path = entry_file_path.get()
    output_dir = entry_output_dir.get()
    if not pdf_path or not output_dir:
        messagebox.showerror("Error", "Por favor seleccione un archivo PDF y un directorio de salida.")
        return
    process_pdf(pdf_path, output_dir)

# Crear la ventana principal
root = tk.Tk()
root.title("Traductor de PDF")

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


