```markdown
# GitHub API CLI (Python, requests, .env) — INTERAKTIF

Proyek ini menyediakan contoh modular untuk berinteraksi dengan GitHub REST API menggunakan `requests`. Token GitHub dibaca dari file `.env` (menggunakan `python-dotenv`). Versi ini menggunakan antarmuka interaktif berbasis menu sehingga Anda tidak perlu menghafal argumen baris perintah.

Fitur
- whoami: tampilkan user yang terautentikasi
- create: buat repository (user atau organization)
- delete: hapus repository
- list: daftar repository milik user
- get: lihat data repository
- update: update repository (nama, deskripsi, private)

Struktur proyek singkat
- main.py — antarmuka interaktif (menu) dan pengendali utama
- modules/
  - github_client.py — wrapper ringan di atas GitHub REST API (requests)
  - create.py, delete.py, list.py, get.py, update.py — modul aksi yang memanggil github_client

Persyaratan
- Python 3.8+
- Paket Python:
  - requests
  - python-dotenv

Contoh requirements.txt
```
requests>=2.31.0
python-dotenv>=1.0.0
```

Menyiapkan token
1. Buat token Personal Access Token (PAT) di GitHub: https://github.com/settings/tokens
2. Beri scope yang sesuai:
   - Untuk membuat/hapus repo private/public: centang `repo` (full control of private repositories).
   - Jika ingin bekerja di organization, pastikan token memiliki izin organization yang dibutuhkan.
3. Buat file `.env` di root proyek dan masukkan:
```
GITHUB_TOKEN=ghp_xxx_your_token_here
```
Anda bisa menyalin dari `.env.example` jika ada.

Instalasi dan menjalankan
1. Clone repository.
2. (Opsional tapi direkomendasikan) Buat virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate    # Linux / macOS
   .venv\Scripts\activate       # Windows (PowerShell/CMD)
   ```
3. Install dependensi:
   ```
   pip install -r requirements.txt
   ```
4. Pastikan `.env` sudah berisi `GITHUB_TOKEN`.
5. Jalankan CLI interaktif:
   ```
   python main.py
   ```

Penggunaan (menu interaktif)
Setelah menjalankan `python main.py` Anda akan melihat menu:

1) Whoami (tampilkan user yang terautentikasi)
2) Buat repository
3) Hapus repository
4) Daftar repository
5) Dapatkan info repository
6) Update repository
0) Keluar

Contoh alur:
- Membuat repo:
  - Pilih 2
  - Masukkan nama repository, deskripsi (opsional), pilih private/public, dan (opsional) organization.
- Menghapus repo:
  - Pilih 3
  - Masukkan owner (kosongkan untuk menggunakan user yang terautentikasi) dan nama repo.
  - Konfirmasi penghapusan.
- Daftar repo:
  - Pilih 4
  - Masukkan visibility (`all`, `public`, `private`) dan jumlah per-page (default 100).
- Dapatkan info repo:
  - Pilih 5
  - Masukkan owner dan nama repo.
- Update repo:
  - Pilih 6
  - Masukkan owner dan nama repo, lalu pilih field yang ingin diubah (nama, deskripsi, private).

Catatan keamanan
- Jangan commit token Anda ke VCS.
- Untuk CI/CD, gunakan secrets management (GitHub Actions secrets, GitLab CI variables, dll.) dan hindari menyimpan PAT di repo.
- Batasi scope token seminimal mungkin.

Pengembangan lebih lanjut
- Mengembangkan modul untuk Issues, Pull Requests, Actions, dan lain-lain:
  - Tambahkan metode pada `modules/github_client.py` yang memanggil endpoint GitHub API yang relevan.
  - Tambahkan wrapper modul baru di `modules/` (mis. issues.py, pulls.py) untuk memisahkan logika tindakan.
  - Perluas menu di `main.py` untuk memanggil modul-modul baru.
- Menambahkan mode "CLI arguments" (dual mode) — jika Anda ingin tetap menggunakan argumen baris perintah sekaligus mode interaktif.

Troubleshooting singkat
- Error "GITHUB_TOKEN tidak ditemukan": pastikan file `.env` ada dan berisi `GITHUB_TOKEN`.
- Error 403 / insufficient permissions: periksa scope token dan apakah operasi memerlukan hak organisasi.
- Jika API mengembalikan error JSON, pesan error akan ditampilkan di CLI.

Lisensi
Gunakan untuk belajar dan modifikasi sesuai kebutuhan. Jangan mengunggah token nyata ke repositori publik.

Terima kasih — jika Anda mau, saya bisa:
- Menambahkan modul Issues / Pull Requests sebagai contoh,
- Menambahkan mode CLI (argparse) sekaligus interaktif (dual mode),
- Membuat test unit sederhana untuk github_client.
```