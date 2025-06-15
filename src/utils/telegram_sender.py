"""
Telegram integration for notifications
"""

import os
import telebot
from rich.console import Console

from ..config.settings import settings

console = Console()


class TelegramSender:
    """Send reports via Telegram"""
    
    def __init__(self):
        self.bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
    
    def send_file(self, file_path: str, chat_id: str) -> bool:
        """Send file via Telegram"""
        if not os.path.exists(file_path):
            console.print(f"[!] Файл {file_path} не найден", style=settings.MAIN_COLOR)
            return False

        try:
            with open(file_path, 'rb') as f:
                self.bot.send_document(chat_id, f)
            console.print("[+] Файл успешно отправлен через Telegram", style=settings.MAIN_COLOR)
            return True
        except Exception as e:
            console.print(f"[!] Ошибка при отправке через Telegram: {e}", style=settings.MAIN_COLOR)
            return False
    
    def send_message(self, message: str, chat_id: str) -> bool:
        """Send text message via Telegram"""
        try:
            self.bot.send_message(chat_id, message)
            console.print("[+] Сообщение отправлено через Telegram", style=settings.MAIN_COLOR)
            return True
        except Exception as e:
            console.print(f"[!] Ошибка при отправке сообщения: {e}", style=settings.MAIN_COLOR)
            return False 