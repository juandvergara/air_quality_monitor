from purple_client.client import PurpleAirClient

client = PurpleAirClient()
history = client.get_sensor_history(sensor_id=127373, start_timestamp=1717718400, end_timestamp=1717804800, average=60)

for row in history:
    print(row)
