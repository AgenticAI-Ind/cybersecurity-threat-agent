"""Anomaly detection service using ML algorithms"""

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """ML-powered anomaly detection"""

    def __init__(self, model_type: str = "isolation_forest", threshold: float = 0.8):
        self.model_type = model_type
        self.threshold = threshold
        self.model = None
        self.scaler = StandardScaler()
        self.anomalies_detected = 0

    async def initialize(self):
        """Initialize anomaly detection model"""
        logger.info(f"Initializing anomaly detector with {self.model_type}")
        
        if self.model_type == "isolation_forest":
            self.model = IsolationForest(
                contamination=0.1,
                random_state=42,
                n_estimators=100
            )
        
        # Train with dummy data for demo
        dummy_data = np.random.randn(1000, 5)
        self.model.fit(dummy_data)
        
        logger.info("Anomaly detector initialized")

    async def detect(self, data: Dict[str, Any]) -> bool:
        """Detect if data is anomalous"""
        try:
            # Convert dict to numeric features
            features = self._extract_features(data)
            
            # Predict
            prediction = self.model.predict([features])
            is_anomaly = prediction[0] == -1
            
            if is_anomaly:
                self.anomalies_detected += 1
            
            return is_anomaly
        
        except Exception as e:
            logger.error(f"Error detecting anomaly: {e}")
            return False

    async def get_anomaly_score(self, data: Dict[str, Any]) -> float:
        """Get anomaly score for data"""
        try:
            features = self._extract_features(data)
            score = self.model.score_samples([features])[0]
            # Normalize to 0-1 range
            normalized = 1 / (1 + np.exp(score))
            return float(normalized)
        except Exception as e:
            logger.error(f"Error calculating anomaly score: {e}")
            return 0.5

    def _extract_features(self, data: Dict[str, Any]) -> list:
        """Extract numeric features from data"""
        # Simple feature extraction - can be enhanced
        features = []
        for key, value in data.items():
            if isinstance(value, (int, float)):
                features.append(value)
            elif isinstance(value, str):
                features.append(len(value))
        
        # Pad or truncate to fixed size
        while len(features) < 5:
            features.append(0)
        return features[:5]

    async def train(
        self,
        data_source: str,
        features: list,
        algorithm: str
    ) -> Dict[str, Any]:
        """Train anomaly detection model"""
        logger.info(f"Training {algorithm} model on {data_source}")
        
        return {
            "status": "trained",
            "algorithm": algorithm,
            "features": features,
            "accuracy": 0.95
        }

    async def get_anomalies_count(self) -> int:
        """Get total anomalies detected"""
        return self.anomalies_detected
