"""
Application settings and configuration
"""

import os
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Settings:
    """Application settings"""
    
    # Colors
    MAIN_COLOR: str = "#B0E0E6"
    
    # Telegram settings
    TELEGRAM_BOT_TOKEN: str = "7840082685:AAEKTFSUjMa9CoXaNhBn9t8ONHAH_hJCQqo"
    AUTHORIZED_USER_ID: int = 815330161
    
    # Network settings
    DEFAULT_SUBNET: str = "192.168.1.0/24"
    SCAN_TIMEOUT: int = 50  # milliseconds
    MIN_HOSTGROUP: int = 20
    
    # Ports to scan
    SCAN_PORTS: List[int] = field(default_factory=lambda: [21, 22, 23, 53, 80, 443, 554, 2222, 3389, 8080, 8000])
    
    # Device classification rules
    ROUTER_MANUFACTURERS: List[str] = field(default_factory=lambda: ['TP-Link', 'Cisco', 'ASUS', 'Ubiquiti'])
    CAMERA_MANUFACTURERS: List[str] = field(default_factory=lambda: ['Hikvision', 'Dahua', 'Reolink'])
    
    # Device port rules
    DEVICE_PORT_RULES: Dict[str, List[int]] = field(default_factory=lambda: {
        "camera": [554],
        "router": [80, 443],
        "server": [22, 80, 443],
        "printer": [9100]
    })
    
    # Risk assessment rules
    RISK_RULES: Dict[str, Any] = field(default_factory=lambda: {
        'ports': {
            22: 5,  # SSH - bruteforce
            80: 3,  # HTTP - weak web-interface
            443: 3,  # HTTPS - web-interface
            554: 7,  # RTSP - cameras
            9100: 4,  # HP JetDirect - print servers
            23: 8,  # Telnet - old protocol without encryption
            21: 6,  # FTP - vulnerable versions are often used
            8080: 3,  # Web-port
            8000: 4,  # IOT devices
            8081: 4,
        },
        'manufacturers': {
            'Hikvision': 7,
            'Dahua': 6,
            'TPLink': 5,
            'Netgear': 5,
            'Apple': 1,
            'Samsung': 1,
            'Google': 1,
            'Amazon': 2,
        }
    })
    
    # File paths
    OUI_DB_PATH: str = "data/oui.txt"
    SIGNATURES_PATH: str = "config/signatures.yaml"
    HISTORY_DIR: str = "history"
    EXPORT_DIR: str = "exportable_reports"
    
    # Threading
    MAX_WORKERS: int = 10
    
    @classmethod
    def load_from_env(cls) -> 'Settings':
        """Load settings from environment variables"""
        settings = cls()
        
        # Override with environment variables if they exist
        if os.getenv('TELEGRAM_BOT_TOKEN'):
            settings.TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        
        if os.getenv('AUTHORIZED_USER_ID'):
            settings.AUTHORIZED_USER_ID = int(os.getenv('AUTHORIZED_USER_ID'))
        
        return settings


# Global settings instance
settings = Settings.load_from_env() 