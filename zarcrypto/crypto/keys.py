# Dokumentasikan tujuan atau perilaku bagian kode ini.
"""Validasi panjang kunci, parity, dan pembangkitan kunci 3DES."""

# Impor modul secrets yang dipakai pada file ini.
import secrets


# Definisikan fungsi/metode validate_algorithm_key untuk tanggung jawab berikut.
def validate_algorithm_key(key, algorithm="DES"):
    # Pilih langkah berdasarkan kondisi algorithm not in ('DES', '3DES').
    if algorithm not in ("DES", "3DES"):
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Algoritma harus DES atau 3DES.")
    # Tetapkan nilai length untuk langkah berikutnya.
    length = 8 if algorithm == "DES" else 24
    # Pilih langkah berdasarkan kondisi len(key) != length.
    if len(key) != length:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError(f"Kunci {algorithm} harus {length} byte ({length * 2} digit hex).")
    # Pilih langkah berdasarkan kondisi algorithm == '3DES'.
    if algorithm == "3DES":
        # Tetapkan nilai effective untuk langkah berikutnya.
        effective = [bytes((b & 254 for b in key[i : i + 8])) for i in (0, 8, 16)]
        # Pilih langkah berdasarkan kondisi effective[0] == effective[1] or effective[1] == effective[2].
        if effective[0] == effective[1] or effective[1] == effective[2]:
            # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
            raise ValueError(
                # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
                "Kunci 3DES menyusut menjadi DES tunggal. Gunakan kunci contoh atau generate ulang."
            # Tutup pengelompokan sintaks di atas.
            )
    # Kembalikan hasil kepada pemanggil.
    return key


# Definisikan fungsi/metode random_3des_key untuk tanggung jawab berikut.
def random_3des_key():
    # Ulangi proses selama kondisi masih terpenuhi.
    while True:
        # Simpan hasil secrets.token_bytes pada raw.
        raw = secrets.token_bytes(24)
        # Tetapkan kunci dalam bentuk byte.
        key = bytes((b & 254 | 1 ^ (b & 254).bit_count() & 1 for b in raw))
        # Mulai operasi yang dapat menimbulkan kesalahan.
        try:
            # Kembalikan hasil kepada pemanggil.
            return validate_algorithm_key(key, "3DES")
        # Tangani kesalahan agar pengguna menerima penjelasan yang jelas.
        except ValueError:
            # Tidak ada tindakan tambahan pada cabang ini.
            pass


# Definisikan fungsi/metode parse_hex untuk tanggung jawab berikut.
def parse_hex(text, length, label):
    # Mulai operasi yang dapat menimbulkan kesalahan.
    try:
        # Simpan hasil bytes.fromhex pada value.
        value = bytes.fromhex(text)
    # Tangani kesalahan agar pengguna menerima penjelasan yang jelas.
    except ValueError as exc:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError(f"{label} harus berupa heksadesimal.") from exc
    # Pilih langkah berdasarkan kondisi len(value) != length.
    if len(value) != length:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError(f"{label} harus {length} byte ({length * 2} digit hex).")
    # Kembalikan hasil kepada pemanggil.
    return value
