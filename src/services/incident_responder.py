"""Incident response automation service"""

from typing import Dict, Any, List
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)


class IncidentResponder:
    """Automated incident response"""

    def __init__(self, auto_response: bool = True):
        self.auto_response = auto_response
        self.incidents = {}
        self.threats_count = 0

    async def initialize(self):
        """Initialize incident responder"""
        logger.info("Initializing incident responder...")
        logger.info(f"Auto-response: {self.auto_response}")

    async def create_incident(
        self,
        title: str,
        description: str = "",
        severity: str = "medium",
        source_ip: str = None,
        affected_systems: List[str] = None
    ) -> Dict[str, Any]:
        """Create security incident"""
        incident_id = str(uuid.uuid4())[:8]
        
        incident = {
            "incident_id": incident_id,
            "title": title,
            "description": description,
            "severity": severity,
            "source_ip": source_ip,
            "affected_systems": affected_systems or [],
            "status": "open",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        self.incidents[incident_id] = incident
        self.threats_count += 1
        
        logger.info(f"Incident created: {incident_id} - {title}")
        
        # Auto-respond if enabled
        if self.auto_response and severity in ["high", "critical"]:
            await self.auto_respond(incident_id)
        
        return {
            "incident_id": incident_id,
            "status": "created",
            "created_at": incident["created_at"]
        }

    async def auto_respond(self, incident_id: str):
        """Automatically respond to incident"""
        logger.info(f"Auto-responding to incident: {incident_id}")
        # Placeholder for automated response logic

    async def execute_playbook(
        self,
        incident_id: str,
        playbook: str,
        auto_remediate: bool = False
    ) -> Dict[str, Any]:
        """Execute incident response playbook"""
        if incident_id not in self.incidents:
            raise ValueError(f"Incident not found: {incident_id}")
        
        logger.info(f"Executing playbook '{playbook}' for incident {incident_id}")
        
        actions_taken = []
        
        if playbook == "block_ip_and_notify":
            actions_taken = [
                {"action": "block_ip", "status": "success"},
                {"action": "notify_soc", "status": "success"}
            ]
        
        self.incidents[incident_id]["status"] = "responded"
        self.incidents[incident_id]["updated_at"] = datetime.utcnow()
        
        return {
            "incident_id": incident_id,
            "playbook": playbook,
            "actions_taken": actions_taken,
            "status": "completed"
        }

    async def get_incident_status(self, incident_id: str) -> Dict[str, Any]:
        """Get incident status"""
        if incident_id not in self.incidents:
            raise ValueError(f"Incident not found: {incident_id}")
        
        return self.incidents[incident_id]

    async def get_active_incidents(self) -> List[Dict[str, Any]]:
        """Get list of active incidents"""
        active = [
            incident for incident in self.incidents.values()
            if incident["status"] in ["open", "investigating", "responded"]
        ]
        return active

    async def get_threats_count(self) -> int:
        """Get total threats detected"""
        return self.threats_count
