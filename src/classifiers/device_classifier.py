"""
Device classification based on manufacturer and ports
"""

from rich.console import Console

from ..config.settings import ROUTER_MANUFACTURERS, CAMERA_MANUFACTURERS, DEVICE_PORT_RULES
from ..scanners.port_scanner import get_http_headers

console = Console()


def classify_by_manufacturer(manufacturer):
    """Classify device by manufacturer"""
    if not manufacturer or manufacturer.lower() in ['unknown', 'not found']:
        return []
        
    manufacturer_lower = manufacturer.lower()
    
    if manufacturer_lower in [m.lower() for m in ROUTER_MANUFACTURERS]:
        return ['router']
    elif manufacturer_lower in [m.lower() for m in CAMERA_MANUFACTURERS]:
        return ['camera']
    elif any(brand in manufacturer_lower for brand in ['apple', 'samsung', 'huawei', 'xiaomi', 'oneplus']):
        return ['smartphone']
    elif any(brand in manufacturer_lower for brand in ['dell', 'hp', 'lenovo', 'asus', 'acer', 'msi']):
        return ['computer']
    elif any(brand in manufacturer_lower for brand in ['canon', 'epson', 'hp', 'brother']):
        return ['printer']
    elif any(brand in manufacturer_lower for brand in ['sony', 'lg', 'samsung', 'philips', 'panasonic']):
        return ['tv', 'media-device']
    else:
        return []


def classify_by_ports(open_ports):
    """Classify device by open ports"""
    if not open_ports:
        return ['unknown']
        
    try:
        open_ports_int = list(map(int, open_ports))
        device_types = []

        for dev_type, ports in DEVICE_PORT_RULES.items():
            if any(port in open_ports_int for port in ports):
                device_types.append(dev_type)
        
        return device_types or ['unknown']
    except (ValueError, TypeError):
        return ['unknown']


def classify_by_http(headers):
    """Classify device by HTTP headers"""
    if not headers:
        return []
    
    try:
        server = headers.get('Server', '').lower()
        powered_by = headers.get('X-Powered-By', '').lower()
        user_agent = headers.get('User-Agent', '').lower()
        
        if 'gsoap' in server or 'axis' in server:
            return ["camera"]
        elif 'nginx' in server or 'apache' in server:
            return ["router", "web-server"]
        elif 'micro_httpd' in server or 'printer' in server:
            return ["printer"]
        elif 'router' in server or 'gateway' in server:
            return ["router"]
        elif 'camera' in server or 'ipcam' in server:
            return ["camera"]
        elif 'nas' in server or 'synology' in server:
            return ["nas", "storage"]
        return []
    except Exception:
        return []


def classify_device(device):
    """Main device classification method"""
    try:
        manufacturer = device.get("manufacturer", "").strip()
        open_ports = device.get("open ports", [])

        classifications = []

        # Classify by manufacturer
        manufacturer_types = classify_by_manufacturer(manufacturer)
        classifications.extend(manufacturer_types)
        
        # Classify by ports
        port_types = classify_by_ports(open_ports)
        classifications.extend(port_types)

        # Classify by HTTP headers if web ports are open
        if open_ports and any(str(port) in ['80', '443'] for port in open_ports):
            headers = get_http_headers(device.get("ip", ""))
            http_types = classify_by_http(headers)
            if http_types:
                classifications.extend(http_types)

        # Remove duplicates and return
        unique_classifications = list(set(classifications))
        return unique_classifications if unique_classifications else ["unknown"]
        
    except Exception as e:
        console.print(f":x: [bold red]Error classifying device {device.get('ip', 'unknown')}:[/bold red] {e}", style="red")
        return ["unknown"] 