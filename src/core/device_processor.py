"""
Device processing and information gathering
"""

from typing import Dict, Any, List
from rich.console import Console

from ..config.settings import settings
from ..scanners.network_scanner import NetworkScanner
from ..scanners.port_scanner import PortScanner
from ..scanners.mac_scanner import MACScanner
from ..classifiers.device_classifier import DeviceClassifier
from .risk_assessor import RiskAssessor

console = Console()


class DeviceProcessor:
    """Process and analyze devices"""
    
    def __init__(self, oui_db: Dict[str, str]):
        self.oui_db = oui_db
    
    def process_ip(self, ip: str) -> Dict[str, Any]:
        """Process a single IP address"""
        # Get MAC address
        mac = MACScanner.get_mac_address(ip)
        if not mac:
            return self._create_empty_device(ip)
        
        # Get open ports
        open_ports = PortScanner.check_ports(ip)
        
        # Get manufacturer
        oui = MACScanner.get_oui(mac)
        manufacturer = MACScanner.get_manufacturer(oui, self.oui_db)
        
        # Create device object
        device = {
            "ip": ip,
            "mac": mac,
            "manufacturer": manufacturer,
            "open ports": open_ports
        }
        
        # Classify device
        device_types = DeviceClassifier.classify_device(device)
        device['device type'] = device_types
        
        # Assess risk
        device = RiskAssessor.assess_device_risk(device)
        
        return device
    
    def _create_empty_device(self, ip: str) -> Dict[str, Any]:
        """Create empty device when MAC is not found"""
        return {
            "ip": ip,
            "mac": "Не найден",
            "manufacturer": "Неизвестный",
            "open ports": [],
            "device type": ["unknown"],
            "score": 0,
            "level": "None"
        }
    
    def process_network(self, subnet: str) -> List[Dict[str, Any]]:
        """Process entire network"""
        # Find active hosts
        active_ips = NetworkScanner.scan_network(subnet)
        
        if not active_ips:
            console.print("[!] Не найдено активных устройств", style=settings.MAIN_COLOR)
            return []
        
        console.print(f"[+] Обрабатываем {len(active_ips)} устройств...", style=settings.MAIN_COLOR)
        
        # Process each device
        devices = []
        for ip in active_ips:
            device = self.process_ip(ip)
            devices.append(device)
        
        return devices 