# -*- coding: utf-8 -*-
"""Modul cipher untuk ZarCryptoDES."""

import secrets
from crypto_backend import DES, DES3
from des_manual import DESManual, decrypt_cbc, encrypt_cbc
from keys import validate_algorithm_key
from triple_des import TripleDESManual, triple_cbc

# BAGIAN 2: FORMAT FILE, PADDING, DAN DES / 3DES LIBRARY
# BARIS ASLI 183: Mendefinisikan fungsi parse_hex. Mengubah string heksadesimal menjadi byte dan memvalidasi panjangnya.
def parse_hex(text, length, label):
    # BARIS ASLI 184: Di parse_hex: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
    try:
        # BARIS ASLI 185: Di parse_hex: Mendekode teks heksadesimal menjadi representasi byte.
        value = bytes.fromhex(text)
    # BARIS ASLI 186: Di parse_hex: Menangani kesalahan ValueError as exc.
    except ValueError as exc:
        # BARIS ASLI 187: Di parse_hex: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
        raise ValueError(f'{label} harus berupa heksadesimal.') from exc
    # BARIS ASLI 188: Di parse_hex: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
    if len(value) != length:
        # BARIS ASLI 189: Di parse_hex: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
        raise ValueError(f'{label} harus {length} byte ({length*2} digit hex).')
    # BARIS ASLI 190: Di parse_hex: Mengembalikan nilai perhitungan ke pemanggil: value.
    return value


# BARIS ASLI 192: Mendefinisikan fungsi pad. Menambahkan padding PKCS#7 hingga panjang data kelipatan 8 byte.
def pad(data):
    # BARIS ASLI 193: Di pad: Menghitung/menyiapkan nilai n untuk dipakai oleh proses berikutnya.
    n = 8 - len(data) % 8
    # BARIS ASLI 194: Di pad: Mengembalikan data dalam representasi byte.
    return data + bytes([n]) * n


# BARIS ASLI 196: Mendefinisikan fungsi unpad. Memeriksa dan membuang padding PKCS#7 dari hasil dekripsi.
def unpad(data):
    # BARIS ASLI 197: Di unpad: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
    if not data or len(data) % 8:
        # BARIS ASLI 198: Di unpad: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
        raise ValueError('Panjang data hasil dekripsi tidak valid.')
    # BARIS ASLI 199: Di unpad: Menghitung/menyiapkan nilai n untuk dipakai oleh proses berikutnya.
    n = data[-1]
    # BARIS ASLI 200: Di unpad: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: n < 1 or n > 8 or data[-n:] != bytes([n]) * n.
    if n < 1 or n > 8 or data[-n:] != bytes([n]) * n:
        # BARIS ASLI 201: Di unpad: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
        raise ValueError('Padding tidak valid. Periksa kunci, algoritma DES/3DES, pilihan CBC/ECB, dan kelengkapan ciphertext.')
    # BARIS ASLI 202: Di unpad: Mengembalikan nilai perhitungan ke pemanggil: data[:-n].
    return data[:-n]


# BARIS ASLI 204: Mendefinisikan fungsi crypt. Memilih mesin DES/3DES manual atau PyCryptodome sesuai backend.
def crypt(data,key,iv,backend,decrypt=False,algorithm='DES'):
    # BARIS ASLI 205: Di crypt: Menjalankan langkah validate_algorithm_key(key,algorithm) sebagai bagian dari alur fungsi ini.
    validate_algorithm_key(key,algorithm)
    # BARIS ASLI 206: Di crypt: Memilih jalur operasi sesuai backend atau jenis algoritma.
    if backend=='manual':
        # BARIS ASLI 207: Di crypt: Memilih jalur operasi sesuai backend atau jenis algoritma.
        if algorithm=='3DES':return triple_cbc(data,key,iv,decrypt)
        # BARIS ASLI 208: Di crypt: Mengembalikan nilai perhitungan ke pemanggil: decrypt_cbc(data,key,iv) if decrypt else encrypt_cbc(data,key,iv).
        return decrypt_cbc(data,key,iv) if decrypt else encrypt_cbc(data,key,iv)
    # BARIS ASLI 209: Di crypt: Memilih jalur operasi sesuai backend atau jenis algoritma.
    if backend!='library':raise ValueError('Backend harus library atau manual.')
    # BARIS ASLI 210: Di crypt: Menghitung/menyiapkan nilai module untuk dipakai oleh proses berikutnya.
    module=DES if algorithm=='DES' else DES3
    # BARIS ASLI 211: Di crypt: Membuat cipher dari PyCryptodome untuk implementasi library/pembanding.
    cipher=module.new(key,module.MODE_CBC,iv=iv)
    # BARIS ASLI 212: Di crypt: Mengembalikan nilai perhitungan ke pemanggil: cipher.decrypt(data) if decrypt else cipher.encrypt(data).
    return cipher.decrypt(data) if decrypt else cipher.encrypt(data)


# BARIS ASLI 214: Mendefinisikan fungsi encrypt_bytes. Mem-padding plaintext, membuat IV acak jika tidak disediakan, dan mengenkripsi byte.
def encrypt_bytes(data,key,backend='library',iv=None,algorithm='DES'):
    # BARIS ASLI 215: Di encrypt_bytes: Menjalankan langkah validate_algorithm_key(key,algorithm) sebagai bagian dari alur fungsi ini.
    validate_algorithm_key(key,algorithm)
    # BARIS ASLI 216: Di encrypt_bytes: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: iv is None:iv=secrets.token_bytes(8).
    if iv is None:iv=secrets.token_bytes(8)
    # BARIS ASLI 217: Di encrypt_bytes: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
    if len(iv)!=8:raise ValueError('IV CBC harus 8 byte untuk DES maupun 3DES.')
    # BARIS ASLI 218: Di encrypt_bytes: Menghitung/menyiapkan nilai ciphertext untuk dipakai oleh proses berikutnya.
    ciphertext=crypt(pad(data),key,iv,backend,algorithm=algorithm)
    # BARIS ASLI 219: Di encrypt_bytes: Mengembalikan nilai perhitungan ke pemanggil: {'version':1,'algorithm':algorithm,'mode':'CBC','padding':'PKCS7',.
    return {'version':1,'algorithm':algorithm,'mode':'CBC','padding':'PKCS7',
            # BARIS ASLI 220: Di encrypt_bytes: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
            'iv_hex':iv.hex(),'ciphertext_hex':ciphertext.hex()}


# BARIS ASLI 222: Mendefinisikan fungsi decrypt_record. Memvalidasi metadata ciphertext lalu mendekripsi dan membuang padding.
def decrypt_record(record,key,backend='library'):
    # BARIS ASLI 223: Di decrypt_record: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: not isinstance(record,dict):raise ValueError('Data ciphertext tidak valid.').
    if not isinstance(record,dict):raise ValueError('Data ciphertext tidak valid.')
    # BARIS ASLI 224: Di decrypt_record: Menghitung/menyiapkan nilai algorithm untuk dipakai oleh proses berikutnya.
    algorithm=record.get('algorithm')
    # BARIS ASLI 225: Di decrypt_record: Menjalankan langkah validate_algorithm_key(key,algorithm) sebagai bagian dari alur fungsi ini.
    validate_algorithm_key(key,algorithm)
    # BARIS ASLI 226: Di decrypt_record: Menghitung/menyiapkan nilai expected untuk dipakai oleh proses berikutnya.
    expected={'version':1,'padding':'PKCS7'}
    # BARIS ASLI 227: Di decrypt_record: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: record.get('mode') not in ('CBC','ECB'):raise ValueError('Mode ciphertext tidak....
    if record.get('mode') not in ('CBC','ECB'):raise ValueError('Mode ciphertext tidak didukung.')
    # BARIS ASLI 228: Di decrypt_record: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: any(record.get(k)!=v for k,v in expected.items()):raise ValueError('Format ciph....
    if any(record.get(k)!=v for k,v in expected.items()):raise ValueError('Format ciphertext tidak didukung.')
    # BARIS ASLI 229: Di decrypt_record: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: not isinstance(record.get('iv_hex'),str) or not isinstance(record.get('cipherte....
    if not isinstance(record.get('iv_hex'),str) or not isinstance(record.get('ciphertext_hex'),str):
        # BARIS ASLI 230: Di decrypt_record: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
        raise ValueError('IV dan ciphertext hex tidak ditemukan atau tipe salah.')
    # BARIS ASLI 231: Di decrypt_record: Menghitung/menyiapkan nilai iv untuk dipakai oleh proses berikutnya.
    iv=parse_hex(record['iv_hex'],8,'IV') if record['mode']=='CBC' else b''
    # BARIS ASLI 232: Di decrypt_record: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
    try:ciphertext=bytes.fromhex(record['ciphertext_hex'])
    # BARIS ASLI 233: Di decrypt_record: Menangani kesalahan ValueError as excraise ValueError('Ciphertext bukan hex yang valid.....
    except ValueError as exc:raise ValueError('Ciphertext bukan hex yang valid.') from exc
    # BARIS ASLI 234: Di decrypt_record: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
    if not ciphertext or len(ciphertext)%8:raise ValueError('Ciphertext harus tidak kosong dan kelipatan 8 byte.')
    # BARIS ASLI 235: Di decrypt_record: Mengembalikan paket data/metadata ciphertext yang siap dipakai.
    return unpad(ecb_blocks(ciphertext,key,backend,algorithm,True) if record['mode']=='ECB' else crypt(ciphertext,key,iv,backend,decrypt=True,algorithm=algorithm))


# BARIS ASLI 238: Mendefinisikan fungsi ecb_blocks. Memproses blok DES/3DES dalam ECB sesuai implementasi manual atau library.
def ecb_blocks(data,key,backend,algorithm,decrypt=False):
    # BARIS ASLI 239: Di ecb_blocks: Menjalankan langkah validate_algorithm_key(key,algorithm) sebagai bagian dari alur fungsi ini.
    validate_algorithm_key(key,algorithm)
    # BARIS ASLI 240: Di ecb_blocks: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
    if not data or len(data)%8:raise ValueError('Data ECB harus kelipatan 8 byte.')
    # BARIS ASLI 241: Di ecb_blocks: Memilih jalur operasi sesuai backend atau jenis algoritma.
    if backend=='library':
        # BARIS ASLI 242: Di ecb_blocks: Membuat cipher dari PyCryptodome untuk implementasi library/pembanding.
        module=DES if algorithm=='DES' else DES3;cipher=module.new(key,module.MODE_ECB)
        # BARIS ASLI 243: Di ecb_blocks: Mengembalikan nilai perhitungan ke pemanggil: cipher.decrypt(data) if decrypt else cipher.encrypt(data).
        return cipher.decrypt(data) if decrypt else cipher.encrypt(data)
    # BARIS ASLI 244: Di ecb_blocks: Memilih jalur operasi sesuai backend atau jenis algoritma.
    if backend!='manual':raise ValueError('Implementasi tidak dikenal.')
    # BARIS ASLI 245: Di ecb_blocks: Menghitung/menyiapkan nilai engine untuk dipakai oleh proses berikutnya.
    engine=DESManual(key) if algorithm=='DES' else TripleDESManual(key)
    # BARIS ASLI 246: Di ecb_blocks: Menghitung/menyiapkan nilai method untuk dipakai oleh proses berikutnya.
    method=engine.decrypt_block if decrypt else engine.encrypt_block
    # BARIS ASLI 247: Di ecb_blocks: Mengembalikan nilai perhitungan ke pemanggil: b''.join(method(data[i:i+8]) for i in range(0,len(data),8)).
    return b''.join(method(data[i:i+8]) for i in range(0,len(data),8))


# BARIS ASLI 250: Mendefinisikan fungsi encrypt_message. Memilih keluaran mode ECB atau CBC untuk enkripsi pesan.
def encrypt_message(data,key,backend,algorithm,wire_format):
    # BARIS ASLI 251: Di encrypt_message: Memeriksa jenis format atau mode penyimpanan data.
    if wire_format=='ecb':
        # BARIS ASLI 252: Di encrypt_message: Mengembalikan nilai perhitungan ke pemanggil: {'version':1,'algorithm':algorithm,'mode':'ECB','padding':'PKCS7','iv_hex':'','cip....
        return {'version':1,'algorithm':algorithm,'mode':'ECB','padding':'PKCS7','iv_hex':'','ciphertext_hex':ecb_blocks(pad(data),key,backend,algorithm).hex()}
    # BARIS ASLI 253: Di encrypt_message: Mengembalikan data dalam representasi byte.
    return encrypt_bytes(data,key,backend,algorithm=algorithm)
