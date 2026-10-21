# Dokumentasikan tujuan atau perilaku bagian kode ini.
"""Tabel permutasi, rotasi, dan S-box DES standar."""

# Tetapkan permutasi awal 64 bit DES.
IP = (
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    58,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    50,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    42,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    34,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    26,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    18,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    10,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    2,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    60,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    52,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    44,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    36,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    28,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    20,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    12,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    4,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    62,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    54,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    46,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    38,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    30,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    22,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    14,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    6,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    64,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    56,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    48,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    40,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    32,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    24,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    16,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    8,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    57,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    49,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    41,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    33,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    25,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    17,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    9,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    1,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    59,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    51,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    43,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    35,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    27,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    19,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    11,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    3,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    61,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    53,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    45,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    37,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    29,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    21,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    13,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    5,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    63,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    55,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    47,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    39,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    31,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    23,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    15,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    7,
# Tutup pengelompokan sintaks di atas.
)
# Tetapkan permutasi akhir DES (invers IP).
FP = (
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    40,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    8,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    48,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    16,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    56,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    24,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    64,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    32,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    39,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    7,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    47,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    15,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    55,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    23,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    63,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    31,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    38,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    6,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    46,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    14,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    54,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    22,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    62,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    30,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    37,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    5,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    45,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    13,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    53,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    21,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    61,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    29,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    36,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    4,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    44,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    12,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    52,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    20,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    60,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    28,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    35,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    3,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    43,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    11,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    51,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    19,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    59,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    27,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    34,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    2,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    42,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    10,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    50,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    18,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    58,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    26,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    33,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    1,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    41,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    9,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    49,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    17,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    57,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    25,
# Tutup pengelompokan sintaks di atas.
)
# Tetapkan ekspansi sisi kanan dari 32 ke 48 bit.
E = (
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    32,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    1,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    2,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    3,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    4,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    5,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    4,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    5,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    6,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    7,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    8,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    9,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    8,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    9,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    10,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    11,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    12,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    13,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    12,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    13,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    14,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    15,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    16,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    17,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    16,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    17,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    18,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    19,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    20,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    21,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    20,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    21,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    22,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    23,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    24,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    25,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    24,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    25,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    26,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    27,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    28,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    29,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    28,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    29,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    30,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    31,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    32,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    1,
# Tutup pengelompokan sintaks di atas.
)
# Tetapkan permutasi keluaran S-box.
P = (
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    16,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    7,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    20,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    21,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    29,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    12,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    28,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    17,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    1,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    15,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    23,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    26,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    5,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    18,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    31,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    10,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    2,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    8,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    24,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    14,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    32,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    27,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    3,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    9,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    19,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    13,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    30,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    6,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    22,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    11,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    4,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    25,
# Tutup pengelompokan sintaks di atas.
)
# Tetapkan seleksi 56 bit material kunci DES.
PC1 = (
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    57,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    49,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    41,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    33,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    25,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    17,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    9,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    1,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    58,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    50,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    42,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    34,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    26,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    18,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    10,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    2,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    59,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    51,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    43,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    35,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    27,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    19,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    11,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    3,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    60,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    52,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    44,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    36,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    63,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    55,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    47,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    39,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    31,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    23,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    15,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    7,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    62,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    54,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    46,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    38,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    30,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    22,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    14,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    6,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    61,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    53,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    45,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    37,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    29,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    21,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    13,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    5,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    28,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    20,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    12,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    4,
# Tutup pengelompokan sintaks di atas.
)
# Tetapkan seleksi subkunci ronde 48 bit.
PC2 = (
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    14,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    17,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    11,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    24,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    1,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    5,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    3,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    28,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    15,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    6,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    21,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    10,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    23,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    19,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    12,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    4,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    26,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    8,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    16,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    7,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    27,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    20,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    13,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    2,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    41,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    52,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    31,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    37,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    47,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    55,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    30,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    40,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    51,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    45,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    33,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    48,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    44,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    49,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    39,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    56,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    34,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    53,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    46,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    42,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    50,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    36,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    29,
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    32,
# Tutup pengelompokan sintaks di atas.
)
# Tetapkan jadwal rotasi C dan D untuk 16 ronde.
SHIFTS = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)
# Tetapkan delapan S-box DES, masing-masing memetakan 6 bit ke 4 bit.
SBOX = (
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    (
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13),
    # Tutup pengelompokan sintaks di atas.
    ),
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    (
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9),
    # Tutup pengelompokan sintaks di atas.
    ),
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    (
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12),
    # Tutup pengelompokan sintaks di atas.
    ),
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    (
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14),
    # Tutup pengelompokan sintaks di atas.
    ),
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    (
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3),
    # Tutup pengelompokan sintaks di atas.
    ),
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    (
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13),
    # Tutup pengelompokan sintaks di atas.
    ),
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    (
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12),
    # Tutup pengelompokan sintaks di atas.
    ),
    # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
    (
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
        # Nilai tabel DES standar; urutan indeksnya dipakai oleh operasi bit.
        (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11),
    # Tutup pengelompokan sintaks di atas.
    ),
# Tutup pengelompokan sintaks di atas.
)
