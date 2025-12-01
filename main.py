import os
import sys
import csv
from dotenv import load_dotenv

from service.geocoding import GeocodingAPIClient

# Load environment variables from .env
load_dotenv()

def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_csv_file> <output_csv_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Initialize geocoding client
    api_key = os.getenv("GEOCODING_API_KEY")
    if not api_key:
        print("Error: GEOCODING_API_KEY not found in environment variables")
        sys.exit(1)
    
    client = GeocodingAPIClient(api_key)
    
    # Read input CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Process each row
    skipped = 0
    for i, row in enumerate(rows, 1):
        # Check if row already has geocoded data
        postal_code = row.get('Postal Code', '').strip()
        latitude = row.get('Latitude', '').strip()
        longitude = row.get('Longitude', '').strip()
        
        # Skip if all three fields are already filled
        if postal_code and latitude and longitude:
            skipped += 1
            print(f"Skipping {i}/{len(rows)}: Already geocoded")
            continue
        
        # Construct full address string
        address_parts = [
            row.get('Address', '').strip(),
            row.get('City', '').strip(),
            row.get('Province', '').strip(),
            row.get('Country', '').strip()
        ]
        address = ', '.join([part for part in address_parts if part])
        
        print(f"Processing {i}/{len(rows)}: {address}")
        
        try:
            # Geocode the address
            data = client.geocode(address)
            
            # Update row with geocoded data (only update if field is empty)
            if not postal_code:
                row['Postal Code'] = data.get('postal_code', '')
            if not latitude:
                row['Latitude'] = str(data.get('latitude', ''))
            if not longitude:
                row['Longitude'] = str(data.get('longitude', ''))
            
        except Exception as e:
            print(f"  Error geocoding address: {e}")
            # Only update empty fields if geocoding fails
            if not postal_code:
                row['Postal Code'] = ''
            if not latitude:
                row['Latitude'] = ''
            if not longitude:
                row['Longitude'] = ''
    
    # Write output CSV
    if rows:
        fieldnames = list(rows[0].keys())
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"\nResults written to {output_file}")
        if skipped > 0:
            print(f"Skipped {skipped} rows that were already geocoded")
    else:
        print("No rows to process")

if __name__ == "__main__":
    main()

