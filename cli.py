# -*- coding: utf-8 -*-
"""Modul cli untuk ZarCryptoDES."""

from pathlib import Path
from cipher import decrypt_record, encrypt_message
from ciphertext import parse_ciphertext, serialize_ciphertext
from keys import parse_key

# BARIS ASLI 3119: Mendefinisikan fungsi terminal_library. Menjalankan mode penggunaan library di terminal.
def terminal_library():
    # BARIS ASLI 3120: Di terminal_library: Menulis status atau hasil pemeriksaan ke terminal.
    print('ZarCryptoDES — terminal pembanding PyCryptodome. Ctrl+C untuk keluar.')
    # BARIS ASLI 3121: Di terminal_library: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
    try:
        # BARIS ASLI 3122: Di terminal_library: Mengulang sampai kriteria True terpenuhi.
        while True:
            # BARIS ASLI 3123: Di terminal_library: Memakai operasi bit AND/OR untuk menyeleksi atau menggabungkan bit.
            action=input('\n1 Enkripsi | 2 Dekripsi | 0 Keluar: ').strip()
            # BARIS ASLI 3124: Di terminal_library: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: action=='0':return.
            if action=='0':return
            # BARIS ASLI 3125: Di terminal_library: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: action not in ('1','2'):continue.
            if action not in ('1','2'):continue
            # BARIS ASLI 3126: Di terminal_library: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
            try:
                # BARIS ASLI 3127: Di terminal_library: Menghitung/menyiapkan nilai algorithm untuk dipakai oleh proses berikutnya.
                algorithm=input('Algoritma DES / 3DES: ').strip().upper()
                # BARIS ASLI 3128: Di terminal_library: Mendekode teks heksadesimal menjadi representasi byte.
                key_format=input('Jenis kunci hex / text [hex]: ').strip().lower() or 'hex'
                key=parse_key(input('Kunci: '),algorithm,key_format)
                # BARIS ASLI 3129: Di terminal_library: Menghitung/menyiapkan nilai fmt untuk dipakai oleh proses berikutnya.
                fmt=input('Format zar / cbc / ecb [cbc]: ').strip().lower() or 'cbc'
                # BARIS ASLI 3130: Di terminal_library: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: fmt not in ('zar','cbc','ecb'):raise ValueError('Format harus zar, cbc, atau ec....
                if fmt not in ('zar','cbc','ecb'):raise ValueError('Format harus zar, cbc, atau ecb.')
                # BARIS ASLI 3131: Di terminal_library: Menghitung/menyiapkan nilai source untuk dipakai oleh proses berikutnya.
                source=Path(input('Path file TXT masukan: ').strip().strip('"'))
                # BARIS ASLI 3132: Di terminal_library: Menghitung/menyiapkan nilai destination untuk dipakai oleh proses berikutnya.
                destination=Path(input('Path file TXT keluaran: ').strip().strip('"')).with_suffix('.txt')
                # BARIS ASLI 3133: Di terminal_library: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: source.resolve()==destination.resolve():raise ValueError('Masukan dan keluaran ....
                if source.resolve()==destination.resolve():raise ValueError('Masukan dan keluaran harus berbeda.')
                # BARIS ASLI 3134: Di terminal_library: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: action=='1'.
                if action=='1':
                    # BARIS ASLI 3135: Di terminal_library: Membaca seluruh konten file sebagai byte/teks.
                    record=encrypt_message(source.read_bytes(),key,'library',algorithm,fmt);output=serialize_ciphertext(record,fmt).encode()
                # BARIS ASLI 3136: Di terminal_library: Cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
                else:
                    # BARIS ASLI 3137: Di terminal_library: Membaca seluruh konten file sebagai byte/teks.
                    record=parse_ciphertext(source.read_text(encoding='utf-8'),algorithm,wire_format=fmt)
                    # BARIS ASLI 3138: Di terminal_library: Memilih jalur operasi sesuai backend atau jenis algoritma.
                    if record['algorithm']!=algorithm:raise ValueError('Algoritma tidak cocok dengan file.')
                    # BARIS ASLI 3139: Di terminal_library: Memulihkan plaintext berdasarkan metadata ciphertext dan kunci.
                    output=decrypt_record(record,key,'library')
                # BARIS ASLI 3140: Di terminal_library: Menyimpan byte/teks hasil operasi ke berkas yang dipilih.
                destination.write_bytes(output);print('BERHASIL:',destination)
            # BARIS ASLI 3141: Di terminal_library: Menangani kesalahan (ValueError,OSError) as excprint('GAGAL',exc).
            except (ValueError,OSError) as exc:print('GAGAL:',exc)
    # BARIS ASLI 3142: Di terminal_library: Menangani kesalahan (EOFError,KeyboardInterrupt)print('\nTerminal ditutup.').
    except (EOFError,KeyboardInterrupt):print('\nTerminal ditutup.')
