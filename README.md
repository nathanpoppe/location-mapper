# Location Mapper

A Python tool for geocoding addresses in CSV files using the Google Maps Geocoding API. This tool reads addresses from a CSV file, geocodes them to obtain postal codes, latitude, and longitude coordinates, and writes the results to an output CSV file.

## Features

- Geocodes addresses using Google Maps Geocoding API
- Automatically skips rows that are already geocoded (have postal code, latitude, and longitude)
- Only updates empty fields, preserving existing data
- Handles errors gracefully and continues processing remaining addresses
- Supports batch processing of large CSV files

## Prerequisites

- Python 3.7 or higher
- A Google Maps Geocoding API key
- `uv` package manager (for installing dependencies)

## Installation

1. **Install `uv`** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Install project dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

## Configuration

1. **Create a `.env` file** in the project root directory:
   ```bash
   touch .env
   ```

2. **Add your Google Maps Geocoding API key** to the `.env` file:
   ```
   GEOCODING_API_KEY=your_api_key_here
   ```

   You can obtain an API key from the [Google Cloud Console](https://console.cloud.google.com/). Make sure to enable the Geocoding API for your project.

## Usage

Run the script with an input CSV file and specify an output CSV file:

```bash
python3 main.py <input_csv_file> <output_csv_file>
```

### Example

```bash
python3 main.py addresses_sample.csv addresses_sample.csv
```

### Input CSV Format

The input CSV file should contain the following columns:
- `Address` - Street address
- `City` - City name
- `Province` - Province/State
- `Country` - Country name
- `Postal Code` - (Optional, will be filled if empty)
- `Latitude` - (Optional, will be filled if empty)
- `Longitude` - (Optional, will be filled if empty)

The script will:
- Skip rows that already have all three fields (Postal Code, Latitude, Longitude) populated
- Only update empty fields for rows that need geocoding
- Construct a full address string from the Address, City, Province, and Country columns

### Output

The script will:
- Process each row and display progress in the console
- Write the geocoded results to the output CSV file
- Preserve all original columns and data
- Display a summary of skipped rows (if any)

## Notes

- The script uses the Google Maps Geocoding API, which has usage limits and may incur costs depending on your usage tier
- Make sure your API key has the Geocoding API enabled in Google Cloud Console
- The script processes addresses sequentially and may take time for large CSV files
