import io
import time
import subprocess

def generate_frames():
    while True:
        # Capturar una imagen usando libcamera-still
        result = subprocess.run(['libcamera-still', '-n', '-o', '-', '-t', '1'], capture_output=True, check=True)
        
        # Convertir la salida a un objeto BytesIO
        img_buffer = io.BytesIO(result.stdout)
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_buffer.getvalue() + b'\r\n')
        
        time.sleep(0.1)