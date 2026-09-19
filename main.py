from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import sqlite3
import os

app = FastAPI(
    title="🌱 EcoTrack REST API",
    description="Экологиялық мониторинг, көміртек ізін (Carbon Footprint) есептеу, қоқыс өңдеу пункттері және эко-челлендждерге арналған толыққанды API жүйесі.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS настройкалары
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "ecotrack.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Ақылы қоқыс өңдеу және қайта тапсыру пункттері кестесі
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recycling_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            address TEXT NOT NULL,
            waste_types TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            contact TEXT
        )
    ''')
    
    # 2. Ауа сапасы индикаторлары
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS air_quality (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            aqi INTEGER NOT NULL,
            status TEXT NOT NULL,
            pm25 REAL,
            pm10 REAL,
            updated_at TEXT
        )
    ''')
    
    # 3. Эко Челлендждер
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eco_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            points INTEGER NOT NULL,
            category TEXT NOT NULL
        )
    ''')

    # Дефолттық мәліметтер
    cursor.execute("SELECT COUNT(*) FROM recycling_points")
    if cursor.fetchone()[0] == 0:
        points = [
            ("EkoKazakhstan Алматы", "Алматы", "Абай даңғылы 150", "Пластик, Әйнек, Қағаз", 43.238949, 76.889709, "+7 (777) 123-4567"),
            ("Taza Qala Астана", "Астана", "Мәңгілік Ел 28", "Электроника, Батарейкалар", 51.128207, 71.430411, "+7 (701) 987-6543"),
            ("EcoShymkent", "Шымкент", "Тауке хан 45", "Пластик, Металл", 42.315514, 69.596954, "+7 (702) 555-1122")
        ]
        cursor.executemany("INSERT INTO recycling_points (name, city, address, waste_types, latitude, longitude, contact) VALUES (?, ?, ?, ?, ?, ?, ?)", points)

    cursor.execute("SELECT COUNT(*) FROM air_quality")
    if cursor.fetchone()[0] == 0:
        aqi_data = [
            ("Алматы", 78, "Орташа (Moderate)", 24.5, 45.1, datetime.now().isoformat()),
            ("Астана", 35, "Жақсы (Good)", 10.2, 18.4, datetime.now().isoformat()),
            ("Шымкент", 52, "Орташа (Moderate)", 15.8, 30.2, datetime.now().isoformat()),
            ("Қарағанды", 112, "Зиянды (Unhealthy)", 42.1, 85.0, datetime.now().isoformat())
        ]
        cursor.executemany("INSERT INTO air_quality (city, aqi, status, pm25, pm10, updated_at) VALUES (?, ?, ?, ?, ?, ?)", aqi_data)

    cursor.execute("SELECT COUNT(*) FROM eco_challenges")
    if cursor.fetchone()[0] == 0:
        challenges = [
            ("Пластиксіз 1 күн", "Бүгін ешқандай бір реттік пластик шөлмек немесе пакет сатып алмаңыз.", 50, "Waste"),
            ("Эко-көлік күні", "Жұмысқа/оқуға қоғамдық көлікпен немесе велосипедпен барыңыз.", 100, "Transport"),
            ("Энергия үнемдеу", "Үйде пайдаланылмай тұрған электрониканы желіден ажыратыңыз.", 30, "Energy")
        ]
        cursor.executemany("INSERT INTO eco_challenges (title, description, points, category) VALUES (?, ?, ?, ?)", challenges)

    conn.commit()
    conn.close()

init_db()

# --- SCHEMAS ---
class CarbonCalculationRequest(BaseModel):
    transport_km: float = Field(..., description="Апталық көлік жүрісі (км)")
    transport_type: str = Field("car", description="Көлік түрі: car, bus, train, bicycle")
    electricity_kwh: float = Field(..., description="Айлық электр энергиясын тұтыну (кВт*сағ)")
    waste_kg: float = Field(..., description="Апталық қоқыс көлемі (кг)")

class CarbonCalculationResponse(BaseModel):
    monthly_co2_kg: float
    yearly_co2_tons: float
    trees_needed_to_offset: int
    eco_grade: str
    recommendation: str

class RecyclingPoint(BaseModel):
    id: int
    name: str
    city: str
    address: str
    waste_types: str
    latitude: Optional[float]
    longitude: Optional[float]
    contact: Optional[str]

class AirQuality(BaseModel):
    id: int
    city: str
    aqi: int
    status: str
    pm25: float
    pm10: float
    updated_at: str

class EcoChallenge(BaseModel):
    id: int
    title: str
    description: str
    points: int
    category: str


# --- ENDPOINTS ---

@app.get("/", tags=["General"])
def root():
    return {
        "project": "EcoTrack REST API",
        "status": "Online 🚀",
        "documentation": "/docs",
        "github_author": "Asylkhan-web",
        "description": "Экологиялық мониторинг және Эко-инновациялар платформасы"
    }

@app.post("/api/v1/carbon-footprint/calculate", response_model=CarbonCalculationResponse, tags=["Carbon Footprint"])
def calculate_carbon_footprint(data: CarbonCalculationRequest):
    """
    Пайдаланушының көміртек ізін (CO2 эмиссиясы) есептейтін API
    """
    transport_factors = {
        "car": 0.192,
        "bus": 0.089,
        "train": 0.041,
        "bicycle": 0.0
    }
    
    factor = transport_factors.get(data.transport_type.lower(), 0.192)
    monthly_transport_co2 = data.transport_km * 4 * factor
    monthly_elec_co2 = data.electricity_kwh * 0.475
    monthly_waste_co2 = data.waste_kg * 4 * 0.5
    
    total_monthly_co2 = monthly_transport_co2 + monthly_elec_co2 + monthly_waste_co2
    yearly_co2_tons = (total_monthly_co2 * 12) / 1000.0
    trees_needed = int(yearly_co2_tons * 45)
    
    if yearly_co2_tons < 2.0:
        grade = "A+ (Үздік Эко-өмір)"
        rec = "Сіздің экологияға әсеріңіз өте төмен! Тамаша!"
    elif yearly_co2_tons < 4.5:
        grade = "B (Орташа көрсеткіш)"
        rec = "Қоғамдық көлікті жиірек пайдаланып, қайта өңдеуге қоқыс тапсыруды ұсынамыз."
    else:
        grade = "C (Жоғары Эмиссия)"
        rec = "Көміртек ізіңіз өте жоғары. Энергия үнемдейтін құрылғыларға ауысып, ағаш отырғызу челленджіне қатысыңыз!"
        
    return CarbonCalculationResponse(
        monthly_co2_kg=round(total_monthly_co2, 2),
        yearly_co2_tons=round(yearly_co2_tons, 2),
        trees_needed_to_offset=trees_needed,
        eco_grade=grade,
        recommendation=rec
    )

@app.get("/api/v1/recycling/points", response_model=List[RecyclingPoint], tags=["Recycling"])
def get_recycling_points(city: Optional[str] = Query(None, description="Қала аты арқылы сүзгілеу")):
    """
    Қайта өңдеу және қоқыс қабылдау пункттерінің тізімін алу
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if city:
        cursor.execute("SELECT id, name, city, address, waste_types, latitude, longitude, contact FROM recycling_points WHERE city LIKE ?", (f"%{city}%",))
    else:
        cursor.execute("SELECT id, name, city, address, waste_types, latitude, longitude, contact FROM recycling_points")
        
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for r in rows:
        result.append(RecyclingPoint(
            id=r[0], name=r[1], city=r[2], address=r[3],
            waste_types=r[4], latitude=r[5], longitude=r[6], contact=r[7]
        ))
    return result

@app.get("/api/v1/air-quality", response_model=List[AirQuality], tags=["Air Quality"])
def get_air_quality(city: Optional[str] = Query(None, description="Қала бойынша ауа сапасын алу")):
    """
    Қалалардың ауа сапасы индексін (AQI) және PM2.5 көрсеткіштерін алу
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if city:
        cursor.execute("SELECT id, city, aqi, status, pm25, pm10, updated_at FROM air_quality WHERE city LIKE ?", (f"%{city}%",))
    else:
        cursor.execute("SELECT id, city, aqi, status, pm25, pm10, updated_at FROM air_quality")
        
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for r in rows:
        result.append(AirQuality(
            id=r[0], city=r[1], aqi=r[2], status=r[3],
            pm25=r[4], pm10=r[5], updated_at=r[6]
        ))
    return result

@app.get("/api/v1/challenges", response_model=List[EcoChallenge], tags=["Eco Challenges"])
def get_eco_challenges():
    """
    Пайдаланушыларға арналған күнделікті эко-челлендждер тізімі
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, points, category FROM eco_challenges")
    rows = cursor.fetchall()
    conn.close()
    
    return [EcoChallenge(id=r[0], title=r[1], description=r[2], points=r[3], category=r[4]) for r in rows]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
