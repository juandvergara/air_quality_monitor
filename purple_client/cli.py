import argparse
import json
from purple_client.client import PurpleAirClient
from purple_client.models import SensorData 
from bigquery_client.bigquery_client import upload_sensor_data

def upload_data(input_file):
    with open(input_file, "r") as f:
        data = json.load(f)

    sensor_data_list = []
    for sensor in data:
        sensor_data_list.append(
            SensorData(
                sensor_id=sensor["sensor_id"],
                name=sensor["name"],
                latitude=sensor["latitude"],
                longitude=sensor["longitude"],
                temperature=sensor["temperature"],
                humidity=sensor["humidity"],
                preassure=sensor["preassure"],
                pm2_5=sensor["pm2_5"],
                confidence=sensor["confidence"],
                last_seen=sensor["last_seen"],
                aqi=sensor["aqi"]
            )
        )
    upload_sensor_data(sensor_data_list)
    print(f"Uploaded {len(sensor_data_list)} sensors from {input_file} to BigQuery.")

def fetch_data(bounds, output_file):
    client = PurpleAirClient()
    sensors = client.get_sensors(bounds)
    print(type(sensors))
    data = [sensor.to_dict() for sensor in sensors]

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Fetched {len(data)} sensors and saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="PurpleAir CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Fetch command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch data from PurpleAir API")
    fetch_parser.add_argument("--nwlng", type=float, required=True)
    fetch_parser.add_argument("--nwlat", type=float, required=True)
    fetch_parser.add_argument("--selng", type=float, required=True)
    fetch_parser.add_argument("--selat", type=float, required=True)
    fetch_parser.add_argument("--output", type=str, default="output.json", help="Output file path")

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload data to BigQuery")
    upload_parser.add_argument("--input", type=str, required=True, help="Input file path (JSON)")

    # TODO: Export command

    args = parser.parse_args()

    if args.command == "fetch":
        bounds = {
            "nwlng": args.nwlng,
            "nwlat": args.nwlat,
            "selng": args.selng,
            "selat": args.selat
        }
        fetch_data(bounds, args.output)
    elif args.command == "upload":
        if not args.input.endswith(".json"):
            print("Error: Input file must be a JSON file.")
            return
        upload_data(args.input)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
