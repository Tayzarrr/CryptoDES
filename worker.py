# -*- coding: utf-8 -*-
"""Modul worker untuk ZarCryptoDES."""

from qt_compat import QThread, Signal

# BARIS ASLI 2601: Mendefinisikan kelas Worker. Thread pekerja agar proses berat tidak membekukan GUI.
class Worker(QThread):
    # BARIS ASLI 2602: Di Worker: Menghitung/menyiapkan nilai completed untuk dipakai oleh proses berikutnya.
    completed=Signal(str,object)
    # BARIS ASLI 2603: Di Worker: Menghitung/menyiapkan nilai failed untuk dipakai oleh proses berikutnya.
    failed=Signal(str)
    # BARIS ASLI 2604: Mendefinisikan fungsi __init__. Fungsi ini menangani aksi khusus dalam aplikasi.
    def __init__(self,kind,fn):super().__init__();self.kind=kind;self.fn=fn
    # BARIS ASLI 2605: Mendefinisikan fungsi run. Fungsi ini menangani aksi khusus dalam aplikasi.
    def run(self):
        # BARIS ASLI 2606: Di run: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
        try:self.completed.emit(self.kind,self.fn())
        # BARIS ASLI 2607: Di run: Menangani kesalahan Exception as excself.failed.emit(str(exc)).
        except Exception as exc:self.failed.emit(str(exc))
