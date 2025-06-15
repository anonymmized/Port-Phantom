"""
Telegram notification functionality
"""

import requests
from rich.console import Console

from ..config.settings import TELEGRAM_BOT_TOKEN, AUTHORIZED_USER_ID, MAIN_COLOR

console = Console()


def send_telegram_message(message, user_id=None):
    """Send message to Telegram"""
    if user_id is None:
        user_id = AUTHORIZED_USER_ID
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": user_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            console.print(":white_check_mark: [bold green]Notification sent to Telegram[/bold green]", style=MAIN_COLOR)
            return True
        else:
            console.print(f":x: [bold red]Telegram send error:[/bold red] {response.status_code}", style=MAIN_COLOR)
            return False
    except Exception as e:
        console.print(f":x: [bold red]Telegram send error:[/bold red] {e}", style=MAIN_COLOR)
        return False


def send_scan_results(devices, user_id=None):
    """Send scan results to Telegram"""
    if not devices:
        return False
    
    message = "🔍 <b>Network scan results</b>\n\n"
    
    for device in devices:
        ip = device.get('ip', 'Unknown')
        manufacturer = device.get('manufacturer', 'Unknown')
        score = device.get('score', 0)
        level = device.get('level', 'None')
        ports = device.get('open ports', [])
        
        message += f"📱 <b>{ip}</b>\n"
        message += f"🏭 Manufacturer: {manufacturer}\n"
        message += f"⚠️ Risk: {level} ({score})\n"
        message += f"🔌 Ports: {', '.join(map(str, ports)) if ports else 'None'}\n\n"
    
    return send_telegram_message(message, user_id) 