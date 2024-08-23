#!/bin/bash

# Navegar al directorio del proyecto
cd /home/pi/babymonitor

# Obtener los últimos cambios
git pull

# Activar el entorno virtual
source venv/bin/activate

# Instalar o actualizar dependencias
pip install -r requirements.txt

# Reiniciar el servicio
sudo systemctl restart webportal.service

echo "Actualización completada y servicio reiniciado."