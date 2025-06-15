"""
Port scanning functionality
"""

import subprocess
from typing import List
from rich.console import Console

from ..config.settings import settings

console = Console()


class PortScanner:
    """Port scanning and detection"""
    
    @staticmethod
    def check_ports(ip: str) -> List[str]:
        """Scan specific ports on a host"""
        open_ports = []
        
        try:
            ports_str = ",".join(map(str, settings.SCAN_PORTS))
            result = subprocess.run([
                "nmap", "-p", ports_str, ip
            ], capture_output=True, text=True)
            
            for line in result.stdout.splitlines():
                if "open" in line:
                    parts = line.split()
                    if parts:
                        port = parts[0].split("/")[0]
                        open_ports.append(port)
            
            return open_ports
            
        except Exception as e:
            console.print(f"[!] Ошибка при сканировании портов {ip}: {e}", style=settings.MAIN_COLOR)
            return []
    
    @staticmethod
    def get_http_headers(ip: str) -> dict:
        """Get HTTP headers from a host"""
        import requests
        
        try:
            response = requests.get(f"http://{ip}", timeout=2)
            return response.headers
        except Exception:
            return {} 