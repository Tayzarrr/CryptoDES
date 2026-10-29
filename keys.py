# -*- coding: utf-8 -*-
"""Modul keys untuk ZarCryptoDES."""

import secrets

# BARIS ASLI 137: Mendefinisikan fungsi validate_algorithm_key. Memeriksa algoritma, ukuran kunci, dan kunci 3DES yang merosot menjadi DES tunggal.
def validate_algorithm_key(key, algorithm='DES'):
    # DES memakai 8 byte; 3DES menerima dua kunci 16 byte atau tiga kunci 24 byte.
    if algorithm not in ('DES', '3DES'):
        raise ValueError('Algoritma harus DES atau 3DES.')
    allowed = (8,) if algorithm == 'DES' else (16, 24)
    if len(key) not in allowed:
        sizes = '8 byte (16 digit HEX)' if algorithm == 'DES' else '16 atau 24 byte (32 atau 48 digit HEX)'
        raise ValueError(f'Kunci {algorithm} harus {sizes}. Untuk teks, ukuran dihitung setelah encoding UTF-8.')
    if algorithm == '3DES':
        # Bentuk dua kunci menggunakan K3 = K1; byte asli tidak dipotong atau di-hash.
        expanded = key + key[:8] if len(key) == 16 else key
        effective = [bytes(b & 0xFE for b in expanded[i:i+8]) for i in (0, 8, 16)]
        if effective[0] == effective[1] or effective[1] == effective[2]:
            raise ValueError('Kunci 3DES menyusut menjadi DES tunggal. Gunakan kunci lain atau generate ulang.')
    return key


def parse_key(value, algorithm='DES', key_format='hex'):
    # Format dipilih secara eksplisit agar teks yang kebetulan berisi angka HEX tidak salah dibaca.
    if key_format == 'hex':
        try:
            key = bytes.fromhex(value)
        except ValueError as exc:
            raise ValueError('Kunci bukan HEX yang valid. Pilih jenis kunci Teks UTF-8 untuk kunci biasa.') from exc
    elif key_format == 'text':
        # Spasi dan kapitalisasi merupakan bagian kunci; tidak menggunakan strip(), padding, atau hash.
        key = value.encode('utf-8')
    else:
        raise ValueError('Jenis kunci harus HEX atau Teks UTF-8.')
    return validate_algorithm_key(key, algorithm)


# BARIS ASLI 151: Mendefinisikan fungsi random_3des_key. Membangkitkan kunci 3DES acak 24 byte dengan paritas ganjil yang sesuai.
def random_3des_key():
    # BARIS ASLI 152: Di random_3des_key: Mengulang sampai kriteria True terpenuhi.
    while True:
        # Odd parity pada masing-masing byte; inti manual tidak memanggil DES3.
        # BARIS ASLI 154: Di random_3des_key: Memakai pembangkit acak kriptografis untuk kunci atau IV.
        raw=secrets.token_bytes(24)
        # BARIS ASLI 155: Di random_3des_key: Menggunakan operator XOR (^) pada bit; berbeda 1 menghasilkan 1, sama menghasilkan 0.
        key=bytes((b & 0xFE) | (1 ^ ((b & 0xFE).bit_count() & 1)) for b in raw)
        # BARIS ASLI 156: Di random_3des_key: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
        try:return validate_algorithm_key(key,'3DES')
        # BARIS ASLI 157: Di random_3des_key: Menangani kesalahan ValueErrorpass.
        except ValueError:pass
