import os
import requests
from dotenv import load_dotenv

from .models import SensorData

load_dotenv()

class PurpleAirClient:
    BASE_URL = "https://api.purpleair.com/v1"

    def __init__(self):
        self.api_key = os.getenv("PURPLEAIR_API_KEY")
        if not self.api_key:
            raise ValueError("API Key no encontrada en variables de entorno")

    def get_sensor(self, sensor_id: int):
        url = f"{self.BASE_URL}/sensors/{sensor_id}"
        headers = {"X-API-Key": self.api_key}
        response = requests.get(url, headers=headers)
        data = response.json().get("sensor", {})

        if response.status_code != 200:
            raise Exception(f"Error en la API: {response.status_code} - {response.text}")

        return SensorData(
            sensor_id=data.get("sensor_index"),
            name=data.get("name"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            temperature=data.get("temperature"),
            humidity=data.get("humidity"),
            preassure=data.get("pressure"),
            pm2_5=data.get("pm2.5"),
            confidence=data.get("confidence"),
            last_seen=data.get("last_seen")  
        )
