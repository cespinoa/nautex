#!/bin/bash

# Comprobación de ejecución con sudo
if [ "$EUID" -ne 0 ]; then
    echo "Este script necesita ejecutarse con privilegios de superusuario (sudo)."
    exit 1
fi

# Ruta del directorio donde se colocará el script y el entorno virtual
extensions_dir="/usr/local/share/nautilus-python/extensions"
venv_dir="$extensions_dir/env"
script_name="pdf_to_jpg_nautilus.py"
script_source="https://github.com/cespinoa/nautex/raw/main/pdf_to_jpg_nautilus.py"

# Paso 1: Crear el directorio /usr/local/share/nautilus-python/extensions/ si no existe
if [ ! -d "$extensions_dir" ]; then
    sudo mkdir -p "$extensions_dir"
fi

# Paso 2: Crear el entorno virtual Python en /usr/local/share/nautilus-python/extensions/env si no existe
if [ ! -d "$venv_dir" ]; then
    sudo python3 -m venv "$venv_dir"
fi

# Paso 3: Activar el entorno virtual
source "$venv_dir/bin/activate"

# Paso 4: Instalar las dependencias necesarias
pip install PyGObject pdf2image notify2 img2pdf

# Paso 5: Descargar el script desde GitHub y copiarlo a /usr/local/share/nautilus-python/extensions
sudo wget "$script_source" -O "$extensions_dir/$script_name"

# Asegurarse de que el script tenga permisos adecuados para ejecución (opcional)
sudo chmod +x "$extensions_dir/$script_name"

# Salir del entorno virtual al finalizar
deactivate

echo "Instalación completada."
