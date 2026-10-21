# Dokumentasikan tujuan atau perilaku bagian kode ini.
"""Assertion dengan pesan yang dipakai oleh pemeriksaan algoritma."""


# Definisikan fungsi/metode verify untuk tanggung jawab berikut.
def verify(condition, message):
    # Pilih langkah berdasarkan kondisi not condition.
    if not condition:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise AssertionError(message)
