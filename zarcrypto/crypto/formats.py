# Dokumentasikan tujuan atau perilaku bagian kode ini.
"""Pembaca dan penulis TXT HEX, format CBC/ECB kompatibel, dan format lama."""

# Impor modul base64 yang dipakai pada file ini.
import base64
# Impor komponen dari .keys untuk modul ini.
from .keys import parse_hex


# Ubah struktur hasil enkripsi menjadi teks HEX sesuai format pilihan.
def serialize_ciphertext(record, wire_format="zar"):
    # Dokumentasikan tujuan atau perilaku bagian kode ini.
    """Format HEX v2: penanda 8 byte, IV 8 byte, ciphertext CBC."""
    # Pilih langkah berdasarkan kondisi record['mode'] == 'ECB'.
    if record["mode"] == "ECB":
        # Kembalikan hasil kepada pemanggil.
        return record["ciphertext_hex"].upper() + "\n"
    # Pilih langkah berdasarkan kondisi wire_format == 'cbc'.
    if wire_format == "cbc":
        # Kembalikan hasil kepada pemanggil.
        return (record["iv_hex"] + record["ciphertext_hex"]).upper() + "\n"
    # Tetapkan nilai header untuk langkah berikutnya.
    header = b"ZCD2" + bytes([1 if record["algorithm"] == "DES" else 3, 1, 1, 0])
    # Kembalikan hasil kepada pemanggil.
    return (
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        header + bytes.fromhex(record["iv_hex"] + record["ciphertext_hex"])
    # Tutup pengelompokan sintaks di atas.
    ).hex().upper() + "\n"


# Kenali format masukan dan ambil algoritma, mode, IV, serta ciphertext.
def parse_ciphertext(value, algorithm="DES", iv_hex="", wire_format="zar"):
    # Dokumentasikan tujuan atau perilaku bagian kode ini.
    """Baca format TXT yang sama untuk DES dan 3DES."""
    # Simpan hasil value.lstrip('\ufeff').strip pada value.
    value = value.lstrip("\ufeff").strip()
    # Simpan hasil ''.join pada compact.
    compact = "".join(value.split())
    # Pilih langkah berdasarkan kondisi compact and all((c in '0123456789abcdefABCDEF' for c in compact)).
    if compact and all((c in "0123456789abcdefABCDEF" for c in compact)):
        # Pilih langkah berdasarkan kondisi len(compact) % 2.
        if len(compact) % 2:
            # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
            raise ValueError("Jumlah digit HEX harus genap.")
        # Simpan hasil bytes.fromhex pada raw.
        raw = bytes.fromhex(compact)
        # Pilih langkah berdasarkan kondisi raw.startswith(b'ZCD2').
        if raw.startswith(b"ZCD2"):
            # Pilih langkah berdasarkan kondisi len(raw) < 24 or len(raw) % 8.
            if len(raw) < 24 or len(raw) % 8:
                # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
                raise ValueError("Data HEX v2 terpotong atau panjangnya tidak valid.")
            # Pilih langkah berdasarkan kondisi raw[4] not in (1, 3) or raw[5:8] != b'\x01\x01\x00'.
            if raw[4] not in (1, 3) or raw[5:8] != b"\x01\x01\x00":
                # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
                raise ValueError("Algoritma, mode, atau padding format HEX v2 tidak didukung.")
            # Tetapkan pilihan DES atau 3DES.
            algorithm = "DES" if raw[4] == 1 else "3DES"
            # Tetapkan nilai (iv, ct) untuk langkah berikutnya.
            iv, ct = (raw[8:16].hex(), raw[16:].hex())
        # Periksa kondisi alternatif sebelum memilih langkah berikutnya.
        elif wire_format in ("cbc", "ecb"):
            # Pilih langkah berdasarkan kondisi algorithm not in ('DES', '3DES').
            if algorithm not in ("DES", "3DES"):
                # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
                raise ValueError("Pilih DES atau 3DES sesuai pengirim.")
            # Pilih langkah berdasarkan kondisi len(raw) % 8 or len(raw) < (16 if wire_format == 'cbc' else 8).
            if len(raw) % 8 or len(raw) < (16 if wire_format == "cbc" else 8):
                # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
                raise ValueError("Panjang HEX tidak sesuai format yang dipilih.")
            # Kembalikan hasil kepada pemanggil.
            return {
                # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
                "version": 1,
                # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
                "algorithm": algorithm,
                # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
                "mode": "CBC" if wire_format == "cbc" else "ECB",
                # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
                "padding": "PKCS7",
                # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
                "iv_hex": raw[:8].hex() if wire_format == "cbc" else "",
                # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
                "ciphertext_hex": (raw[8:] if wire_format == "cbc" else raw).hex(),
            # Tutup pengelompokan sintaks di atas.
            }
        # Periksa kondisi alternatif sebelum memilih langkah berikutnya.
        elif iv_hex:
            # Panggil parse_hex dengan argumen yang ditentukan.
            parse_hex(iv_hex, 8, "IV")
            # Pilih langkah berdasarkan kondisi not raw or len(raw) % 8.
            if not raw or len(raw) % 8:
                # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
                raise ValueError("Panjang ciphertext lama tidak valid.")
            # Tetapkan nilai (iv, ct) untuk langkah berikutnya.
            iv, ct = (iv_hex, compact)
        # Jalankan cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
        else:
            # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
            raise ValueError(
                # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
                "HEX ini tanpa penanda ZarCryptoDES. Pilih format CBC (IV + ciphertext) atau ECB sesuai pengirim, lalu pilih / tempel ulang masukan. Jangan menebak mode; samakan dengan pengirim."
            # Tutup pengelompokan sintaks di atas.
            )
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
            "iv_hex": iv.upper(),
            # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
            "ciphertext_hex": ct.upper(),
        # Tutup pengelompokan sintaks di atas.
        }
    # Pilih langkah berdasarkan kondisi value.startswith('ZAR1:').
    if value.startswith("ZAR1:"):
        # Simpan hasil value.split pada parts.
        parts = value.split(":", 2)
        # Pilih langkah berdasarkan kondisi len(parts) != 3 or parts[1] not in ('DES', '3DES').
        if len(parts) != 3 or parts[1] not in ("DES", "3DES"):
            # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
            raise ValueError("Penanda algoritma ZAR1 tidak valid.")
        # Simpan hasil ''.join pada encoded.
        encoded = "".join(parts[2].split())
        # Mulai operasi yang dapat menimbulkan kesalahan.
        try:
            # Simpan hasil base64.b64decode pada raw.
            raw = base64.b64decode(
                # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
                encoded + "=" * (-len(encoded) % 4), altchars=b"-_", validate=True
            # Tutup pengelompokan sintaks di atas.
            )
        # Tangani kesalahan agar pengguna menerima penjelasan yang jelas.
        except ValueError as exc:
            # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
            raise ValueError("Isi Base64 pada ciphertext ZAR1 tidak valid.") from exc
        # Pilih langkah berdasarkan kondisi len(raw) < 16 or len(raw) % 8.
        if len(raw) < 16 or len(raw) % 8:
            # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
            raise ValueError("Panjang payload ZAR1 tidak valid untuk IV 8 byte dan ciphertext CBC.")
        # Kembalikan hasil kepada pemanggil.
        return {
            # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
            "version": 1,
            # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
            "algorithm": parts[1],
            # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
            "mode": "CBC",
            # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
            "padding": "PKCS7",
            # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
            "iv_hex": raw[:8].hex(),
            # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
            "ciphertext_hex": raw[8:].hex(),
        # Tutup pengelompokan sintaks di atas.
        }
    # Simpan hasil value.splitlines pada lines.
    lines = value.splitlines()
    # Pilih langkah berdasarkan kondisi len(lines) != 6 or lines[0] != 'ZarCryptoDES Ciphertext v1'.
    if len(lines) != 6 or lines[0] != "ZarCryptoDES Ciphertext v1":
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("File ciphertext TXT tidak valid. Pilih file hasil enkripsi aplikasi ini.")
    # Tetapkan nilai fields untuk langkah berikutnya.
    fields = {}
    # Ulangi langkah untuk setiap elemen lines[1:].
    for line in lines[1:]:
        # Simpan hasil line.partition pada (name, sep, content).
        name, sep, content = line.partition(":")
        # Pilih langkah berdasarkan kondisi not sep or name in fields.
        if not sep or name in fields:
            # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
            raise ValueError("Format ciphertext TXT tidak valid.")
        # Simpan hasil content.strip pada fields[name].
        fields[name] = content.strip()
    # Pilih langkah berdasarkan kondisi set(fields) != {'Algoritma', 'Mode', 'Padding', 'IV', 'Ciphertext'}.
    if set(fields) != {"Algoritma", "Mode", "Padding", "IV", "Ciphertext"}:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Informasi ciphertext TXT tidak lengkap.")
    # Pilih langkah berdasarkan kondisi fields['Algoritma'] not in ('DES', '3DES') or fields['Mode'] != 'CBC' or fields['Padding'] !.
    if (
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        fields["Algoritma"] not in ("DES", "3DES")
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        or fields["Mode"] != "CBC"
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        or fields["Padding"] != "PKCS7"
    # Tutup pengelompokan sintaks di atas.
    ):
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Algoritma, mode, atau padding ciphertext TXT tidak didukung.")
    # Panggil parse_hex dengan argumen yang ditentukan.
    parse_hex(fields["IV"], 8, "IV")
    # Mulai operasi yang dapat menimbulkan kesalahan.
    try:
        # Simpan hasil bytes.fromhex pada ct.
        ct = bytes.fromhex(fields["Ciphertext"])
    # Tangani kesalahan agar pengguna menerima penjelasan yang jelas.
    except ValueError as exc:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Ciphertext bukan HEX yang valid.") from exc
    # Pilih langkah berdasarkan kondisi not ct or len(ct) % 8.
    if not ct or len(ct) % 8:
        # Laporkan kesalahan dan hentikan jalur input yang tidak valid.
        raise ValueError("Ciphertext harus tidak kosong dan kelipatan 8 byte.")
    # Kembalikan hasil kepada pemanggil.
    return {
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        "version": 1,
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        "algorithm": fields["Algoritma"],
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        "mode": "CBC",
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        "padding": "PKCS7",
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        "iv_hex": fields["IV"],
        # Lanjutkan argumen, elemen data, atau ekspresi pada pernyataan di atas.
        "ciphertext_hex": fields["Ciphertext"],
    # Tutup pengelompokan sintaks di atas.
    }
