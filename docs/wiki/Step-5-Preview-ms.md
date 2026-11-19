[English](Step-5-Preview) · [Dansk](Step-5-Preview-da) · **Bahasa Malaysia**

# Langkah 5: Pratonton

## Apa yang dibina dalam langkah ini

Satu arahan menunjukkan laman. `python -m portfolio serve` memulakan pelayan Flask di <http://127.0.0.1:8000>. Ia ada pilihan `--db`, `--data`, `--host` dan `--port`. Setiap permintaan membaca pangkalan data dan menjana halaman dengan templat Jinja, jadi tiada langkah binaan. Apabila pangkalan data tiada, `serve` memberi satu baris mesej yang menyebut arahan `init` dan `import`, serta kod keluar bukan sifar.

![Arahan serve dan pangkalan data yang tiada](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-05-serve-command.png)

![Laman pada pelayan pratonton setempat](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-05-preview-server.png)

## Apa yang kita pelajari

- Antara muka baris arahan dengan `argparse`, dengan teks bantuan percuma.
- Pelayan mendengar pada `127.0.0.1` secara lalai, jadi hanya komputer anda sendiri boleh mencapainya.
- Akar gubahan (`__main__.py`) ialah satu-satunya tempat yang menyambung lapisan; kod lain tidak mengenali kelas konkrit.

## Cuba sendiri

```text
python -m portfolio --help
python -m portfolio serve --db data/portfolio.db --data data --port 8000
```

Seterusnya: [Langkah 6: Ujian](Step-6-Tests-ms).
