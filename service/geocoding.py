import requests
import pprint

class GeocodingAPIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def geocode(self, address: str) -> dict:
        """
        Takes a full address string and returns all associated geocoding info from the Google Maps Geocoding API.
        """

        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": self.api_key
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data["status"] != "OK":
            raise ValueError(f"Geocoding failed: {data['status']} - {data.get('error_message')}")

        result = data["results"][0]

        # Extract address components into a dictionary
        components = {}
        for comp in result["address_components"]:
            for comp_type in comp["types"]:
                components[comp_type] = comp["long_name"]

        geocoded_data = {
            "formatted_address": result.get("formatted_address"),
            "latitude": result["geometry"]["location"]["lat"],
            "longitude": result["geometry"]["location"]["lng"],
            "place_id": result.get("place_id"),
            "postal_code": components.get("postal_code"),
            "street_number": components.get("street_number"),
            "route": components.get("route"),
            "city": (
                components.get("locality")
                or components.get("postal_town")
                or components.get("administrative_area_level_2")
            ),
            "province_state": components.get("administrative_area_level_1"),
            "country": components.get("country"),
        }

        return geocoded_data