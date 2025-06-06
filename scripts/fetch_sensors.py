from purple_client.client import PurpleAirClient

bounds = {
    "nwlng": -74.15,
    "nwlat": 4.85,
    "selng": -74.00,
    "selat": 4.60,
}

client = PurpleAirClient()
data = client.get_sensors(bounds)

print(f"Total sensores encontrados: {len(data)}")
print("Ejemplo de datos:")
for i, sensor in enumerate(data):
    print(f"Sensor {i + 1}:")
    print(f"  ID: {sensor.sensor_id}")
    print(f"  Name: {sensor.name}")
    print(f"  Location: ({sensor.latitude}, {sensor.longitude})")
    print(f"  Temperature: {sensor.temperature}")
    print(f"  Humidity: {sensor.humidity}")
    print(f"  Pressure: {sensor.preassure}")
    print(f"  PM2.5: {sensor.pm2_5}")
    print(f"  Confidence: {sensor.confidence}")
    print(f"  Last Seen: {sensor.last_seen}")
    print()