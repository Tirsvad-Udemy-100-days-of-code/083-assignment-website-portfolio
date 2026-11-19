[English](Step-1-Project-Data) · [Dansk](Step-1-Project-Data-da) · **Bahasa Malaysia**

# Langkah 1: Data projek

## Apa yang dibina dalam langkah ini

Projek tidak ditulis dalam kod. Ia disimpan dalam `data/projects.json`, satu entri setiap satu dengan `title`, `type`, `description`, `img_url` dan `source_code_url`. Fungsi `load_from_json` membaca fail itu dan menukar setiap entri kepada `Project`, objek kecil yang tidak boleh diubah dan disemak apabila dibuat: tajuk kosong atau pautan tidak selamat ditolak dengan mesej yang menyebut entri itu.

![Beberapa baris pertama data/projects.json](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-01-project-data.png)

## Apa yang kita pelajari

- Data dan kod diasingkan: anda mengubah portfolio dengan menyunting fail, bukan atur cara.
- JSON terus sepadan dengan senarai dan kamus Python, jadi pustaka standard sudah memadai untuk membacanya.
- Semak data di sempadan: bahagian lain atur cara boleh mempercayai `Project`.
- Mesej ralat yang jelas (fail mana, entri mana, apa yang salah) ialah sebahagian daripada reka bentuk.

## Cuba sendiri

```text
python -m pytest tests/unit -q
```

Seterusnya: [Langkah 2: Halaman utama](Step-2-Home-Page-ms).
