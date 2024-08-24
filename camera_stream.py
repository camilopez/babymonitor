import subprocess
import time

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
            frame = process.stdout.read(65536)  # Leer un chunk grande
            if not frame:
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.01)  # Pequeña pausa para evitar sobrecarga de CPU
    finally:
        process.terminate()

# Elimina las funciones start_camera_stream y stop_camera_stream por ahora