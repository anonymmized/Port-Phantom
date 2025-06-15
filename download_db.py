#!/usr/bin/env python3
"""
OUI Database Downloader
Downloads and validates the IEEE OUI database for MAC address manufacturer lookup
"""

import os
import sys
import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich import box

console = Console()

def download_oui_database():
    """Download OUI database from IEEE"""
    url = "https://standards-oui.ieee.org/oui.txt"
    filename = "data/oui.txt"
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Check if file already exists
    if os.path.exists(filename):
        console.print(":information_source: [yellow]OUI database already exists[/yellow]", style="yellow")
        console.print(f":file_folder: [blue]Location:[/blue] {filename}", style="blue")
        
        # Check file size
        file_size = os.path.getsize(filename)
        if file_size > 1024 * 1024:  # More than 1MB
            console.print(":white_check_mark: [green]Database appears to be valid (size: {:.1f} MB)[/green]".format(file_size / (1024 * 1024)), style="green")
            return True
        else:
            console.print(":warning: [yellow]Database file seems too small, re-downloading...[/yellow]", style="yellow")
    
    console.print(":cloud: [bold blue]Downloading OUI database from IEEE...[/bold blue]", style="blue")
    console.print(f":link: [blue]URL:[/blue] {url}", style="blue")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            
            task = progress.add_task("Downloading...", total=None)
            
            # Download with stream=True for large files
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Get total size if available
            total_size = int(response.headers.get('content-length', 0))
            if total_size:
                progress.update(task, total=total_size)
            
            downloaded_size = 0
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size:
                            progress.update(task, completed=downloaded_size)
                        else:
                            progress.update(task, description=f"Downloaded: {downloaded_size / (1024*1024):.1f} MB")
        
        # Validate downloaded file
        file_size = os.path.getsize(filename)
        if file_size < 1024 * 1024:  # Less than 1MB
            console.print(":x: [bold red]Downloaded file is too small, download may have failed[/bold red]", style="red")
            return False
        
        # Check file content
        with open(filename, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if not first_line.startswith('Registry'):
                console.print(":x: [bold red]Downloaded file doesn't appear to be a valid OUI database[/bold red]", style="red")
                return False
        
        console.print(":white_check_mark: [bold green]OUI database downloaded successfully![/bold green]", style="green")
        console.print(f":file_folder: [blue]File size:[/blue] {file_size / (1024*1024):.1f} MB", style="blue")
        console.print(f":file_folder: [blue]Location:[/blue] {filename}", style="blue")
        
        # Show statistics
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                oui_count = sum(1 for line in lines if '(base 16)' in line)
                console.print(f":bookmark_tabs: [blue]OUI entries:[/blue] {oui_count:,}", style="blue")
        except Exception:
            pass
        
        return True
        
    except requests.exceptions.RequestException as e:
        console.print(f":x: [bold red]Download failed:[/bold red] {e}", style="red")
        return False
    except Exception as e:
        console.print(f":x: [bold red]Unexpected error:[/bold red] {e}", style="red")
        return False

def main():
    """Main function"""
    console.print(Panel.fit(
        "[bold blue]Port-Phantom OUI Database Downloader[/bold blue]\n"
        "Downloads the IEEE OUI database for MAC address manufacturer lookup",
        border_style="blue",
        box=box.ROUNDED
    ))
    console.print()
    
    success = download_oui_database()
    
    if success:
        console.print()
        console.print(":information_source: [blue]Usage:[/blue]", style="blue")
        console.print("  The OUI database will be automatically used by Port-Phantom", style="blue")
        console.print("  for manufacturer identification during network scans.", style="blue")
        console.print()
        console.print(":warning: [yellow]Note:[/yellow] The database is updated regularly by IEEE.", style="yellow")
        console.print("  Consider re-downloading periodically for the latest data.", style="yellow")
    else:
        console.print()
        console.print(":x: [bold red]Failed to download OUI database[/bold red]", style="red")
        console.print("  Port-Phantom will still work but manufacturer identification", style="red")
        console.print("  may be limited.", style="red")
        sys.exit(1)

if __name__ == "__main__":
    main() 