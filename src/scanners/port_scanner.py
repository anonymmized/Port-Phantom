"""
Port scanning functionality
"""

import subprocess
from rich.console import Console

from ..config.settings import MAIN_COLOR, SCAN_PORTS

console = Console()


def check_ports(ip, ports=None):
    """Scan specific ports on a host"""
    open_ports = []
    
    if ports is None:
        ports = SCAN_PORTS
    
    try:
        ports_str = ",".join(map(str, ports))
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
        console.print(f":x: [bold red]Error scanning ports for {ip}:[/bold red] {e}", style=MAIN_COLOR)
        return []


def get_http_headers(ip):
    """Get HTTP headers from a host"""
    import requests
    
    try:
        response = requests.get(f"http://{ip}", timeout=2)
        return response.headers
    except Exception:
        return {} 