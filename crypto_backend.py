# -*- coding: utf-8 -*-
# BARIS ASLI 26: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
try:
    # BARIS ASLI 27: Mengimpor modul Crypto yang diperlukan oleh aplikasi.
    import Crypto
    # BARIS ASLI 28: Mengimpor komponen Crypto.Cipher import DES, DES3 untuk fungsi terkait.
    from Crypto.Cipher import DES, DES3
# BARIS ASLI 29: Menangani kesalahan ImportError.
except ImportError:
    # BARIS ASLI 30: Menghitung/menyiapkan nilai Crypto untuk dipakai oleh proses berikutnya.
    Crypto=None
    # BARIS ASLI 31: Menghitung/menyiapkan nilai DES untuk dipakai oleh proses berikutnya.
    DES=None
    # BARIS ASLI 32: Menghitung/menyiapkan nilai DES3 untuk dipakai oleh proses berikutnya.
    DES3=None
