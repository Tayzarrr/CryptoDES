# -*- coding: utf-8 -*-
"""Modul file_ops untuk ZarCryptoDES."""

from pathlib import Path
from cipher import decrypt_record, encrypt_bytes
from ciphertext import parse_ciphertext, serialize_ciphertext

# BARIS ASLI 363: Mendefinisikan fungsi process_file. Mengelola pembacaan file, enkripsi/dekripsi, dan penulisan hasil ke file lain.
def process_file(operation, backend, key, source, destination, algorithm='DES', iv_hex=''):
    # BARIS ASLI 364: Di process_file: Menghitung/menyiapkan nilai source, destination untuk dipakai oleh proses berikutnya.
    source, destination = Path(source), Path(destination)
    # BARIS ASLI 365: Di process_file: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: source.resolve() == destination.resolve().
    if source.resolve() == destination.resolve():
        # BARIS ASLI 366: Di process_file: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
        raise ValueError('File masukan dan keluaran harus berbeda.')
    # BARIS ASLI 367: Di process_file: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: operation == 'encrypt'.
    if operation == 'encrypt':
        # BARIS ASLI 368: Di process_file: Membaca seluruh konten file sebagai byte/teks.
        data = source.read_bytes()
        # BARIS ASLI 369: Di process_file: Memanggil operasi enkripsi lalu membentuk metadata ciphertext.
        record = encrypt_bytes(data, key, backend, algorithm=algorithm)
        # BARIS ASLI 370: Di process_file: Menghitung/menyiapkan nilai payload untuk dipakai oleh proses berikutnya.
        payload = serialize_ciphertext(record).encode('utf-8')
        # BARIS ASLI 371: Di process_file: Mendekode teks heksadesimal menjadi representasi byte.
        result = {'input_bytes': len(data), 'output_bytes': len(bytes.fromhex(record['ciphertext_hex'])),
                  # BARIS ASLI 372: Di process_file: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
                  'preview': payload.decode('utf-8').strip(), 'iv': record['iv_hex']}
    # BARIS ASLI 373: Di process_file: Cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
    else:
        # BARIS ASLI 374: Di process_file: Membaca seluruh konten file sebagai byte/teks.
        raw = source.read_text(encoding='utf-8')
        # BARIS ASLI 375: Di process_file: Menghitung/menyiapkan nilai record untuk dipakai oleh proses berikutnya.
        record = parse_ciphertext(raw,algorithm,iv_hex)
        # BARIS ASLI 376: Di process_file: Memulihkan plaintext berdasarkan metadata ciphertext dan kunci.
        payload = decrypt_record(record, key, backend)
        # BARIS ASLI 377: Di process_file: Mendekode teks heksadesimal menjadi representasi byte.
        result = {'input_bytes': len(bytes.fromhex(record['ciphertext_hex'])), 'output_bytes': len(payload),
                  # BARIS ASLI 378: Di process_file: Menghitung/menyiapkan nilai 'preview': payload.decode('utf-8', er... untuk dipakai oleh proses berikutnya.
                  'preview': payload.decode('utf-8', errors='replace'), 'iv': record['iv_hex']}
    # BARIS ASLI 379: Di process_file: Menyimpan byte/teks hasil operasi ke berkas yang dipilih.
    destination.write_bytes(payload)
    # BARIS ASLI 380: Di process_file: Menghitung/menyiapkan nilai result['path'] untuk dipakai oleh proses berikutnya.
    result['path'] = str(destination.resolve())
    # BARIS ASLI 381: Di process_file: Menghitung/menyiapkan nilai result['operation'] untuk dipakai oleh proses berikutnya.
    result['operation'] = operation
    # BARIS ASLI 382: Di process_file: Mengembalikan nilai perhitungan ke pemanggil: result.
    return result
