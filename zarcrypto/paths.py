# Dokumentasikan tujuan atau perilaku bagian kode ini.
"""Lokasi aset dihitung dari file modul; tidak bergantung direktori terminal."""

# Impor komponen dari pathlib untuk modul ini.
from pathlib import Path

# Tetapkan nilai PROJECT_ROOT untuk langkah berikutnya.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Tetapkan nilai ASSETS_DIR untuk langkah berikutnya.
ASSETS_DIR = PROJECT_ROOT / "assets"
