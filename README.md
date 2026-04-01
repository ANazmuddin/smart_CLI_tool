# 🤖 Asisten Terminal AI (Smart CLI Tool)

Asisten Terminal AI adalah *Command Line Interface* (CLI) pintar yang menerjemahkan bahasa manusia (natural language) menjadi perintah Bash Linux yang valid. Project ini dibangun menggunakan Python, LangChain, dan model Google Gemini untuk membantu mengotomatisasi tugas-tugas terminal sehari-hari.

## ✨ Fitur Utama
* **Natural Language to Bash:** Cukup ketik apa yang ingin kamu lakukan dalam bahasa Indonesia, dan AI akan merumuskan perintah Bash-nya.
* **Aman & Terkontrol:** Dilengkapi dengan fitur konfirmasi (Y/n) sebelum mengeksekusi perintah apa pun di sistem operasimu, sehingga mencegah modifikasi sistem yang tidak disengaja.
* **Ringan & Cepat:** Menggunakan model `gemini-2.5-flash` untuk respons yang instan.

## 🛠️ Tech Stack
* **Python** (Kompatibel dengan Python 3.14)
* **LangChain Core** (Framework Orkestrasi AI)
* **Google Generative AI** (LLM Provider)
* **Typer** (CLI Interface Builder)
* **Python-dotenv** (Environment Management)

---

## 🚀 Cara Instalasi (Local Development)

Ikuti langkah-langkah berikut untuk menjalankan project ini di komputer lokalmu:

### 1. Clone Repository
Buka terminal dan *clone repository* ini ke direktori lokalmu:
```bash
git clone https://github.com/ANazmuddin/smart_CLI_tool.git
cd smart_CLI_tool
```
*(Catatan: Ubah URL di atas dengan URL repository GitHub aslimu nanti)*

### 2. Siapkan Virtual Environment
Sangat disarankan untuk menggunakan *virtual environment* agar *library* project ini tidak bercampur dengan sistem utama:
```bash
python -m venv env
source env/bin/activate
```

### 3. Install Dependencies
Install semua *library* yang dibutuhkan menggunakan `pip`:
```bash
pip install langchain_core langchain-google-genai typer python-dotenv
```

### 4. Konfigurasi API Key (Environment Variables)
Project ini membutuhkan Google Gemini API Key.
1. Dapatkan API Key gratis di [Google AI Studio](https://aistudio.google.com/).
2. Buat file baru bernama `.env` di direktori utama project (sejajar dengan file `asisten.py`).
3. Tambahkan API Key kamu ke dalam file `.env` tersebut dengan format berikut:
```env
GOOGLE_API_KEY="paste_api_key_kamu_di_sini"
```
*(Catatan: File `.env` sudah dimasukkan ke dalam `.gitignore` sehingga API Key kamu aman dan tidak akan ter-push ke GitHub).*

---

## 💡 Cara Penggunaan

Pastikan *virtual environment* kamu sedang aktif (`source env/bin/activate`). 

Gunakan perintah `python asisten.py` diikuti dengan instruksi natural yang dibungkus tanda kutip (`" "`).

**Contoh Penggunaan:**

1. Membuat struktur folder dan file:
```bash
python asisten.py "buat folder bernama frontend_app dan di dalamnya buat file index.html"
```

2. Mencari file tertentu:
```bash
python asisten.py "tampilkan daftar semua file yang berakhiran .py di folder ini"
```

3. Mengelola sistem:
```bash
python asisten.py "tampilkan informasi penggunaan RAM saat ini"
```

**Alur Kerja:**
1. AI akan membaca instruksimu dan memproses perintah Bash yang paling tepat.
2. Terminal akan menampilkan perintah yang dihasilkan.
3. Program akan bertanya: `Apakah kamu ingin menjalankan perintah ini? [y/N]:`
4. Ketik `y` lalu `Enter` untuk mengeksekusi, atau `N` untuk membatalkan.

---
