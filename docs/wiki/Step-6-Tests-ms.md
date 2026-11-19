[English](Step-6-Tests) · [Dansk](Step-6-Tests-da) · **Bahasa Malaysia**

# Langkah 6: Ujian

## Apa yang dibina dalam langkah ini

`pytest` menjalankan ujian unit untuk entiti dan kes guna, ujian integrasi untuk repositori JSON dan penulis laman, serta ujian hujung ke hujung yang membina laman contoh sebenar dan membaca hasilnya. `lint-imports` menyemak bahawa lapisan hanya bergantung ke dalam, `ruff` menyemak gaya dan `mypy --strict` menyemak jenis.

![Larian ujian](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-06-tests.png)

## Apa yang kita pelajari

- Ujian pada tiga peringkat: kecil dan pantas di bawah, beberapa yang membuktikan seluruh laman di atas.
- Kerana kes guna bergantung pada port, ia diuji dengan pengganti mudah dalam memori, tanpa fail dan tanpa pelayar.
- Peraturan yang disemak oleh alat (kontrak lapisan) kekal benar apabila kod membesar.

## Cuba sendiri

```text
python -m pytest
python -m ruff check .
python -m mypy
lint-imports
```

Seterusnya: [Langkah 7: Kad terbalik dan profil](Step-7-Flip-Cards-and-Profile-ms).
