import subprocess

def setup_ap():
    # Configurar interfaz
    with open('/etc/dhcpcd.conf', 'a') as f:
        f.write('\ninterface wlan0\nstatic ip_address=192.168.4.1/24\nnohook wpa_supplicant\n')

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
    with open('/etc/hostapd/hostapd.conf', 'w') as f:
        f.write(hostapd_conf)

    # Configurar dnsmasq
    dnsmasq_conf = '''
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
'''
    with open('/etc/dnsmasq.conf', 'w') as f:
        f.write(dnsmasq_conf)

    # Habilitar el enrutamiento IP
    with open('/etc/sysctl.conf', 'a') as f:
        f.write('\nnet.ipv4.ip_forward=1\n')

    # Aplicar cambios
    subprocess.call(['sudo', 'sysctl', '-p'])
    subprocess.call(['sudo', 'systemctl', 'unmask', 'hostapd'])
    subprocess.call(['sudo', 'systemctl', 'enable', 'hostapd'])
    subprocess.call(['sudo', 'systemctl', 'enable', 'dnsmasq'])

def start_ap():
    subprocess.call(['sudo', 'systemctl', 'start', 'hostapd'])
    subprocess.call(['sudo', 'systemctl', 'start', 'dnsmasq'])

def stop_ap():
    subprocess.call(['sudo', 'systemctl', 'stop', 'hostapd'])
    subprocess.call(['sudo', 'systemctl', 'stop', 'dnsmasq'])

def check_wifi_connection():
    try:
        output = subprocess.check_output(['iwgetid', '-r']).decode('utf-8').strip()
        return bool(output)
    except subprocess.CalledProcessError:
        return False