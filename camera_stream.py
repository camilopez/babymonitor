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
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    
    try:
        while True:
            frame = process.stdout.read(100000)  # Ajusta este valor según sea necesario
            if not frame:
                break
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