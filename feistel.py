# -*- coding: utf-8 -*-
"""Modul feistel untuk ZarCryptoDES."""



# 2. FEISTEL PENDIDIKAN DARI MATERI, BUKAN DES LENGKAP.
# BARIS ASLI 331: Mendefinisikan fungsi F. Menghitung fungsi F pada simulasi Feistel 4 ronde dari contoh dosen, bukan F DES standar.
def F(r, k):
    # BARIS ASLI 332: Di F: Memakai geser bit untuk mengambil, menggabungkan, atau memutar bagian data biner.
    rot = ((r << 1) | (r >> 7)) & 255
    # BARIS ASLI 333: Di F: Mengembalikan nilai perhitungan ke pemanggil: (rot + k) & 255.
    return (rot + k) & 255


# BARIS ASLI 335: Mendefinisikan fungsi feistel_encrypt. Mengenkripsi nilai 16-bit dengan Feistel sederhana empat ronde dari dosen.
def feistel_encrypt(p, keys):
    # BARIS ASLI 336: Di feistel_encrypt: Memakai geser bit untuk mengambil, menggabungkan, atau memutar bagian data biner.
    l, r = (p >> 8) & 255, p & 255
    # BARIS ASLI 337: Di feistel_encrypt: Melakukan iterasi pada elemen/urutan: k in keys.
    for k in keys:
        # BARIS ASLI 338: Di feistel_encrypt: Menggunakan operator XOR (^) pada bit; berbeda 1 menghasilkan 1, sama menghasilkan 0.
        l, r = r, l ^ F(r, k)
    # BARIS ASLI 339: Di feistel_encrypt: Mengembalikan nilai perhitungan ke pemanggil: (l << 8) | r.
    return (l << 8) | r


# BARIS ASLI 341: Mendefinisikan fungsi feistel_decrypt. Memulihkan nilai 16-bit dengan membalik urutan kunci Feistel sederhana.
def feistel_decrypt(c, keys):
    # BARIS ASLI 342: Di feistel_decrypt: Memakai geser bit untuk mengambil, menggabungkan, atau memutar bagian data biner.
    l, r = (c >> 8) & 255, c & 255
    # BARIS ASLI 343: Di feistel_decrypt: Melakukan iterasi pada elemen/urutan: k in reversed(keys).
    for k in reversed(keys):
        # BARIS ASLI 344: Di feistel_decrypt: Menggunakan operator XOR (^) pada bit; berbeda 1 menghasilkan 1, sama menghasilkan 0.
        l, r = r ^ F(l, k), l
    # BARIS ASLI 345: Di feistel_decrypt: Mengembalikan nilai perhitungan ke pemanggil: (l << 8) | r.
    return (l << 8) | r
