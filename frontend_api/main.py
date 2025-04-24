from fastapi import FastAPI, Query
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


# Heartbeat to check if the service is reachable
@app.get("/heartbeat")
def get_heartbeat():
    return {"status":"hb_ok"}

@app.get("/summary")
def get_summary(zip_code: str = Query(...), country_code: str = Query(...)):
    resp = requests.get(f"http://nginx/analytics/process?zip_code={zip_code}&country_code={country_code}")
    return resp.json()


@app.get("/history")
def get_history():
    resp = requests.get(f"http://nginx/analytics/history")
    return resp.json()
