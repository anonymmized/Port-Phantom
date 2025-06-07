import subprocess
command = subprocess.run(['ifconfig'], capture_output=True, text=True)
for line in command.stdout.splitlines():
    if 'inet' in line and not '127.0.0.1' in line:
        parts = line.split()
        if 'netmask' in line:
            ip = parts[1]
            subnet = ip.split('.')[:-1]
            subnet.append('0')
            subnet = '.'.join(subnet)
            subnet = f"{subnet}/24"
            print(subnet)