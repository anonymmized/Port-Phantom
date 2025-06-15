"""
Network discovery and subnet detection
"""

import subprocess
from typing import List
from rich.console import Console

from ..config.settings import settings

console = Console()


class NetworkScanner:
    """Network discovery and scanning"""
    
    @staticmethod
    def find_subnet() -> str:
        """Detect local subnet automatically"""
        try:
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
                                    console.print(f"[+] Обнаружена подсеть: {network}", style=settings.MAIN_COLOR)
                                    return network
                            except ValueError:
                                continue
        except Exception as e:
            console.print(f"[!] Ошибка при определении подсети: {e}", style=settings.MAIN_COLOR)
        
        console.print(f"[*] Используется подсеть по умолчанию: {settings.DEFAULT_SUBNET}", style=settings.MAIN_COLOR)
        return settings.DEFAULT_SUBNET
    
    @staticmethod
    def scan_network(subnet: str) -> List[str]:
        """Scan network for active hosts"""
        found_ips = []
        
        try:
            command = subprocess.run([
                "nmap", "-sn", 
                "--host-timeout", f"{settings.SCAN_TIMEOUT}ms", 
                "--min-hostgroup", str(settings.MIN_HOSTGROUP), 
                subnet
            ], capture_output=True, text=True)
            
            for line in command.stdout.splitlines():
                if "Nmap scan report" in line:
                    ip = line.split()[-1]
                    if ip != subnet.split('/')[0]:  # Exclude network address
                        found_ips.append(ip)
            
            console.print(f"[+] Найдено {len(found_ips)} активных устройств", style=settings.MAIN_COLOR)
            return found_ips
            
        except Exception as e:
            console.print(f"[!] Ошибка при сканировании сети: {e}", style=settings.MAIN_COLOR)
            return [] 