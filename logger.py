from datetime import datetime

LOG_FILE = "weather_log.txt"

def tulis_log(pesan):
    """WRITING — tambahkan baris log baru, tanpa menghapus yang lama"""
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as file:
        file.write(f"[{waktu}] {pesan}\n")

def baca_log():
    """READING — baca semua isi log"""
    try:
        with open(LOG_FILE, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return ["Belum ada log."]