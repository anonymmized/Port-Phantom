import os
import csv
import yaml
import time
import json
import requests
import subprocess
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor
main_color = "#B0E0E6"
console = Console()
ROUTER_MANUFACTURER = ['TP-Link', 'Cisco', 'ASUS', 'Ubiquiti']
CAMERA_MANUFACTURER = ['Hikvision', 'Dahua', 'Reolink']
DEVICE_PORT_RULES = {
    "camera": [554],
    "router": [80, 443],
    "server": [22, 80, 443],
    "printer": [9100]
}
RISK_RULES = {
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

def banner_print():
    s1 =" ██▓███  ▒█████   ██▀███  ▄▄▄█████▓    ██▓███   ██░ ██  ▄▄▄      ███▄    █ ▄▄▄█████▓ ▒█████   ███▄ ▄███▓"
    s2 ="▓██░  ██▒██▒  ██▒▓██ ▒ ██▒▓  ██▒ ▓▒   ▓██░  ██▒▓██░ ██▒▒████▄    ██ ▀█   █ ▓  ██▒ ▓▒▒██▒  ██▒▓██▒▀█▀ ██▒"
    s3 ="▓██░ ██▓▒██░  ██▒▓██ ░▄█ ▒▒ ▓██░ ▒░   ▓██░ ██▓▒▒██▀▀██░▒██  ▀█▄ ▓██  ▀█ ██▒▒ ▓██░ ▒░▒██░  ██▒▓██    ▓██░"
    s4 ="▒██▄█▓▒ ▒██   ██░▒██▀▀█▄  ░ ▓██▓ ░    ▒██▄█▓▒ ▒░▓█ ░██ ░██▄▄▄▄██▓██▒  ▐▌██▒░ ▓██▓ ░ ▒██   ██░▒██    ▒██ "
    s5 ="▒██▒ ░  ░ ████▓▒░░██▓ ▒██▒  ▒██▒ ░    ▒██▒ ░  ░░▓█▒░██▓ ▓█   ▓██▒██░   ▓██░  ▒██▒ ░ ░ ████▓▒░▒██▒   ░██▒"
    s6 ="▒▓▒░ ░  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░  ▒ ░░      ▒▓▒░ ░  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒░   ▒ ▒   ▒ ░░   ░ ▒░▒░▒░ ░ ▒░   ░  ░"
    s7 ="░▒ ░      ░ ▒ ▒░   ░▒ ░ ▒░    ░       ░▒ ░      ▒ ░▒░ ░  ▒   ▒▒ ░ ░░   ░ ▒░    ░      ░ ▒ ▒░ ░  ░      ░"
    s8 ="░░      ░ ░ ░ ▒    ░░   ░   ░         ░░        ░  ░░ ░  ░   ▒     ░   ░ ░   ░      ░ ░ ░ ▒  ░      ░   "
    s9 ="            ░ ░     ░                           ░  ░  ░      ░  ░        ░              ░ ░         ░   "                                                                              
    s10 ="                      Port-Phantom v 1.0 - Network Security Scanner"
    s11 ="             Network Security Tool for Scanning and Monitoring Local Networks"
    s12 ="   Features:"
    s13 ="    • Scans local networks to discover devices"
    s14 ="    • Identifies devices by MAC address and manufacturer"
    s15 ="    • Checks open ports and classifies device types"
    s16 ="    • Calculates risk levels based on signatures and port configurations"
    s17 ="    • Compares current scan with previous scans to detect changes"
    s18 ="    • Saves results in JSON and CSV formats"
    s19 ="    • Supports multiple subnets and historical data tracking"
    s20 ="   Contact:"
    s21 ="    • GitHub: https://github.com/yourusername/Port-Phantom"
    s22 ="    • Email: yourname@example.com"
    s23 ="                                  Disclaimer:"
    s24 ="              This tool is for educational purposes only. Use responsibly."
    s25 ="                          © 2025 Port-Phantom Team"
    console.print(s1, style="#48D1CC")
    console.print(s2, style="#48D1CC")
    console.print(s3, style="#48D1CC")
    console.print(s4, style="#48D1CC")
    console.print(s5, style="#40E0D0")
    console.print(s6, style="#40E0D0")
    console.print(s7, style="#5F9EA0")
    console.print(s8, style="#5F9EA0")
    console.print(s9, style="#5F9EA0")

    console.print(f'[italic][bold]{s10}[/bold][/italic]', style="#7B68EE")
    console.print(f'[italic][bold]{s11}[/bold][/italic]', style="#7B68EE")
    console.print(f'[italic][bold]{s12}[/bold][/italic]', style="#1E90FF")
    console.print(f'[italic]{s13}[/italic]', style="#6495ED")
    console.print(f'[italic]{s14}[/italic]', style="#6495ED")
    console.print(f'[italic]{s15}[/italic]', style="#6495ED")
    console.print(f'[italic]{s16}[/italic]', style="#6495ED")
    console.print(f'[italic]{s17}[/italic]', style="#6495ED")
    console.print(f'[italic]{s18}[/italic]', style="#6495ED")
    console.print(f'[italic]{s19}[/italic]', style="#6495ED")
    console.print(f'[italic][bold]{s20}[/bold][/italic]', style="#1E90FF")
    console.print(f'[italic]{s21}[/italic]', style="#6495ED")
    console.print(f'[italic]{s22}[/italic]', style="#6495ED")
    console.print(f'[italic][bold]{s23}[/bold][/italic]', style="#7B68EE")
    console.print(f'[italic][bold]{s24}[/bold][/italic]', style="#7B68EE")
    console.print(f'[italic][bold]{s25}[/bold][/italic]', style="#7B68EE")

    return 0

def find_subnet():
    result = subprocess.run(['ifconfig'], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if 'inet' in line and '127.0.0.1' not in line and 'inet6' not in line:
            parts = line.split()
            for item in parts:
                if '.' in item and len(item.split('.')) == 4:
                    try:
                        ip_parts = item.split('.')
                        if len(ip_parts) == 4 and all(0 <= int(x) < 256 for x in ip_parts):
                            network = ".".join(ip_parts[:3]) + ".0/24"
                            return network
                    except ValueError:
                        continue
    return "192.168.1.0/24"


def load_signatures(filename='signatures.yaml'):
    if not os.path.exists(filename):
        console.print(f"[!] Файла {filename} не существует", style=main_color)
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
            return data.get('signatures', [])
        except yaml.YAMLError as e:
            console.print(f"Ошибка при парсинга YAML: {e}", style=main_color)
            return []

def check_against_signatures(device, signatures):
    matched = []
    for sig in signatures:
        manufacturers = sig['conditions'].get('manufacturer', [])
        ports = list(map(int, sig['conditions'].get('ports', [])))

        if manufacturers and device['manufacturer'] not in manufacturers:
            continue
        if ports and not any(port in ports for port in map(int, device['open ports'])):
            continue
        
        matched.append(sig)
    return matched

def scan_network(subnet):
    found_ips = [] #✅ Самому находить свою подсеть через (ifconfig -a | grep netmask) и сканировать ее
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
            console.print(f"[!] Файл {filename} не найден", style=main_color)
    except Exception as e:
        console.print(f"[!] Ошибка загрузки базы: {e}", style=main_color)
    return oui_dict

def get_manufacturer(oui, oui_db):
    return oui_db.get(oui, "Неизвестный производитель")

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

    if 80 in open_ports or 443 in open_ports:
        headers = get_http_headers(device["ip"])
        http_types = classify_by_http(headers)
        if http_types:
            classifications += http_types

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
            "manufacturer": "Неизвестный",
            "open ports": [],
            "device type": ["unknown"],
            "score": 0,
            "level": "None"
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
        with open(f"history/{filename}", 'w', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(headers)
            csv_writer.writerow(row)
        console.print(f"[+] Отчёт сохранён в: {filename}", style=main_color)
        return True
    except Exception as e:
        console.print(f"[!] Ошибка при сохранении CSV: {e}", style=main_color)
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
        with open(f"history/{filename}", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        console.print(f"[+] Отчет сохранен в: {filename}", style=main_color)
        return True
    except Exception as e:
        console.print(f"[!] Ошибка при сохранении JSON: {e}", style=main_color)
        return False
    
def save_current_scan(devices, subnet):
    timestamp = int(time.time())
    filename = f"history/scan_{timestamp}_{subnet.replace('/', '-')}.json"

    data_to_save = {
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'subnet': subnet,
        'devices': devices
    }

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4)
        console.print(f"[+] Текущее сканирование сохранено в {filename}", style=main_color)
        return data_to_save
    except Exception as e:
        console.print(f"[!] Не удалось сохранить историю: {e}", style=main_color)
        return data_to_save

def load_prev_scan(subnet):
    if not os.path.exists('history'):
        os.makedirs("history")

    scans = []
    for file in os.listdir('history'):
        if subnet.replace('/', '-') in file and file.endswith('json'):
            scans.append(os.path.join('history', file))
    
    if not scans:
        console.print("[*] Предыдущих сканирований не найдено", style=main_color)
        return None
    
    latest_file = max(scans, key=os.path.getctime)
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[!] Ошибка загрузки прошлого сканирования: {e}", style=main_color)
        return None

def compare_scans(current_devices, previous_data):
    console.print("\n[!] Анализ изменений в сети...", style=main_color)
    previous_devices = {dev['ip']: dev for dev in previous_data.get('devices', [])}
    changes_found = False

    new_devices = []
    vanished_devices = []

    current_ips = set()

    for device in current_devices:
        ip = device['ip']
        current_ips.add(ip)

        if not ip in previous_devices:
            new_devices.append(device)
        else:
            prev_score = previous_devices[ip].get('score', 0)
            curr_score = device.get('score', 0)
            if curr_score > prev_score:
                console.print(f"[!] Риск повысился у {ip}: {previous_devices[ip]['level']} → {device['level']} ({prev_score} → {curr_score})", style=main_color)
                changes_found = True
    
    for ip in previous_devices:
        if ip not in current_ips:
            vanished_devices.append(previous_devices[ip])
    
    if new_devices:
        console.print(f"[+] 🆕 Новые устройства:", style=main_color)
        for dev in new_devices:
            console.print(f"   IP: {dev['ip']} | Производитель: {dev['manufacturer']} | Порты: {dev['open ports']}", style=main_color)
        changes_found = True
    
    if vanished_devices:
        console.print("[+] 🗑 Исчезнувшие устройства:", style=main_color)
        for dev in vanished_devices:
            console.print(f"   IP: {dev['ip']} | Производитель: {dev['manufacturer']}", style=main_color)
        changes_found = True
    
    if not changes_found:
        console.print("[+] Изменений в сети не обнаружено", style=main_color)


if __name__ == '__main__':
    banner_print()
    starting_time = time.time()  # в будущем убрать время выполнения, сейчас нужно для оптимизации
    oui_db = load_oui_db("oui.txt")
    subnet = find_subnet()
    console.print("\n[+] Начинаем сканирование сети...", style=main_color)  # перевод на английский
    result = scan_network(subnet)

    console.print(f"[+] Найдено устройств: {len(result)}", style=main_color)
    console.print("[+] Обрабатываем устройства...", style=main_color)

    devices = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        tasks = [executor.submit(process_ip, ip, oui_db) for ip in result]
        for task in tasks:
            devices.append(task.result())
    
    previous_data = load_prev_scan(subnet)
    if previous_data:
        compare_scans(devices, previous_data)
    
    save_current_scan(devices, subnet)
    signatures = load_signatures()

    console.print("\n[+] Результаты:", style=main_color)
    for device in devices:
        matches = check_against_signatures(device, signatures)

        console.print(f"IP: {device.get('ip', 'unknown')}", style=main_color)
        console.print(f"MAC: {device.get('mac', 'Не найден')}", style=main_color)
        console.print(f"Manufacturer: {device.get('manufacturer', 'Неизвестный')}", style=main_color)
        console.print(f"Open ports: {', '.join(device.get('open ports', [])) if device.get('open ports') else 'None'}", style=main_color)
        console.print(f"Device type: {', '.join(device.get('device type', ['unknown']))}", style=main_color)
        console.print(f"Risk level: {device.get('level', 'None')} ({device.get('score', 0)})", style=main_color)

        if matches:
            console.print(f"[!] Устройство {device.get('ip')} совпадает с сигнатурами:", style=main_color)
            for match in matches:
                console.print(f"    → {match.get('name', 'No name')}", style=main_color)
                console.print(f"      {match.get('description', 'No description')}", style=main_color)

        console.print("-" * 50, style=main_color)
                # Сохранение тревожных сообщений в отдельный файл, данные из которого будут отправляться по email/telegram
                # if {match['risk level]} == Какой-либо тип вывода: то вызывать функцию, которая сохраняет сигнатуру
                # Сохранять в файл вместе с документацией по каждому правилу (она будет отдельным пунктом в файле yaml по сигнатуре) например, Hikvision + 554 → возможна CVE-XXXX-XXXX
                # Скорее всего после сборки модульной структуры и cli добавление сравнения сигнатуры с прошлым сканированием

                # Функция проверки на известные CVE по типу устройства
 
                # Интеграция с Telegram / email

                # Автоматическое сканирование по расписанию

                # Поддержка нескольких сетей

                # Добавление белого списка

                # API / Web-панель мониторинга

                # Добавление проверки, если в открытых портах есть 80 или 443, то проверять по программе httpx
    #        csv_reporter(device)

    ending_time = time.time()
    console.print(f"\n[+] Lead time: {ending_time - starting_time:.2f} seconds", style=main_color)\