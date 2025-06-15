# Port-Phantom - Network Security Scanner

Port-Phantom is a powerful tool for scanning and monitoring local networks with device discovery, classification, and security risk assessment capabilities.

## 🚀 Features

- **Automatic subnet detection** - automatically determines local subnet
- **Device scanning** - finds active devices on the network
- **Manufacturer identification** - identifies devices by MAC addresses
- **Port scanning** - checks open ports on devices
- **Device classification** - determines device type by ports and manufacturer
- **Risk assessment** - calculates risk level based on signatures and port configuration
- **Scan comparison** - compares current scan with previous scans
- **Result export** - saves results in JSON and CSV formats
- **Telegram notifications** - sends results via Telegram
- **CLI interface** - convenient command-line interface with multiple options
- **Real-time monitoring** - continuous network monitoring capabilities
- **Custom signatures** - user-defined device signatures and patterns
- **Historical analysis** - track network changes over time

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Port-Phantom.git
cd Port-Phantom
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download OUI database (optional):
```bash
python3 download_db.py
```

## 🛠 Usage

### Basic Usage

```bash
python3 main.py
```

### CLI Options

#### Network Options
- `-s, --subnet SUBNET` - specify subnet to scan (default: auto-detect)
- `--ports PORTS` - comma-separated list of ports to scan
- `--timeout TIMEOUT` - host timeout in milliseconds (default: 50)

#### Output Options
- `--export {json,csv,both}` - export results in specified format
- `--output-dir DIR` - directory to save reports (default: history)
- `--no-save` - do not save scan results to files

#### Feature Toggles
- `--no-telegram` - disable Telegram notifications
- `--no-signatures` - skip signature matching
- `--no-comparison` - skip comparison with previous scans
- `--compare-only` - only compare with previous scan, do not scan network

#### Display Options
- `-v, --verbose` - enable verbose output
- `--no-banner` - do not display banner
- `--quiet` - minimal output (errors only)

#### Advanced Options
- `--oui-file FILE` - path to custom OUI database file
- `--signatures-file FILE` - path to custom signatures file
- `--telegram-user TELEGRAM_USER` - custom Telegram user ID for notifications

### Usage Examples

```bash
# Scan with default settings
python3 main.py

# Scan specific subnet
python3 main.py -s 192.168.1.0/24

# Disable Telegram notifications
python3 main.py --no-telegram

# Export results in CSV
python3 main.py --export csv

# Only compare with previous scan
python3 main.py --compare-only

# Verbose output
python3 main.py --verbose

# Scan only specific ports
python3 main.py --ports 22,80,443

# Minimal output without banner
python3 main.py --no-banner --quiet

# Export in both formats
python3 main.py --export both

# Custom OUI database
python3 main.py --oui-file /path/to/custom/oui.txt
```

## 📁 Project Structure

```
Port-Phantom/
├── main.py                 # Main entry point with CLI
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
├── download_db.py         # OUI database download script
├── src/                   # Source code
│   ├── config/           # Configuration
│   │   ├── settings.py   # Application settings
│   │   └── signature_loader.py  # Signature loading
│   ├── scanners/         # Scanners
│   │   ├── network_scanner.py   # Network scanning
│   │   ├── port_scanner.py      # Port scanning
│   │   └── mac_scanner.py       # MAC scanning
│   ├── classifiers/      # Classifiers
│   │   ├── device_classifier.py # Device classification
│   │   └── signature_matcher.py # Signature matching
│   ├── core/            # Core logic
│   │   ├── device_processor.py  # Device processing
│   │   └── risk_assessor.py     # Risk assessment
│   ├── reports/         # Reports
│   │   ├── report_generator.py  # Report generation
│   │   └── scan_comparator.py   # Scan comparison
│   └── utils/           # Utilities
│       ├── banner.py           # Banner display
│       └── telegram_sender.py  # Telegram sending
├── config/              # Configuration files
│   └── signatures.yaml  # Device signatures
├── data/               # Data
│   └── oui.txt         # OUI database (optional)
├── history/            # Scan history
└── exportable_reports/ # Exportable reports
```

## ⚙️ Configuration

### Telegram Settings

Edit `src/config/settings.py`:

```python
TELEGRAM_BOT_TOKEN = "your_bot_token_here"
AUTHORIZED_USER_ID = your_user_id_here
```

### Custom Signatures

Create `config/signatures.yaml`:

```yaml
signatures:
  - name: "Router"
    description: "Network router device"
    conditions:
      manufacturer: ["TP-Link", "Cisco", "ASUS"]
      ports: [80, 443]
    cve_info: "Router-specific vulnerabilities"
```

## 📊 Output Formats

### JSON Format
```json
{
  "ip": "192.168.1.1",
  "mac": "AA:BB:CC:DD:EE:FF",
  "manufacturer": "TP-Link",
  "open_ports": ["80", "443"],
  "device_type": ["router"],
  "score": 5,
  "level": "Medium"
}
```

### CSV Format
```csv
ip,mac,manufacturer,open_ports,device_type,score,level
192.168.1.1,AA:BB:CC:DD:EE:FF,TP-Link,"80, 443",router,5,Medium
```

## 🔧 Requirements

- Python 3.7+
- nmap
- requests
- rich
- pyyaml

## 📝 License

This project is for educational purposes only. Use responsibly.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Create a Pull Request

## 📞 Contact

- GitHub: https://github.com/anonymmized

---

**Disclaimer**: This tool is for educational purposes only. Use responsibly and only on networks you own or have permission to test.