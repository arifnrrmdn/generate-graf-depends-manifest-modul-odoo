# Generate Odoo Module Dependency Visualizer

Tool ini digunakan untuk **menggambarkan hubungan dependensi antar modul Odoo** dengan membaca file `__manifest__.py` pada folder addons lokal, kemudian memvisualisasikannya menggunakan **Graphviz**.

## ✨ Fitur
- Membaca semua modul di folder `addons` lokal.
- Mengambil informasi `depends` dari file `__manifest__.py` masing-masing modul.
- Menggambarkan hubungan dependensi dalam bentuk graf.
- Modul eksternal (tidak ditemukan di folder addons lokal) ditandai dengan **warna abu-abu dan garis putus-putus**.
- Output berupa file gambar `.png` yang bisa digunakan untuk dokumentasi atau analisis arsitektur modul.

## 📦 Kebutuhan
- Python 3.x
- [Graphviz](https://graphviz.org/download/) (wajib terinstall di sistem)
- Modul Python:
  ```bash
  pip install graphviz


## Cara Menjalankan
1. Jalankan Perintah
    ```bash
    python generate_dependencies.py

2. File Output berupa gambar dan file raw akan tersimpan di:
    ```bash
    {OUTPUT_DIAGRAM}/odoo_dependencies_full.png


## Hasil Output

- Node biru = modul lokal di folder addons.
- Node abu-abu putus-putus = modul eksternal (tidak ditemukan di folder addons).
- Panah menunjukkan arah dependensi (dependensi → modul).


