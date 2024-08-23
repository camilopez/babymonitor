import io
import picamera
from time import sleep

def generate_frames():
    with picamera.PiCamera() as camera:
        # Inicializar la cámara
        camera.resolution = (640, 480)
        camera.framerate = 24
        sleep(2)  # Dar tiempo a la cámara para inicializarse
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            stream.seek(0)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')
            stream.seek(0)
            stream.truncate()