"""
Network discovery and subnet detection
"""

import subprocess
from rich.console import Console

from ..config.settings import MAIN_COLOR, DEFAULT_SUBNET, SCAN_TIMEOUT, MIN_HOSTGROUP

console = Console()


def find_subnet():
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
                                console.print(f":mag: [bold green]Subnet detected:[/bold green] {network}", style=MAIN_COLOR)
                                return network
                        except ValueError:
                            continue
    except Exception as e:
        console.print(f":x: [bold red]Error detecting subnet:[/bold red] {e}", style=MAIN_COLOR)
    
    console.print(f":information_source: [yellow]Using default subnet:[/yellow] {DEFAULT_SUBNET}", style=MAIN_COLOR)
    return DEFAULT_SUBNET


def scan_network(subnet):
    """Scan network for active hosts"""
    found_ips = []
    
    try:
        command = subprocess.run([
            "nmap", "-sn", 
            "--host-timeout", f"{SCAN_TIMEOUT}ms", 
            "--min-hostgroup", str(MIN_HOSTGROUP), 
            subnet
        ], capture_output=True, text=True)
        
        for line in command.stdout.splitlines():
            if "Nmap scan report" in line:
                ip = line.split()[-1]
                if ip != subnet.split('/')[0]:  # Exclude network address
                    found_ips.append(ip)
        
        console.print(f":mag: [bold green]{len(found_ips)} active devices found[/bold green]", style=MAIN_COLOR)
        return found_ips
        
    except Exception as e:
        console.print(f":x: [bold red]Error scanning network:[/bold red] {e}", style=MAIN_COLOR)
        return [] 