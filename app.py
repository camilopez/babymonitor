from flask import Flask, render_template, request, Response, jsonify
from flask_socketio import SocketIO
import subprocess
import threading
import time
import logging
from ap_config import setup_ap, start_ap, stop_ap, check_wifi_connection
from camera_stream import generate_frames, start_camera_stream, stop_camera_stream

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

# Reducir la frecuencia de verificación de la red
CHECK_NETWORK_INTERVAL = 300  # 5 minutos

def check_and_switch_network():
    while True:
        if check_wifi_connection():
            stop_ap()
        else:
            start_ap()
        time.sleep(CHECK_NETWORK_INTERVAL)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    subprocess.call(['sudo', 'shutdown', '-h', 'now'])
    return jsonify({"message": "Apagando..."})

@app.route('/reboot', methods=['POST'])
def reboot():
    subprocess.call(['sudo', 'reboot'])
    return jsonify({"message": "Reiniciando..."})

@app.route('/wificonfig', methods=['GET', 'POST'])
def wifi_config():
    if request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']
        configure_wifi(ssid, password)
        return jsonify({"message": f"Configurando WiFi: {ssid}"})
    return render_template('wifi.html')

@app.route('/video_feed')
def video_feed():
    logger.debug("Iniciando video_feed")
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def configure_wifi(ssid, password):
    config = f'''
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=ES

network={{
    ssid="{ssid}"
    psk="{password}"
}}
'''
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f:
        f.write(config)
    subprocess.call(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'])

def start_camera():
    logger.debug("Iniciando cámara")
    start_camera_stream()

def stop_camera():
    logger.debug("Deteniendo cámara")
    stop_camera_stream()

if __name__ == '__main__':
    logger.info("Iniciando aplicación")
    setup_ap()
    network_thread = threading.Thread(target=check_and_switch_network)
    network_thread.daemon = True  # Hacer que el hilo sea un demonio    
    network_thread.start()
    start_camera()
    try:
        #socketio.run(app, host='0.0.0.0', port=8080, allow_unsafe_werkzeug=True)
        socketio.run(app, host='0.0.0.0', port=8080)
    except Exception as e:
        logger.error(f"Error al iniciar la aplicación: {e}")
    finally:
        stop_camera()
        logger.info("Aplicación terminada")