#!/usr/bin/env python3
"""
Port-Phantom - Network Security Scanner
Main application entry point
"""

import os
import time
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console

from src.config.settings import settings
from src.config.signature_loader import SignatureLoader
from src.scanners.network_scanner import NetworkScanner
from src.scanners.mac_scanner import MACScanner
from src.core.device_processor import DeviceProcessor
from src.reports.report_generator import ReportGenerator
from src.reports.scan_comparator import ScanComparator
from src.classifiers.signature_matcher import SignatureMatcher
from src.utils.banner import Banner
from src.utils.telegram_sender import TelegramSender
from src.utils.oui_loader import OUILoader

console = Console()

def get_user_id() -> str:
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            stored_id = f.read().strip()
        
        response = input(f"Ваш ID: {stored_id} [Y/n]: ")
        if response.lower() in ['y', 'yes', '']:
            return stored_id
        elif response.lower() in ['n', 'no']:
            os.remove('.env')
        else:
            console.print("Неверный параметр", style="red")
            return None
    
    user_id = input("Введите ваш ID: ")
    with open('.env', 'w') as f:
        f.write(user_id)
    return user_id


def main():
    Banner.print_banner()
    
    console.print('Проверка user ID...', style=settings.MAIN_COLOR)
    user_id = get_user_id()
    if user_id is None:
        console.print("[!] Не удалось получить user ID. Завершение работы.", style="red")
        return
    
    start_time = time.time()
    
    # Download OUI database if needed
    if not OUILoader.download_oui_db():
        console.print("[!] Не удалось загрузить базу OUI", style="red")
        return
    
    # Load OUI database
    oui_db = MACScanner.load_oui_db()
    
    # Find and scan network
    subnet = NetworkScanner.find_subnet()
    console.print(f"\n[+] Начинаем сканирование сети {subnet}...", style=settings.MAIN_COLOR)
    
    # Create device processor
    processor = DeviceProcessor(oui_db)
    
    # Process devices
    devices = processor.process_network(subnet)
    
    if not devices:
        console.print("[!] Не найдено устройств для обработки", style="red")
        return
    
    # Load signatures
    signature_loader = SignatureLoader()
    signatures = signature_loader.get_signatures()
    
    # Compare with previous scan
    previous_data = ReportGenerator.load_prev_scan(subnet)
    if previous_data:
        ScanComparator.compare_scans(devices, previous_data)
    
    # Save current scan
    ReportGenerator.save_current_scan(devices, subnet)
    
    # Display results
    console.print("\n[+] Результаты:", style=settings.MAIN_COLOR)
    
    for device in devices:
        # Check signatures
        matches = SignatureMatcher.check_against_signatures(device, signatures)
        
        # Display device info
        console.print(f"IP: {device.get('ip', 'unknown')}", style=settings.MAIN_COLOR)
        console.print(f"MAC: {device.get('mac', 'Не найден')}", style=settings.MAIN_COLOR)
        console.print(f"Manufacturer: {device.get('manufacturer', 'Неизвестный')}", style=settings.MAIN_COLOR)
        console.print(f"Open ports: {', '.join(device.get('open ports', [])) if device.get('open ports') else 'None'}", style=settings.MAIN_COLOR)
        console.print(f"Device type: {', '.join(device.get('device type', ['unknown']))}", style=settings.MAIN_COLOR)
        console.print(f"Risk level: {device.get('level', 'None')} ({device.get('score', 0)})", style=settings.MAIN_COLOR)
        
        # Display signature matches
        SignatureMatcher.print_matches(device, matches)
        
        console.print("-" * 50, style=settings.MAIN_COLOR)
    
    # Save exportable report and send via Telegram
    timestamp = int(time.time())
    export_file = ReportGenerator.save_exportable_report(devices, timestamp, user_id)
    
    if export_file:
        telegram_sender = TelegramSender()
        telegram_sender.send_file(export_file, user_id)
    
    # Display execution time
    end_time = time.time()
    console.print(f"\n[+] Время выполнения: {end_time - start_time:.2f} секунд", style=settings.MAIN_COLOR)


if __name__ == '__main__':
    main() 