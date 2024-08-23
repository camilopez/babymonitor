import io
import time
import subprocess
import threading

def generate_frames():
    cmd = [
        'libcamera-vid',
        '-t', '0',  # Tiempo infinito
        '--inline',  # Frames H264 completos
        '--width', '640',
        '--height', '480',
        '--framerate', '30',
        '--codec', 'mjpeg',
        '-o', '-'  # Salida a stdout
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        data = b''
        while True:
            chunk = process.stdout.read(4096)  # Leer en bloques de 4096 bytes
            if not chunk:
                break
            data += chunk
            # Buscamos el delimitador de frame para generar cada imagen completa
            while b'\xff\xd9' in data:  # Marca de fin de JPEG
                frame_end = data.index(b'\xff\xd9') + 2
                frame = data[:frame_end]
                data = data[frame_end:]
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        process.terminate()


def start_camera_stream():
    global camera_thread
    camera_thread = threading.Thread(target=generate_frames)
    camera_thread.start()

def stop_camera_stream():
    global camera_thread
    if camera_thread:
        camera_thread.join()