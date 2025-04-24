from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fetches the lat & lon coordinates from an API
def get_lat_lon(zip_code: str, country_code: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "postalcode": zip_code,
        "country": country_code,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "zip-to-coords-script"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return {"lat": float(lat), "lon": float(lon)}
    return {"error": "Location not found"}

# Returns the lat and lon coordinates for a given zip & country code
# E.g /location?zip_code=2040&country_code=HU
@app.get("/location")
def get_location(zip_code: str = Query(...), country_code: str = Query(...)):
    coords = get_lat_lon(zip_code, country_code)
    return JSONResponse(content=coords)

# Heartbeat to check if the service is reachable
@app.get("/heartbeat")
def get_heartbeat():
    return {"status":"hb_ok"}


@app.get("/fetch")
def fetch_weather(lat: str = Query(...), lon: str = Query(...)):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=sunshine_duration,precipitation_sum&timezone=auto"
    response = requests.get(url)
    return response.json()
