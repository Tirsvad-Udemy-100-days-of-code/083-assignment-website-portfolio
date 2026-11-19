[English](Step-7-Flip-Cards-and-Profile) · [Dansk](Step-7-Flip-Cards-and-Profile-da) · **Bahasa Malaysia**

# Langkah 7: Kad terbalik dan profil

## Apa yang dibina dalam langkah ini

Setiap projek ialah kad terbalik. Bahagian depan menunjukkan gambar, nama dan penerangan projek. Bahagian belakang menunjukkan pautan ke kod sumber, tag dan kemahiran yang ditunjukkan oleh projek. Kad berpusing apabila tetikus di atasnya, apabila fokus papan kekunci dan apabila diketik. Halaman tentang memaut ke profil LinkedIn pemilik dan menunjukkan gambar profil pemilik, atau avatar bulat dengan huruf awal jika tiada gambar ditetapkan. Binaan menyalin semua gambar daripada folder data ke dalam laman.

![Bahagian depan kad projek](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-07-flip-card-front.png)

![Bahagian belakang kad projek](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-07-flip-card-back.png)

![Halaman tentang dengan pautan LinkedIn dan gambar profil](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-07-about-page.png)

## Apa yang kita pelajari

- Putaran 3D ialah CSS biasa (`transform-style: preserve-3d` dan `backface-visibility: hidden`), tanpa JavaScript.
- Kebolehcapaian: kad boleh dicapai dengan papan kekunci, dan pelawat yang lebih suka gerakan dikurangkan tidak mendapat animasi.
- Jenis fail baharu, imej binari, memerlukan port baharu untuk membaca fail dan cara bagi penulis laman menulis bait, dan semakan laluan yang sama seperti untuk teks menghalang laluan yang buruk keluar daripada folder.
- Projek contoh ialah kerja sebenar yang menunjukkan kemahiran sebenar, bukan latihan kursus: fail data ialah portfolio.

## Cuba sendiri

Sunting `data/projects.json` untuk menambah `tags` dan `skills` pada projek, letakkan gambar anda dalam `data/images/` dan tetapkan `"photo"` dalam `data/profile.json`, kemudian bina semula.
