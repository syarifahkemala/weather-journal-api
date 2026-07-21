def rekomendasi_pakaian(suhu):
    if suhu < 20:
        return "Pakai jaket, cuaca dingin"
    elif suhu < 28:
        return "Baju biasa cukup, cuaca sejuk"
    else:
        return "Pakai baju tipis, bawa topi, cuaca panas"