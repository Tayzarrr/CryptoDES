# Dokumentasikan tujuan atau perilaku bagian kode ini.
"""Terminal interaktif pembanding yang selalu memilih backend PyCryptodome."""

# Impor komponen dari pathlib untuk modul ini.
from pathlib import Path
# Impor komponen dari .crypto.keys untuk modul ini.
from .crypto.keys import validate_algorithm_key
# Impor komponen dari .crypto.cipher untuk modul ini.
from .crypto.cipher import encrypt_message, decrypt_record
# Impor komponen dari .crypto.formats untuk modul ini.
from .crypto.formats import serialize_ciphertext, parse_ciphertext


# Jalankan alur terminal yang selalu memakai backend PyCryptodome.
def terminal_library():
    # Panggil print dengan argumen yang ditentukan.
    print("ZarCryptoDES — terminal pembanding PyCryptodome. Ctrl+C untuk keluar.")
    # Mulai operasi yang dapat menimbulkan kesalahan.
    try:
        # Ulangi proses selama kondisi masih terpenuhi.
        while True:
            # Simpan hasil input('\n1 Enkripsi | 2 Dekripsi | 0 Keluar: ').strip pada action.
            action = input("\n1 Enkripsi | 2 Dekripsi | 0 Keluar: ").strip()
            # Pilih langkah berdasarkan kondisi action == '0'.
            if action == "0":
                # Akhiri fungsi tanpa hasil tambahan.
                return
            # Pilih langkah berdasarkan kondisi action not in ('1', '2').
            if action not in ("1", "2"):
                # Lanjutkan ke iterasi berikutnya.
                continue
            # Mulai operasi yang dapat menimbulkan kesalahan.
            try:
                # Tetapkan pilihan DES atau 3DES.
                algorithm = input("Algoritma DES / 3DES: ").strip().upper()
                # Tetapkan kunci dalam bentuk byte.
                key = validate_algorithm_key(bytes.fromhex(input("Kunci HEX: ").strip()), algorithm)
                # Tetapkan nilai fmt untuk langkah berikutnya.
                fmt = input("Format zar / cbc / ecb [cbc]: ").strip().lower() or "cbc"
                # Pilih langkah berdasarkan kondisi fmt not in ('zar', 'cbc', 'ecb').
                if fmt not in ("zar", "cbc", "ecb"):
                    # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
                    raise ValueError("Format harus zar, cbc, atau ecb.")
                # Tetapkan lokasi berkas masukan.
                source = Path(input("Path file TXT masukan: ").strip().strip('"'))
                # Tetapkan lokasi berkas keluaran.
                destination = Path(
                    # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
                    input("Path file TXT keluaran: ").strip().strip('"')
                # Tutup pengelompokan sintaks di atas.
                ).with_suffix(".txt")
                # Pilih langkah berdasarkan kondisi source.resolve() == destination.resolve().
                if source.resolve() == destination.resolve():
                    # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
                    raise ValueError("Masukan dan keluaran harus berbeda.")
                # Pilih langkah berdasarkan kondisi action == '1'.
                if action == "1":
                    # Tetapkan catatan algoritma, mode, IV, dan ciphertext.
                    record = encrypt_message(source.read_bytes(), key, "library", algorithm, fmt)
                    # Tetapkan hasil pemrosesan.
                    output = serialize_ciphertext(record, fmt).encode()
                # Jalankan cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
                else:
                    # Tetapkan catatan algoritma, mode, IV, dan ciphertext.
                    record = parse_ciphertext(
                        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
                        source.read_text(encoding="utf-8"), algorithm, wire_format=fmt
                    # Tutup pengelompokan sintaks di atas.
                    )
                    # Pilih langkah berdasarkan kondisi record['algorithm'] != algorithm.
                    if record["algorithm"] != algorithm:
                        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
                        raise ValueError("Algoritma tidak cocok dengan file.")
                    # Tetapkan hasil pemrosesan.
                    output = decrypt_record(record, key, "library")
                # Simpan byte hasil tanpa mengubah isinya.
                destination.write_bytes(output)
                # Panggil print dengan argumen yang ditentukan.
                print("BERHASIL:", destination)
            # Tangani kesalahan agar pengguna menerima penjelasan yang jelas.
            except (ValueError, OSError) as exc:
                # Panggil print dengan argumen yang ditentukan.
                print("GAGAL:", exc)
    # Tangani kesalahan agar pengguna menerima penjelasan yang jelas.
    except (EOFError, KeyboardInterrupt):
        # Panggil print dengan argumen yang ditentukan.
        print("\nTerminal ditutup.")
