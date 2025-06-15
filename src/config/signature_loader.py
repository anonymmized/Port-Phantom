"""
Signature loading and management
"""

import os
import yaml
from typing import List, Dict, Any
from rich.console import Console

from ..config.settings import settings

console = Console()


class SignatureLoader:
    """Load and manage device signatures"""
    
    def __init__(self, filename: str = None):
        self.filename = filename or settings.SIGNATURES_PATH
        self.signatures = []
        self.load_signatures()
    
    def load_signatures(self) -> List[Dict[str, Any]]:
        """Load signatures from YAML file"""
        if not os.path.exists(self.filename):
            console.print(f"[!] Файла {self.filename} не существует", style=settings.MAIN_COLOR)
            return []
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                self.signatures = data.get('signatures', [])
                console.print(f"[+] Загружено {len(self.signatures)} сигнатур", style=settings.MAIN_COLOR)
                return self.signatures
        except yaml.YAMLError as e:
            console.print(f"Ошибка при парсинга YAML: {e}", style=settings.MAIN_COLOR)
            return []
        except Exception as e:
            console.print(f"Ошибка при загрузке сигнатур: {e}", style=settings.MAIN_COLOR)
            return []
    
    def get_signatures(self) -> List[Dict[str, Any]]:
        """Get loaded signatures"""
        return self.signatures
    
    def reload_signatures(self) -> List[Dict[str, Any]]:
        """Reload signatures from file"""
        return self.load_signatures() 