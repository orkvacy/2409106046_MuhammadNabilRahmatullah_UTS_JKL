# Muhammad Nabil Rahmatullah - 2409106046

# UTS JKL: Integration Network with Python

Repo ini berisi pengerjaan UTS mata kuliah Jaringan Komputer Lanjut. Di sini saya membuat satu project Python untuk mengotomasi kantor cabang virtual saya, yaitu cabang **046** (diambil dari 3 digit terakhir NIM). Project-nya saya pecah per modul supaya lebih rapi, lalu semuanya digabung di `main.py`.

## Isi Project

```
2409106046_MuhammadNabilRahmatullah_UTS_JKL/
├── .gitignore
├── README.md
├── requirements.txt
├── identitas.py        # identitas cabang dan function buat_id_perangkat()
├── ssh_modul.py        # login SSH pakai Paramiko
├── snmp_modul.py       # ambil sysName pakai PySNMP (SNMPv2c)
├── netconf_modul.py    # bikin pesan NETCONF <edit-config> untuk VLAN
├── telemetry_modul.py  # klasifikasi data sampel telemetry CPU
└── main.py             # gabungan semua modul + class LaporanCabang
```

## Personalisasi

Semua nilai di bawah ini diturunkan dari NIM saya di `identitas.py`, jadi tidak ada yang saya tulis manual di modul lain.

| Bagian | Nilai |
|---|---|
| Kode cabang | `046` |
| Username SSH | `admin_046` |
| Community SNMP | `comm_046` |
| VLAN NETCONF | ID `46`, nama `VLAN_CABANG_046` |
| ID router | `RTR-046-01` |

Untuk telemetry, saya pakai 4 sampel `cpuUsage (in-uti)` yang angkanya saya ambil dari pasangan digit NIM. Hasilnya 96 (KRITIS), 60 (WASPADA), serta 46 dan 24 (NORMAL), jadi ketiga kategori bisa muncul semua.

## Cara Menjalankan

1. Buat virtual environment lalu install library yang dibutuhkan

   ```powershell
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Siapkan VM tujuan. Di VM saya buat user `admin_046`, lalu di `/etc/snmp/snmpd.conf` saya tambahkan `rocommunity comm_046 default`, `sysName CBG-046-RTR`, dan `agentAddress udp:161`.

3. Atur alamat VM lewat environment variable. Kalau tidak diatur, defaultnya `127.0.0.1` port 22 dan 161. VM saya pakai NAT dengan port forwarding, jadi saya set seperti ini

   ```powershell
   $env:SSH_HOST="127.0.0.1"
   $env:SSH_PORT="2222"
   $env:SNMP_HOST="127.0.0.1"
   $env:SNMP_PORT="1161"
   ```

4. Jalankan program utama

   ```powershell
   python main.py
   ```

   Password SSH nanti ditanyakan saat program jalan, jadi tidak saya simpan di kode. Tiap modul juga bisa dijalankan sendiri, misalnya `python telemetry_modul.py`.

## Catatan

- Koneksi SSH dan SNMP sudah dibungkus `try/except`, jadi kalau VM sedang mati programnya tetap jalan sampai laporan akhir.
- Laporan akhir dicetak ke terminal dan juga disimpan ke `laporan_cabang_046.log`.
- Folder `venv/`, `__pycache__/`, file `.log`, dan `.env` tidak ikut di-commit karena sudah masuk `.gitignore`.
