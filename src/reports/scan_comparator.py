"""
Scan comparison and change detection
"""

from typing import Dict, Any, List
from rich.console import Console

from ..config.settings import settings

console = Console()


class ScanComparator:
    """Compare current scan with previous scans"""
    
    @staticmethod
    def compare_scans(current_devices: List[Dict[str, Any]], previous_data: Dict[str, Any]) -> None:
        """Compare current scan with previous scan"""
        console.print("\n[!] Анализ изменений в сети...", style=settings.MAIN_COLOR)
        
        if not previous_data or 'devices' not in previous_data:
            console.print("[*] Нет данных для сравнения", style=settings.MAIN_COLOR)
            return
        
        previous_devices = {dev['ip']: dev for dev in previous_data.get('devices', [])}
        changes_found = False

        new_devices = []
        vanished_devices = []
        current_ips = set()

        # Check for new devices and risk changes
        for device in current_devices:
            ip = device['ip']
            current_ips.add(ip)

            if ip not in previous_devices:
                new_devices.append(device)
            else:
                prev_score = previous_devices[ip].get('score', 0)
                curr_score = device.get('score', 0)
                if curr_score > prev_score:
                    console.print(
                        f"[!] Риск повысился у {ip}: {previous_devices[ip]['level']} → {device['level']} ({prev_score} → {curr_score})", 
                        style=settings.MAIN_COLOR
                    )
                    changes_found = True
        
        # Check for vanished devices
        for ip in previous_devices:
            if ip not in current_ips:
                vanished_devices.append(previous_devices[ip])
        
        # Report new devices
        if new_devices:
            console.print(f"[+] 🆕 Новые устройства:", style=settings.MAIN_COLOR)
            for dev in new_devices:
                console.print(
                    f"   IP: {dev['ip']} | Производитель: {dev['manufacturer']} | Порты: {dev['open ports']}", 
                    style=settings.MAIN_COLOR
                )
            changes_found = True
        
        # Report vanished devices
        if vanished_devices:
            console.print("[+] 🗑 Исчезнувшие устройства:", style=settings.MAIN_COLOR)
            for dev in vanished_devices:
                console.print(
                    f"   IP: {dev['ip']} | Производитель: {dev['manufacturer']}", 
                    style=settings.MAIN_COLOR
                )
            changes_found = True
        
        if not changes_found:
            console.print("[+] Изменений в сети не обнаружено", style=settings.MAIN_COLOR) 