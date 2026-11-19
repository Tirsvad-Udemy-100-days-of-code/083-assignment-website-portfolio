[English](Lecture-Summary) · [Dansk](Lecture-Summary-da) · **Bahasa Malaysia**

# Ringkasan kuliah

Ini ringkasan pendek kuliah Hari 83, dengan perkataan saya sendiri. Kuliah itu sengaja tidak memberi bantuan langkah demi langkah.

## Tugasan

Bina laman web yang menunjukkan siapa anda sebagai pembangun: halaman utama dengan projek yang telah anda buat, dan halaman tentang dengan beberapa perkataan mengenai diri dan kemahiran anda. Setiap projek ada nama, jenis, penerangan, gambar dan pautan ke kod sumbernya.

## Idea di sebaliknya

Selepas 82 hari latihan kecil, kursus meminta anda merancang dan membina sesuatu sendiri. Kuliah mencadangkan aplikasi web dengan pangkalan data kecil, tetapi tujuannya ialah berlatih memecahkan matlamat kepada langkah, mencari tahu apa yang anda tidak tahu dan menyelesaikannya sendiri.

## Fungsi yang dinamakan dalam tugasan

Tugasan menamakan tiga fungsi: `home` (halaman dengan projek), `about` (halaman tentang anda) dan `load_from_json` (membaca projek daripada fail). Projek ini mengekalkan nama itu.

## Bagaimana projek ini menjawabnya

Projek ini mencapai matlamat yang sama dengan Flask untuk halaman web dan SQLite, melalui modul `sqlite3` Python sendiri, untuk data. Halaman dijana daripada pangkalan data pada setiap permintaan, jadi perubahan kelihatan serta-merta. Alasannya ditulis dalam rekod keputusan [ADR-0003](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/src/branch/main/docs/adr/adr-0003-flask-and-jinja-on-sqlite.md). Setiap langkah diterangkan pada halamannya sendiri, bermula dengan [Langkah 1](Step-1-Project-Data-ms).
