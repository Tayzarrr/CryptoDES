# Dokumentasikan tujuan atau perilaku bagian kode ini.
"""Pemilihan backend manual/library dan operasi pesan CBC atau ECB."""

# Impor modul secrets yang dipakai pada file ini.
import secrets
# Impor komponen dari .backend untuk modul ini.
from .backend import DES, DES3
# Impor komponen dari .des untuk modul ini.
from .des import DESManual, encrypt_cbc, decrypt_cbc
# Impor komponen dari .triple_des untuk modul ini.
from .triple_des import TripleDESManual, triple_cbc
# Impor komponen dari .keys untuk modul ini.
from .keys import validate_algorithm_key, parse_hex
# Impor komponen dari .padding untuk modul ini.
from .padding import pad, unpad


# Definisikan fungsi/metode crypt untuk tanggung jawab berikut.
def crypt(data, key, iv, backend, decrypt=False, algorithm="DES"):
    # Panggil validate_algorithm_key dengan argumen yang ditentukan.
    validate_algorithm_key(key, algorithm)
    # Pilih langkah berdasarkan kondisi backend == 'manual'.
    if backend == "manual":
        # Pilih langkah berdasarkan kondisi algorithm == '3DES'.
        if algorithm == "3DES":
            # Kembalikan hasil kepada pemanggil.
            return triple_cbc(data, key, iv, decrypt)
        # Kembalikan hasil kepada pemanggil.
        return decrypt_cbc(data, key, iv) if decrypt else encrypt_cbc(data, key, iv)
    # Pilih langkah berdasarkan kondisi backend != 'library'.
    if backend != "library":
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Backend harus library atau manual.")
    # Tetapkan nilai module untuk langkah berikutnya.
    module = DES if algorithm == "DES" else DES3
    # Simpan hasil module.new pada cipher.
    cipher = module.new(key, module.MODE_CBC, iv=iv)
    # Kembalikan hasil kepada pemanggil.
    return cipher.decrypt(data) if decrypt else cipher.encrypt(data)


# Definisikan fungsi/metode encrypt_bytes untuk tanggung jawab berikut.
def encrypt_bytes(data, key, backend="library", iv=None, algorithm="DES"):
    # Panggil validate_algorithm_key dengan argumen yang ditentukan.
    validate_algorithm_key(key, algorithm)
    # Pilih langkah berdasarkan kondisi iv is None.
    if iv is None:
        # Tetapkan initialization vector CBC.
        iv = secrets.token_bytes(8)
    # Pilih langkah berdasarkan kondisi len(iv) != 8.
    if len(iv) != 8:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("IV CBC harus 8 byte untuk DES maupun 3DES.")
    # Tetapkan byte ciphertext.
    ciphertext = crypt(pad(data), key, iv, backend, algorithm=algorithm)
    # Kembalikan hasil kepada pemanggil.
    return {
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        "version": 1,
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        "algorithm": algorithm,
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        "mode": "CBC",
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        "padding": "PKCS7",
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        "iv_hex": iv.hex(),
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        "ciphertext_hex": ciphertext.hex(),
    # Tutup pengelompokan sintaks di atas.
    }


# Definisikan fungsi/metode decrypt_record untuk tanggung jawab berikut.
def decrypt_record(record, key, backend="library"):
    # Pilih langkah berdasarkan kondisi not isinstance(record, dict).
    if not isinstance(record, dict):
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Data ciphertext tidak valid.")
    # Tetapkan pilihan DES atau 3DES.
    algorithm = record.get("algorithm")
    # Panggil validate_algorithm_key dengan argumen yang ditentukan.
    validate_algorithm_key(key, algorithm)
    # Tetapkan nilai expected untuk langkah berikutnya.
    expected = {"version": 1, "padding": "PKCS7"}
    # Pilih langkah berdasarkan kondisi record.get('mode') not in ('CBC', 'ECB').
    if record.get("mode") not in ("CBC", "ECB"):
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Mode ciphertext tidak didukung.")
    # Pilih langkah berdasarkan kondisi any((record.get(k) != v for k, v in expected.items())).
    if any((record.get(k) != v for k, v in expected.items())):
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Format ciphertext tidak didukung.")
    # Pilih langkah berdasarkan kondisi not isinstance(record.get('iv_hex'), str) or not isinstance(record.get('ciphertext_hex'), st.
    if not isinstance(record.get("iv_hex"), str) or not isinstance(
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        record.get("ciphertext_hex"), str
    # Tutup pengelompokan sintaks di atas.
    ):
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("IV dan ciphertext hex tidak ditemukan atau tipe salah.")
    # Tetapkan initialization vector CBC.
    iv = parse_hex(record["iv_hex"], 8, "IV") if record["mode"] == "CBC" else b""
    # Mulai operasi yang dapat menimbulkan kesalahan.
    try:
        # Tetapkan byte ciphertext.
        ciphertext = bytes.fromhex(record["ciphertext_hex"])
    # Tangani kesalahan agar pengguna menerima penjelasan yang jelas.
    except ValueError as exc:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Ciphertext bukan hex yang valid.") from exc
    # Pilih langkah berdasarkan kondisi not ciphertext or len(ciphertext) % 8.
    if not ciphertext or len(ciphertext) % 8:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Ciphertext harus tidak kosong dan kelipatan 8 byte.")
    # Kembalikan hasil kepada pemanggil.
    return unpad(
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        ecb_blocks(ciphertext, key, backend, algorithm, True)
        # Periksa syarat sebelum menjalankan blok di bawah.
        if record["mode"] == "ECB"
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        else crypt(ciphertext, key, iv, backend, decrypt=True, algorithm=algorithm)
    # Tutup pengelompokan sintaks di atas.
    )


# Definisikan fungsi/metode ecb_blocks untuk tanggung jawab berikut.
def ecb_blocks(data, key, backend, algorithm, decrypt=False):
    # Panggil validate_algorithm_key dengan argumen yang ditentukan.
    validate_algorithm_key(key, algorithm)
    # Pilih langkah berdasarkan kondisi not data or len(data) % 8.
    if not data or len(data) % 8:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Data ECB harus kelipatan 8 byte.")
    # Pilih langkah berdasarkan kondisi backend == 'library'.
    if backend == "library":
        # Tetapkan nilai module untuk langkah berikutnya.
        module = DES if algorithm == "DES" else DES3
        # Simpan hasil module.new pada cipher.
        cipher = module.new(key, module.MODE_ECB)
        # Kembalikan hasil kepada pemanggil.
        return cipher.decrypt(data) if decrypt else cipher.encrypt(data)
    # Pilih langkah berdasarkan kondisi backend != 'manual'.
    if backend != "manual":
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Implementasi tidak dikenal.")
    # Tetapkan nilai engine untuk langkah berikutnya.
    engine = DESManual(key) if algorithm == "DES" else TripleDESManual(key)
    # Tetapkan nilai method untuk langkah berikutnya.
    method = engine.decrypt_block if decrypt else engine.encrypt_block
    # Kembalikan hasil kepada pemanggil.
    return b"".join((method(data[i : i + 8]) for i in range(0, len(data), 8)))


# Definisikan fungsi/metode encrypt_message untuk tanggung jawab berikut.
def encrypt_message(data, key, backend, algorithm, wire_format):
    # Pilih langkah berdasarkan kondisi wire_format == 'ecb'.
    if wire_format == "ecb":
        # Kembalikan hasil kepada pemanggil.
        return {
            # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
            "version": 1,
            # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
            "algorithm": algorithm,
            # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
            "mode": "ECB",
            # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
            "padding": "PKCS7",
            # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
            "iv_hex": "",
            # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
            "ciphertext_hex": ecb_blocks(pad(data), key, backend, algorithm).hex(),
        # Tutup pengelompokan sintaks di atas.
        }
    # Kembalikan hasil kepada pemanggil.
    return encrypt_bytes(data, key, backend, algorithm=algorithm)
