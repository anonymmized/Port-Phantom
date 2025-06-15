"""
Risk assessment and scoring
"""

from typing import Dict, Any
from rich.console import Console

from ..config.settings import settings

console = Console()


class RiskAssessor:
    """Risk assessment and scoring"""
    
    @staticmethod
    def calculate_risk_score(device: Dict[str, Any]) -> int:
        """Calculate risk score for a device"""
        risk_score = 0
        manufacturer = device.get("manufacturer", "").strip()
        open_ports = list(map(int, device.get("open ports", [])))

        # Add port-based risk
        for port in open_ports:
            risk_score += settings.RISK_RULES['ports'].get(port, 1)
        
        # Add manufacturer-based risk
        if manufacturer in settings.RISK_RULES['manufacturers']:
            risk_score += settings.RISK_RULES['manufacturers'][manufacturer]

        return risk_score
    
    @staticmethod
    def get_risk_level(score: int) -> str:
        """Get risk level based on score"""
        if score >= 10:
            return "High"
        elif score >= 5:
            return "Medium"
        elif score > 0:
            return "Low"
        else:
            return "None"
    
    @classmethod
    def assess_device_risk(cls, device: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk for a device and add risk data"""
        risk_score = cls.calculate_risk_score(device)
        risk_level = cls.get_risk_level(risk_score)
        
        device['score'] = risk_score
        device['level'] = risk_level
        
        return device 