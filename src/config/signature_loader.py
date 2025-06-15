"""
Signature loading and management
"""

import os
import yaml
from rich.console import Console

from .settings import MAIN_COLOR, SIGNATURES_PATH

console = Console()


def load_signatures(filename=None):
    """Load signatures from YAML file"""
    if filename is None:
        filename = SIGNATURES_PATH
    
    if not os.path.exists(filename):
        console.print(f":x: [bold red]File not found:[/bold red] {filename}", style=MAIN_COLOR)
        return []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            signatures = data.get('signatures', [])
            console.print(f":bookmark_tabs: [bold green]{len(signatures)} signatures loaded[/bold green]", style=MAIN_COLOR)
            return signatures
    except yaml.YAMLError as e:
        console.print(f":x: [bold red]YAML parsing error:[/bold red] {e}", style=MAIN_COLOR)
        return []
    except Exception as e:
        console.print(f":x: [bold red]Error loading signatures:[/bold red] {e}", style=MAIN_COLOR)
        return []

def get_signatures(signatures):
    """Get loaded signatures"""
    return signatures

def reload_signatures(filename=None):
    """Reload signatures from file"""
    return load_signatures(filename) 