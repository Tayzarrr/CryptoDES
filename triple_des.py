# -*- coding: utf-8 -*-
"""Modul triple_des untuk ZarCryptoDES."""

from des_manual import DESManual, validate_cbc, xor_bytes
from keys import validate_algorithm_key

# BARIS ASLI 160: Mendefinisikan kelas TripleDESManual. Menyusun tiga mesin DES manual menjadi Triple DES EDE.
class TripleDESManual:
    # BARIS ASLI 161: Di TripleDESManual: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
    """3DES-EDE dua atau tiga kunci. Setiap tahap memakai DESManual, bukan DES3 library."""
    # BARIS ASLI 162: Mendefinisikan fungsi __init__. Fungsi ini menangani aksi khusus dalam aplikasi.
    def __init__(self,key):
        # BARIS ASLI 163: Di __init__: Menjalankan langkah validate_algorithm_key(key,'3DES') sebagai bagian dari alur fungsi ini.
        validate_algorithm_key(key,'3DES')
        key = key + key[:8] if len(key) == 16 else key  # Dua kunci 3DES: K3 = K1.
        # BARIS ASLI 164: Di __init__: Menghitung/menyiapkan nilai self.d1 untuk dipakai oleh proses berikutnya.
        self.d1=DESManual(key[:8]);self.d2=DESManual(key[8:16]);self.d3=DESManual(key[16:24])
    # BARIS ASLI 165: Mendefinisikan fungsi encrypt_block. Mengenkripsi satu blok DES menggunakan subkunci dengan urutan maju.
    def encrypt_block(self,block):
        # BARIS ASLI 166: Di encrypt_block: Mengembalikan keluaran metode/hasil pemrosesan objek.
        return self.d3.encrypt_block(self.d2.decrypt_block(self.d1.encrypt_block(block)))
    # BARIS ASLI 167: Mendefinisikan fungsi decrypt_block. Mendekripsi satu blok DES dengan urutan subkunci dibalik.
    def decrypt_block(self,block):
        # BARIS ASLI 168: Di decrypt_block: Mengembalikan keluaran metode/hasil pemrosesan objek.
        return self.d1.decrypt_block(self.d2.encrypt_block(self.d3.decrypt_block(block)))


# BARIS ASLI 171: Mendefinisikan fungsi triple_cbc. Memproses 3DES manual dalam CBC untuk enkripsi atau dekripsi.
def triple_cbc(data,key,iv,decrypt=False):
    # BARIS ASLI 172: Di triple_cbc: Menjalankan langkah validate_cbc(data,iv) sebagai bagian dari alur fungsi ini.
    validate_cbc(data,iv)
    # BARIS ASLI 173: Di triple_cbc: Menghitung/menyiapkan nilai cipher untuk dipakai oleh proses berikutnya.
    cipher=TripleDESManual(key);previous=iv;out=bytearray()
    # BARIS ASLI 174: Di triple_cbc: Menelusuri data per blok agar tiap iterasi memproses ukuran yang sesuai.
    for pos in range(0,len(data),8):
        # BARIS ASLI 175: Di triple_cbc: Menghitung/menyiapkan nilai block untuk dipakai oleh proses berikutnya.
        block=data[pos:pos+8]
        # BARIS ASLI 176: Di triple_cbc: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: decrypt.
        if decrypt:
            # BARIS ASLI 177: Di triple_cbc: Menerapkan XOR per byte sebagai bagian dari mode CBC.
            out.extend(xor_bytes(cipher.decrypt_block(block),previous));previous=block
        # BARIS ASLI 178: Di triple_cbc: Cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
        else:
            # BARIS ASLI 179: Di triple_cbc: Menerapkan XOR per byte sebagai bagian dari mode CBC.
            previous=cipher.encrypt_block(xor_bytes(block,previous));out.extend(previous)
    # BARIS ASLI 180: Di triple_cbc: Mengembalikan data dalam representasi byte.
    return bytes(out)
