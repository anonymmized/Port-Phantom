# Port-Phantom CLI Usage Guide

## Quick Start

```bash
# Basic scan
python3 main.py

# Scan specific subnet
python3 main.py -s 192.168.1.0/24

# Scan only specific ports
python3 main.py --ports 22,80,443
```

## Common Use Cases

### 1. Quick Network Assessment
```bash
python3 main.py --no-banner --quiet
```

### 2. Detailed Analysis with Export
```bash
python3 main.py --verbose --export both
```

### 3. Check for Network Changes
```bash
python3 main.py --compare-only
```

### 4. Silent Operation (No Notifications)
```bash
python3 main.py --no-telegram --no-banner --quiet
```

### 5. Custom Port Scan
```bash
python3 main.py --ports 21,22,23,80,443,3389
```

### 6. Export Results Only
```bash
python3 main.py --export csv --no-telegram --no-comparison
```

## Command Line Options

### Network Options
- `-s, --subnet SUBNET` - Target subnet (default: auto-detect)
- `--ports PORTS` - Comma-separated port list
- `--timeout TIMEOUT` - Host timeout in ms (default: 50)

### Output Options
- `--export {json,csv,both}` - Export format
- `--output-dir DIR` - Output directory (default: history)
- `--no-save` - Don't save results

### Feature Toggles
- `--no-telegram` - Disable Telegram notifications
- `--no-signatures` - Skip signature matching
- `--no-comparison` - Skip comparison with previous scans
- `--compare-only` - Only compare, don't scan

### Display Options
- `-v, --verbose` - Verbose output
- `--no-banner` - Hide banner
- `--quiet` - Minimal output

### Advanced Options
- `--oui-file FILE` - Custom OUI database
- `--signatures-file FILE` - Custom signatures file
- `--telegram-user ID` - Custom Telegram user ID

## Examples

```bash
# Full scan with all features
python3 main.py

# Quick scan without notifications
python3 main.py --no-telegram --no-banner

# Export to CSV only
python3 main.py --export csv --no-telegram

# Verbose scan of specific ports
python3 main.py --verbose --ports 22,80,443

# Compare with previous scan only
python3 main.py --compare-only

# Silent operation
python3 main.py --quiet --no-banner --no-telegram

# Custom configuration
python3 main.py --oui-file /path/to/oui.txt --signatures-file /path/to/signatures.yaml
```

## Output Files

- `history/scan_*.json` - Full scan results
- `history/*_device.csv` - Individual device CSV reports
- `history/*_device.json` - Individual device JSON reports
- `exportable_reports/scan_*.json` - Telegram export files 