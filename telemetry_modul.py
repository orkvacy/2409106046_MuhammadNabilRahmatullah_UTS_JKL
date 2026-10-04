#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Muhammad Nabil Rahmatullah - 2409106046

Nama file : telemetry_modul.py
Tujuan    : Menyimpan data SAMPEL telemetry (menyerupai hasil decode GPB di
            collector) berupa cpuUsage (in-uti) yang diturunkan dari digit NIM,
            lalu mengklasifikasikan tiap sampel:
              > 80   -> "KRITIS"
              50-80  -> "WASPADA"
              < 50   -> "NORMAL"
Pembuat   : Muhammad Nabil Rahmatullah (2409106046)
"""

from identitas import buat_id_perangkat, nim

# Digit NIM 2409106046 -> d = [2, 4, 0, 9, 1, 0, 6, 0, 4, 6]
#                   indeks:  0  1  2  3  4  5  6  7  8  9
d = [int(angka) for angka in nim]

NODE = buat_id_perangkat("router", 1)
ENCODING_PATH = "Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization"

# Nilai in-uti dibentuk dari pasangan digit NIM (puluhan, satuan):
#   sampel_1 = d[3], d[6] -> 9 dan 6 -> 96
#   sampel_2 = d[6], d[2] -> 6 dan 0 -> 60
#   sampel_3 = d[1], d[9] -> 4 dan 6 -> 46
#   sampel_4 = d[0], d[8] -> 2 dan 4 -> 24
data_telemetry = {
    "sampel_1": {
        "node_id": NODE,
        "encoding_path": ENCODING_PATH,
        "timestamp": "2026-10-04T10:00:00Z",
        "cpuUsage": {"in-uti": d[3] * 10 + d[6]},
    },
    "sampel_2": {
        "node_id": NODE,
        "encoding_path": ENCODING_PATH,
        "timestamp": "2026-10-04T10:00:10Z",
        "cpuUsage": {"in-uti": d[6] * 10 + d[2]},
    },
    "sampel_3": {
        "node_id": NODE,
        "encoding_path": ENCODING_PATH,
        "timestamp": "2026-10-04T10:00:20Z",
        "cpuUsage": {"in-uti": d[1] * 10 + d[9]},
    },
    "sampel_4": {
        "node_id": NODE,
        "encoding_path": ENCODING_PATH,
        "timestamp": "2026-10-04T10:00:30Z",
        "cpuUsage": {"in-uti": d[0] * 10 + d[8]},
    },
}


def tentukan_status(nilai):
    """Kembalikan status berdasarkan ambang batas CPU."""
    if nilai > 80:
        return "KRITIS"
    elif nilai >= 50:
        return "WASPADA"
    return "NORMAL"


def klasifikasi_telemetry(data=None):
    """Iterasi seluruh sampel, klasifikasikan, cetak, dan kembalikan hasilnya."""
    data = data_telemetry if data is None else data
    hasil = []

    print(f"[TELEMETRY] Node: {NODE}")
    print(f"[TELEMETRY] Path: {ENCODING_PATH}")
    for nama_sampel, isi in data.items():
        nilai = isi["cpuUsage"]["in-uti"]
        status = tentukan_status(nilai)
        hasil.append(
            {
                "sampel": nama_sampel,
                "timestamp": isi["timestamp"],
                "in-uti": nilai,
                "status": status,
            }
        )
        print(f"  {nama_sampel} | {isi['timestamp']} | cpuUsage in-uti = {nilai:>3}% -> {status}")
    return hasil


if __name__ == "__main__":
    klasifikasi_telemetry()
