import sqlite3

DB_NAME = "weather.db"

def init_db():
    """Membuat tabel kalau belum ada — dijalankan sekali saat API start"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kota TEXT NOT NULL,
            suhu REAL,
            kondisi TEXT,
            waktu TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def simpan_history(kota, suhu, kondisi):
    """INSERT data cuaca ke database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (kota, suhu, kondisi) VALUES (?, ?, ?)",
        (kota, suhu, kondisi)
    )
    conn.commit()
    conn.close()

def ambil_semua_history():
    """SELECT semua data history, urut dari yang terbaru"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT kota, suhu, kondisi, waktu FROM history ORDER BY waktu DESC")
    hasil = cursor.fetchall()
    conn.close()
    return hasil

def ambil_history_per_kota(kota):
    """SELECT dengan WHERE — filter berdasarkan kota"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT kota, suhu, kondisi, waktu FROM history WHERE kota = ? ORDER BY waktu DESC",
        (kota,)
    )
    hasil = cursor.fetchall()
    conn.close()
    return hasil