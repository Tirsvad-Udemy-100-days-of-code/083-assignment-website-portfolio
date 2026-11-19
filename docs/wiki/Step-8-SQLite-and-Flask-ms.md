[English](Step-8-SQLite-and-Flask) · [Dansk](Step-8-SQLite-and-Flask-da) · **Bahasa Malaysia**

# Langkah 8: SQLite dan Flask

## Apa yang dibina dalam langkah ini

Laman ini dinamik. Data disimpan dalam pangkalan data SQLite, `data/portfolio.db`, yang dibaca Python dengan modul `sqlite3` sendiri. `python -m portfolio init` mencipta pangkalan data, dan `python -m portfolio import` menyalin fail JSON contoh ke dalamnya sekali. Selepas itu pangkalan data ialah satu-satunya sumber. Anda mengubahnya dengan arahan: `project list`, `project add`, `project set`, `project remove` dan `profile set`. `serve` memulakan aplikasi Flask yang membuka pangkalan data secara baca sahaja pada setiap permintaan, menjalankan kes guna `home` atau `about` dan menjana templat Jinja. Jadi projek yang anda tambah dengan arahan kelihatan pada muat semula seterusnya, tanpa binaan dan tanpa mula semula.

![Mencipta pangkalan data, mengimport data contoh dan menyenaraikan projek](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-08-database-commands.png)

![Projek yang ditambah dengan arahan kelihatan pada muat semula seterusnya](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-08-project-added.png)

## Apa yang kita pelajari

- Pangkalan data memisahkan data daripada fail: satu tempat untuk membaca dan menulis, dengan peraturan yang boleh dipercayai atur cara.
- Setiap pernyataan SQL ditulis lebih awal dan menerima nilainya sebagai parameter, tidak pernah ditampal ke dalam teks, jadi tajuk seperti `'; DROP TABLE project; --` hanyalah tajuk.
- Pelayan web hanya membaca. Ia tiada laluan yang mengubah data, tiada log masuk dan tiada sesi, jadi sedikit sahaja yang boleh diserang.
- Flask ialah satu kebergantungan yang dikunci. Kes guna dan domain tidak mengimportnya, dan semakan lapisan membuktikannya, jadi lapisan web boleh diganti tanpa menyentuh peraturan.
- Pelayan menghantar pengepala `Content-Security-Policy`, `X-Content-Type-Options` dan `Referrer-Policy` pada setiap jawapan.

## Cuba sendiri

```text
python -m portfolio init
python -m portfolio import
python -m portfolio project list
python -m portfolio project add --title "My new project" --kind Website --description "Added with a command while the server runs." --source-code-url https://example.com/my-new-project --tag Flask --skill SQLite
python -m portfolio serve
```

Muat semula halaman utama selepas arahan `project add` dan kad baharu ada di situ.
