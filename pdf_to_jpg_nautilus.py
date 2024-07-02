#!/usr/local/share/nautilus-python/extensions/env/bin/python

import os
import sys

# Entorno virtual está en el sys.path
venv_path = os.path.expanduser('/usr/local/share/nautilus-python/extensions/env')
venv_lib = os.path.join(venv_path, 'lib', 'python3.12', 'site-packages')
sys.path.insert(0, venv_lib)

import notify2
import gi
gi.require_version('Nautilus', '4.0')
from gi.repository import Nautilus, GObject
from pdf2image import convert_from_path
import img2pdf
# ~ from typing import List

class PdfToJpgExtension(GObject.GObject, Nautilus.MenuProvider):

    def __init__(self):
        super(PdfToJpgExtension, self).__init__()
        notify2.init("PdfToJpgExtension")

    def convert_pdf_to_jpg(self, menu, files):
        for file in files:
            if file.get_uri_scheme() == 'file' and file.is_mime_type('application/pdf'):
                filepath = file.get_location().get_path()
                self._convert(filepath)

    def _convert(self, pdf_path):
        output_dir = os.path.dirname(pdf_path)
        try:
            images = convert_from_path(pdf_path)
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            
            output_folder = os.path.join(output_dir, f"{base_name}_converted_to_jpg")
            os.makedirs(output_folder, exist_ok=True)
            
            for i, image in enumerate(images):
                jpg_path = os.path.join(output_folder, f"{base_name}_page_{i + 1}.jpg")
                image.save(jpg_path, 'JPEG')
            
            self.show_notification(f"Converted {pdf_path} to JPEG images", f"In folder: {output_folder}")
        except Exception as e:
            self.show_notification(f"Error converting {pdf_path}: {e}")

    def show_notification(self, title, message):
        notification = notify2.Notification(title, message)
        notification.show()


    def get_file_items(self, files):
        pdf_items = []
        jpg_items = []

        for file in files:
            if file.is_mime_type('application/pdf'):
                pdf_items.append(file)
            elif file.is_mime_type('image/jpeg'):
                jpg_items.append(file)

        menu_items = []

        if pdf_items:
            pdf_item = Nautilus.MenuItem(
                name="PdfToJpgExtension::ConvertPdfToJpg",
                label="Convert PDF to JPG",
                tip="Convert each page of the PDF to a JPG image",
                icon="image-x-generic"
            )
            pdf_item.connect("activate", self.convert_pdf_to_jpg, pdf_items)
            menu_items.append(pdf_item)

        if jpg_items:
            join_pdf_item = Nautilus.MenuItem(
                name="PdfToJpgExtension::JoinJpgToPdf",
                label="Join JPGs into PDF",
                tip="Combine selected JPG files into a single PDF",
                icon="image-x-generic"
            )
            join_pdf_item.connect("activate", self.join_jpg_to_pdf, jpg_items)
            menu_items.append(join_pdf_item)

        return menu_items
        
    def join_jpg_to_pdf(self, menu, files):
        # Filtrar solo archivos JPG seleccionados
        jpg_files = [file for file in files if file.get_uri_scheme() == 'file' and file.is_mime_type('image/jpeg')]

        if not jpg_files:
            self.show_notification("No JPG files selected", "Please select JPG files to merge into PDF.")
            return

        # Obtener la carpeta de salida basada en el primer archivo JPG
        first_file_path = jpg_files[0].get_location().get_path()
        output_dir = os.path.dirname(first_file_path)
        base_name = os.path.splitext(os.path.basename(first_file_path))[0]
        pdf_output_path = os.path.join(output_dir, f"{base_name}.pdf")

        # Ordenar los archivos JPG seleccionados por nombre de archivo
        jpg_files.sort(key=lambda f: f.get_name())

        # Convertir los archivos JPG a PDF
        with open(pdf_output_path, "wb") as pdf_file:
            pdf_file.write(img2pdf.convert([file.get_location().get_path() for file in jpg_files]))

        self.show_notification(f"Created PDF: {pdf_output_path}", "Successfully merged JPG files into PDF.")


        
    

# Para probar la inicialización en la terminal
if __name__ == "__main__":
    extension = PdfToJpgExtension()
