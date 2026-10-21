<div align="center">
<img src="assets/logo.png" alt="Logo ZarCryptoDES" width="90">

# ZarCryptoDES
### DES & Triple DES · Manual × PyCryptodome

**Aplikasi desktop untuk mengenkripsi pesan, membuktikan hasil, dan mempelajari ronde Feistel.**

`Python` · `PySide6` · `DES / 3DES` · `CBC / ECB` · `TXT HEX`

[Mulai](#menjalankan-aplikasi) · [Fitur](#fitur) · [Struktur](#struktur-proyek) · [Pengujian](#pengujian) · [Panduan GitHub](docs/PANDUAN_GITHUB.md)
</div>

---

![Beranda ZarCryptoDES](docs/images/beranda.png)

## Kolaborasi Andika dan Rafael

Repository GitHub: [Tayzarrr/CryptoDES](https://github.com/Tayzarrr/CryptoDES). Andika mengunggah 21 file kerangka proyek dan kriptografi; Rafael mengunggah 22 file GUI, aset, pengujian, dan dokumentasi. Ikuti [panduan dua PC](docs/PANDUAN_GITHUB.md) dan [urutan unggah per file](docs/URUTAN_PUSH.md). Aplikasi dijalankan setelah seluruh file tergabung.

## Tentang proyek

ZarCryptoDES adalah proyek pembelajaran kriptografi simetris. Implementasi DES manual menggunakan tabel permutasi, pembangkitan subkunci, fungsi F, S-box, XOR, dan 16 ronde Feistel. Triple DES manual menyusun tiga proses DES dalam urutan **E(K1) → D(K2) → E(K3)**.

Implementasi **PyCryptodome** menjadi pembanding untuk memeriksa ciphertext dan pemulihan plaintext. Kode manual tidak memakai `DES.new()` atau `DES3.new()` untuk melakukan cipher manual. Proyek dipecah dari sumber `ZarCryptoDES(6).py`; antarmuka, logo, dan alur dasarnya dipertahankan.

## Fitur

| Bagian | Kemampuan |
|---|---|
| Enkripsi & dekripsi | Pilih TXT atau ketik/tempel pesan langsung. |
| Dua implementasi | DES/3DES buatan sendiri dan library PyCryptodome. |
| Format CBC | HEX berisi **IV 8 byte + ciphertext**; IV dibaca otomatis. |
| Format ECB | HEX berisi ciphertext saja; tidak menggunakan IV. |
| Padding | PKCS#7, dilengkapi informasi byte, bit, nilai padding, dan jumlah blok. |
| Perbandingan | Ciphertext identik dan dekripsi silang diperiksa byte demi byte. |
| Jejak Feistel | Teks/TXT, nomor blok, ronde, tiga tahap 3DES, tabel XOR dan notasi biner. |
| Pengujian | Vektor standar, variasi ukuran, UTF-8, file, dan isolasi backend manual. |
| Terminal | Pembanding library melalui `--terminal`. |
| Riwayat | Aktivitas sesi dan ekspor riwayat ke TXT. |

## Menjalankan aplikasi

Disarankan Python **3.11 atau lebih baru**; verifikasi paket ini dilakukan menggunakan Python 3.12. Jalankan perintah dari folder yang berisi `app.py` dan `requirements.txt`.

### Windows / PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Tidak perlu mengaktifkan virtual environment sehingga langkah ini tidak bergantung pada pengaturan execution policy PowerShell. Jika `py` tidak dikenali, gunakan `python` pada perintah pertama.

### Linux / macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Alternatif setelah memakai interpreter yang sudah berisi dependensi:

```bash
python app.py
python -m zarcrypto
```

**Ekstrak seluruh ZIP.** Jangan menjalankan `window.py`, `des.py`, atau file modul lain secara langsung. Aset dan modul harus tetap berada dalam susunan folder proyek.

## Pemakaian singkat

1. Buka **Enkripsi File**; pilih TXT atau **Tulis / tempel**.
2. Pilih **DES** atau **3DES**, backend manual/library, dan masukkan kunci HEX.
3. Pilih format **CBC · IV + ciphertext** atau **ECB · ciphertext saja**.
4. Klik **Enkripsi**, lalu simpan hasil di folder `output/`.
5. Pada **Dekripsi File**, buka hasil tersebut; samakan algoritma, kunci, dan format, kemudian klik **Dekripsi**.
6. Gunakan **Perbandingan** untuk membuktikan kesamaan hasil dan **Jejak Feistel** untuk memeriksa ronde/XOR.

![Halaman enkripsi](docs/images/enkripsi.png)

### Kunci dan blok

| Algoritma | Panjang kunci masukan | Ukuran blok | Keterangan |
|---|---:|---:|---|
| DES | 8 byte / 16 digit HEX | 8 byte / 64 bit | Material kunci efektif 56 bit. |
| 3DES | 24 byte / 48 digit HEX | 8 byte / 64 bit | Tiga bagian K1, K2, K3; aplikasi menolak degenerasi menjadi DES tunggal. |

Kunci contoh di kode bersifat **publik**, khusus untuk demonstrasi. Tombol **Generate** menyediakan kunci lain; gunakan kunci yang sama untuk pemulihan.

Untuk `cryptography`: 12 byte ASCII = 96 bit; PKCS#7 menambahkan empat byte `04`, sehingga data diproses menjadi 16 byte / dua blok. Untuk UTF-8, jumlah karakter tidak selalu sama dengan jumlah byte. Pesan tepat 8 byte tetap mendapat satu blok padding penuh.

### Bertukar ciphertext dengan aplikasi lain

- **CBC kompatibel:** kedua aplikasi menyepakati DES/3DES, kunci HEX, PKCS#7 ukuran 8 byte, dan susunan `IV || ciphertext`. Kirim seluruh HEX; IV tidak perlu diketik terpisah.
- **ECB kompatibel:** kedua aplikasi memakai mode ECB dan padding yang sama.
- Ekstensi `.txt` saja tidak menentukan mode. Aplikasi tidak menjamin kompatibilitas dengan setiap format yang dibuat aplikasi lain.
- Pembaca format lama `ZAR1` dan format ZarCryptoDES berversi dipertahankan untuk berkas yang didukung. Pilihan format baru di GUI tetap **CBC / ECB**.

<details>
<summary><b>Lihat Jejak Feistel dan pembuktian XOR</b></summary>

![Jejak Feistel dan XOR](docs/images/feistel.png)

</details>

## Struktur proyek

```text
ZarCryptoDES/
├── app.py                    # Jalankan GUI / --test / --terminal
├── requirements.txt          # Dependensi
├── README.md                 # Dokumentasi utama
├── .gitignore                # Cache, environment, dan hasil lokal
├── .gitattributes            # Aturan line ending dan aset biner
├── assets/
│   ├── logo.png              # Logo asli dari sumber
│   └── style.qss             # Stylesheet GUI
├── contoh/plaintext.txt      # Contoh pesan publik
├── output/.gitkeep           # Tempat hasil lokal
├── zarcrypto/
│   ├── constants.py          # Kunci/vektor contoh
│   ├── paths.py              # Lokasi aset
│   ├── cli.py                # Terminal pembanding library
│   ├── crypto/               # DES, 3DES, padding, key, format, backend
│   ├── services/files.py     # Operasi file dan perbandingan
│   ├── testing/verification.py # Suite verifikasi dari sumber asli
│   └── ui/                   # Window, komponen GUI, worker, tema, aset
├── tests/test_project.py     # Regresi proyek modular
└── docs/
    ├── PANDUAN_GITHUB.md      # Langkah lengkap upload/push
    ├── URUTAN_PUSH.md         # Perintah commit/push per file
    ├── PETA_MODUL.md          # Penjelasan pembagian kode
    └── images/               # Screenshot dari aplikasi yang dijalankan
```

Alur dependensi: **`app.py` → GUI / CLI / pengujian → services → crypto**. Logo dan stylesheet dibaca melalui lokasi file proyek, bukan bergantung pada folder terminal.

## Pengujian

```powershell
.\.venv\Scripts\python.exe app.py --test
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Pengujian inti dan terminal tidak membuka GUI. Sesudah environment aktif atau memakai interpreter yang tepat, perintahnya dapat disingkat menjadi `python app.py --test` dan `python -m unittest discover -s tests -v`.

Vektor DES: `133457799BBCDFF1` + plaintext `0123456789ABCDEF` → `85E813540F0AB405`. Vektor 3DES contoh menghasilkan `372C1D08A4F057BA`. Pengujian menunjukkan kecocokan pada kasus yang diuji, bukan pembuktian matematis untuk semua kemungkinan masukan.

## Terminal library

```powershell
.\.venv\Scripts\python.exe app.py --terminal
```

Pilih enkripsi/dekripsi, algoritma, kunci HEX, format `cbc` / `ecb`, lalu path TXT masukan dan keluaran. Jalur ini menggunakan backend library untuk pembanding. GUI tetap dijalankan tanpa argumen: `python app.py`.

## Membaca kode

Komentar penjelasan berbahasa Indonesia disertakan pada setiap baris kode Python yang dapat dieksekusi dan baris lanjutan sintaks. Docstring menjelaskan tujuan modul/fungsi. Isi string multiline, logo PNG, dan nilai data bukan langkah eksekusi terpisah; keterangannya diletakkan pada bagian yang memuatnya. Komentar tidak mengubah proses algoritma.

Lihat [Peta Modul](docs/PETA_MODUL.md) untuk urutan belajar dan [Panduan GitHub](docs/PANDUAN_GITHUB.md) untuk mengunggah per file tanpa merusak struktur.

## Batas penggunaan

DES dan 3DES dipakai untuk **pembelajaran**. CBC/ECB di proyek ini tidak menyediakan autentikasi pesan; keberhasilan unpadding saja bukan bukti bahwa pesan tidak diubah. Verifikasi terhadap plaintext asli dilakukan pada menu Perbandingan.

---
**ZarCryptoDES · Proyek pembelajaran kriptografi simetris**
