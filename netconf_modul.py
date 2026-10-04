#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Muhammad Nabil Rahmatullah - 2409106046

Nama file : netconf_modul.py
Tujuan    : MEMBANGUN (bukan menulis manual) string XML NETCONF
            <rpc><edit-config> untuk membuat VLAN dengan ID = kode_cabang,
            memakai modul xml.etree.ElementTree, lalu mencetaknya.
Pembuat   : Muhammad Nabil Rahmatullah (2409106046)

Struktur 4 lapisan NETCONF:
  1. Transport layer  : SSH (port 830)  -> tidak dibangun di sini, hanya jalur kirim
  2. Messages layer   : elemen <rpc message-id="..."> / <rpc-reply>
  3. Operations layer : elemen <edit-config> beserta <target>
  4. Content layer    : isi <config> (data YANG: konfigurasi VLAN)
"""

import xml.etree.ElementTree as ET

from identitas import kode_cabang

NS_NETCONF = "urn:ietf:params:xml:ns:netconf:base:1.0"
NS_NATIVE = "http://cisco.com/ns/yang/Cisco-IOS-XE-native"
NS_VLAN = "http://cisco.com/ns/yang/Cisco-IOS-XE-vlan"


def buat_pesan_netconf(vlan_id=None, message_id="101"):
    """Bangun pesan <rpc><edit-config> pembuatan VLAN dan kembalikan string XML."""
    vlan_id = int(kode_cabang) if vlan_id is None else int(vlan_id)  # "046" -> 46
    nama_vlan = f"VLAN_CABANG_{kode_cabang}"

    # ===== TRANSPORT LAYER =====
    # Tidak dibangun di sini. Pada perangkat nyata, string XML ini dikirim
    # melalui sesi SSH ke port 830 (subsystem "netconf").

    # ===== MESSAGES LAYER =====
    # <rpc> membungkus permintaan; message-id dipakai untuk mencocokkan <rpc-reply>.
    rpc = ET.Element("rpc", {"xmlns": NS_NETCONF, "message-id": message_id})

    # ===== OPERATIONS LAYER =====
    # <edit-config> = operasi mengubah konfigurasi; <target> = datastore tujuan.
    edit_config = ET.SubElement(rpc, "edit-config")
    target = ET.SubElement(edit_config, "target")
    ET.SubElement(target, "running")

    # ===== CONTENT LAYER =====
    # <config> berisi data konfigurasi berbasis model YANG (di sini: VLAN baru).
    config = ET.SubElement(edit_config, "config")
    native = ET.SubElement(config, "native", {"xmlns": NS_NATIVE})
    vlan = ET.SubElement(native, "vlan")
    vlan_list = ET.SubElement(vlan, "vlan-list", {"xmlns": NS_VLAN})
    ET.SubElement(vlan_list, "id").text = str(vlan_id)
    ET.SubElement(vlan_list, "name").text = nama_vlan

    ET.indent(rpc, space="  ")
    xml_body = ET.tostring(rpc, encoding="unicode")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_body


if __name__ == "__main__":
    print("=== PESAN NETCONF <edit-config> ===")
    print(buat_pesan_netconf())
