"""
Device classification based on manufacturer and ports
"""

from typing import List, Dict, Any
from rich.console import Console

from ..config.settings import settings
from ..scanners.port_scanner import PortScanner

console = Console()


class DeviceClassifier:
    """Device type classification"""
    
    @staticmethod
    def classify_by_manufacturer(manufacturer: str) -> List[str]:
        """Classify device by manufacturer"""
        if manufacturer in settings.ROUTER_MANUFACTURERS:
            return ['router']
        elif manufacturer in settings.CAMERA_MANUFACTURERS:
            return ['camera']
        elif "Apple" in manufacturer or "Samsung" in manufacturer:
            return ['smartphone']
        else:
            return []
    
    @staticmethod
    def classify_by_ports(open_ports: List[str]) -> List[str]:
        """Classify device by open ports"""
        open_ports_int = list(map(int, open_ports))
        device_types = []

        for dev_type, ports in settings.DEVICE_PORT_RULES.items():
            if any(port in open_ports_int for port in ports):
                device_types.append(dev_type)
        
        return device_types or ['unknown']
    
    @staticmethod
    def classify_by_http(headers: Dict[str, str]) -> List[str]:
        """Classify device by HTTP headers"""
        if not headers:
            return []
        
        server = headers.get('Server', '').lower()
        powered_by = headers.get('X-Powered-By', '').lower()
        
        if 'gsoap' in server:
            return ["camera"]
        elif 'nginx' in server or 'apache' in server:
            return ["router", "web-server"]
        elif 'micro_httpd' in server:
            return ["printer"]
        return []
    
    @classmethod
    def classify_device(cls, device: Dict[str, Any]) -> List[str]:
        """Main device classification method"""
        manufacturer = device["manufacturer"].strip()
        open_ports = list(map(int, device["open ports"]))

        classifications = []

        # Classify by manufacturer
        classifications += cls.classify_by_manufacturer(manufacturer)
        
        # Classify by ports
        classifications += cls.classify_by_ports(device["open ports"])

        # Classify by HTTP headers if web ports are open
        if 80 in open_ports or 443 in open_ports:
            headers = PortScanner.get_http_headers(device["ip"])
            http_types = cls.classify_by_http(headers)
            if http_types:
                classifications += http_types

        return list(set(classifications)) or ["unknown"] 