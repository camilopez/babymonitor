from picamera2 import Picamera2
import io
import time
import threading

picam2 = None
camera_thread = None

def generate_frames():
    global picam2
    if picam2 is None:
        picam2 = Picamera2()
        config = picam2.create_still_configuration(main={"size": (640, 480)})
        picam2.configure(config)
        picam2.start()

    try:
        while True:
            stream = io.BytesIO()
            picam2.capture_file(stream, format='jpeg')
            frame = stream.getvalue()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)  # Ajusta este valor según sea necesario
    except Exception as e:
        print(f"Error en generate_frames: {e}")
    finally:
        if picam2:
            picam2.stop()
            picam2 = None

def start_camera_stream():
    global camera_thread
    camera_thread = threading.Thread(target=generate_frames)
    camera_thread.start()

def stop_camera_stream():
    global camera_thread, picam2
    if camera_thread:
        camera_thread.join()
    if picam2:
        picam2.stop()
        picam2 = None