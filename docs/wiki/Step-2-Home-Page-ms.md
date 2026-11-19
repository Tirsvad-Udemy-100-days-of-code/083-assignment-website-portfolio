[English](Step-2-Home-Page) · [Dansk](Step-2-Home-Page-da) · **Bahasa Malaysia**

# Langkah 2: Halaman utama

## Apa yang dibina dalam langkah ini

Kes guna `home` meminta repositori projek untuk semua projek dan memulangkan `HomePage` dengan satu kad data biasa bagi setiap projek. Paparan halaman utama menukarkannya kepada HTML. Gambar menunjukkan halaman tanpa helaian gaya, jadi anda nampak struktur asasnya: tajuk, senarai projek dan bagi setiap satu, tajuk, gambar, penerangan dan pautan.

![Halaman utama tanpa helaian gaya](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-02-home-page-structure.png)

## Apa yang kita pelajari

- Kes guna memegang apa yang atur cara lakukan; paparan hanya menentukan rupanya.
- Semua yang datang daripada fail data di-escape dengan `html.escape` sebelum sampai ke halaman, jadi tajuk dengan `<script>` dipaparkan sebagai teks dan tidak pernah dijalankan.
- HTML semantik (tajuk, senarai, pautan) berfungsi tanpa CSS, dan halaman boleh diuji tanpa pelayar.

## Cuba sendiri

```text
python -m portfolio build
# open build/index.html in a browser
```

Seterusnya: [Langkah 3: Halaman tentang](Step-3-About-Page-ms).
