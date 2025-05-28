
for ip in result:
    mac = get_macaddress(ip)
    print(f"[+] IP: {ip} → MAC: {mac if mac else 'Не найден'}")