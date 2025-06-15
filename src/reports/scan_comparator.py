"""
Scan comparison and change detection
"""

from rich.console import Console

from ..config.settings import MAIN_COLOR

console = Console()


def compare_scans(current_devices, previous_data):
    """Compare current scan with previous scan"""
    console.print("\n:arrows_counterclockwise: [bold cyan]Analyzing network changes...[/bold cyan]", style=MAIN_COLOR)
    
    if not previous_data or 'devices' not in previous_data:
        console.print(":information_source: [yellow]No data to compare[/yellow]", style=MAIN_COLOR)
        return
    
    previous_devices = {dev['ip']: dev for dev in previous_data.get('devices', [])}
    changes_found = False

    new_devices = []
    vanished_devices = []
    current_ips = set()

    # Check for new devices and risk changes
    for device in current_devices:
        ip = device['ip']
        current_ips.add(ip)

        if ip not in previous_devices:
            new_devices.append(device)
        else:
            prev_score = previous_devices[ip].get('score', 0)
            curr_score = device.get('score', 0)
            if curr_score > prev_score:
                console.print(
                    f":warning: [bold yellow]Risk increased for {ip}:[/bold yellow] {previous_devices[ip]['level']} → {device['level']} ({prev_score} → {curr_score})",
                    style=MAIN_COLOR
                )
                changes_found = True
    
    # Check for vanished devices
    for ip in previous_devices:
        if ip not in current_ips:
            vanished_devices.append(previous_devices[ip])
    
    # Report new devices
    if new_devices:
        console.print(f":sparkles: [bold green]New devices:[/bold green]", style=MAIN_COLOR)
        for dev in new_devices:
            console.print(
                f"   IP: {dev['ip']} | Manufacturer: {dev['manufacturer']} | Ports: {dev['open ports']}",
                style=MAIN_COLOR
            )
        changes_found = True
    
    # Report vanished devices
    if vanished_devices:
        console.print(":wastebasket: [bold yellow]Vanished devices:[/bold yellow]", style=MAIN_COLOR)
        for dev in vanished_devices:
            console.print(
                f"   IP: {dev['ip']} | Manufacturer: {dev['manufacturer']}",
                style=MAIN_COLOR
            )
        changes_found = True
    
    if not changes_found:
        console.print(":white_check_mark: [bold green]No network changes detected[/bold green]", style=MAIN_COLOR) 