[English](Step-5-Preview) · [Dansk](Step-5-Preview-da) · **Bahasa Malaysia**

# Langkah 5: Pratonton

## Apa yang dibina dalam langkah ini

Dua arahan melengkapkan alat ini. `python -m portfolio build` membaca data dan menulis `index.html`, `about.html` dan `style.css` ke dalam folder. `python -m portfolio serve` menunjukkan folder itu dengan `http.server` pustaka standard di <http://127.0.0.1:8000>. Kedua-duanya ada pilihan (`--data`, `--out`, `--host`, `--port`) dan memberi satu baris mesej serta kod keluar bukan sifar apabila ada masalah, contohnya fail data tiada.

![Arahan build dan outputnya](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-05-build-command.png)

![Laman pada pelayan pratonton setempat](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-05-preview-server.png)

## Apa yang kita pelajari

- Antara muka baris arahan dengan `argparse`, dengan teks bantuan percuma.
- Pelayan mendengar pada `127.0.0.1` secara lalai, jadi hanya komputer anda sendiri boleh mencapainya.
- Akar gubahan (`__main__.py`) ialah satu-satunya tempat yang menyambung lapisan; kod lain tidak mengenali kelas konkrit.

## Cuba sendiri

```text
python -m portfolio --help
python -m portfolio build --data data --out build
python -m portfolio serve --out build
```

Seterusnya: [Langkah 6: Ujian](Step-6-Tests-ms).
