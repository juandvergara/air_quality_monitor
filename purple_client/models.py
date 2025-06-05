from dataclasses import dataclass
from typing import Optional


@dataclass
class SensorData:
    sensor_id: int
    name: str
    latitude: float
    longitude: float
    temperature: Optional[float]
    humidity: Optional[float]
    preassure: Optional[float]
    pm2_5: Optional[float]
    confidence: Optional[int]
    last_seen: Optional[int]
