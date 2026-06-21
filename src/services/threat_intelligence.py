"""Threat intelligence aggregation service"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ThreatIntelligence:
    """Threat intelligence feed aggregation"""

    def __init__(self):
        self.known_threats = set()
        self.ioc_database = {}
        self.feeds = []

    async def initialize(self):
        """Initialize threat intelligence feeds"""
        logger.info("Initializing threat intelligence...")
        
        # Load known malicious IPs (dummy data for demo)
        self.known_threats = {
            "192.0.2.1",
            "198.51.100.1", 
            "203.0.113.1"
        }
        
        self.feeds = [
            {"name": "MITRE ATT&CK", "status": "active"},
            {"name": "AlienVault OTX", "status": "active"},
            {"name": "Abuse.ch", "status": "active"}
        ]
        
        logger.info(f"Loaded {len(self.known_threats)} known threats")

    async def check_ioc(
        self,
        ip: Optional[str] = None,
        domain: Optional[str] = None
    ) -> bool:
        """Check if IP or domain is in threat intelligence"""
        if ip and ip in self.known_threats:
            logger.warning(f"Threat intelligence match: {ip}")
            return True
        
        if domain and domain in self.known_threats:
            logger.warning(f"Threat intelligence match: {domain}")
            return True
        
        return False

    async def get_active_feeds(self) -> List[Dict[str, str]]:
        """Get list of active threat intelligence feeds"""
        return self.feeds

    async def submit_ioc(
        self,
        ioc_type: str,
        value: str,
        confidence: float
    ) -> Dict[str, Any]:
        """Submit Indicator of Compromise"""
        self.ioc_database[value] = {
            "type": ioc_type,
            "confidence": confidence,
            "submitted_at": datetime.utcnow()
        }
        
        logger.info(f"IOC submitted: {ioc_type} = {value}")
        
        return {
            "status": "submitted",
            "ioc_type": ioc_type,
            "value": value
        }
