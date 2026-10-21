# Dokumentasikan tujuan atau perilaku bagian kode ini.
"""Titik masuk proyek: GUI, --test, atau --terminal."""

# Impor modul sys yang dipakai pada file ini.
import sys


# Definisikan fungsi/metode main untuk tanggung jawab berikut.
def main():
    # Pilih langkah berdasarkan kondisi '--terminal' in sys.argv[1:].
    if "--terminal" in sys.argv[1:]:
        # Impor komponen dari zarcrypto.cli untuk modul ini.
        from zarcrypto.cli import terminal_library

        # Panggil terminal_library dengan argumen yang ditentukan.
        terminal_library()
        # Akhiri fungsi tanpa hasil tambahan.
        return
    # Pilih langkah berdasarkan kondisi '--test' in sys.argv[1:].
    if "--test" in sys.argv[1:]:
        # Impor komponen dari zarcrypto.testing.verification untuk modul ini.
        from zarcrypto.testing.verification import run_verification, run_3des_verification

        # Panggil print dengan argumen yang ditentukan.
        print(run_verification()["log"])
        # Panggil print dengan argumen yang ditentukan.
        print("\n" + run_3des_verification()["log"])
        # Akhiri fungsi tanpa hasil tambahan.
        return
    # Mulai operasi yang dapat menimbulkan kesalahan.
    try:
        # Impor komponen dari PySide6.QtWidgets untuk modul ini.
        from PySide6.QtWidgets import QApplication
        # Impor komponen dari PySide6.QtGui untuk modul ini.
        from PySide6.QtGui import QFont
        # Impor komponen dari zarcrypto.crypto.backend untuk modul ini.
        from zarcrypto.crypto.backend import Crypto
        # Impor komponen dari zarcrypto.ui.window untuk modul ini.
        from zarcrypto.ui.window import ZarCryptoDES
    # Tangani kesalahan agar pengguna menerima penjelasan yang jelas.
    except ImportError as exc:
        # Panggil print dengan argumen yang ditentukan.
        print("Dependensi belum tersedia: " + str(exc))
        # Panggil print dengan argumen yang ditentukan.
        print("Jalankan: python -m pip install -r requirements.txt")
        # Kembalikan hasil kepada pemanggil.
        return 1
    # Pilih langkah berdasarkan kondisi Crypto is None.
    if Crypto is None:
        # Panggil print dengan argumen yang ditentukan.
        print("Pasang PyCryptodome: python -m pip install -r requirements.txt")
        # Kembalikan hasil kepada pemanggil.
        return 1
    # Simpan hasil QApplication pada app.
    app = QApplication(sys.argv)
    # Jalankan app.setApplicationName pada komponen/data ini.
    app.setApplicationName("ZarCryptoDES")
    # Tentukan jenis dan ukuran huruf komponen.
    app.setFont(QFont("Segoe UI", 10))
    # Simpan hasil ZarCryptoDES pada window.
    window = ZarCryptoDES()
    # Tampilkan jendela atau komponen.
    window.show()
    # Kembalikan hasil kepada pemanggil.
    return app.exec()


# Pilih langkah berdasarkan kondisi __name__ == '__main__'.
if __name__ == "__main__":
    # Jalankan sys.exit pada komponen/data ini.
    sys.exit(main())
