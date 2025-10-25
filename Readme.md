<h1 align="center">FinWise</h1>
<hr>

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,ts,js,tailwind,next" />
  </a>
</p>

## Deskripsi

FinWise adalah sistem pakar berbasis web yang memberikan rekomendasi alokasi aset investasi berdasarkan profil pengguna seperti usia, profil risiko, tujuan finansial, pengalaman, dan pendapatan yang dapat diinvestasikan.
Proyek ini menggabungkan FastAPI (Python) sebagai inference engine dan Next.js + TypeScript (React) sebagai antarmuka pengguna (frontend).


## Alur Data

1. Pengguna mengisi profil (usia, profil risiko, tujuan, dsb) di halaman web.

2. Data dikirim ke endpoint FastAPI /inferen.

3. Engine forward_chaining() membaca knowledge base, mengevaluasi aturan, dan mengembalikan hasil rekomendasi.

4. Frontend menampilkan hasil dalam bentuk kartu rekomendasi dan penjelasan.

## Cara Menjalankan

1. Clone Repository

    ``` bash
    git clone https://github.com/muhammadhizqilalfi/uts-ai-invest.git
    cd uts-ai-invest 
    ```

2. Jalankan Backend (FastAPI)

    Masuk ke folder ```engine```:

    ```bash
    cd  engine
    ```
    
    Install depedensi Python:

    ```bash
    pip install -r requirement.txt
    ```

    Jalankan server:

    ```bash
    uvicorn server:app --reload
    ```

    Server akan berjalan di:
    http://localhost:8000


3. Jalankan Frontend

    Buka terminal baru lalu masuk ke folder ```ui```:

    ```bash
    cd ui
    ```

    Install dependensi:

    ```bash
    npm install
    ```

    Jalankan server node:

    ```bash
    npm run dev
    ```

    Frontend akan berjalan di:
    http://localhost:3000
