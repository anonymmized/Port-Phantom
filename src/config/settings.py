"""
Application settings and configuration
"""

import os

# Colors
MAIN_COLOR = "#B0E0E6"

# Telegram settings
TELEGRAM_BOT_TOKEN = "7840082685:AAEKTFSUjMa9CoXaNhBn9t8ONHAH_hJCQqo"
AUTHORIZED_USER_ID = 815330161

# Network settings
DEFAULT_SUBNET = "192.168.1.0/24"
SCAN_TIMEOUT = 50  # milliseconds
MIN_HOSTGROUP = 20
MAX_RETRIES = 3

# Ports to scan (expanded list)
SCAN_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995,  # Basic services
    554, 8000, 8080, 8081, 8443,  # Web and streaming
    2222, 3389, 5900,  # Remote access
    9100, 515, 631,  # Printing
    1433, 3306, 5432,  # Databases
    27017, 6379,  # NoSQL databases
    1883, 8883,  # MQTT
    5683, 5684,  # CoAP
    161, 162,  # SNMP
    123,  # NTP
    137, 138, 139, 445,  # SMB/NetBIOS
    67, 68,  # DHCP
    514,  # Syslog
]

# Device classification rules (expanded)
ROUTER_MANUFACTURERS = [
    'TP-Link', 'Cisco', 'ASUS', 'Ubiquiti', 'Netgear', 'Linksys', 
    'D-Link', 'Belkin', 'Buffalo', 'ZyXEL', 'MikroTik', 'Huawei',
    'ZTE', 'Fritz!Box', 'AVM', 'Technicolor', 'Sagemcom'
]

CAMERA_MANUFACTURERS = [
    'Hikvision', 'Dahua', 'Reolink', 'Axis', 'Foscam', 'Amcrest',
    'Wyze', 'Ring', 'Arlo', 'Nest', 'Eufy', 'Blink', 'Vivint'
]

SMARTPHONE_MANUFACTURERS = [
    'Apple', 'Samsung', 'Huawei', 'Xiaomi', 'OnePlus', 'Google',
    'Sony', 'LG', 'Motorola', 'Nokia', 'HTC', 'BlackBerry'
]

COMPUTER_MANUFACTURERS = [
    'Dell', 'HP', 'Lenovo', 'ASUS', 'Acer', 'MSI', 'Gigabyte',
    'Apple', 'Samsung', 'Toshiba', 'Fujitsu', 'Gateway'
]

PRINTER_MANUFACTURERS = [
    'Canon', 'Epson', 'HP', 'Brother', 'Samsung', 'Xerox',
    'Lexmark', 'Ricoh', 'Kyocera', 'Sharp', 'Konica Minolta'
]

# Device port rules (expanded)
DEVICE_PORT_RULES = {
    "camera": [554, 8000, 8080, 8081, 8443, 37777, 37778, 37779],
    "router": [80, 443, 8080, 8443, 22, 23],
    "server": [22, 80, 443, 21, 25, 53, 1433, 3306, 5432, 27017, 6379],
    "printer": [9100, 515, 631, 80, 443],
    "nas": [21, 22, 80, 443, 139, 445, 548, 873, 2049],
    "smartphone": [22, 80, 443, 8080, 8443],
    "computer": [22, 80, 443, 3389, 5900, 139, 445],
    "tv": [80, 443, 8080, 8443, 8008, 8009],
    "iot": [1883, 8883, 5683, 5684, 161, 162, 123, 514],
    "database": [1433, 3306, 5432, 27017, 6379, 1521, 1433],
    "web-server": [80, 443, 8080, 8443, 3000, 5000, 8000],
    "mail-server": [25, 110, 143, 993, 995, 587],
    "dns-server": [53],
    "dhcp-server": [67, 68],
    "file-server": [21, 22, 139, 445, 548, 873, 2049],
    "remote-access": [22, 23, 3389, 5900, 2222],
    "streaming": [554, 8000, 8080, 8081, 8443],
    "monitoring": [161, 162, 514, 123, 1883, 8883]
}

# Risk assessment rules (enhanced)
RISK_RULES = {
    'ports': {
        # High risk ports
        22: 5,    # SSH - potential bruteforce
        23: 8,    # Telnet - unencrypted, very high risk
        21: 6,    # FTP - often unencrypted
        3389: 6,  # RDP - remote desktop
        5900: 5,  # VNC - remote desktop
        
        # Medium risk ports
        80: 3,    # HTTP - weak web interface
        443: 3,   # HTTPS - web interface
        8080: 3,  # Alternative web port
        8443: 3,  # Alternative HTTPS port
        8000: 4,  # IoT devices
        8081: 4,  # IoT devices
        
        # IoT and camera ports
        554: 7,   # RTSP - cameras
        37777: 7, # Hikvision cameras
        37778: 7, # Hikvision cameras
        37779: 7, # Hikvision cameras
        
        # Database ports
        1433: 6,  # MSSQL
        3306: 5,  # MySQL
        5432: 5,  # PostgreSQL
        27017: 5, # MongoDB
        6379: 4,  # Redis
        
        # Network services
        53: 2,    # DNS
        67: 2,    # DHCP
        161: 4,   # SNMP
        162: 4,   # SNMP trap
        123: 2,   # NTP
        514: 3,   # Syslog
        
        # File sharing
        139: 4,   # NetBIOS
        445: 4,   # SMB
        548: 3,   # AFP
        
        # IoT protocols
        1883: 4,  # MQTT
        8883: 4,  # MQTT over SSL
        5683: 3,  # CoAP
        5684: 3,  # CoAP over DTLS
        
        # Printing
        9100: 4,  # HP JetDirect
        515: 3,   # LPR
        631: 3,   # IPP
    },
    'manufacturers': {
        # High risk manufacturers
        'Hikvision': 7,
        'Dahua': 6,
        'Axis': 5,
        'Foscam': 6,
        'Amcrest': 5,
        
        # Router manufacturers
        'TP-Link': 5,
        'Netgear': 5,
        'Linksys': 4,
        'D-Link': 4,
        'ASUS': 4,
        'Cisco': 3,
        'Ubiquiti': 3,
        
        # Consumer electronics
        'Apple': 1,
        'Samsung': 1,
        'Google': 1,
        'Amazon': 2,
        'Xiaomi': 2,
        'Huawei': 2,
        
        # Computer manufacturers
        'Dell': 2,
        'HP': 2,
        'Lenovo': 2,
        'ASUS': 2,
        'Acer': 2,
        
        # Printer manufacturers
        'Canon': 3,
        'Epson': 3,
        'Brother': 3,
        'Xerox': 3,
    },
    'device_types': {
        'camera': 6,
        'router': 4,
        'server': 5,
        'printer': 3,
        'nas': 4,
        'smartphone': 2,
        'computer': 2,
        'tv': 2,
        'iot': 5,
        'database': 6,
        'web-server': 4,
        'mail-server': 5,
        'dns-server': 3,
        'dhcp-server': 3,
        'file-server': 4,
        'remote-access': 5,
        'streaming': 4,
        'monitoring': 3,
    }
}

# Risk level thresholds
RISK_THRESHOLDS = {
    'Low': 0,
    'Medium': 3,
    'High': 6,
    'Critical': 9
}

# File paths
OUI_DB_PATH = "data/oui.txt"
SIGNATURES_PATH = "config/signatures.yaml"
HISTORY_DIR = "history"
EXPORT_DIR = "exportable_reports"

# Performance settings
MAX_WORKERS = 10
CONNECTION_TIMEOUT = 5
HTTP_TIMEOUT = 3

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Scan settings
SCAN_BATCH_SIZE = 50
SCAN_DELAY = 0.1  # seconds between scans

def load_settings_from_env():
    """Load settings from environment variables"""
    global TELEGRAM_BOT_TOKEN, AUTHORIZED_USER_ID, SCAN_TIMEOUT, MAX_WORKERS
    
    if os.getenv('TELEGRAM_BOT_TOKEN'):
        TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if os.getenv('AUTHORIZED_USER_ID'):
        AUTHORIZED_USER_ID = int(os.getenv('AUTHORIZED_USER_ID'))
    
    if os.getenv('SCAN_TIMEOUT'):
        SCAN_TIMEOUT = int(os.getenv('SCAN_TIMEOUT'))
    
    if os.getenv('MAX_WORKERS'):
        MAX_WORKERS = int(os.getenv('MAX_WORKERS'))

# Load settings
load_settings_from_env() 