import subprocess
import time
import io

def generate_frames():
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
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        while True:
            # Leer los primeros 4 bytes para obtener el tamaño del frame
            frame_size_bytes = process.stdout.read(4)
            if not frame_size_bytes:
                break
            frame_size = int.from_bytes(frame_size_bytes, 'little')
            
            # Leer el frame completo
            frame_data = process.stdout.read(frame_size)
            if not frame_data:
                break
            
            # Crear un objeto BytesIO para el frame
            frame = io.BytesIO(frame_data)
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.getvalue() + b'\r\n')
    finally:
        process.terminate()