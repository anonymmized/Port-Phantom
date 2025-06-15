"""
Application banner display
"""

from rich.console import Console

console = Console()


def print_banner():
    """Print the application banner"""
    s1 = " ██▓███  ▒█████   ██▀███  ▄▄▄█████▓    ██▓███   ██░ ██  ▄▄▄      ███▄    █ ▄▄▄█████▓ ▒█████   ███▄ ▄███▓"
    s2 = "▓██░  ██▒██▒  ██▒▓██ ▒ ██▒▓  ██▒ ▓▒   ▓██░  ██▒▓██░ ██▒▒████▄    ██ ▀█   █ ▓  ██▒ ▓▒▒██▒  ██▒▓██▒▀█▀ ██▒"
    s3 = "▓██░ ██▓▒██░  ██▒▓██ ░▄█ ▒▒ ▓██░ ▒░   ▓██░ ██▓▒▒██▀▀██░▒██  ▀█▄ ▓██  ▀█ ██▒▒ ▓██░ ▒░▒██░  ██▒▓██    ▓██░"
    s4 = "▒██▄█▓▒ ▒██   ██░▒██▀▀█▄  ░ ▓██▓ ░    ▒██▄█▓▒ ▒░▓█ ░██ ░██▄▄▄▄██▓██▒  ▐▌██▒░ ▓██▓ ░ ▒██   ██░▒██    ▒██ "
    s5 = "▒██▒ ░  ░ ████▓▒░░██▓ ▒██▒  ▒██▒ ░    ▒██▒ ░  ░░▓█▒░██▓ ▓█   ▓██▒██░   ▓██░  ▒██▒ ░ ░ ████▓▒░▒██▒   ░██▒"
    s6 = "▒▓▒░ ░  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░  ▒ ░░      ▒▓▒░ ░  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒░   ▒ ▒   ▒ ░░   ░ ▒░▒░▒░ ░ ▒░   ░  ░"
    s7 = "░▒ ░      ░ ▒ ▒░   ░▒ ░ ▒░    ░       ░▒ ░      ▒ ░▒░ ░  ▒   ▒▒ ░ ░░   ░ ▒░    ░      ░ ▒ ▒░ ░  ░      ░"
    s8 = "░░      ░ ░ ░ ▒    ░░   ░   ░         ░░        ░  ░░ ░  ░   ▒     ░   ░ ░   ░      ░ ░ ░ ▒  ░      ░   "
    s9 = "            ░ ░     ░                           ░  ░  ░      ░  ░        ░              ░ ░         ░   "
    s10 = "                      Port-Phantom v 1.0 - Network Security Scanner"
    s11 = "             Network Security Tool for Scanning and Monitoring Local Networks"
    s12 = "   Features:"
    s13 = "    • Scans local networks to discover devices"
    s14 = "    • Identifies devices by MAC address and manufacturer"
    s15 = "    • Checks open ports and classifies device types"
    s16 = "    • Calculates risk levels based on signatures and port configurations"
    s17 = "    • Compares current scan with previous scans to detect changes"
    s18 = "    • Saves results in JSON and CSV formats"
    s19 = "    • Supports multiple subnets and historical data tracking"
    s20 = "   Contact:"
    s21 = "    • GitHub: https://github.com/yourusername/Port-Phantom"
    s22 = "    • Email: yourname@example.com"
    s23 = "                                  Disclaimer:"
    s24 = "              This tool is for educational purposes only. Use responsibly."
    s25 = "                          © 2025 Port-Phantom Team"
    
    console.print(s1, style="#48D1CC")
    console.print(s2, style="#48D1CC")
    console.print(s3, style="#48D1CC")
    console.print(s4, style="#48D1CC")
    console.print(s5, style="#40E0D0")
    console.print(s6, style="#40E0D0")
    console.print(s7, style="#5F9EA0")
    console.print(s8, style="#5F9EA0")
    console.print(s9, style="#5F9EA0")

    console.print(f'[italic][bold]{s10}[/bold][/italic]', style="#7B68EE")
    console.print(f'[italic][bold]{s11}[/bold][/italic]', style="#7B68EE")
    console.print(f'[italic][bold]{s12}[/bold][/italic]', style="#1E90FF")
    console.print(f'[italic]{s13}[/italic]', style="#6495ED")
    console.print(f'[italic]{s14}[/italic]', style="#6495ED")
    console.print(f'[italic]{s15}[/italic]', style="#6495ED")
    console.print(f'[italic]{s16}[/italic]', style="#6495ED")
    console.print(f'[italic]{s17}[/italic]', style="#6495ED")
    console.print(f'[italic]{s18}[/italic]', style="#6495ED")
    console.print(f'[italic]{s19}[/italic]', style="#6495ED")
    console.print(f'[italic][bold]{s20}[/bold][/italic]', style="#1E90FF")
    console.print(f'[italic]{s21}[/italic]', style="#6495ED")
    console.print(f'[italic]{s22}[/italic]', style="#6495ED")
    console.print(f'[italic][bold]{s23}[/bold][/italic]', style="#7B68EE")
    console.print(f'[italic][bold]{s24}[/bold][/italic]', style="#7B68EE")
    console.print(f'[italic][bold]{s25}[/bold][/italic]', style="#7B68EE") 