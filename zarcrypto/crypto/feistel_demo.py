# Dokumentasikan tujuan atau perilaku bagian kode ini.
"""Contoh Feistel pendidikan 16-bit; terpisah dari DES standar."""


# Definisikan fungsi/metode F untuk tanggung jawab berikut.
def F(r, k):
    # Masking bit untuk membatasi nilai rot.
    rot = (r << 1 | r >> 7) & 255
    # Kembalikan hasil kepada pemanggil.
    return rot + k & 255


# Definisikan fungsi/metode feistel_encrypt untuk tanggung jawab berikut.
def feistel_encrypt(p, keys):
    # Tetapkan nilai (l, r) untuk langkah berikutnya.
    l, r = (p >> 8 & 255, p & 255)
    # Ulangi langkah untuk setiap elemen keys.
    for k in keys:
        # Tetapkan nilai (l, r) untuk langkah berikutnya.
        l, r = (r, l ^ F(r, k))
    # Kembalikan hasil kepada pemanggil.
    return l << 8 | r


# Definisikan fungsi/metode feistel_decrypt untuk tanggung jawab berikut.
def feistel_decrypt(c, keys):
    # Tetapkan nilai (l, r) untuk langkah berikutnya.
    l, r = (c >> 8 & 255, c & 255)
    # Ulangi langkah untuk setiap elemen reversed(keys).
    for k in reversed(keys):
        # Tetapkan nilai (l, r) untuk langkah berikutnya.
        l, r = (r ^ F(l, k), l)
    # Kembalikan hasil kepada pemanggil.
    return l << 8 | r
