"""
Report generation and file management
"""

import os
import json
import csv
import time
from rich.console import Console

from ..config.settings import MAIN_COLOR, HISTORY_DIR, EXPORT_DIR

console = Console()


def save_current_scan(devices, subnet):
    """Save current scan results"""
    timestamp = int(time.time())
    filename = f"{HISTORY_DIR}/scan_{timestamp}_{subnet.replace('/', '-')}.json"

    data_to_save = {
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'subnet': subnet,
        'devices': devices
    }

    try:
        os.makedirs(HISTORY_DIR, exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        console.print(f":floppy_disk: [bold green]Current scan saved to[/bold green] [underline]{filename}[/underline]", style=MAIN_COLOR)
        return data_to_save
    except Exception as e:
        console.print(f":x: [bold red]Failed to save scan history:[/bold red] {e}", style=MAIN_COLOR)
        return data_to_save


def load_prev_scan(subnet):
    """Load previous scan results"""
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR)
        return None

    scans = []
    for file in os.listdir(HISTORY_DIR):
        if subnet.replace('/', '-') in file and file.endswith('json'):
            scans.append(os.path.join(HISTORY_DIR, file))
    
    if not scans:
        console.print(":mag: [yellow]No previous scans found[/yellow]", style=MAIN_COLOR)
        return None
    
    latest_file = max(scans, key=os.path.getctime)
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        console.print(f":x: [bold red]Failed to load previous scan:[/bold red] {e}", style=MAIN_COLOR)
        return None


def save_csv_report(device):
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
        os.makedirs(HISTORY_DIR, exist_ok=True)
        with open(f"{HISTORY_DIR}/{filename}", 'w', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(headers)
            csv_writer.writerow(row)
        console.print(f":page_facing_up: [bold green]Report saved as:[/bold green] [underline]{filename}[/underline]", style=MAIN_COLOR)
        return True
    except Exception as e:
        console.print(f":x: [bold red]Error saving CSV:[/bold red] {e}", style=MAIN_COLOR)
        return False


def save_json_report(device):
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
        os.makedirs(HISTORY_DIR, exist_ok=True)
        with open(f"{HISTORY_DIR}/{filename}", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        console.print(f":page_facing_up: [bold green]Report saved as:[/bold green] [underline]{filename}[/underline]", style=MAIN_COLOR)
        return True
    except Exception as e:
        console.print(f":x: [bold red]Error saving JSON:[/bold red] {e}", style=MAIN_COLOR)
        return False


def save_exportable_report(devices, timestamp, user_id):
    """Save exportable report for Telegram"""
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    filename = f"{EXPORT_DIR}/scan_{timestamp}.json"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(devices, f, ensure_ascii=False, indent=4)
        console.print(":outbox_tray: [bold green]Exportable report saved[/bold green]", style=MAIN_COLOR)
        return filename
    except Exception as e:
        console.print(f":x: [bold red]Error creating exportable report:[/bold red] {e}", style=MAIN_COLOR)
        return None 