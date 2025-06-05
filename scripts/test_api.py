from purple_client.client import PurpleAirClient

client = PurpleAirClient()
sensor_data = client.get_sensor(sensor_id=127373)  # Usa un ID real si tienes

print(sensor_data)
