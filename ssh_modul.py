#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Muhammad Nabil Rahmatullah - 2409106046

Nama file : ssh_modul.py
Tujuan    : Login SSH ke VM/laptop memakai Paramiko dengan username
            admin_<kode_cabang>, menjalankan beberapa perintah diagnostik,
            lalu mencetak hasilnya. Kegagalan koneksi ditangani try/except
            sehingga program utama tetap berjalan.
Pembuat   : Muhammad Nabil Rahmatullah (2409106046)

Catatan   : Password TIDAK ditulis di kode (repo publik). Password dibaca dari
            environment variable SSH_PASSWORD, atau ditanyakan saat program jalan.
"""

import getpass
import os

import paramiko

from identitas import username_ssh

SSH_HOST = os.environ.get("SSH_HOST", "127.0.0.1")
SSH_PORT = int(os.environ.get("SSH_PORT", "22"))
PERINTAH_DIAGNOSTIK = ["hostname", "whoami", "uptime"]


def cek_ssh(host=SSH_HOST, port=SSH_PORT, username=username_ssh, password=None):
    """Login SSH, jalankan perintah diagnostik, dan kembalikan ringkasan hasil."""
    hasil = {
        "host": f"{host}:{port}",
        "username": username,
        "status": "GAGAL",
        "output": {},
        "error": None,
    }

    if password is None:
        password = os.environ.get("SSH_PASSWORD") or getpass.getpass(
            f"Password SSH untuk {username}@{host}: "
        )

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"[SSH] Menghubungkan ke {host}:{port} sebagai {username} ...")
    try:
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=5,
            look_for_keys=False,
            allow_agent=False,
        )
        print("[SSH] Login berhasil.\n")

        for perintah in PERINTAH_DIAGNOSTIK:
            _, stdout, stderr = client.exec_command(perintah, timeout=10)
            keluaran = stdout.read().decode(errors="replace").strip()
            galat = stderr.read().decode(errors="replace").strip()
            teks = keluaran if keluaran else f"(stderr) {galat or '-'}"
            hasil["output"][perintah] = teks
            print(f"$ {perintah}\n{teks}\n")

        hasil["status"] = "BERHASIL"
    except paramiko.AuthenticationException:
        hasil["error"] = "Autentikasi gagal (username/password salah)"
    except (paramiko.SSHException, OSError) as e:
        hasil["error"] = f"Koneksi gagal: {e}"
    except Exception as e:  # pengaman terakhir agar program utama tidak berhenti
        hasil["error"] = f"Error tak terduga: {e}"
    finally:
        client.close()

    if hasil["error"]:
        print(f"[SSH] {hasil['error']}")
    return hasil


if __name__ == "__main__":
    cek_ssh()
