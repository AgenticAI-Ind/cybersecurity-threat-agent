"""
Cybersecurity Threat Detection Agent
Real-time threat detection with ML-powered anomaly detection
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Optional
from datetime import datetime
import logging

from config import settings
from models.schemas import (
    ThreatDetectionRequest, ThreatResponse,
    AnomalyDetectionRequest, AnomalyResponse,
    IncidentRequest, IncidentResponse,
    VulnerabilityScanRequest
)
from services.anomaly_detector import AnomalyDetector
from services.threat_intelligence import ThreatIntelligence
from services.siem_integrator import SIEMIntegrator
from services.incident_responder import IncidentResponder

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global services
anomaly_detector = None
threat_intel = None
siem = None
incident_responder = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup services"""
    global anomaly_detector, threat_intel, siem, incident_responder

    logger.info("Starting Cybersecurity Threat Detection Agent...")

    # Initialize services
    anomaly_detector = AnomalyDetector(
        model_type=settings.ANOMALY_MODEL,
        threshold=settings.ANOMALY_THRESHOLD
    )
    await anomaly_detector.initialize()

    threat_intel = ThreatIntelligence()
    await threat_intel.initialize()

    siem = SIEMIntegrator(
        host=settings.ELASTICSEARCH_HOST,
        port=settings.ELASTICSEARCH_PORT
    )
    await siem.connect()

    incident_responder = IncidentResponder(
        auto_response=settings.AUTO_RESPONSE_ENABLED
    )
    await incident_responder.initialize()

    logger.info("All services initialized successfully")

    yield

    # Cleanup
    logger.info("Shutting down...")
    if siem:
        await siem.disconnect()


app = FastAPI(
    title="Cybersecurity Threat Detection Agent",
    description="Real-time threat detection with ML-powered anomaly detection",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Cybersecurity Threat Detection Agent",
        "status": "running",
        "version": "1.0.0",
        "features": [
            "Anomaly Detection",
            "Threat Intelligence",
            "SIEM Integration",
            "Incident Response",
            "Vulnerability Scanning"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "siem": "connected" if siem and siem.is_connected() else "disconnected",
        "threat_intel": "active" if threat_intel else "inactive",
        "anomaly_detector": "ready" if anomaly_detector else "not ready",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/threats/detect", response_model=ThreatResponse)
async def detect_threat(request: ThreatDetectionRequest):
    """
    Analyze event for potential threats

    Uses ML models and threat intelligence to detect malicious activity
    """
    try:
        # Check against threat intelligence
        threat_match = await threat_intel.check_ioc(
            ip=request.source_ip,
            domain=getattr(request, 'domain', None)
        )

        # Perform anomaly detection
        is_anomaly = await anomaly_detector.detect(request.dict())

        # Determine if threat
        is_threat = threat_match or is_anomaly

        if is_threat:
            # Create incident automatically
            await incident_responder.create_incident(
                title=f"Threat detected: {request.event_type}",
                source_ip=request.source_ip,
                severity="high" if threat_match else "medium"
            )

            # Send to SIEM
            await siem.send_event({
                "type": "threat_detected",
                "event": request.dict(),
                "threat_intelligence": threat_match,
                "anomaly": is_anomaly
            })

        return ThreatResponse(
            is_threat=is_threat,
            threat_type="known_malicious" if threat_match else "anomalous_behavior",
            severity="critical" if threat_match and is_anomaly else "high" if threat_match else "medium",
            confidence=0.95 if threat_match else 0.75,
            details={
                "threat_intelligence_match": bool(threat_match),
                "anomaly_detected": is_anomaly,
                "mitre_tactics": ["TA0001"] if is_threat else []
            },
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        logger.error(f"Error detecting threat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/threats/active")
async def get_active_threats():
    """Get list of active threats"""
    try:
        threats = await incident_responder.get_active_incidents()
        return {
            "active_threats": threats,
            "count": len(threats),
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/anomaly/detect", response_model=AnomalyResponse)
async def detect_anomaly(request: AnomalyDetectionRequest):
    """Detect anomalies in data using ML models"""
    try:
        is_anomaly = await anomaly_detector.detect(request.data)
        score = await anomaly_detector.get_anomaly_score(request.data)

        return AnomalyResponse(
            is_anomaly=is_anomaly,
            anomaly_score=score,
            threshold=settings.ANOMALY_THRESHOLD,
            model_type=settings.ANOMALY_MODEL,
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/anomaly/train")
async def train_anomaly_model(
    data_source: str,
    features: List[str],
    algorithm: str = "isolation_forest"
):
    """Train anomaly detection model"""
    try:
        result = await anomaly_detector.train(
            data_source=data_source,
            features=features,
            algorithm=algorithm
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/siem/events")
async def send_siem_event(event: dict):
    """Send security event to SIEM"""
    try:
        await siem.send_event(event)
        return {"status": "sent", "event_id": event.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/siem/query")
async def query_siem(
    query: str,
    time_range: str = "1h",
    limit: int = 100
):
    """Query SIEM for security events"""
    try:
        results = await siem.query(query, time_range, limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/incidents/create", response_model=IncidentResponse)
async def create_incident(request: IncidentRequest):
    """Create security incident"""
    try:
        incident = await incident_responder.create_incident(
            title=request.title,
            description=request.description,
            severity=request.severity,
            source_ip=request.source_ip,
            affected_systems=request.affected_systems
        )
        return incident
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/incidents/{incident_id}/respond")
async def respond_to_incident(
    incident_id: str,
    playbook: str,
    auto_remediate: bool = False
):
    """Execute incident response playbook"""
    try:
        result = await incident_responder.execute_playbook(
            incident_id=incident_id,
            playbook=playbook,
            auto_remediate=auto_remediate
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/incidents/{incident_id}/status")
async def get_incident_status(incident_id: str):
    """Get incident status"""
    try:
        status = await incident_responder.get_incident_status(incident_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Incident not found: {incident_id}")


@app.post("/vulnerabilities/scan")
async def scan_vulnerabilities(
    request: VulnerabilityScanRequest,
    background_tasks: BackgroundTasks
):
    """Start vulnerability scan"""
    try:
        scan_id = f"scan_{datetime.utcnow().timestamp()}"
        background_tasks.add_task(run_vulnerability_scan, scan_id, request)
        return {
            "scan_id": scan_id,
            "status": "started",
            "targets": request.targets
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def run_vulnerability_scan(scan_id: str, request: VulnerabilityScanRequest):
    """Background task for vulnerability scanning"""
    logger.info(f"Running vulnerability scan: {scan_id}")
    # Placeholder for actual vulnerability scanning logic


@app.get("/threat-intel/feeds")
async def get_threat_intel_feeds():
    """Get threat intelligence feeds"""
    try:
        feeds = await threat_intel.get_active_feeds()
        return feeds
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/threat-intel/ioc")
async def submit_ioc(
    ioc_type: str,
    value: str,
    confidence: float = 0.8
):
    """Submit Indicator of Compromise"""
    try:
        result = await threat_intel.submit_ioc(ioc_type, value, confidence)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    return {
        "threats_detected": await incident_responder.get_threats_count(),
        "anomalies_detected": await anomaly_detector.get_anomalies_count(),
        "incidents_active": len(await incident_responder.get_active_incidents()),
        "siem_events_sent": await siem.get_events_count() if siem else 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
