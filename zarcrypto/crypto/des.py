# Dokumentasikan tujuan atau perilaku bagian kode ini.
"""DES lengkap buatan sendiri; inti modul ini tidak memanggil cipher library."""

# Impor komponen dari .tables untuk modul ini.
from .tables import IP, FP, E, P, PC1, PC2, SHIFTS, SBOX


# Susun ulang bit mengikuti tabel permutasi DES.
def permute(value, table, width):
    # Dokumentasikan tujuan atau perilaku bagian kode ini.
    """Pilih bit berdasarkan tabel permutasi, dari kiri ke kanan."""
    # Tetapkan nilai out untuk langkah berikutnya.
    out = 0
    # Ulangi langkah untuk setiap elemen table.
    for position in table:
        # Geser keluaran satu bit; ambil bit masukan sesuai posisi tabel dan gabungkan dengan OR.
        out = out << 1 | value >> width - position & 1
    # Kembalikan hasil kepada pemanggil.
    return out


# Bangkitkan 16 subkunci DES, masing-masing 48 bit.
def make_subkeys(key):
    # Pilih langkah berdasarkan kondisi len(key) != 8.
    if len(key) != 8:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Kunci DES harus tepat 8 byte.")
    # Ubah kunci menjadi integer big endian lalu pilih 56 bit dengan PC1.
    selected = permute(int.from_bytes(key, "big"), PC1, 64)
    # Pisahkan hasil PC1 menjadi C dan D, masing-masing 28 bit.
    c, d = (selected >> 28, selected & 268435455)
    # Tetapkan daftar subkunci ronde.
    subkeys = []
    # Ulangi langkah untuk setiap elemen SHIFTS.
    for shift in SHIFTS:
        # Rotasi C ke kiri sesuai jadwal, lalu batasi hasilnya menjadi 28 bit.
        c = (c << shift | c >> 28 - shift) & 268435455
        # Rotasi D ke kiri sesuai jadwal, lalu batasi hasilnya menjadi 28 bit.
        d = (d << shift | d >> 28 - shift) & 268435455
        # Gabungkan C/D menjadi 56 bit lalu pilih 48 bit subkunci ronde menggunakan PC2.
        subkeys.append(permute(c << 28 | d, PC2, 56))
    # Kembalikan hasil kepada pemanggil.
    return tuple(subkeys)


# Hitung fungsi F melalui ekspansi, XOR, S-box, dan permutasi P.
def round_function(right, subkey):
    # Ekspansi R dari 32 ke 48 bit, kemudian XOR dengan subkunci ronde.
    mixed = permute(right, E, 32) ^ subkey
    # Tetapkan nilai substituted untuk langkah berikutnya.
    substituted = 0
    # Ulangi langkah untuk setiap elemen enumerate(SBOX).
    for i, box in enumerate(SBOX):
        # Ambil potongan 6 bit untuk S-box ke-i, dimulai dari bagian paling kiri.
        six = mixed >> 42 - 6 * i & 63
        # Gabungkan bit pertama dan terakhir dari 6 bit sebagai indeks baris S-box.
        row = (six & 32) >> 4 | six & 1
        # Ambil empat bit tengah sebagai indeks kolom S-box.
        column = six >> 1 & 15
        # Tambahkan keluaran S-box 4 bit ke rangkaian hasil substitusi.
        substituted = substituted << 4 | box[row][column]
    # Kembalikan hasil kepada pemanggil.
    return permute(substituted, P, 32)


# Definisikan kelas DESManual yang mengelompokkan keadaan dan perilakunya.
class DESManual:
    # Dokumentasikan tujuan atau perilaku bagian kode ini.
    """Enkripsi/dekripsi satu blok DES 8 byte, big endian."""

    # Definisikan fungsi/metode __init__ untuk tanggung jawab berikut.
    def __init__(self, key):
        # Simpan hasil make_subkeys pada self.subkeys.
        self.subkeys = make_subkeys(key)

    # Definisikan fungsi/metode _process untuk tanggung jawab berikut.
    def _process(self, block, subkeys, trace=None):
        # Pilih langkah berdasarkan kondisi len(block) != 8.
        if len(block) != 8:
            # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
            raise ValueError("Satu blok DES harus tepat 8 byte.")
        # Simpan hasil permute pada state.
        state = permute(int.from_bytes(block, "big"), IP, 64)
        # Pisahkan blok hasil IP menjadi L0 dan R0 yang masing-masing 32 bit.
        left, right = (state >> 32, state & 4294967295)
        # Pilih langkah berdasarkan kondisi trace is not None.
        if trace is not None:
            # Tambahkan satu elemen ke daftar.
            trace.append({"round": 0, "L": f"{left:08X}", "R": f"{right:08X}", "K": None})
        # Ulangi langkah untuk setiap elemen enumerate(subkeys, 1).
        for i, key in enumerate(subkeys, 1):
            # L baru mengambil R lama; R baru adalah L lama XOR F(R lama, subkunci).
            left, right = (right, left ^ round_function(right, key))
            # Pilih langkah berdasarkan kondisi trace is not None.
            if trace is not None:
                # Tambahkan satu elemen ke daftar.
                trace.append(
                    # Tambahkan satu elemen ke daftar.
                    {"round": i, "L": f"{left:08X}", "R": f"{right:08X}", "K": f"{key:012X}"}
                # Tutup pengelompokan sintaks di atas.
                )
        # Kembalikan hasil kepada pemanggil.
        return permute(right << 32 | left, FP, 64).to_bytes(8, "big")

    # Definisikan fungsi/metode encrypt_block untuk tanggung jawab berikut.
    def encrypt_block(self, block, trace=None):
        # Kembalikan hasil kepada pemanggil.
        return self._process(block, self.subkeys, trace)

    # Definisikan fungsi/metode decrypt_block untuk tanggung jawab berikut.
    def decrypt_block(self, block, trace=None):
        # Dekripsi memakai proses DES yang sama dengan urutan subkunci dibalik.
        return self._process(block, self.subkeys[::-1], trace)


# Definisikan fungsi/metode xor_bytes untuk tanggung jawab berikut.
def xor_bytes(a, b):
    # Kembalikan hasil kepada pemanggil.
    return bytes((x ^ y for x, y in zip(a, b)))


# Definisikan fungsi/metode validate_cbc untuk tanggung jawab berikut.
def validate_cbc(data, iv):
    # Pilih langkah berdasarkan kondisi len(iv) != 8.
    if len(iv) != 8:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("IV DES-CBC harus tepat 8 byte.")
    # Pilih langkah berdasarkan kondisi not data or len(data) % 8.
    if not data or len(data) % 8:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Data CBC harus tidak kosong dan kelipatan 8 byte.")


# Rangkai enkripsi CBC manual dengan XOR blok pesan dan ciphertext sebelumnya.
def encrypt_cbc(data, key, iv):
    # Dokumentasikan tujuan atau perilaku bagian kode ini.
    """Masukan sudah di-padding; CBC memakai C_i=E(P_i XOR C_(i-1))."""
    # Panggil validate_cbc dengan argumen yang ditentukan.
    validate_cbc(data, iv)
    # Tetapkan nilai (des, previous, output) untuk langkah berikutnya.
    des, previous, output = (DESManual(key), iv, bytearray())
    # Ulangi langkah untuk setiap elemen range(0, len(data), 8).
    for start in range(0, len(data), 8):
        # Jalankan enkripsi satu blok DES/3DES. Simpan sebagai previous.
        previous = des.encrypt_block(xor_bytes(data[start : start + 8], previous))
        # Jalankan output.extend pada komponen/data ini.
        output.extend(previous)
    # Kembalikan hasil kepada pemanggil.
    return bytes(output)


# Pulihkan CBC manual melalui dekripsi blok dan XOR dengan blok sebelumnya.
def decrypt_cbc(data, key, iv):
    # Panggil validate_cbc dengan argumen yang ditentukan.
    validate_cbc(data, iv)
    # Tetapkan nilai (des, previous, output) untuk langkah berikutnya.
    des, previous, output = (DESManual(key), iv, bytearray())
    # Ulangi langkah untuk setiap elemen range(0, len(data), 8).
    for start in range(0, len(data), 8):
        # Tetapkan nilai block untuk langkah berikutnya.
        block = data[start : start + 8]
        # Jalankan output.extend pada komponen/data ini.
        output.extend(xor_bytes(des.decrypt_block(block), previous))
        # Tetapkan nilai previous untuk langkah berikutnya.
        previous = block
    # Kembalikan hasil kepada pemanggil.
    return bytes(output)
