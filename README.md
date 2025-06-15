# Port-Phantom v1.0

Network Security Scanner for discovering and monitoring devices on local networks.

## Features

- Scans local networks to discover devices
- Identifies devices by MAC address and manufacturer
- Checks open ports and classifies device types
- Calculates risk levels based on signatures and port configurations
- Compares current scan with previous scans to detect changes
- Saves results in JSON and CSV formats
- Supports multiple subnets and historical data tracking
- Telegram integration for notifications

## Project Structure

```
Port-Phantom/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/                   # Source code
│   ├── __init__.py
│   ├── config/           # Configuration modules
│   │   ├── __init__.py
│   │   ├── settings.py   # Application settings
│   │   └── signature_loader.py
│   ├── core/             # Core functionality
│   │   ├── __init__.py
│   │   ├── device_processor.py
│   │   └── risk_assessor.py
│   ├── scanners/         # Network scanning
│   │   ├── __init__.py
│   │   ├── network_scanner.py
│   │   ├── port_scanner.py
│   │   └── mac_scanner.py
│   ├── classifiers/      # Device classification
│   │   ├── __init__.py
│   │   ├── device_classifier.py
│   │   └── signature_matcher.py
│   ├── reports/          # Report generation
│   │   ├── __init__.py
│   │   ├── report_generator.py
│   │   └── scan_comparator.py
│   └── utils/            # Utilities
│       ├── __init__.py
│       ├── banner.py
│       ├── telegram_sender.py
│       └── oui_loader.py
├── config/               # Configuration files
│   └── signatures.yaml   # Device signatures
├── data/                 # Data files
│   └── oui.txt          # OUI database
├── history/              # Scan history (auto-created)
├── exportable_reports/   # Reports for Telegram (auto-created)
├── tests/                # Test files
└── docs/                 # Documentation
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Port-Phantom
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install nmap (required for network scanning):
   - **macOS**: `brew install nmap`
   - **Ubuntu/Debian**: `sudo apt-get install nmap`
   - **CentOS/RHEL**: `sudo yum install nmap`

## Usage

Run the main scanner:
```bash
python main.py
```

The tool will:
1. Automatically detect your local subnet
2. Download OUI database if needed
3. Scan for active devices
4. Identify device types and manufacturers
5. Calculate risk scores
6. Compare with previous scans
7. Save results and send via Telegram

## Configuration

### Telegram Bot Setup

1. Create a bot via @BotFather on Telegram
2. Get your bot token and user ID
3. Update the following variables in `src/config/settings.py`:
   - `TELEGRAM_BOT_TOKEN`: Your bot token
   - `AUTHORIZED_USER_ID`: Your Telegram user ID

### Signatures

Edit `config/signatures.yaml` to customize device detection rules and risk assessment.

### Settings

Modify `src/config/settings.py` to adjust:
- Network scanning parameters
- Risk assessment rules
- Device classification rules
- File paths

## Modules

### Core Modules
- **DeviceProcessor**: Main device processing logic
- **RiskAssessor**: Risk calculation and assessment

### Scanners
- **NetworkScanner**: Network discovery and host scanning
- **PortScanner**: Port scanning and HTTP header analysis
- **MACScanner**: MAC address detection and OUI processing

### Classifiers
- **DeviceClassifier**: Device type classification
- **SignatureMatcher**: Signature matching and CVE detection

### Reports
- **ReportGenerator**: Report generation and file management
- **ScanComparator**: Scan comparison and change detection

### Utils
- **Banner**: Application banner display
- **TelegramSender**: Telegram integration
- **OUILoader**: OUI database management

## Output

Results are saved in:
- `history/` - Scan history and device reports
- `exportable_reports/` - Reports sent via Telegram

## Development

### Adding New Features

1. Create new modules in appropriate directories
2. Update `__init__.py` files with exports
3. Add imports to `main.py`
4. Update documentation

### Testing

Run tests (when implemented):
```bash
python -m pytest tests/
```

## Disclaimer

This tool is for educational purposes only. Use responsibly and only on networks you own or have permission to scan.

## License

© 2025 Port-Phantom Team