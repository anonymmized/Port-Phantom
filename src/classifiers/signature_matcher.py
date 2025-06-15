"""
Signature matching for device identification
"""

from rich.console import Console

from ..config.settings import MAIN_COLOR

console = Console()


def check_against_signatures(device, signatures):
    """Check if device matches any signatures"""
    matched = []
    
    for sig in signatures:
        manufacturers = sig['conditions'].get('manufacturer', [])
        ports = list(map(int, sig['conditions'].get('ports', [])))

        # Check manufacturer match
        if manufacturers and device['manufacturer'] not in manufacturers:
            continue
            
        # Check port match
        if ports and not any(port in ports for port in map(int, device['open ports'])):
            continue
        
        matched.append(sig)
    
    return matched


def print_matches(device, matches):
    """Print signature matches for a device"""
    if matches:
        console.print(f":warning: [bold yellow]Device {device.get('ip')} matches signatures:[/bold yellow]", style=MAIN_COLOR)
        for match in matches:
            console.print(f"    → {match.get('name', 'No name')}", style=MAIN_COLOR)
            console.print(f"      {match.get('description', 'No description')}", style=MAIN_COLOR)
            if match.get('cve_info'):
                console.print(f"      CVE: {match.get('cve_info')}", style="red") 