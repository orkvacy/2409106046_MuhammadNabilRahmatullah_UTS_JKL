#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Muhammad Nabil Rahmatullah - 2409106046

Nama file : snmp_modul.py
Tujuan    : Mengambil nilai sysName (OID 1.3.6.1.2.1.1.5.0) dari agent SNMP
            memakai SNMPv2c dengan community string comm_<kode_cabang>,
            mencetak hasilnya, dan menangani kegagalan dengan try/except.
Pembuat   : Muhammad Nabil Rahmatullah (2409106046)

Catatan   : Mendukung PySNMP versi baru (7.x, API asyncio) dan versi lama
            (4.x, API sinkron getCmd).
"""

import asyncio
import os

from identitas import community_snmp

SNMP_HOST = os.environ.get("SNMP_HOST", "127.0.0.1")
SNMP_PORT = int(os.environ.get("SNMP_PORT", "161"))
OID_SYSNAME = "1.3.6.1.2.1.1.5.0"


async def _snmp_get_baru(host, port, community, oid):
    """GET SNMPv2c memakai PySNMP 7.x (asyncio)."""
    from pysnmp.hlapi.v3arch.asyncio import (
        CommunityData,
        ContextData,
        ObjectIdentity,
        ObjectType,
        SnmpEngine,
        UdpTransportTarget,
        get_cmd,
    )

    engine = SnmpEngine()
    try:
        target = await UdpTransportTarget.create((host, port), timeout=2, retries=1)
        return await get_cmd(
            engine,
            CommunityData(community, mpModel=1),  # mpModel=1 -> SNMPv2c
            target,
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
        )
    finally:
        engine.close_dispatcher()


def _snmp_get_lama(host, port, community, oid):
    """GET SNMPv2c memakai PySNMP 4.x (sinkron)."""
    from pysnmp.hlapi import (
        CommunityData,
        ContextData,
        ObjectIdentity,
        ObjectType,
        SnmpEngine,
        UdpTransportTarget,
        getCmd,
    )

    return next(
        getCmd(
            SnmpEngine(),
            CommunityData(community, mpModel=1),
            UdpTransportTarget((host, port), timeout=2, retries=1),
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
        )
    )


def cek_snmp(host=SNMP_HOST, port=SNMP_PORT, community=community_snmp):
    """Ambil sysName dari agent SNMP dan kembalikan ringkasan hasil."""
    hasil = {
        "host": f"{host}:{port}",
        "versi": "SNMPv2c",
        "oid": OID_SYSNAME,
        "status": "GAGAL",
        "sysName": None,
        "error": None,
    }

    print(f"[SNMP] GET {OID_SYSNAME} (sysName) ke {host}:{port} ...")
    try:
        try:
            respon = asyncio.run(_snmp_get_baru(host, port, community, OID_SYSNAME))
        except ImportError:
            respon = _snmp_get_lama(host, port, community, OID_SYSNAME)

        error_indication, error_status, error_index, var_binds = respon

        if error_indication:
            hasil["error"] = str(error_indication)
        elif error_status:
            hasil["error"] = f"{error_status.prettyPrint()} pada indeks {error_index}"
        else:
            for oid, nilai in var_binds:
                hasil["sysName"] = nilai.prettyPrint()
                print(f"[SNMP] {oid.prettyPrint()} = {hasil['sysName']}")
            hasil["status"] = "BERHASIL"
    except Exception as e:
        hasil["error"] = f"Error SNMP: {e}"

    if hasil["error"]:
        print(f"[SNMP] Gagal: {hasil['error']}")
    return hasil


if __name__ == "__main__":
    cek_snmp()
