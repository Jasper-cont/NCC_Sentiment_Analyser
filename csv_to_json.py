import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    data = {}

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data[row['Symbol']] = row['Name']

    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file)

    print("CSV data converted to JSON successfully.")

if __name__ == "__main__":
    csv_path = "sdaq_screener_1691932979728.csv"   # Provide the path to your CSV file
    json_path = "company_ticker.json"  # Provide the desired path for the output JSON file
    csv_to_json(csv_path, json_path)
