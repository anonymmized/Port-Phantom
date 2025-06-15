"""
Risk assessment and scoring
"""

from rich.console import Console

from ..config.settings import RISK_RULES

console = Console()


def calculate_risk_score(device):
    """Calculate risk score for a device"""
    risk_score = 0
    manufacturer = device.get("manufacturer", "").strip()
    open_ports = list(map(int, device.get("open ports", [])))

    # Add port-based risk
    for port in open_ports:
        risk_score += RISK_RULES['ports'].get(port, 1)
    
    # Add manufacturer-based risk
    if manufacturer in RISK_RULES['manufacturers']:
        risk_score += RISK_RULES['manufacturers'][manufacturer]

    return risk_score


def get_risk_level(score):
    """Get risk level based on score"""
    if score >= 10:
        return "High"
    elif score >= 5:
        return "Medium"
    elif score > 0:
        return "Low"
    else:
        return "None"


def assess_device_risk(device):
    """Assess risk for a device and add risk data"""
    risk_score = calculate_risk_score(device)
    risk_level = get_risk_level(risk_score)
    
    device['score'] = risk_score
    device['level'] = risk_level
    
    return device 