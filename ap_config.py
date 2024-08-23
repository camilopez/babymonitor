import subprocess

def setup_ap():
    # Configurar interfaz
    dhcpcd_config = '\ninterface wlan0\nstatic ip_address=192.168.4.1/24\nnohook wpa_supplicant\n'
    subprocess.run(['sudo', 'bash', '-c', f'echo "{dhcpcd_config}" >> /etc/dhcpcd.conf'], check=True)

    # Configurar hostapd
    hostapd_conf = '''
interface=wlan0
driver=nl80211
ssid=BabyMonitorAP
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=babymonitor123
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
'''
    # Asegurar que el directorio existe
    subprocess.run(['sudo', 'mkdir', '-p', '/etc/hostapd'], check=True)
    subprocess.run(['sudo', 'bash', '-c', f'echo "{hostapd_conf}" > /etc/hostapd/hostapd.conf'], check=True)

    # Configurar dnsmasq
    dnsmasq_conf = '''
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
'''
    subprocess.run(['sudo', 'bash', '-c', f'echo "{dnsmasq_conf}" > /etc/dnsmasq.conf'], check=True)

    # Habilitar el enrutamiento IP
    subprocess.run(['sudo', 'bash', '-c', 'echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf'], check=True)

    # Aplicar cambios
    subprocess.run(['sudo', 'sysctl', '-p'], check=True)
    
    # Verificar si hostapd está instalado
    if subprocess.run(['which', 'hostapd'], capture_output=True).returncode != 0:
        print("hostapd no está instalado. Instalando...")
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'hostapd'], check=True)
    
    subprocess.run(['sudo', 'systemctl', 'unmask', 'hostapd'], check=True)
    subprocess.run(['sudo', 'systemctl', 'enable', 'hostapd'], check=True)
    
    # Verificar si dnsmasq está instalado
    if subprocess.run(['which', 'dnsmasq'], capture_output=True).returncode != 0:
        print("dnsmasq no está instalado. Instalando...")
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'dnsmasq'], check=True)
    
    subprocess.run(['sudo', 'systemctl', 'enable', 'dnsmasq'], check=True)

# Las funciones start_ap, stop_ap y check_wifi_connection permanecen sin cambios

def start_ap():
    subprocess.run(['sudo', 'systemctl', 'start', 'hostapd'], check=True)
    subprocess.run(['sudo', 'systemctl', 'start', 'dnsmasq'], check=True)

def stop_ap():
    subprocess.run(['sudo', 'systemctl', 'stop', 'hostapd'], check=True)
    subprocess.run(['sudo', 'systemctl', 'stop', 'dnsmasq'], check=True)

def check_wifi_connection():
    try:
        output = subprocess.check_output(['iwgetid', '-r']).decode('utf-8').strip()
        return bool(output)
    except subprocess.CalledProcessError:
        return False