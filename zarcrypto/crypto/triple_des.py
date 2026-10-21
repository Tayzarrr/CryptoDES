# Dokumentasikan tujuan atau perilaku bagian kode ini.
"""3DES-EDE tiga tahap menggunakan DES manual."""

# Impor komponen dari .des untuk modul ini.
from .des import DESManual, validate_cbc, xor_bytes
# Impor komponen dari .keys untuk modul ini.
from .keys import validate_algorithm_key


# Definisikan kelas TripleDESManual yang mengelompokkan keadaan dan perilakunya.
class TripleDESManual:
    # Dokumentasikan tujuan atau perilaku bagian kode ini.
    """3DES-EDE tiga kunci. Setiap tahap memakai DESManual, bukan DES3 library."""

    # Definisikan fungsi/metode __init__ untuk tanggung jawab berikut.
    def __init__(self, key):
        # Panggil validate_algorithm_key dengan argumen yang ditentukan.
        validate_algorithm_key(key, "3DES")
        # Simpan hasil DESManual pada self.d1.
        self.d1 = DESManual(key[:8])
        # Simpan hasil DESManual pada self.d2.
        self.d2 = DESManual(key[8:16])
        # Simpan hasil DESManual pada self.d3.
        self.d3 = DESManual(key[16:24])

    # Definisikan fungsi/metode encrypt_block untuk tanggung jawab berikut.
    def encrypt_block(self, block):
        # 3DES-EDE: enkripsi K1, dekripsi K2, lalu enkripsi K3.
        return self.d3.encrypt_block(self.d2.decrypt_block(self.d1.encrypt_block(block)))

    # Definisikan fungsi/metode decrypt_block untuk tanggung jawab berikut.
    def decrypt_block(self, block):
        # Balikkan EDE: dekripsi K3, enkripsi K2, lalu dekripsi K1.
        return self.d1.decrypt_block(self.d2.encrypt_block(self.d3.decrypt_block(block)))


# Terapkan rantai CBC pada cipher blok 3DES-EDE.
def triple_cbc(data, key, iv, decrypt=False):
    # Panggil validate_cbc dengan argumen yang ditentukan.
    validate_cbc(data, iv)
    # Simpan hasil TripleDESManual pada cipher.
    cipher = TripleDESManual(key)
    # Tetapkan nilai previous untuk langkah berikutnya.
    previous = iv
    # Simpan hasil bytearray pada out.
    out = bytearray()
    # Ulangi langkah untuk setiap elemen range(0, len(data), 8).
    for pos in range(0, len(data), 8):
        # Tetapkan nilai block untuk langkah berikutnya.
        block = data[pos : pos + 8]
        # Pilih langkah berdasarkan kondisi decrypt.
        if decrypt:
            # Jalankan out.extend pada komponen/data ini.
            out.extend(xor_bytes(cipher.decrypt_block(block), previous))
            # Tetapkan nilai previous untuk langkah berikutnya.
            previous = block
        # Jalankan cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
        else:
            # Jalankan enkripsi satu blok DES/3DES. Simpan sebagai previous.
            previous = cipher.encrypt_block(xor_bytes(block, previous))
            # Jalankan out.extend pada komponen/data ini.
            out.extend(previous)
    # Kembalikan hasil kepada pemanggil.
    return bytes(out)
