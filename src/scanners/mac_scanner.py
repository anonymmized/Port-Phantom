"""
MAC address detection and OUI processing
"""

import subprocess
import os
from typing import Dict, Optional
from rich.console import Console

from ..config.settings import settings

console = Console()


class MACScanner:
    """MAC address scanning and OUI processing"""
    
    @staticmethod
    def get_mac_address(ip: str) -> Optional[str]:
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
            console.print(f"[!] Ошибка при получении MAC адреса для {ip}: {e}", style=settings.MAIN_COLOR)
            return None
    
    @staticmethod
    def get_oui(mac: str) -> Optional[str]:
        """Extract OUI from MAC address"""
        if not mac:
            return None
        return mac.replace(":", "").replace("-", "").upper()[:6]
    
    @staticmethod
    def load_oui_db(filename: str = None) -> Dict[str, str]:
        """Load OUI database from file"""
        oui_dict = {}
        filename = filename or settings.OUI_DB_PATH
        
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if '(base 16)' in line and len(parts) >= 4:
                            oui = parts[0].replace('-', '').upper()
                            manufacturer = ' '.join(parts[3:])
                            oui_dict[oui] = manufacturer
                console.print(f"[+] Загружено {len(oui_dict)} записей OUI", style=settings.MAIN_COLOR)
            else:
                console.print(f"[!] Файл {filename} не найден", style=settings.MAIN_COLOR)
        except Exception as e:
            console.print(f"[!] Ошибка загрузки базы OUI: {e}", style=settings.MAIN_COLOR)
        
        return oui_dict
    
    @staticmethod
    def get_manufacturer(oui: str, oui_db: Dict[str, str]) -> str:
        """Get manufacturer name from OUI"""
        return oui_db.get(oui, "Неизвестный производитель") 