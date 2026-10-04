#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Muhammad Nabil Rahmatullah - 2409106046

Nama file : main.py
Tujuan    : Integrasi akhir. Meng-import modul identitas, ssh_modul,
            snmp_modul, netconf_modul, dan telemetry_modul, menjalankan
            seluruh function secara berurutan, lalu mencetak SATU laporan
            akhir gabungan memakai class LaporanCabang.
Pembuat   : Muhammad Nabil Rahmatullah (2409106046)
"""

from datetime import datetime

import identitas
import netconf_modul
import snmp_modul
import ssh_modul
import telemetry_modul


class LaporanCabang:
    """Menyusun dan menampilkan laporan akhir kantor cabang virtual."""

    def __init__(self, nim, nama, kode_cabang):
        self.nim = nim
        self.nama = nama
        self.kode_cabang = kode_cabang
        self.id_router = identitas.buat_id_perangkat("router", 1)
        self.waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def tampilkan_laporan(self, hasil_ssh, hasil_snmp, pesan_netconf, hasil_telemetry):
        garis = "=" * 64
        baris = [
            garis,
            "LAPORAN AKHIR KANTOR CABANG VIRTUAL".center(64),
            garis,
            f"Nama        : {self.nama}",
            f"NIM         : {self.nim}",
            f"Kode cabang : {self.kode_cabang}",
            f"ID router   : {self.id_router}",
            f"Waktu       : {self.waktu}",
            "",
            "[1] SSH (Paramiko)",
            f"    Host     : {hasil_ssh['host']}",
            f"    Username : {hasil_ssh['username']}",
            f"    Status   : {hasil_ssh['status']}",
        ]
        if hasil_ssh["error"]:
            baris.append(f"    Error    : {hasil_ssh['error']}")
        for perintah, keluaran in hasil_ssh["output"].items():
            baris.append(f"    $ {perintah:<9}: {keluaran.splitlines()[0] if keluaran else '-'}")

        baris += [
            "",
            "[2] SNMP (PySNMP)",
            f"    Host     : {hasil_snmp['host']} ({hasil_snmp['versi']})",
            f"    OID      : {hasil_snmp['oid']} (sysName)",
            f"    Status   : {hasil_snmp['status']}",
            f"    sysName  : {hasil_snmp['sysName'] or '-'}",
        ]
        if hasil_snmp["error"]:
            baris.append(f"    Error    : {hasil_snmp['error']}")

        baris += ["", "[3] NETCONF <edit-config> yang dibangun"]
        baris += [f"    {b}" for b in pesan_netconf.splitlines()]

        baris += ["", "[4] Klasifikasi Telemetry (cpuUsage in-uti)"]
        rekap = {"KRITIS": 0, "WASPADA": 0, "NORMAL": 0}
        for item in hasil_telemetry:
            rekap[item["status"]] += 1
            baris.append(
                f"    {item['sampel']} | {item['timestamp']} | {item['in-uti']:>3}% -> {item['status']}"
            )
        baris.append(
            f"    Rekap: KRITIS={rekap['KRITIS']}, WASPADA={rekap['WASPADA']}, NORMAL={rekap['NORMAL']}"
        )
        baris.append(garis)

        laporan = "\n".join(baris)
        print(laporan)
        return laporan

    def simpan_log(self, laporan):
        nama_file = f"laporan_cabang_{self.kode_cabang}.log"
        with open(nama_file, "w", encoding="utf-8") as f:
            f.write(laporan + "\n")
        print(f"\nLaporan juga disimpan ke {nama_file}")


def main():
    print("\n### BAGIAN A - IDENTITAS ###")
    print(f"{identitas.nama} ({identitas.nim}) - cabang {identitas.kode_cabang}")

    print("\n### BAGIAN B - SSH ###")
    hasil_ssh = ssh_modul.cek_ssh()

    print("\n### BAGIAN C - SNMP ###")
    hasil_snmp = snmp_modul.cek_snmp()

    print("\n### BAGIAN D - NETCONF ###")
    pesan_netconf = netconf_modul.buat_pesan_netconf()
    print(pesan_netconf)

    print("\n### BAGIAN E - TELEMETRY ###")
    hasil_telemetry = telemetry_modul.klasifikasi_telemetry()

    print("\n### BAGIAN F - LAPORAN AKHIR ###")
    laporan = LaporanCabang(identitas.nim, identitas.nama, identitas.kode_cabang)
    teks = laporan.tampilkan_laporan(hasil_ssh, hasil_snmp, pesan_netconf, hasil_telemetry)
    laporan.simpan_log(teks)


if __name__ == "__main__":
    main()
