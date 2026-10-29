# -*- coding: utf-8 -*-
"""Modul des_manual untuk ZarCryptoDES."""

from constants import E, FP, IP, P, PC1, PC2, SBOX, SHIFTS

# BARIS ASLI 55: Mendefinisikan fungsi permute. Memilih dan menyusun ulang bit sesuai tabel permutasi DES.
def permute(value, table, width):
    # BARIS ASLI 56: Di permute: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
    """Pilih bit berdasarkan tabel permutasi, dari kiri ke kanan."""
    # BARIS ASLI 57: Di permute: Menghitung/menyiapkan nilai out untuk dipakai oleh proses berikutnya.
    out = 0
    # BARIS ASLI 58: Di permute: Melakukan iterasi pada elemen/urutan: position in table.
    for position in table:
        # BARIS ASLI 59: Di permute: Memakai geser bit untuk mengambil, menggabungkan, atau memutar bagian data biner.
        out = (out << 1) | ((value >> (width - position)) & 1)
    # BARIS ASLI 60: Di permute: Mengembalikan hasil akumulasi pemrosesan.
    return out


# BARIS ASLI 62: Mendefinisikan fungsi make_subkeys. Menghasilkan 16 subkunci DES dari kunci 64-bit melalui PC-1, pergeseran kiri, dan PC-2.
def make_subkeys(key):
    # BARIS ASLI 63: Di make_subkeys: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
    if len(key) != 8:
        # BARIS ASLI 64: Di make_subkeys: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
        raise ValueError('Kunci DES harus tepat 8 byte.')
    # BARIS ASLI 65: Di make_subkeys: Mengubah urutan byte menjadi bilangan bulat untuk operasi bit.
    selected = permute(int.from_bytes(key, 'big'), PC1, 64)
    # BARIS ASLI 66: Di make_subkeys: Memakai geser bit untuk mengambil, menggabungkan, atau memutar bagian data biner.
    c, d = selected >> 28, selected & 0xFFFFFFF
    # BARIS ASLI 67: Di make_subkeys: Mengolah subkunci DES 48-bit yang digunakan pada tiap ronde.
    subkeys = []
    # BARIS ASLI 68: Di make_subkeys: Menerapkan jadwal pergeseran 16 subkunci DES.
    for shift in SHIFTS:
        # BARIS ASLI 69: Di make_subkeys: Memakai geser bit untuk mengambil, menggabungkan, atau memutar bagian data biner.
        c = ((c << shift) | (c >> (28 - shift))) & 0xFFFFFFF
        # BARIS ASLI 70: Di make_subkeys: Memakai geser bit untuk mengambil, menggabungkan, atau memutar bagian data biner.
        d = ((d << shift) | (d >> (28 - shift))) & 0xFFFFFFF
        # BARIS ASLI 71: Di make_subkeys: Memakai geser bit untuk mengambil, menggabungkan, atau memutar bagian data biner.
        subkeys.append(permute((c << 28) | d, PC2, 56))
    # BARIS ASLI 72: Di make_subkeys: Mengembalikan nilai perhitungan ke pemanggil: tuple(subkeys).
    return tuple(subkeys)


# BARIS ASLI 74: Mendefinisikan fungsi round_function. Menghitung F(R,K): ekspansi E, XOR subkunci, substitusi S-Box, lalu permutasi P.
def round_function(right, subkey):
    # BARIS ASLI 75: Di round_function: Menggunakan operator XOR (^) pada bit; berbeda 1 menghasilkan 1, sama menghasilkan 0.
    mixed = permute(right, E, 32) ^ subkey
    # BARIS ASLI 76: Di round_function: Menghitung/menyiapkan nilai substituted untuk dipakai oleh proses berikutnya.
    substituted = 0
    # BARIS ASLI 77: Di round_function: Memproses delapan S-Box pada fungsi F DES.
    for i, box in enumerate(SBOX):
        # BARIS ASLI 78: Di round_function: Memakai geser bit untuk mengambil, menggabungkan, atau memutar bagian data biner.
        six = (mixed >> (42 - 6 * i)) & 0x3F
        # BARIS ASLI 79: Di round_function: Memakai geser bit untuk mengambil, menggabungkan, atau memutar bagian data biner.
        row = ((six & 0x20) >> 4) | (six & 1)
        # BARIS ASLI 80: Di round_function: Memakai geser bit untuk mengambil, menggabungkan, atau memutar bagian data biner.
        column = (six >> 1) & 0xF
        # BARIS ASLI 81: Di round_function: Memakai geser bit untuk mengambil, menggabungkan, atau memutar bagian data biner.
        substituted = (substituted << 4) | box[row][column]
    # BARIS ASLI 82: Di round_function: Mengembalikan hasil permutasi bit ke pemanggil.
    return permute(substituted, P, 32)


# BARIS ASLI 84: Mendefinisikan kelas DESManual. Mesin DES standar buatan sendiri yang memproses blok 64-bit dengan 16 ronde Feistel.
class DESManual:
    # BARIS ASLI 85: Di DESManual: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
    """Enkripsi/dekripsi satu blok DES 8 byte, big endian."""
    # BARIS ASLI 86: Mendefinisikan fungsi __init__. Fungsi ini menangani aksi khusus dalam aplikasi.
    def __init__(self, key):
        # BARIS ASLI 87: Di __init__: Mengolah subkunci DES 48-bit yang digunakan pada tiap ronde.
        self.subkeys = make_subkeys(key)

    # BARIS ASLI 89: Mendefinisikan fungsi _process. Menjalankan 16 ronde Feistel dan permutasi awal/akhir, serta merekam jejak jika diminta.
    def _process(self, block, subkeys, trace=None):
        # BARIS ASLI 90: Di _process: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
        if len(block) != 8:
            # BARIS ASLI 91: Di _process: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
            raise ValueError('Satu blok DES harus tepat 8 byte.')
        # BARIS ASLI 92: Di _process: Mengubah urutan byte menjadi bilangan bulat untuk operasi bit.
        state = permute(int.from_bytes(block, 'big'), IP, 64)
        # BARIS ASLI 93: Di _process: Memakai geser bit untuk mengambil, menggabungkan, atau memutar bagian data biner.
        left, right = state >> 32, state & 0xFFFFFFFF
        # BARIS ASLI 94: Di _process: Memastikan perekaman jejak ronde memang diminta.
        if trace is not None:
            # BARIS ASLI 95: Di _process: Mencatat nilai ronde agar dapat ditampilkan pada visualisasi dan laporan.
            trace.append({'round': 0, 'L': f'{left:08X}', 'R': f'{right:08X}', 'K': None})
        # BARIS ASLI 96: Di _process: Menelusuri subkunci yang dipakai dalam 16 ronde DES.
        for i, key in enumerate(subkeys, 1):
            # BARIS ASLI 97: Di _process: Menggunakan operator XOR (^) pada bit; berbeda 1 menghasilkan 1, sama menghasilkan 0.
            left, right = right, left ^ round_function(right, key)
            # BARIS ASLI 98: Di _process: Memastikan perekaman jejak ronde memang diminta.
            if trace is not None:
                # BARIS ASLI 99: Di _process: Mencatat nilai ronde agar dapat ditampilkan pada visualisasi dan laporan.
                trace.append({'round': i, 'L': f'{left:08X}', 'R': f'{right:08X}', 'K': f'{key:012X}'})
        # Preoutput DES adalah R16 || L16, dilanjutkan invers IP.
        # BARIS ASLI 101: Di _process: Mengembalikan hasil permutasi bit ke pemanggil.
        return permute((right << 32) | left, FP, 64).to_bytes(8, 'big')

    # BARIS ASLI 103: Mendefinisikan fungsi encrypt_block. Mengenkripsi satu blok DES menggunakan subkunci dengan urutan maju.
    def encrypt_block(self, block, trace=None):
        # BARIS ASLI 104: Di encrypt_block: Mengembalikan keluaran metode/hasil pemrosesan objek.
        return self._process(block, self.subkeys, trace)

    # BARIS ASLI 106: Mendefinisikan fungsi decrypt_block. Mendekripsi satu blok DES dengan urutan subkunci dibalik.
    def decrypt_block(self, block, trace=None):
        # BARIS ASLI 107: Di decrypt_block: Mengembalikan keluaran metode/hasil pemrosesan objek.
        return self._process(block, self.subkeys[::-1], trace)


# BARIS ASLI 109: Mendefinisikan fungsi xor_bytes. Meng-XOR setiap pasangan byte dari dua rangkaian data.
def xor_bytes(a, b):
    # BARIS ASLI 110: Di xor_bytes: Mengembalikan data dalam representasi byte.
    return bytes(x ^ y for x, y in zip(a, b))


# BARIS ASLI 112: Mendefinisikan fungsi validate_cbc. Memastikan IV 8 byte dan data sesuai kelipatan blok DES.
def validate_cbc(data, iv):
    # BARIS ASLI 113: Di validate_cbc: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
    if len(iv) != 8:
        # BARIS ASLI 114: Di validate_cbc: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
        raise ValueError('IV DES-CBC harus tepat 8 byte.')
    # BARIS ASLI 115: Di validate_cbc: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
    if not data or len(data) % 8:
        # BARIS ASLI 116: Di validate_cbc: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
        raise ValueError('Data CBC harus tidak kosong dan kelipatan 8 byte.')


# BARIS ASLI 118: Mendefinisikan fungsi encrypt_cbc. Mengenkripsi semua blok DES pada mode CBC, dengan XOR terhadap IV/ciphertext sebelumnya.
def encrypt_cbc(data, key, iv):
    # BARIS ASLI 119: Di encrypt_cbc: Menghitung/menyiapkan nilai """Masukan sudah di-padding; CBC mema... untuk dipakai oleh proses berikutnya.
    """Masukan sudah di-padding; CBC memakai C_i=E(P_i XOR C_(i-1))."""
    # BARIS ASLI 120: Di encrypt_cbc: Menjalankan langkah validate_cbc(data, iv) sebagai bagian dari alur fungsi ini.
    validate_cbc(data, iv)
    # BARIS ASLI 121: Di encrypt_cbc: Menghitung/menyiapkan nilai des, previous, output untuk dipakai oleh proses berikutnya.
    des, previous, output = DESManual(key), iv, bytearray()
    # BARIS ASLI 122: Di encrypt_cbc: Menelusuri data per blok agar tiap iterasi memproses ukuran yang sesuai.
    for start in range(0, len(data), 8):
        # BARIS ASLI 123: Di encrypt_cbc: Menerapkan XOR per byte sebagai bagian dari mode CBC.
        previous = des.encrypt_block(xor_bytes(data[start:start+8], previous))
        # BARIS ASLI 124: Di encrypt_cbc: Menambahkan kumpulan byte/elemen ke hasil sementara.
        output.extend(previous)
    # BARIS ASLI 125: Di encrypt_cbc: Mengembalikan data dalam representasi byte.
    return bytes(output)


# BARIS ASLI 127: Mendefinisikan fungsi decrypt_cbc. Mendekripsi blok DES-CBC dan melakukan XOR untuk memulihkan plaintext.
def decrypt_cbc(data, key, iv):
    # BARIS ASLI 128: Di decrypt_cbc: Menjalankan langkah validate_cbc(data, iv) sebagai bagian dari alur fungsi ini.
    validate_cbc(data, iv)
    # BARIS ASLI 129: Di decrypt_cbc: Menghitung/menyiapkan nilai des, previous, output untuk dipakai oleh proses berikutnya.
    des, previous, output = DESManual(key), iv, bytearray()
    # BARIS ASLI 130: Di decrypt_cbc: Menelusuri data per blok agar tiap iterasi memproses ukuran yang sesuai.
    for start in range(0, len(data), 8):
        # BARIS ASLI 131: Di decrypt_cbc: Menghitung/menyiapkan nilai block untuk dipakai oleh proses berikutnya.
        block = data[start:start+8]
        # BARIS ASLI 132: Di decrypt_cbc: Menerapkan XOR per byte sebagai bagian dari mode CBC.
        output.extend(xor_bytes(des.decrypt_block(block), previous))
        # BARIS ASLI 133: Di decrypt_cbc: Menghitung/menyiapkan nilai previous untuk dipakai oleh proses berikutnya.
        previous = block
    # BARIS ASLI 134: Di decrypt_cbc: Mengembalikan data dalam representasi byte.
    return bytes(output)
