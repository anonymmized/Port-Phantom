"""
Signature matching for device identification
"""

from typing import List, Dict, Any
from rich.console import Console

from ..config.settings import settings

console = Console()


class SignatureMatcher:
    """Match devices against known signatures"""
    
    @staticmethod
    def check_against_signatures(device: Dict[str, Any], signatures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check if device matches any signatures"""
        matched = []
        
        for sig in signatures:
            manufacturers = sig['conditions'].get('manufacturer', [])
            ports = list(map(int, sig['conditions'].get('ports', [])))

            # Check manufacturer match
            if manufacturers and device['manufacturer'] not in manufacturers:
                continue
                
            # Check port match
            if ports and not any(port in ports for port in map(int, device['open ports'])):
                continue
            
            matched.append(sig)
        
        return matched
    
    @staticmethod
    def print_matches(device: Dict[str, Any], matches: List[Dict[str, Any]]) -> None:
        """Print signature matches for a device"""
        if matches:
            console.print(f"[!] Устройство {device.get('ip')} совпадает с сигнатурами:", style=settings.MAIN_COLOR)
            for match in matches:
                console.print(f"    → {match.get('name', 'No name')}", style=settings.MAIN_COLOR)
                console.print(f"      {match.get('description', 'No description')}", style=settings.MAIN_COLOR)
                if match.get('cve_info'):
                    console.print(f"      CVE: {match.get('cve_info')}", style="red") 