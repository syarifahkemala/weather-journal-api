# Weather Journal API

API sederhana untuk cek cuaca, menyimpan history ke SQLite, dan mencatat log aktivitas.

## Setup
1. `python3 -m venv venv && source venv/bin/activate`
2. `pip3 install -r requirements.txt`
3. Buat file `.env` berisi `WEATHER_API_KEY=xxxx`
4. `uvicorn main:app --reload`
5. Buka `http://127.0.0.1:8000/docs`

## Endpoints
- `GET /cuaca/{kota}` — cek cuaca & simpan ke history
- `GET /history` — lihat semua history
- `GET /history/{kota}` — lihat history per kota
- `GET /logs` — lihat log aktivitas