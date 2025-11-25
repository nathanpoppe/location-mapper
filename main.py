from geopy.geocoders import Nominatim
import time
import csv

def get_location_info(addresses):
    geolocator = Nominatim(user_agent="address_to_postalcode")
    results = []

    for addr in addresses:
        try:
            location = geolocator.geocode(addr + ", Winnipeg, Manitoba, Canada", addressdetails=True, timeout=10)
            if location and location.raw.get("address"):
                addr_info = location.raw["address"]
                results.append({
                    "input_address": addr,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "postal_code": addr_info.get("postcode"),
                    "city": addr_info.get("city") or addr_info.get("town") or addr_info.get("village"),
                    "province/state": addr_info.get("state"),
                    "country": addr_info.get("country"),
                })
            else:
                results.append({"input_address": addr, "error": "Not found"})
        except Exception as e:
            results.append({"input_address": addr, "error": str(e)})
        
        # polite delay for free service
        time.sleep(1)
    return results


if __name__ == "__main__":
    addresses = [
        "64 Aspen Forest Point",
        "38 Lake Forest Road",
        "15 Prominence Point",
        "31 Prominence Point",
        "51 Prominence Point",
        "54 Prominence Point",
        "58 Prominence Point",
        "27 Clovercrest Bay",
        "107 Bridlewood Road",
        "2 Ashgrove Point",
        "15 Edington Point",
        "19 Edington Point",
        "31 Forest Creek Road",
        "53 Oak Lawn Road",
        "65 Oak Lawn Road",
        "85 Oak Lawn Road",
        "233 Oak Lawn Road",
        "124 North Town Road",
        "176 North Town Road",
        "520 Bridgeland Drive North",
        "127 Park Valley Road",
        "145 Park Valley Road",
        "149 Park Valley Road",
        "153 Park Valley Road",
        "159 Park Valley Road",
        "169 Park Valley Road",
        "185 Park Valley Road",
        "58 Highland Creek Road",
        "125 Highland Creek Road",
        "157 Highland Creek Road",
        "184 Highland Creek Road",
        "188 Highland Creek Road"
    ]

    info = get_location_info(addresses)

    # Write results to a CSV file
    with open("address_results.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=info[0].keys())
        writer.writeheader()
        writer.writerows(info)

    print("Results written to address_results.csv")
