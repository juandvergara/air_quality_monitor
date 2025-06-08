from google.cloud import bigquery
from typing import List
from purple_client.models import SensorData  # Importa tu dataclass SensorData
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Parámetros de configuración
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET_ID")
TABLE_ID = os.getenv("BQ_TABLE_ID")

client = bigquery.Client(project=PROJECT_ID)

def upload_sensor_data(sensor_data_list: List[SensorData]):
    """Sube una lista de SensorData a BigQuery."""
    
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    print(f"Subiendo datos a BigQuery: {table_id}")
    table = client.get_table(table_id)

    rows_to_insert = []
    for sensor in sensor_data_list:
        row = {
            "sensor_id": sensor.sensor_id,
            "name": sensor.name,
            "latitude": sensor.latitude if sensor.latitude is not None else 0.0,
            "longitude": sensor.longitude if sensor.longitude is not None else 0.0,
            "temperature": sensor.temperature,
            "humidity": sensor.humidity,
            "pm2_5": sensor.pm2_5,
            "aqi": sensor.aqi,
            "timestamp": datetime.utcfromtimestamp(sensor.last_seen).isoformat() + "Z"
        }
        rows_to_insert.append(row)


    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",  # o "WRITE_TRUNCATE" si quieres reemplazar toda la tabla
        autodetect=True  # deja que infiera el esquema automáticamente
    )
    
    # Lanzar el load job desde json
    job = client.load_table_from_json(rows_to_insert, table_id, job_config=job_config)
    job.result()  # Espera a que termine

    print(f"✅ Subida exitosa: {len(rows_to_insert)} filas insertadas con load job.")