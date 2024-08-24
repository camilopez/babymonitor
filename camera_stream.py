import logging

logging.basicConfig(level=logging.DEBUG)

def generate_frames():
    logging.debug("Iniciando generate_frames")
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
    
    logging.debug(f"Ejecutando comando: {' '.join(cmd)}")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        while True:
            frame = process.stdout.read(65536)
            if not frame:
                logging.debug("No se leyeron datos del subproceso")
                break
            logging.debug(f"Leído frame de {len(frame)} bytes")
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.01)
    except Exception as e:
        logging.error(f"Error en generate_frames: {e}")
    finally:
        logging.debug("Terminando subproceso de la cámara")
        process.terminate()