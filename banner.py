from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich import box

console = Console()

def banner_print():
    """Display enhanced Port-Phantom banner"""
    
    # ASCII Art with gradient colors
    ascii_art = [
        " ██▓███  ▒█████   ██▀███  ▄▄▄█████▓    ██▓███   ██░ ██  ▄▄▄      ███▄    █ ▄▄▄█████▓ ▒█████   ███▄ ▄███▓",
        "▓██░  ██▒██▒  ██▒▓██ ▒ ██▒▓  ██▒ ▓▒   ▓██░  ██▒▓██░ ██▒▒████▄    ██ ▀█   █ ▓  ██▒ ▓▒▒██▒  ██▒▓██▒▀█▀ ██▒",
        "▓██░ ██▓▒██░  ██▒▓██ ░▄█ ▒▒ ▓██░ ▒░   ▓██░ ██▓▒▒██▀▀██░▒██  ▀█▄ ▓██  ▀█ ██▒▒ ▓██░ ▒░▒██░  ██▒▓██    ▓██░",
        "▒██▄█▓▒ ▒██   ██░▒██▀▀█▄  ░ ▓██▓ ░    ▒██▄█▓▒ ▒░▓█ ░██ ░██▄▄▄▄██▓██▒  ▐▌██▒░ ▓██▓ ░ ▒██   ██░▒██    ▒██ ",
        "▒██▒ ░  ░ ████▓▒░░██▓ ▒██▒  ▒██▒ ░    ▒██▒ ░  ░░▓█▒░██▓ ▓█   ▓██▒██░   ▓██░  ▒██▒ ░ ░ ████▓▒░▒██▒   ░██▒",
        "▒▓▒░ ░  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░  ▒ ░░      ▒▓▒░ ░  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒░   ▒ ▒   ▒ ░░   ░ ▒░▒░▒░ ░ ▒░   ░  ░",
        "░▒ ░      ░ ▒ ▒░   ░▒ ░ ▒░    ░       ░▒ ░      ▒ ░▒░ ░  ▒   ▒▒ ░ ░░   ░ ▒░    ░      ░ ▒ ▒░ ░  ░      ░",
        "░░      ░ ░ ░ ▒    ░░   ░   ░         ░░        ░  ░░ ░  ░   ▒     ░   ░ ░   ░      ░ ░ ░ ▒  ░      ░   ",
        "            ░ ░     ░                           ░  ░  ░      ░  ░        ░              ░ ░         ░   "
    ]
    
    # Title and version
    title = Text("Port-Phantom v 1.0", style="bold #7B68EE")
    subtitle = Text("Network Security Scanner", style="italic #48D1CC")
    
    # Features table
    features_table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    features_table.add_column("Feature", style="bold #1E90FF")
    features_table.add_column("Description", style="#6495ED")
    
    features = [
        ("🔍 Device Discovery", "Automatically finds active devices on local networks"),
        ("🏭 Manufacturer ID", "Identifies devices by MAC address and manufacturer"),
        ("🔌 Port Analysis", "Checks open ports and classifies device types"),
        ("⚠️ Risk Assessment", "Calculates security risk levels based on signatures"),
        ("📊 Change Detection", "Compares scans to detect network changes"),
        ("📁 Export Options", "Saves results in JSON and CSV formats"),
        ("📱 Telegram Alerts", "Sends notifications via Telegram"),
        ("⚡ Real-time Monitoring", "Continuous network monitoring capabilities")
    ]
    
    for feature, description in features:
        features_table.add_row(feature, description)
    
    # Contact information
    contact_info = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    contact_info.add_column("Contact", style="bold #1E90FF")
    contact_info.add_column("Details", style="#6495ED")
    
    contact_info.add_row("🌐 GitHub", "https://github.com/yourusername/Port-Phantom")
    contact_info.add_row("📧 Email", "yourname@example.com")
    
    # Disclaimer
    disclaimer = Text("⚠️  This tool is for educational purposes only. Use responsibly.", style="bold #FF6B6B")
    
    # Display ASCII art with gradient
    colors = ["#48D1CC", "#40E0D0", "#5F9EA0", "#4682B4", "#6495ED", "#7B68EE"]
    for i, line in enumerate(ascii_art):
        color = colors[i % len(colors)]
        console.print(line, style=color)
    
    console.print()
    
    # Display title and subtitle
    console.print(Align.center(title))
    console.print(Align.center(subtitle))
    console.print()
    
    # Display features
    console.print(Panel(features_table, title="🚀 Features", border_style="#1E90FF"))
    console.print()
    
    # Display contact info
    console.print(Panel(contact_info, title="📞 Contact", border_style="#1E90FF"))
    console.print()
    
    # Display disclaimer
    console.print(Align.center(disclaimer))
    console.print()
    
    return 0 