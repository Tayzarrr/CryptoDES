# -*- coding: utf-8 -*-
"""Modul main untuk ZarCryptoDES."""

import sys
from cli import terminal_library
from crypto_backend import Crypto
from verification import run_3des_verification, run_verification

# BARIS ASLI 3145: Mendefinisikan fungsi main. Menentukan mode --test, --terminal, atau menjalankan GUI utama.
def main():
    # BARIS ASLI 3146: Di main: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: '--terminal' in sys.argv[1:]:terminal_library();return.
    if '--terminal' in sys.argv[1:]:terminal_library();return
    # BARIS ASLI 3147: Di main: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: '--test' in sys.argv[1:].
    if '--test' in sys.argv[1:]:
        # BARIS ASLI 3148: Di main: Menulis status atau hasil pemeriksaan ke terminal.
        print(run_verification()['log']);print('\n'+run_3des_verification()['log']);return
    # BARIS ASLI 3149: Di main: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
    from qt_compat import QApplication, QFont, QMessageBox
    from window import ZarCryptoDES
    app=QApplication(sys.argv);app.setApplicationName('ZarCryptoDES');app.setFont(QFont('Segoe UI',10))
    # BARIS ASLI 3150: Di main: Memastikan dependensi atau algoritma kriptografi tersedia/valid.
    if Crypto is None:
        # BARIS ASLI 3151: Di main: Menampilkan pesan dialog informasi, peringatan, atau kegagalan.
        QMessageBox.critical(None,'PyCryptodome belum tersedia','Jalankan: python -m pip install PySide6-Essentials pycryptodome');return
    # BARIS ASLI 3152: Di main: Menghitung/menyiapkan nilai window untuk dipakai oleh proses berikutnya.
    window=ZarCryptoDES();window.show();sys.exit(app.exec())


if __name__ == "__main__":
    main()
