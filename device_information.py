import os
import time
import subprocess
from tqdm import tqdm


def scan_network(subnet="192.168.1.0/24"):
    found_ips = []
    command = subprocess.run(["nmap", "-sn", subnet], capture_output=True, text=True)
    for line in command.stdout.splitlines():
        if "Nmap scan report" in line:
            found_ips.append(line.split()[-1])
    return found_ips


def check_ports(ip):
    command = subprocess.run(["nmap", "-p", "21,22,23,53,80,443,554,2222,3389,8080,8000", ip], capture_output=True, text=True)
    open_ports = []
    for line in command.stdout.splitlines():
        if "open" in line:
            parts = line.split()
            open_ports.append(parts[0].split('/')[0])
    return open_ports


def get_macaddress(ip):
    try:
        result = subprocess.run(["arp", ip], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if 'at' in line:
                parts = line.split()
                mac = parts[3]
                return mac.upper()
    except Exception as e:
        print(f"[!] Не удалось получить MAC для {ip}: {e}")
    return None


def get_oui(mac):
    if not mac:
        return None
    return mac.replace(":", "").replace("-", "").upper()[:6]


def load_oui_db(filename):
    oui_dict = {}
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                a = f.readlines()
                for line in a:
                    parts = line.split()
                    if 'base 16' in line and len(line) >= 4:
                        oui = parts[0]
                        manufacturer = ' '.join(parts[3:])
                        oui_dict[oui] = manufacturer
        else:
            print(f"[!] Файл {filename} не найден")
    except Exception as e:
        print(f"[!] Ошибка чтения файла {filename}: {e}")

    return oui_dict

def get_manufacturer(oui, oui_db):
    return oui_db.get(oui, "Низвестный производитель")

def check_reachable(ip):
    command = subprocess.run(["nmap", "-sP", ip], capture_output=True, text=True)
    reachable = False
    for line in command.stdout.splitlines():
        if "Host is up" in line:
            reachable = True
    return reachable


starting_time = time.time()
result = scan_network()
oui_db = load_oui_db('oui.txt')
for ip in result:
    reachable = check_reachable(ip)
    mac = get_macaddress(ip)
    if not mac:
        print(f"[!] Не удалось получить MAC для {ip}")
        continue
    open_ports = check_ports(ip)
    oui = get_oui(mac)
    manufacturer = get_manufacturer(oui, oui_db)
    network_dict = {
        "ip": ip,
        "reachable": reachable,
        "mac": mac,
        "manufacturer": manufacturer,
        "open ports": open_ports,
        "risk score": "в процессе",
        "device type": "в процессе"
    }
    print(network_dict)
ending_time = time.time()
print(f"Время выполнения программы: {ending_time - starting_time}")