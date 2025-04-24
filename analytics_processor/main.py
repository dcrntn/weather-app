from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import psycopg2
import os
import time

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to PostgreSQL
def get_db_connection():
    max_retries = 10
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(os.getenv("DATABASE_URL"))
            return conn
        except psycopg2.OperationalError as e:
            print(f"[DB CONNECT] Attempt {i+1}/{max_retries} failed, retrying...")
            time.sleep(2)
    raise Exception("Could not connect to the database after several retries.")

# Initialize table on startup
@app.on_event("startup")
def startup_event():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            zip_code TEXT,
            country_code TEXT,
            lat DOUBLE PRECISION,
            lon DOUBLE PRECISION,
            start_date TEXT,
            end_date TEXT,
            avg_sunshine  DOUBLE PRECISION,
            avg_rain  DOUBLE PRECISION,
            needs_light BOOL,
            needs_water BOOL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# Heartbeat
@app.get("/heartbeat")
def get_heartbeat():
    return {"status": "hb_ok"}

# Process weather data and store in DB
@app.get("/process")
def process_weather(zip_code: str = Query(...), country_code: str = Query(...)):
    # Get coordinates
    loc_resp = requests.get(
        f"http://nginx/weather/location?zip_code={zip_code}&country_code={country_code}"
    )
    lat_lon = loc_resp.json()
    if "error" in lat_lon:
        return {"error": "Could not resolve coordinates"}

    # Fetch weather
    weather_resp = requests.get(
        f"http://nginx/weather/fetch?lat={lat_lon['lat']}&lon={lat_lon['lon']}"
    )
    weather_data = weather_resp.json()

    start_date = weather_data["daily"]['time'][0]
    end_date = weather_data["daily"]["time"][-1]

    sunshine_avg = sum(weather_data["daily"]["sunshine_duration"]) / len(weather_data["daily"]["sunshine_duration"])
    rain_avg = sum(weather_data["daily"]["precipitation_sum"]) / len(weather_data["daily"]["precipitation_sum"])

    needs_light = False
    if sunshine_avg < 20000:
        needs_light = True

    needs_water = False
    if rain_avg < 20:
        needs_water = True
    # Store in DB
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO weather_data (zip_code, country_code, lat, lon, start_date, end_date, avg_sunshine, avg_rain, needs_light, needs_water)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """,
        (zip_code, country_code, lat_lon['lat'], lat_lon['lon'], start_date, end_date, sunshine_avg, rain_avg, needs_light, needs_water)
    )
    conn.commit()
    cur.close()
    conn.close()

    return {"status": "success", "weather": weather_data}

# Read from DB
@app.get("/history")
def get_weather_history():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT zip_code, country_code, lat, lon, start_date, end_date, avg_sunshine, avg_rain, needs_light, needs_water, timestamp FROM weather_data ORDER BY timestamp DESC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    history = [
        {
            "zip_code": row[0],
            "country_code": row[1],
            "lat": row[2],
            "lon": row[3],
            "start_date": row[4],
            "end_date": row[5],
            "avg_sunshine": row[6],
            "avg_rain": row[7],
            "needs_light": row[8],
            "needs_water": row[9],
            "timestamp": row[10].isoformat()
        }
        for row in rows
    ]
    return {"history": history}
