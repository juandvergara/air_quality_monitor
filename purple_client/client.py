import os
import requests
from dotenv import load_dotenv

from .models import SensorData

load_dotenv()

class PurpleAirClient:
    BASE_URL = "https://api.purpleair.com/v1"

    def __init__(self):
        self.api_key = os.getenv("PURPLEAIR_API_KEY")
        self.headers = {"X-API-Key": self.api_key}
        if not self.api_key:
            raise ValueError("API Key no encontrada en variables de entorno")
    
    def _handle_response(self, response):
        if response.status_code != 200:
            raise Exception(f"Error en la API: {response.status_code} - {response.text}")
        return response.json()
    
    def get_sensor(self, sensor_id: int):
        """
        Obtiene los datos de un sensor específico por su ID.
        
        Args: 
            :param sensor_id: ID del sensor a consultar.
        
        Returns:
            Un objeto SensorData con la información del sensor.
        """
        url = f"{self.BASE_URL}/sensors/{sensor_id}"
        response = requests.get(url, headers=self.headers)
        data = response.json().get("sensor", {})

        self._handle_response(response)

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
    
    def get_sensors(self, bounds: dict):
        """
        Obtiene una lista de sensores dentro de los límites especificados.
        :param bounds: Un diccionario con las coordenadas de los límites:
            {
                "nwlng": float,
                "nwlat": float,
                "selng": float,
                "selat": float
            }
        :return: Una lista de objetos SensorData con la información de los sensores.
        
        """
        url = f"{self.BASE_URL}/sensors"
        params = {
            'fields': 'sensor_index,name,latitude,longitude,temperature,humidity,pressure,pm2.5,confidence,last_seen',
            "nwlng": bounds["nwlng"],
            "nwlat": bounds["nwlat"],
            "selng": bounds["selng"],
            "selat": bounds["selat"]
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        data = response.json().get("data", [])
        fields = response.json().get("fields", [])

        self._handle_response(response)

        return [SensorData(
            sensor_id=sensor[fields.index("sensor_index")],
            name=sensor[fields.index("name")],
            latitude=sensor[fields.index("latitude")],
            longitude=sensor[fields.index("longitude")],
            temperature=sensor[fields.index("temperature")],
            humidity=sensor[fields.index("humidity")],
            preassure=sensor[fields.index("pressure")],
            pm2_5=sensor[fields.index("pm2.5")],
            confidence=sensor[fields.index("confidence")],
            last_seen=sensor[fields.index("last_seen")]
        ) for sensor in data]

    def get_sensor_history(self, sensor_id: int, start_timestamp: int, end_timestamp: int, average: int = 60):
        """
        Obtiene el histórico de un sensor específico.

        Args:
            sensor_id (int): ID del sensor.
            start_timestamp (int): Timestamp inicial (epoch seconds).
            end_timestamp (int): Timestamp final (epoch seconds).
            average (int): Intervalo de agregación en minutos (default 60 min).

        Returns:
            List[dict]: Lista de registros históricos con timestamp y valores medidos.
        """
        url = f"{self.BASE_URL}/sensors/{sensor_id}/history"
        params = {
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "average": average,
            "fields": "temperature,humidity,pm2.5_atm"

        }

        response = requests.get(url, headers=self.headers, params=params)
        self._handle_response(response)

        data = response.json()
        fields = data.get("fields", [])
        rows = data.get("data", [])

        history = []
        for row in rows:
            row_dict = {field: value for field, value in zip(fields, row)}
            history.append(row_dict)

        return history
