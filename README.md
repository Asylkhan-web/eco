# 🌱 EcoTrack REST API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

**EcoTrack API** — Экологиялық мониторинг, көміртек ізін (Carbon Footprint) есептеу, қайта өңдеу пункттері және эко-челлендждерге арналған толыққанды RESTful API платформасы.

---

## 🚀 Мүмкіндіктер (Features)

*   **🌱 Carbon Footprint Calculator:** Көлік, электр энергиясы және қоқыс көлемі бойынша жеке CO2 эмиссиясын есептеу.
*   **♻️ Recycling Points Directory:** Қалалар бойынша қайта өңдеу және қоқыс қабылдау орындарын іздеу.
*   **🌬️ Air Quality Index (AQI):** Ауаның сапасы мен PM2.5 / PM10 бөлшектерінің деңгейін мониторингтеу.
*   **🏆 Eco Challenges:** Пайдаланушылардың экологиялық әдеттерін қалыптастыруға арналған эко-челлендждер.
*   **📖 Auto Swagger & Redoc Docs:** Барлық API эндпоинттері интерактивті құжатталған.

---

## 📌 API Эндпоинттері (Endpoints)

| Әдіс | Эндпоинт | Сипаттамасы |
| :--- | :--- | :--- |
| `GET` | `/` | API статусын тексеру |
| `POST` | `/api/v1/carbon-footprint/calculate` | Көміртек ізін есептеу |
| `GET` | `/api/v1/recycling/points` | Қайта өңдеу пункттерінің тізімі (`?city=Алматы`) |
| `GET` | `/api/v1/air-quality` | Қалалардың ауа сапасы (`?city=Астана`) |
| `GET` | `/api/v1/challenges` | Күнделікті эко-челлендждер |

---

## 🛠️ Іске қосу (Quick Start)

### 1. Тәуелділіктерді орнату
```bash
pip install -r requirements.txt
```

### 2. API Серверін іске қосу
```bash
python main.py
```
немесе `uvicorn` арқылы:
```bash
uvicorn main:app --reload --port 8000
```

### 3. Интерактивті құжаттаманы ашу
Браузерде ашыңыз:
*   **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
*   **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🐳 Docker арқылы іске қосу

```bash
docker build -t ecotrack-api .
docker run -p 8000:8000 ecotrack-api
```

---

## 👤 Автор
**GitHub:** [@Asylkhan-web](https://github.com/Asylkhan-web)
