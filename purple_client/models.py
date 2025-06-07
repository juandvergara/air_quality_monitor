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

    @property
    def aqi(self) -> Optional[int]:
        return self._AQI_from_pm2_5(self.pm2_5)

    def _AQI_from_pm2_5(self, pm2_5: float) -> int:
        """
        Determina el AQI basado en los rangos de PM2.5.
        """
        if pm2_5 > 350.5:
            return self._calculate_AQI(pm2_5, 500, 401, 500.4, 350.5)  # Hazardous
        elif pm2_5 > 250.5:
            return self._calculate_AQI(pm2_5, 400, 301, 350.4, 250.5)  # Hazardous
        elif pm2_5 > 150.5:
            return self._calculate_AQI(pm2_5, 300, 201, 250.4, 150.5)  # Very Unhealthy
        elif pm2_5 > 55.5:
            return self._calculate_AQI(pm2_5, 200, 151, 150.4, 55.5)  # Unhealthy
        elif pm2_5 > 35.5:
            return self._calculate_AQI(pm2_5, 150, 101, 55.4, 35.5)  # Unhealthy for Sensitive Groups
        elif pm2_5 > 12.1:
            return self._calculate_AQI(pm2_5, 100, 51, 35.4, 12.1)  # Moderate
        elif pm2_5 >= 0:
            return self._calculate_AQI(pm2_5, 50, 0, 12, 0)  # Good
        else:
            return -1

    def _calculate_AQI(self, Cp: float, Ih: int, Il: int, BPh: float, BPl: float) -> int:
        a = Ih - Il
        b = BPh - BPl
        c = Cp - BPl
        return round((a / b) * c + Il)
