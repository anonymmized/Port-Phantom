"""
MAC address detection and OUI processing
"""

import subprocess
import os
from rich.console import Console

from ..config.settings import MAIN_COLOR, OUI_DB_PATH

console = Console()


def get_mac_address(ip):
    """Get MAC address for an IP using ARP"""
    try:
        result = subprocess.run(["arp", ip], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if 'at' in line:
                parts = line.split()
                if len(parts) >= 4:
                    return parts[3].upper()
        return None
    except Exception as e:
        console.print(f":x: [bold red]Error getting MAC address for {ip}:[/bold red] {e}", style=MAIN_COLOR)
        return None


def get_oui(mac):
    """Extract OUI from MAC address"""
    if not mac:
        return None
    return mac.replace(":", "").replace("-", "").upper()[:6]


def load_oui_db(filename=None):
    """Load OUI database from file"""
    oui_dict = {}
    filename = filename or OUI_DB_PATH
    
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if '(base 16)' in line and len(parts) >= 4:
                        oui = parts[0].replace('-', '').upper()
                        manufacturer = ' '.join(parts[3:])
                        oui_dict[oui] = manufacturer
            console.print(f":bookmark_tabs: [bold green]{len(oui_dict)} OUI records loaded[/bold green]", style=MAIN_COLOR)
        else:
            console.print(f":x: [bold red]File not found:[/bold red] {filename}", style=MAIN_COLOR)
    except Exception as e:
        console.print(f":x: [bold red]Error loading OUI database:[/bold red] {e}", style=MAIN_COLOR)
    
    return oui_dict


def get_manufacturer(oui, oui_db):
    """Get manufacturer name from OUI"""
    return oui_db.get(oui, "Unknown manufacturer") 