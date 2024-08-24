import io
import time
import subprocess
import threading

def generate_frames():
    cmd = [
        'libcamera-vid',
        '-t', '0',
        '--inline',
        '--width', '640',
        '--height', '480',
        '--framerate', '15',  # Reducido a 15 fps
        '--codec', 'mjpeg',
        '-o', '-'
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        while True:
            # Leer el tamaño del frame (4 bytes)
            frame_size_bytes = process.stdout.read(4)
            if not frame_size_bytes:
                break
            frame_size = int.from_bytes(frame_size_bytes, byteorder='little')
            
            # Leer el frame completo
            frame = process.stdout.read(frame_size)
            if not frame:
                break
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        process.terminate()

def start_camera_stream():
    global camera_thread
    camera_thread = threading.Thread(target=generate_frames)
    camera_thread.daemon = True  # Hacer el hilo un demonio
    camera_thread.start()

def stop_camera_stream():
    global camera_thread
    if camera_thread:
        camera_thread.join(timeout=1)  # Esperar máximo 1 segundo