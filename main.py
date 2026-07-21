from fastapi import FastAPI, HTTPException
import os
import requests
from dotenv import load_dotenv

from database import init_db, simpan_history, ambil_semua_history, ambil_history_per_kota
from logger import tulis_log, baca_log

load_dotenv()
app = FastAPI(title="Weather Journal API")

api_key = os.environ.get("WEATHER_API_KEY")

# Jalankan sekali saat aplikasi start — siapkan tabel database
@app.on_event("startup")
def startup():
    init_db()
    tulis_log("Aplikasi dinyalakan")


@app.get("/")
def home():
    return {"pesan": "Weather Journal API aktif"}


@app.get("/cuaca/{kota}")
def cek_cuaca(kota: str):
    """
    1. HTTP request ke OpenWeatherMap
    2. Error handling kalau gagal
    3. Simpan ke database
    4. Tulis ke log file
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={kota}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        tulis_log(f"GAGAL koneksi saat cek cuaca {kota}")
        raise HTTPException(status_code=503, detail="Gagal terhubung ke layanan cuaca")

    if response.status_code == 404:
        tulis_log(f"Kota tidak ditemukan: {kota}")
        raise HTTPException(status_code=404, detail=f"Kota '{kota}' tidak ditemukan")

    if response.status_code != 200:
        tulis_log(f"Error tak terduga untuk kota {kota}: {response.status_code}")
        raise HTTPException(status_code=500, detail="Terjadi kesalahan pada layanan cuaca")

    data = response.json()
    suhu = data["main"]["temp"]
    kondisi = data["weather"][0]["description"]

    # Simpan ke SQLite
    simpan_history(kota, suhu, kondisi)

    # Tulis ke file log
    tulis_log(f"Cek cuaca {kota}: {suhu}°C, {kondisi}")

    return {"kota": kota, "suhu": suhu, "kondisi": kondisi}


@app.get("/history")
def lihat_history():
    """SELECT semua history dari SQLite"""
    data = ambil_semua_history()
    hasil = [
        {"kota": row[0], "suhu": row[1], "kondisi": row[2], "waktu": row[3]}
        for row in data
    ]
    return {"jumlah": len(hasil), "data": hasil}


@app.get("/history/{kota}")
def lihat_history_kota(kota: str):
    """SELECT dengan WHERE kota tertentu"""
    data = ambil_history_per_kota(kota)
    if not data:
        raise HTTPException(status_code=404, detail=f"Belum ada history untuk kota '{kota}'")
    hasil = [
        {"kota": row[0], "suhu": row[1], "kondisi": row[2], "waktu": row[3]}
        for row in data
    ]
    return {"jumlah": len(hasil), "data": hasil}


@app.get("/logs")
def lihat_log():
    """READING isi file log"""
    return {"logs": baca_log()}