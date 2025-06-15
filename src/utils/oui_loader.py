"""
OUI database downloader
"""

import os
import requests
from rich.console import Console

console = Console()


class OUILoader:
    """Download and manage OUI database"""
    
    OUI_URL = "https://standards-oui.ieee.org/oui.txt"
    
    @staticmethod
    def download_oui_db(filename: str = "data/oui.txt") -> bool:
        """Download OUI database from IEEE"""
        try:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            if os.path.exists(filename):
                console.print("oui.txt уже существует", style="yellow")
                return True
            
            console.print("[+] Загружаем базу OUI...", style="green")
            response = requests.get(OUILoader.OUI_URL, timeout=30)
            response.raise_for_status()
            
            with open(filename, "wb") as f:
                f.write(response.content)
            
            console.print("[+] База OUI успешно скачана!", style="green")
            return True
            
        except Exception as e:
            console.print(f"[!] Ошибка при загрузке OUI базы: {e}", style="red")
            return False 