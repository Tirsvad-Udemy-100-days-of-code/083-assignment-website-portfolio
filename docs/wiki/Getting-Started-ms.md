[English](Getting-Started) · [Dansk](Getting-Started-da) · **Bahasa Malaysia**

# Bermula

Anda memerlukan Python 3.13 atau lebih baharu dan Git. `pip` memasang Flask, satu-satunya kebergantungan semasa dijalankan, bersama pakej yang diperlukan Flask. Docker hanya diperlukan untuk mengambil semula tangkapan skrin, dan Doxygen hanya untuk membina rujukan API.

## Sediakan

Windows (PowerShell):

```text
git clone https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio.git
cd 083-assignment-website-portfolio
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Linux dan macOS:

```text
git clone https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio.git
cd 083-assignment-website-portfolio
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Folder `.venv` ialah salinan Python yang peribadi untuk projek ini, jadi tiada apa dipasang pada seluruh sistem. Jalankan `deactivate` untuk keluar.

## Jalankan

```text
python -m portfolio init
python -m portfolio import
python -m portfolio serve
```

`init` mencipta pangkalan data, `import` mengisinya daripada fail JSON contoh dalam `data/`, dan `serve` memulakan pelayan Flask. Buka <http://127.0.0.1:8000> dalam pelayar. Tekan `Ctrl+C` untuk menghentikan pelayan.

## Uji

```text
python -m pytest
```

Teruskan dengan [Ringkasan kuliah](Lecture-Summary-ms) atau terus ke [Langkah 1](Step-1-Project-Data-ms).
