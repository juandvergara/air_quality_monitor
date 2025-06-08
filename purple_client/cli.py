import argparse
import json
import csv
from datetime import datetime
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
    
def export_data(input_file, output_file, start_date=None, end_date=None, pm2_5_threshold=None):
    """Lee un archivo JSON de sensores, filtra por fecha/PM2.5, y exporta CSV."""
    # Cargar el JSON
    with open(input_file, "r") as f:
        data = json.load(f)

    # Preparar filtros
    def filter_row(row):
        # Filtro de fecha (last_seen es epoch timestamp)
        if start_date:
            start_ts = datetime.fromisoformat(start_date).timestamp()
            if row["last_seen"] < start_ts:
                return False
        if end_date:
            end_ts = datetime.fromisoformat(end_date).timestamp()
            print(f"Comparando {row['last_seen']} con {end_ts}")
            if row["last_seen"] > end_ts:
                print(f"Row {row['sensor_id']} filtered out by end date")
                return False
        # Filtro de PM2.5
        if pm2_5_threshold is not None and row["pm2_5"] is not None:
            if row["pm2_5"] < pm2_5_threshold:
                return False
        return True

    # Aplicar filtros
    filtered_data = [row for row in data if filter_row(row)]

    # Escribir CSV
    if filtered_data:
        fieldnames = filtered_data[0].keys()
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_data)

        print(f"✅ Exported {len(filtered_data)} rows to {output_file}")
    else:
        print("⚠️ No data matched the filters.")

def main():
    parser = argparse.ArgumentParser(description="PurpleAir CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Fetch command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch data from PurpleAir API")
    fetch_parser.add_argument("--nwlng", type=float, required=True, help="Northwest longitude of the bounding box")
    fetch_parser.add_argument("--nwlat", type=float, required=True, help="Northwest latitude of the bounding box")
    fetch_parser.add_argument("--selng", type=float, required=True, help="Southeast longitude of the bounding box")
    fetch_parser.add_argument("--selat", type=float, required=True, help="Southeast latitude of the bounding box")
    fetch_parser.add_argument("--output", type=str, default="output.json", help="Output file path")

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload data to BigQuery")
    upload_parser.add_argument("--input", type=str, required=True, help="Input file path (JSON)")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export filtered CSV")
    export_parser.add_argument("--input", type=str, required=True, help="Input JSON file")
    export_parser.add_argument("--output", type=str, required=True, help="Output CSV file")
    export_parser.add_argument("--start_date", type=str, help="Start date (YYYY-MM-DD)")
    export_parser.add_argument("--end_date", type=str, help="End date (YYYY-MM-DD)")
    export_parser.add_argument("--pm2_5_threshold", type=float, help="PM2.5 threshold")
    
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
    elif args.command == "export":
        export_data(
            input_file=args.input,
            output_file=args.output,
            start_date=args.start_date,
            end_date=args.end_date,
            pm2_5_threshold=args.pm2_5_threshold
        )
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
