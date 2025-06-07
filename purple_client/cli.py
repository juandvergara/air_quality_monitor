import argparse
import json
from purple_client.client import PurpleAirClient

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

    # TODO: Upload command
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
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
