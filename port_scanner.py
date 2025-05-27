import subprocess

def scan_network():
    result = []
    command = subprocess.run(["nmap", "-sn", "192.168.1.0/24"], capture_output=True, text=True)
    for line in command.stdout.splitlines():
        if "Nmap scan report" in line:
            result.append(line.split()[-1])
    return result

def check_ports(ip):
    result = subprocess.run(["nmap", "-p", "21,22,23,53,80,443,554,2222,3389,8080,8000,8081", ip], capture_output=True, text=True)
    if "open" in result.stdout:
        print(f"По адресу {ip} обнаружился открытый порт {result.stdout}")
    return result.stdout

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


result = scan_network()


for ip in result:
    mac = get_macaddress(ip)
    print(f"[+] IP: {ip} → MAC: {mac if mac else 'Не найден'}")