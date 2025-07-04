from dataclasses import dataclass
from typing import Optional


def _AQI_from_pm2_5(pm2_5: float) -> int:
        """
        Determina el AQI basado en los rangos de PM2.5.
        """
        if pm2_5 is None:
            return -1
        if pm2_5 > 350.5:
            return _calculate_AQI(pm2_5, 500, 401, 500.4, 350.5)  # Hazardous
        elif pm2_5 > 250.5:
            return _calculate_AQI(pm2_5, 400, 301, 350.4, 250.5)  # Hazardous
        elif pm2_5 > 150.5:
            return _calculate_AQI(pm2_5, 300, 201, 250.4, 150.5)  # Very Unhealthy
        elif pm2_5 > 55.5:
            return _calculate_AQI(pm2_5, 200, 151, 150.4, 55.5)  # Unhealthy
        elif pm2_5 > 35.5:
            return _calculate_AQI(pm2_5, 150, 101, 55.4, 35.5)  # Unhealthy for Sensitive Groups
        elif pm2_5 > 12.1:
            return _calculate_AQI(pm2_5, 100, 51, 35.4, 12.1)  # Moderate
        elif pm2_5 >= 0:
            return _calculate_AQI(pm2_5, 50, 0, 12, 0)  # Good
        else:
            return -1

def _calculate_AQI(Cp: float, Ih: int, Il: int, BPh: float, BPl: float) -> int:
        a = Ih - Il
        b = BPh - BPl
        c = Cp - BPl
        return round((a / b) * c + Il)

@dataclass
class SensorData:
    sensor_id: int
    name: str
    latitude: float
    longitude: float
    temperature: Optional[int]
    humidity: Optional[int]
    preassure: Optional[float]
    pm2_5: Optional[float]
    confidence: Optional[int]
    last_seen: Optional[int]
    aqi: int = None

    def __post_init__(self):
        self.aqi = _AQI_from_pm2_5(self.pm2_5)
    
    def to_dict(self):
        return {
            "sensor_id": self.sensor_id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "preassure": self.preassure,
            "pm2_5": self.pm2_5,
            "confidence": self.confidence,
            "last_seen": self.last_seen,
            "aqi": self.aqi
        }


@dataclass
class SensorHistory:
    sensor_id: int
    timestamp: int
    pm2_5: Optional[float]
    temperature: Optional[int]
    humidity: Optional[int]
    aqi: int = None

    def __post_init__(self):
        self.aqi = _AQI_from_pm2_5(self.pm2_5)