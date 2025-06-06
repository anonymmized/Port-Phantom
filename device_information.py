import os
import csv
import time
import json
import requests
import subprocess
from concurrent.futures import ThreadPoolExecutor

ROUTER_MANUFACTURER = ['TP-Link', 'Cisco', 'ASUS', 'Ubiquiti']
CAMERA_MANUFACTURER = ['Hikvision', 'Dahua', 'Reolink']
DEVICE_PORT_RULES = {
    "camera": [554],
    "router": [80, 443],
    "server": [22, 80, 443],
    "printer": [9100]
}
RISK_RULES={
    'ports': {
        22: 5, # SSH - bruteforce
        80: 3, # HTTP - weak web-interface
        443: 3, # HTTPS - web-interface
        554: 7, # RTSP - cameras
        9100: 4, # HP JetDirect - print servers
        23: 8, # Telnet - old protocol without encryption
        21: 6, # FTP - vulnerable versions are often used
        8080: 3, # Web-port
        8000: 4, # IOT devices
        8081: 4,
    },

    'manufacturers': {
        'Hikvision': 7,
        'Dahua': 6,
        'TPLink': 5,
        'Netgear': 5,
        'Apple': 1,
        'Samsung': 1,
        'Google': 1,
        'Amazon': 2,
    }
}

def scan_network(subnet="192.168.1.0/24"):
    found_ips = []
    command = subprocess.run(
        ["nmap", "-sn", "--host-timeout", "50ms", "--min-hostgroup", "20", subnet],
        capture_output=True,
        text=True
    )
    for line in command.stdout.splitlines():
        if "Nmap scan report" in line:
            found_ips.append(line.split()[-1])
    return found_ips

def check_ports(ip):
    open_ports = []
    result = subprocess.run(
        ["nmap", "-p", "21,22,23,53,80,443,554,2222,3389,8080,8000", ip],
        capture_output=True,
        text=True
    )
    for line in result.stdout.splitlines():
        if "open" in line:
            parts = line.split()
            open_ports.append(parts[0].split("/")[0])
    return open_ports

def get_macaddress(ip):
    try:
        result = subprocess.run(["arp", ip], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if 'at' in line:
                parts = line.split()
                return parts[3].upper()
    except Exception as e:
        return None
    return None

def get_oui(mac):
    if not mac:
        return None
    return mac.replace(":", "").replace("-", "").upper()[:6]

def load_oui_db(filename="oui.txt"):
    oui_dict = {}
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if '(base 16)' in line and len(parts) >= 4:
                        oui = parts[0].replace('-', '').upper()
                        manufacturer = ' '.join(parts[3:])
                        oui_dict[oui] = manufacturer
        else:
            print(f"[!] Файл {filename} не найден")
    except Exception as e:
        print(f"[!] Ошибка загрузки базы: {e}")
    return oui_dict

def get_manufacturer(oui, oui_db):
    return oui_db.get(oui, "Незвестный производитель")

def classify_by_manufacturer(manufacturer):
    if manufacturer in ROUTER_MANUFACTURER:
        return ['router']
    elif manufacturer in CAMERA_MANUFACTURER:
        return ['camera']
    elif "Apple" in manufacturer or "Samsung" in manufacturer:
        return ['smartphone']
    else:
        return []

def classify_by_ports(open_ports):
    open_ports = list(map(int, open_ports))
    device_types = []

    for dev_type, ports in DEVICE_PORT_RULES.items():
        if any(port in open_ports for port in ports):
            device_types.append(dev_type)
    
    return device_types or ['unknown']

def get_http_headers(ip):
    try:
        response = requests.get(f"http://{ip}", timeout=2)
        return response.headers
    except:
        return None
    
def classify_by_http(headers):
    if not headers:
        return None
    
    server = headers.get('Server', '').lower()
    powered_by = headers.get('X-Powered-By', '').lower()
    if 'gsoap' in server:
        return ["camera"]
    elif 'nginx' in server or 'apache' in server:
        return ["router", "web-server"]
    elif 'micro_httpd' in server:
        return ["printer"]
    return []

def classify_device(device):
    manufacturer = device["manufacturer"].strip()
    open_ports = device["open ports"]

    classifications = []

    classifications += classify_by_manufacturer(manufacturer)
    classifications += classify_by_ports(open_ports)

    if '80' in open_ports or '443' in open_ports:
        headers = get_http_headers(device["ip"])
        classifications += classify_by_http(headers)

    return list(set(classifications)) or ["unknown"]

def calculate_risk_score(device):
    risk_score = 0
    manufacturer = device.get("manufacturer", "").strip()
    open_ports = list(map(int, device.get("open ports", [])))

    for port in open_ports:
        risk_score += RISK_RULES['ports'].get(port, 1)
    
    if manufacturer in RISK_RULES['manufacturers']:
        risk_score += RISK_RULES['manufacturers'][manufacturer]

    return risk_score

def get_risk_level(score):
    if score >= 10:
        return "High"
    elif score >= 5:
        return "Medium"
    elif score > 0:
        return "Low"
    else:
        return "None"

def process_ip(ip, oui_db):
    mac = get_macaddress(ip)
    if not mac:
        return {
            "ip": ip,
            "mac": "Не найден",
            "manufacturer": "Незвестный",
            "open ports": [],
        }
    open_ports = check_ports(ip)
    oui = get_oui(mac)
    manufacturer = get_manufacturer(oui, oui_db)
    device = {
        "ip": ip,
        "mac": mac,
        "manufacturer": manufacturer,
        "open ports": open_ports
    }

    device_types = classify_device(device)
    risk_score = calculate_risk_score(device)
    risk_level = get_risk_level(risk_score)
    device['device type'] = device_types
    device['score'] = risk_score
    device['level'] = risk_level
    return device

def csv_reporter(device):

    headers = ['ip', 'mac', 'manufacturer', 'open_ports', 'device_type', 'score', 'level']
    row = [
        device['ip'],
        device['mac'],
        device['manufacturer'],
        ', '.join(device['open ports']) if device['open ports'] else 'None',
        ', '.join(device['device type']),
        device['score'],
        device['level']
    ]

    filename = f"{device['ip']}_device.csv"

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(headers)
            csv_writer.writerow(row)
        print(f"[+] Отчёт сохранён в: {filename}")
        return True
    except Exception as e:
        print(f"[!] Ошибка при сохранении CSV: {e}")
        return False

def json_reporter(device):
    data = {
        "ip": device['ip'],
        "mac": device['mac'],
        "manufacturer": device['manufacturer'],
        "open_ports": device['open ports'],
        "device_type": device['device type'],
        "score": device['score'],
        "level": device['level'],
    }
    filename = f"{data['ip']}_device.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"[+] Отчет сохранен в: {filename}")
        return True
    except Exception as e:
        print(f"[!] Ошибка при сохранении JSON: {e}")
        return False

if __name__ == "__main__":
    starting_time = time.time()
    oui_db = load_oui_db("oui.txt")

    print("[+] Начинаем сканирование сети...")
    result = scan_network("192.168.1.0/24")

    print(f"[+] Найдено устройств: {len(result)}")
    print("[+] Обрабатываем устройства...")

    devices = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        tasks = [executor.submit(process_ip, ip, oui_db) for ip in result]
        for task in tasks:
            devices.append(task.result())

    print("\n[+] Результаты:")
    for device in devices:
        print(f"IP: {device['ip']}")
        print(f"MAC: {device['mac']}")
        print(f"Manufacturer: {device['manufacturer']}")
        print(f"Open ports: {', '.join(device['open ports']) if device['open ports'] else "None"}")
        print(f"Device type: {device['device type']}")
        print(f"Risk level: {device['level']} ({device['score']})")
        print("-" * 50)
        json_reporter(device)
        csv_reporter(device)

    ending_time = time.time()
    print(f"\n[+] Lead time: {ending_time - starting_time:.2f} seconds")