"""Pydantic models for API"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ThreatDetectionRequest(BaseModel):
    """Request for threat detection"""
    event_type: str
    source_ip: str
    username: Optional[str] = None
    failed_attempts: Optional[int] = None
    timestamp: datetime
    domain: Optional[str] = None


class ThreatResponse(BaseModel):
    """Response for threat detection"""
    is_threat: bool
    threat_type: str
    severity: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    details: Dict[str, Any]
    timestamp: datetime


class AnomalyDetectionRequest(BaseModel):
    """Request for anomaly detection"""
    data: Dict[str, Any]


class AnomalyResponse(BaseModel):
    """Response for anomaly detection"""
    is_anomaly: bool
    anomaly_score: float
    threshold: float
    model_type: str
    timestamp: datetime


class IncidentRequest(BaseModel):
    """Request to create incident"""
    title: str
    description: str
    severity: str
    source_ip: Optional[str] = None
    affected_systems: List[str] = []


class IncidentResponse(BaseModel):
    """Response for incident creation"""
    incident_id: str
    status: str
    created_at: datetime


class VulnerabilityScanRequest(BaseModel):
    """Request for vulnerability scan"""
    targets: List[str]
    scan_type: str = "full"
    priority: str = "normal"
