"""
Report generation and file management
"""

import os
import json
import csv
import time
from typing import Dict, Any, List
from rich.console import Console

from ..config.settings import settings

console = Console()


class ReportGenerator:
    """Generate and save reports"""
    
    @staticmethod
    def save_current_scan(devices: List[Dict[str, Any]], subnet: str) -> Dict[str, Any]:
        """Save current scan results"""
        timestamp = int(time.time())
        filename = f"{settings.HISTORY_DIR}/scan_{timestamp}_{subnet.replace('/', '-')}.json"

        data_to_save = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'subnet': subnet,
            'devices': devices
        }

        try:
            os.makedirs(settings.HISTORY_DIR, exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
            console.print(f"[+] Текущее сканирование сохранено в {filename}", style=settings.MAIN_COLOR)
            return data_to_save
        except Exception as e:
            console.print(f"[!] Не удалось сохранить историю: {e}", style=settings.MAIN_COLOR)
            return data_to_save
    
    @staticmethod
    def load_prev_scan(subnet: str) -> Dict[str, Any]:
        """Load previous scan results"""
        if not os.path.exists(settings.HISTORY_DIR):
            os.makedirs(settings.HISTORY_DIR)
            return None

        scans = []
        for file in os.listdir(settings.HISTORY_DIR):
            if subnet.replace('/', '-') in file and file.endswith('json'):
                scans.append(os.path.join(settings.HISTORY_DIR, file))
        
        if not scans:
            console.print("[*] Предыдущих сканирований не найдено", style=settings.MAIN_COLOR)
            return None
        
        latest_file = max(scans, key=os.path.getctime)
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            console.print(f"[!] Ошибка загрузки прошлого сканирования: {e}", style=settings.MAIN_COLOR)
            return None
    
    @staticmethod
    def save_csv_report(device: Dict[str, Any]) -> bool:
        """Save device report in CSV format"""
        headers = ['ip', 'mac', 'manufacturer', 'open_ports', 'device_type', 'score', 'level']
        row = [
            device['ip'],
            device['mac'],
            device['manufacturer'],
            ', '.join(device['open ports']) if device['open ports'] else 'None',
            ', '.join(device['device type']),
            device['score'],
            device['level']
        ]

        filename = f"{device['ip']}_device.csv"

        try:
            os.makedirs(settings.HISTORY_DIR, exist_ok=True)
            with open(f"{settings.HISTORY_DIR}/{filename}", 'w', newline='', encoding='utf-8') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(headers)
                csv_writer.writerow(row)
            console.print(f"[+] Отчёт сохранён в: {filename}", style=settings.MAIN_COLOR)
            return True
        except Exception as e:
            console.print(f"[!] Ошибка при сохранении CSV: {e}", style=settings.MAIN_COLOR)
            return False
    
    @staticmethod
    def save_json_report(device: Dict[str, Any]) -> bool:
        """Save device report in JSON format"""
        data = {
            "ip": device['ip'],
            "mac": device['mac'],
            "manufacturer": device['manufacturer'],
            "open_ports": device['open ports'],
            "device_type": device['device type'],
            "score": device['score'],
            "level": device['level'],
        }
        filename = f"{data['ip']}_device.json"
        try:
            os.makedirs(settings.HISTORY_DIR, exist_ok=True)
            with open(f"{settings.HISTORY_DIR}/{filename}", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            console.print(f"[+] Отчет сохранен в: {filename}", style=settings.MAIN_COLOR)
            return True
        except Exception as e:
            console.print(f"[!] Ошибка при сохранении JSON: {e}", style=settings.MAIN_COLOR)
            return False
    
    @staticmethod
    def save_exportable_report(devices: List[Dict[str, Any]], timestamp: int, user_id: str) -> bool:
        """Save exportable report for Telegram"""
        if not os.path.exists(settings.EXPORT_DIR):
            os.makedirs(settings.EXPORT_DIR)

        filename = f"{settings.EXPORT_DIR}/scan_{timestamp}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(devices, f, ensure_ascii=False, indent=4)
            console.print("[+] Экспортируемый отчет сохранен", style=settings.MAIN_COLOR)
            return filename
        except Exception as e:
            console.print(f"[!] Ошибка при создании экспортируемого отчета: {e}", style=settings.MAIN_COLOR)
            return None 