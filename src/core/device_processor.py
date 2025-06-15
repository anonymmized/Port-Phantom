"""
Device processing and information gathering
"""

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from ..config.settings import MAIN_COLOR
from ..scanners.network_scanner import scan_network
from ..scanners.port_scanner import check_ports
from ..scanners.mac_scanner import get_mac_address, get_oui, get_manufacturer
from ..classifiers.device_classifier import classify_device
from .risk_assessor import assess_device_risk

console = Console()


def create_empty_device(ip):
    """Create empty device when MAC is not found"""
    return {
        "ip": ip,
        "mac": "Not found",
        "manufacturer": "Unknown",
        "open ports": [],
        "device type": ["unknown"],
        "score": 0,
        "level": "None"
    }


def process_ip(ip, oui_db, ports=None):
    """Process a single IP address"""
    try:
        # Get MAC address
        mac = get_mac_address(ip)
        if not mac:
            return create_empty_device(ip)
        
        # Get open ports
        open_ports = check_ports(ip, ports)
        
        # Get manufacturer
        oui = get_oui(mac)
        manufacturer = get_manufacturer(oui, oui_db)
        
        # Create device object
        device = {
            "ip": ip,
            "mac": mac,
            "manufacturer": manufacturer,
            "open ports": open_ports
        }
        
        # Classify device
        device_types = classify_device(device)
        device['device type'] = device_types
        
        # Assess risk
        device = assess_device_risk(device)
        
        return device
        
    except Exception as e:
        console.print(f":x: [bold red]Error processing {ip}:[/bold red] {e}", style=MAIN_COLOR)
        return create_empty_device(ip)


def process_network(subnet, oui_db, ports=None):
    """Process entire network"""
    # Find active hosts
    active_ips = scan_network(subnet)
    
    if not active_ips:
        console.print(":x: [bold red]No active devices found[/bold red]", style=MAIN_COLOR)
        return []
    
    console.print(f":gear: [bold green]Processing {len(active_ips)} devices...[/bold green]", style=MAIN_COLOR)
    
    # Process each device with progress bar
    devices = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("Processing devices...", total=len(active_ips))
        
        for ip in active_ips:
            device = process_ip(ip, oui_db, ports)
            devices.append(device)
            progress.update(task, advance=1)
    
    # Filter out devices with errors
    valid_devices = [d for d in devices if d.get('mac') != 'Not found']
    if len(valid_devices) != len(devices):
        console.print(f":warning: [yellow]Processed {len(devices)} devices, {len(valid_devices)} with valid data[/yellow]", style=MAIN_COLOR)
    
    return devices 