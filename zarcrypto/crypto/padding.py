# Dokumentasikan tujuan atau perilaku bagian kode ini.
"""Padding PKCS#7 untuk blok DES/3DES 8 byte."""


# Lengkapi pesan menjadi kelipatan 8 byte menggunakan PKCS#7.
def pad(data):
    # Hitung banyak padding; pesan yang sudah tepat blok tetap mendapat 8 byte padding.
    n = 8 - len(data) % 8
    # Tambahkan n byte yang masing-masing bernilai n sesuai aturan PKCS#7.
    return data + bytes([n]) * n


# Validasi dan lepaskan byte padding PKCS#7.
def unpad(data):
    # Pilih langkah berdasarkan kondisi not data or len(data) % 8.
    if not data or len(data) % 8:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Panjang data hasil dekripsi tidak valid.")
    # Baca byte terakhir untuk mengetahui banyak byte padding yang harus dilepas.
    n = data[-1]
    # Pilih langkah berdasarkan kondisi n < 1 or n > 8 or data[-n:] != bytes([n]) * n.
    if n < 1 or n > 8 or data[-n:] != bytes([n]) * n:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError(
            # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
            "Padding tidak valid. Periksa kunci, algoritma DES/3DES, pilihan CBC/ECB, dan kelengkapan ciphertext."
        # Tutup pengelompokan sintaks di atas.
        )
    # Buang padding yang sudah lolos validasi dan kembalikan pesan asli.
    return data[:-n]
