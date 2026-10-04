#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Muhammad Nabil Rahmatullah - 2409106046

Nama file : identitas.py
Tujuan    : Menyimpan identitas kantor cabang virtual (NIM, nama, kode cabang),
            nilai personalisasi (username SSH & community SNMP), serta function
            untuk membuat ID perangkat yang unik per cabang.
Pembuat   : Muhammad Nabil Rahmatullah (2409106046)
"""

nim = "2409106046"
nama = "Muhammad Nabil Rahmatullah"
kode_cabang = nim[-3:]  # 3 digit terakhir NIM -> "046"

# Nilai personalisasi yang diturunkan dari kode_cabang
username_ssh = f"admin_{kode_cabang}"
community_snmp = f"comm_{kode_cabang}"


def buat_id_perangkat(jenis, nomor):
    """Membuat ID perangkat berformat <JENIS>-<kode_cabang>-<nomor 2 digit>.

    Contoh: buat_id_perangkat("router", 1) -> "RTR-046-01"
    """
    singkatan = {
        "router": "RTR",
        "switch": "SW",
        "server": "SRV",
        "firewall": "FW",
    }
    prefix = singkatan.get(jenis.lower(), jenis.upper()[:3])
    return f"{prefix}-{kode_cabang}-{int(nomor):02d}"


if __name__ == "__main__":
    print("=== IDENTITAS CABANG ===")
    print(f"NIM          : {nim}")
    print(f"Nama         : {nama}")
    print(f"Kode cabang  : {kode_cabang}")
    print(f"Username SSH : {username_ssh}")
    print(f"Community    : {community_snmp}")
    print("Contoh ID perangkat:")
    for jenis, nomor in [("router", 1), ("switch", 1), ("server", 2)]:
        print(f"  - {jenis:<7}: {buat_id_perangkat(jenis, nomor)}")
