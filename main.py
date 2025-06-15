#!/usr/bin/env python3
"""
Port-Phantom - Network Security Scanner
Main entry point with CLI interface
"""

import sys
import os
import time
import argparse
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.table import Table
from rich import box

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.banner import print_banner
from src.config.settings import MAIN_COLOR, DEFAULT_SUBNET
from src.config.signature_loader import load_signatures
from src.scanners.mac_scanner import load_oui_db
from src.scanners.network_scanner import find_subnet
from src.core.device_processor import process_network
from src.classifiers.signature_matcher import check_against_signatures, print_matches
from src.reports.report_generator import save_current_scan, load_prev_scan, save_exportable_report, save_csv_report, save_json_report
from src.reports.scan_comparator import compare_scans
from src.utils.telegram_sender import send_scan_results

console = Console()


def create_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Port-Phantom - Network Security Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Scan default network with all features
  %(prog)s -s 192.168.1.0/24  # Scan specific subnet
  %(prog)s --no-telegram      # Disable Telegram notifications
  %(prog)s --export csv       # Export results in CSV format
  %(prog)s --compare-only     # Only compare with previous scan
  %(prog)s --verbose          # Enable verbose output
  %(prog)s --ports 22,80,443  # Scan specific ports only
        """
    )
    
    # Network options
    network_group = parser.add_argument_group('Network Options')
    network_group.add_argument(
        '-s', '--subnet',
        metavar='SUBNET',
        default=None,
        help='Target subnet to scan (default: auto-detect)'
    )
    network_group.add_argument(
        '--ports',
        metavar='PORTS',
        help='Comma-separated list of ports to scan (default: 21,22,23,53,80,443,554,2222,3389,8080,8000)'
    )
    network_group.add_argument(
        '--timeout',
        type=int,
        default=50,
        help='Host timeout in milliseconds (default: 50)'
    )
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument(
        '--export',
        choices=['json', 'csv', 'both'],
        help='Export results in specified format(s)'
    )
    output_group.add_argument(
        '--output-dir',
        metavar='DIR',
        default='history',
        help='Directory to save reports (default: history)'
    )
    output_group.add_argument(
        '--no-save',
        action='store_true',
        help='Do not save scan results to files'
    )
    
    # Feature toggles
    features_group = parser.add_argument_group('Feature Toggles')
    features_group.add_argument(
        '--no-telegram',
        action='store_true',
        help='Disable Telegram notifications'
    )
    features_group.add_argument(
        '--no-signatures',
        action='store_true',
        help='Skip signature matching'
    )
    features_group.add_argument(
        '--no-comparison',
        action='store_true',
        help='Skip comparison with previous scans'
    )
    features_group.add_argument(
        '--compare-only',
        action='store_true',
        help='Only compare with previous scan, do not scan network'
    )
    
    # Display options
    display_group = parser.add_argument_group('Display Options')
    display_group.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    display_group.add_argument(
        '--no-banner',
        action='store_true',
        help='Do not display banner'
    )
    display_group.add_argument(
        '--quiet',
        action='store_true',
        help='Minimal output (errors only)'
    )
    
    # Advanced options
    advanced_group = parser.add_argument_group('Advanced Options')
    advanced_group.add_argument(
        '--oui-file',
        metavar='FILE',
        help='Custom OUI database file path'
    )
    advanced_group.add_argument(
        '--signatures-file',
        metavar='FILE',
        help='Custom signatures file path'
    )
    advanced_group.add_argument(
        '--telegram-user',
        type=int,
        help='Custom Telegram user ID for notifications'
    )
    
    return parser


def update_settings_from_args(args):
    """Update settings based on command line arguments"""
    from src.config.settings import SCAN_PORTS, SCAN_TIMEOUT
    
    ports = SCAN_PORTS.copy()
    timeout = SCAN_TIMEOUT
    
    if args.ports:
        ports = [int(p.strip()) for p in args.ports.split(',')]
    
    if args.timeout:
        timeout = args.timeout
    
    return ports, timeout


def display_scan_statistics(devices, subnet, scan_time):
    """Display scan statistics in a beautiful table"""
    if not devices:
        return
    
    # Calculate statistics
    total_devices = len(devices)
    high_risk = sum(1 for d in devices if d.get('level') == 'High')
    medium_risk = sum(1 for d in devices if d.get('level') == 'Medium')
    low_risk = sum(1 for d in devices if d.get('level') == 'Low')
    
    manufacturers = {}
    for device in devices:
        mfr = device.get('manufacturer', 'Unknown')
        manufacturers[mfr] = manufacturers.get(mfr, 0) + 1
    
    # Create statistics table
    stats_table = Table(box=box.ROUNDED, title="📊 Scan Statistics", title_style="bold #1E90FF")
    stats_table.add_column("Metric", style="bold #6495ED")
    stats_table.add_column("Value", style="#48D1CC")
    
    stats_table.add_row("Subnet Scanned", subnet)
    stats_table.add_row("Total Devices Found", str(total_devices))
    stats_table.add_row("Scan Duration", f"{scan_time:.2f} seconds")
    stats_table.add_row("High Risk Devices", f"{high_risk} ({high_risk/total_devices*100:.1f}%)")
    stats_table.add_row("Medium Risk Devices", f"{medium_risk} ({medium_risk/total_devices*100:.1f}%)")
    stats_table.add_row("Low Risk Devices", f"{low_risk} ({low_risk/total_devices*100:.1f}%)")
    stats_table.add_row("Unique Manufacturers", str(len(manufacturers)))
    
    console.print(stats_table)
    console.print()
    
    # Top manufacturers
    if manufacturers:
        mfr_table = Table(box=box.ROUNDED, title="🏭 Top Manufacturers", title_style="bold #1E90FF")
        mfr_table.add_column("Manufacturer", style="bold #6495ED")
        mfr_table.add_column("Count", style="#48D1CC")
        
        sorted_mfrs = sorted(manufacturers.items(), key=lambda x: x[1], reverse=True)[:5]
        for mfr, count in sorted_mfrs:
            mfr_table.add_row(mfr, str(count))
        
        console.print(mfr_table)
        console.print()


def scan_network_with_options(args):
    """Perform network scan with specified options"""
    start_time = time.time()
    
    # Update settings
    ports, timeout = update_settings_from_args(args)
    
    # Determine subnet
    subnet = args.subnet or find_subnet()
    
    if args.verbose:
        console.print(f":mag: [bold green]Using subnet:[/bold green] {subnet}", style=MAIN_COLOR)
        console.print(f":gear: [bold green]Scanning ports:[/bold green] {ports}", style=MAIN_COLOR)
    
    # Load databases with progress
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        
        # Load signatures
        signatures = None
        if not args.no_signatures:
            task = progress.add_task("Loading signatures...", total=1)
            signatures = load_signatures(args.signatures_file)
            progress.update(task, completed=1)
        
        # Load OUI database
        task = progress.add_task("Loading OUI database...", total=1)
        oui_db = load_oui_db(args.oui_file)
        progress.update(task, completed=1)
        
        # Process network
        task = progress.add_task("Scanning network...", total=1)
        devices = process_network(subnet, oui_db, ports)
        progress.update(task, completed=1)
    
    scan_time = time.time() - start_time
    
    if not devices:
        console.print(":x: [bold red]Failed to process network[/bold red]", style=MAIN_COLOR)
        return None, subnet, scan_time
    
    # Check signatures
    if signatures and not args.no_signatures:
        console.print(":warning: [bold yellow]Checking device signatures...[/bold yellow]", style=MAIN_COLOR)
        for device in devices:
            matches = check_against_signatures(device, signatures)
            print_matches(device, matches)
    
    return devices, subnet, scan_time


def save_results_with_options(devices, subnet, args):
    """Save results based on command line options"""
    if args.no_save:
        return
    
    # Save current scan
    current_data = save_current_scan(devices, subnet)
    
    # Export in specified format
    if args.export:
        for device in devices:
            if args.export in ['csv', 'both']:
                save_csv_report(device)
            if args.export in ['json', 'both']:
                save_json_report(device)
    
    # Save exportable report for Telegram
    if not args.no_telegram:
        timestamp = int(time.time())
        save_exportable_report(devices, timestamp, args.telegram_user or "user")


def compare_with_previous(devices, subnet, args):
    """Compare with previous scan if enabled"""
    if args.no_comparison:
        return
    
    previous_data = load_prev_scan(subnet)
    compare_scans(devices, previous_data)


def send_notifications(devices, args):
    """Send notifications if enabled"""
    if args.no_telegram:
        return
    
    send_scan_results(devices, args.telegram_user)


def compare_only_mode(args):
    """Handle compare-only mode"""
    subnet = args.subnet or find_subnet()
    
    if args.verbose:
        console.print(f":mag: [bold green]Loading previous scan for subnet:[/bold green] {subnet}", style=MAIN_COLOR)
    
    previous_data = load_prev_scan(subnet)
    if not previous_data:
        console.print(":x: [bold red]No previous scan found for comparison[/bold red]", style=MAIN_COLOR)
        return
    
    console.print(f":white_check_mark: [bold green]Found previous scan from:[/bold green] {previous_data.get('timestamp', 'Unknown')}", style=MAIN_COLOR)
    console.print(f":mag: [bold green]Devices in previous scan:[/bold green] {len(previous_data.get('devices', []))}", style=MAIN_COLOR)
    
    # For compare-only, we just show the previous data
    devices = previous_data.get('devices', [])
    
    # Create a table for previous scan results
    if devices:
        prev_table = Table(box=box.ROUNDED, title="📋 Previous Scan Results", title_style="bold #1E90FF")
        prev_table.add_column("IP", style="bold #6495ED")
        prev_table.add_column("Manufacturer", style="#48D1CC")
        prev_table.add_column("Risk Level", style="#FF6B6B")
        prev_table.add_column("Open Ports", style="#FFD93D")
        
        for device in devices:
            risk_color = {
                'High': 'red',
                'Medium': 'yellow', 
                'Low': 'green'
            }.get(device.get('level', 'Unknown'), 'white')
            
            prev_table.add_row(
                device.get('ip', 'Unknown'),
                device.get('manufacturer', 'Unknown'),
                f"[{risk_color}]{device.get('level', 'Unknown')}[/{risk_color}]",
                ', '.join(map(str, device.get('open ports', []))) or 'None'
            )
        
        console.print(prev_table)


def main():
    """Main application entry point with CLI"""
    try:
        parser = create_parser()
        args = parser.parse_args()
        
        # Display banner unless disabled
        if not args.no_banner:
            print_banner()
        
        # Handle compare-only mode
        if args.compare_only:
            compare_only_mode(args)
            return
        
        # Perform scan
        devices, subnet, scan_time = scan_network_with_options(args)
        if not devices:
            return
        
        # Display statistics
        if not args.quiet:
            display_scan_statistics(devices, subnet, scan_time)
        
        # Save results
        save_results_with_options(devices, subnet, args)
        
        # Compare with previous
        compare_with_previous(devices, subnet, args)
        
        # Send notifications
        send_notifications(devices, args)
        
        if not args.quiet:
            console.print(":white_check_mark: [bold green]Scan completed successfully![/bold green]", style=MAIN_COLOR)
            
    except KeyboardInterrupt:
        console.print("\n:warning: [bold yellow]Scan interrupted by user[/bold yellow]", style=MAIN_COLOR)
        sys.exit(1)
    except Exception as e:
        console.print(f":x: [bold red]Unexpected error:[/bold red] {e}", style=MAIN_COLOR)
        if args.verbose:
            import traceback
            console.print(traceback.format_exc(), style="red")
        sys.exit(1)


if __name__ == "__main__":
    main() 