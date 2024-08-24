import subprocess
import time
import io
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def generate_frames():
    logger.debug("Iniciando generate_frames")
    cmd = [
        'libcamera-vid',
        '-t', '0',
        '--inline',
        '--width', '640',
        '--height', '480',
        '--framerate', '15',
        '--codec', 'mjpeg',
        '-o', '-'
    ]
    
    logger.debug(f"Ejecutando comando: {' '.join(cmd)}")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        while True:
            # Leer los primeros 4 bytes para obtener el tamaño del frame
            frame_size_bytes = process.stdout.read(4)
            if not frame_size_bytes:
                logger.debug("No se pudo leer el tamaño del frame")
                break
            frame_size = int.from_bytes(frame_size_bytes, 'little')
            logger.debug(f"Tamaño del frame leído: {frame_size}")
            
            if frame_size <= 0 or frame_size > 10000000:  # 10MB como límite arbitrario
                logger.warning(f"Tamaño de frame inválido: {frame_size}")
                continue
            
            # Leer el frame completo
            frame_data = process.stdout.read(frame_size)
            if len(frame_data) != frame_size:
                logger.warning(f"Tamaño de frame incompleto. Esperado: {frame_size}, Leído: {len(frame_data)}")
                continue
            
            # Crear un objeto BytesIO para el frame
            frame = io.BytesIO(frame_data)
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.getvalue() + b'\r\n')
    except Exception as e:
        logger.error(f"Error en generate_frames: {e}")
    finally:
        logger.debug("Terminando subproceso de la cámara")
        process.terminate()