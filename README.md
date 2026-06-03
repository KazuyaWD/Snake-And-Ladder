# Snake-And-Ladder

Anggota:
Moch Syaifulloh Yusuf  (25051204054)
Muhammad Izmul Fadhil (25051204098)
Hafizh Luqmanul Hakim (25051204447)
Hafizh Ahmad Yusuf (25051204138)

Deskripsi Project:  
Snake and Ladder adalah game interaktif yang mengubah permainan ular tangga klasik ke dalam bentuk digital. Melalui game ini, pengguna dapat memulai permainan dari halaman utama, menentukan jumlah pemain, memilih pion, lalu bermain pada papan bernomor 1 sampai 100.
Dalam project ini, Python digunakan sebagai bahasa pemrograman utama. Python berfungsi untuk mengatur mekanisme permainan, mulai dari pemilihan pemain, pemilihan karakter pion, pengacakan angka dadu, perpindahan giliran, pergerakan pion, sampai pembaruan posisi pemain pada papan permainan.

Fitur Utama
  Game Snake and Ladder memiliki beberapa fitur yang membantu pemain menjalankan permainan secara digital. Pada halaman awal, terdapat tombol Play untuk memulai game dan tombol Exit untuk keluar dari aplikasi. Setelah menekan tombol Play, pemain akan diarahkan ke halaman pemilihan jumlah pemain. Pada halaman ini, pengguna dapat memilih jumlah peserta, yaitu 2, 3, atau 4 pemain. Game ini juga menyediakan pilihan pion dengan beberapa karakter, yaitu Phoenix, Horse, Dragon, dan Hydra. Fitur pemilihan pion dibuat agar setiap pemain dapat menggunakan karakter yang berbeda selama permainan berlangsung.
Setelah semua pemain memilih pion, game akan menampilkan halaman Ready sebagai tanda bahwa permainan siap dimulai. Pada halaman utama permainan, tersedia papan ular tangga digital dengan kotak bernomor dari 1 sampai 100. Pemain dapat menggunakan tombol Roll untuk melempar dadu secara otomatis. Hasil lemparan dadu ditampilkan dalam bentuk visual agar mudah dilihat oleh pemain. Selain itu, sistem juga mengatur giliran pemain secara bergantian dan menyediakan leaderboard untuk menampilkan urutan posisi pemain. Dengan fitur tersebut, permainan menjadi lebih teratur, jelas, dan mudah dimainkan.

Cara menjalankan project
Untuk menjalankan project game Snake and Ladder, pengguna perlu memastikan bahwa perangkat yang digunakan sudah memiliki aplikasi pendukung yang diperlukan. Project ini dijalankan menggunakan bahasa pemrograman Python, sehingga Python harus sudah terinstal terlebih dahulu pada komputer atau laptop. Setelah itu, pengguna dapat membuka folder project melalui aplikasi editor kode, seperti Visual Studio Code atau editor lain yang mendukung file Python. Folder project perlu dibuka secara lengkap agar semua file pendukung, seperti gambar, tombol, tampilan, dan file program utama dapat terbaca dengan baik. lalu jalankan file main.py karena itu file utama

Implementasi OOP
Class: Pondasi utama dari game ini, contohnya adalah main, menu, control, board, dice, pause
Abstraksi: class utama yang tidak bisa di jadi class objek
Enkapsulasi: konsep membungkus data (variabel/atribut) dan fungsi (method) menjadi satu kesatuan di dalam Class dan menyembunyikan detail proses internal dan membatasi akses langsung dari luar. contohnya Di kelas Board, fungsi _build_cell_map() dan _load_image() diawali garis bawah karena fungsi luar tidak perlu tahu bagaimana cara papan memuat gambar atau memetakan koordinat kotak.

