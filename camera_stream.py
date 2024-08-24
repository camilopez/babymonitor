import subprocess
import time
import io
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def generate_frames():
    logger.debug("Iniciando generate_frames")
    cmd = [
        'raspivid',
        '-t', '0',
        '-o', '-',
        '-w', '640',
        '-h', '480',
        '-fps', '15',
        '-pf', 'baseline'
    ]
    
    logger.debug(f"Ejecutando comando: {' '.join(cmd)}")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        while True:
            # Leer un chunk fijo de datos
            chunk = process.stdout.read(4096)
            if not chunk:
                logger.debug("No se pudo leer datos del proceso")
                break
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + chunk + b'\r\n')
    except Exception as e:
        logger.error(f"Error en generate_frames: {e}")
    finally:
        logger.debug("Terminando subproceso de la cámara")
        process.terminate()