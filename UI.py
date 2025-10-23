# app.py yang baru
import streamlit as st
# Hapus: from inference_engine import InferenceEngine
from inference_engine import forward_chaining # <-- Import fungsi inferensi Anda
from inference_engine import load_knowledge_base

st.set_page_config(layout="centered")

# Bagian Judul dan Informasi
st.title("💰 Sistem Pakar Rekomendasi Alokasi Aset Investasi")
st.caption("Proyek UTS Kecerdasan Artifisial - Rule-Based Expert System") # Baris yang sering error, pastikan sudah bersih

# --- Kolom Input ---
with st.sidebar:
    st.header("Masukkan Profil Anda")
    
    # 1. Usia
    usia = st.slider("Usia Anda (Tahun)", 17, 70, 25)
    
    # 2. Profil Risiko
    profil_risiko = st.radio(
        "Profil Risiko",
        ('Konservatif', 'Moderat', 'Aggresif'),
        index=1,
        help="Aggresif: Berani rugi besar demi untung besar. Konservatif: Prioritas keamanan modal."
    )
    
    # 3. Tujuan Finansial
    tujuan_finansial = st.radio(
        "Tujuan Investasi",
        ('Jangka Pendek', 'Jangka Panjang'),
        index=1,
        help="Jangka Pendek: 1-3 tahun. Jangka Panjang: > 5 tahun."
    )
    
    # 4. Status Investor
    status_investor = st.radio(
        "Pengalaman Investasi",
        ('Pemula', 'Bukan Pemula'),
        index=0,
    )

    # 5. Investable Income
    investable_income = st.number_input(
        "Pendapatan yang Diinvestasikan (Rp)",
        min_value=0,
        value=500000,
        step=100000,
        help="Jumlah uang yang siap Anda investasikan per bulan/waktu tertentu."
    )

    # Kumpulkan Data Input
    user_data = {
        "usia": usia,
        "profil_risiko": profil_risiko,
        "tujuan_finansial": tujuan_finansial,
        "status_investor": status_investor,
        "investable_income": investable_income
    }

# --- Tombol Inferensi ---
if st.button("Dapatkan Rekomendasi Alokasi"):
    
    # 1. Panggil fungsi forward_chaining dari inference_engine.py
    # Tidak perlu inisialisasi class, langsung panggil fungsi
    hasil_inferensi = forward_chaining(user_data)
    
    # 2. Tampilkan Hasil
    results = hasil_inferensi["results"]

    if results:
        st.header("Hasil Rekomendasi & Alokasi Aset 🎯")
        
        # Pisahkan Rekomendasi Utama (R1-R6) dan Rekomendasi Tambahan (R7+)
        rekomendasi_utama = [r for r in results if r['rule'] in ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']]
        rekomendasi_tambahan = [r for r in results if r['rule'] not in ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']]
        
        # Tampilkan Rekomendasi Utama (Alokasi)
        if rekomendasi_utama:
            utama = rekomendasi_utama[0] # Ambil yang pertama (asumsi hanya satu R1-R6 yang fire)
            st.subheader(f"✅ {utama['rekomendasi']} (CF: {utama['CF']})")

            # Tampilkan Alokasi Aset dalam bentuk tabel
            if utama.get('alokasi'):
                st.markdown("---")
                st.metric(label="Total Dana Investasi", value=f"Rp {investable_income:,}")
                st.markdown("**ALOKASI ASET**")
                
                alokasi_data = []
                for aset, persen in utama['alokasi'].items():
                    alokasi_data.append({
                        "Aset": aset,
                        "Persentase": persen,
                        "Nominal": f"Rp {round(float(persen.replace('%', ''))/100 * investable_income):,}"
                    })
                
                st.dataframe(alokasi_data, hide_index=True)
                st.caption(f"Penjelasan: {utama['penjelasan']}")
        else:
            # Jika tidak ada R1-R6 yang fire, kemungkinan R9 (Dana Darurat) atau R10 (Usia) yang fire
            darurat_atau_usia = [r for r in results if r['rule'] in ['R9', 'R10']]
            if darurat_atau_usia:
                darurat = darurat_atau_usia[0]
                st.error(f"⚠️ {darurat['rekomendasi']}")
                st.caption(f"Penjelasan: {darurat['penjelasan']}")
            else:
                st.warning("Tidak ada rekomendasi alokasi spesifik yang cocok dengan profil Anda.")


        # Tampilkan Rekomendasi Tambahan/Tips
        if rekomendasi_tambahan:
            st.markdown("---")
            st.subheader("📚 Rekomendasi Tambahan & Tips Investasi")
            for r_t in rekomendasi_tambahan:
                st.info(f"**[{r_t['rule']}] {r_t['rekomendasi']}**")
                st.caption(r_t['penjelasan'])

        # Tampilkan Reasoning Path (Opsional)
        st.markdown("---")
        st.caption("Jalur Penalaran (Reasoning Path):")
        st.code(", ".join(hasil_inferensi['reasoning_path']))
        
    else:
        st.warning("Tidak ada aturan yang terpenuhi untuk data input ini. Mohon periksa kembali input Anda.")