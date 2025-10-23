import streamlit as st
from inference_engine import forward_chaining
from inference_engine import load_knowledge_base

st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="Sistem Pakar Investasi", page_icon="💎")

# Inject custom CSS untuk tampilan modern dan meriah
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

/* Background dengan gradient */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 100%);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    font-family: 'Poppins', sans-serif;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Sidebar Styling - Card Style */
.sidebar .sidebar-content {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Header dengan efek glassmorphism */
[data-testid="stHeader"] {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
}

/* Styling untuk judul utama */
h1 {
    color: #ffffff !important;
    text-align: center;
    font-weight: 700 !important;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    margin-bottom: 10px;
    animation: slideDown 0.5s ease-out;
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Caption styling */
.stApp .stMarkdown p {
    color: #ffffff;
    text-align: center;
    font-size: 1.1rem;
}

/* Card untuk input section */
.input-card {
    background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    margin-bottom: 20px;
    border: 2px solid #10b981;
    animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}

/* Sidebar header */
.sidebar .sidebar-content h2 {
    color: #10b981 !important;
    font-weight: 600 !important;
    text-align: center;
    padding: 15px;
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
    border-radius: 10px;
    margin-bottom: 20px;
}

/* Input field styling */
.stSlider > div > div > div {
    background: linear-gradient(90deg, #10b981 0%, #059669 100%);
}

.stRadio > label {
    color: #047857 !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
}

.stNumberInput > label {
    color: #047857 !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
}

/* Card hasil utama dengan efek 3D */
.big-result-card {
    background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(16, 185, 129, 0.3);
    margin-bottom: 30px;
    border: 3px solid #10b981;
    transform: perspective(1000px) rotateX(2deg);
    transition: all 0.3s ease;
    animation: popIn 0.6s ease-out;
}

@keyframes popIn {
    0% {
        opacity: 0;
        transform: scale(0.8) perspective(1000px) rotateX(10deg);
    }
    100% {
        opacity: 1;
        transform: scale(1) perspective(1000px) rotateX(2deg);
    }
}

.big-result-card:hover {
    transform: perspective(1000px) rotateX(0deg);
    box-shadow: 0 25px 70px rgba(16, 185, 129, 0.4);
}

/* Header hasil */
.stApp h2 {
    color: #065f46 !important;
    font-weight: 700 !important;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.stApp h3 {
    color: #047857 !important;
    font-weight: 600 !important;
}

/* Button dengan efek animasi */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    font-weight: 700;
    font-size: 1.2rem;
    border-radius: 15px;
    border: none;
    padding: 15px 30px;
    transition: all 0.3s ease;
    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
    text-transform: uppercase;
    letter-spacing: 1px;
}

div.stButton > button:first-child:hover {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 12px 30px rgba(16, 185, 129, 0.6);
}

div.stButton > button:first-child:active {
    transform: translateY(-1px);
}

/* Metric cards dengan glassmorphism */
[data-testid="stMetricValue"] {
    color: #065f46 !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
}

[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    border: 2px solid #d1fae5;
}

/* Dataframe styling */
.stDataFrame {
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

/* Expander dengan warna menarik */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #a7f3d0 0%, #6ee7b7 100%);
    border-radius: 10px;
    font-weight: 600;
    color: #065f46 !important;
}

/* Info box */
.stAlert {
    border-radius: 15px;
    border-left: 5px solid #10b981;
}

/* Success message */
div[data-baseweb="notification"] {
    border-radius: 15px;
    border-left: 5px solid #10b981;
}

/* Animasi untuk tips cards */
.tip-card {
    animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Emoji dengan animasi */
.emoji-bounce {
    display: inline-block;
    animation: bounce 2s infinite;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

/* Responsive adjustments */
@media (max-width: 768px) {
    h1 {
        font-size: 1.8rem !important;
    }
    .big-result-card {
        padding: 20px;
    }
}
</style>
""", unsafe_allow_html=True)

# Header dengan emoji animasi
st.markdown("""
<h1>
    <span class="emoji-bounce">💎</span> 
    Sistem Pakar Rekomendasi Alokasi Aset Investasi 
    <span class="emoji-bounce">📈</span>
</h1>
""", unsafe_allow_html=True)

st.caption("🤖 Proyek Kecerdasan Artifisial - Rule-Based Expert System | Investasi Cerdas Untuk Masa Depan Cerah ✨")

# --- Kolom Input (Sidebar) dengan Card Style ---
with st.sidebar:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.header("📋 Profil Investor Anda")
    st.markdown("Isi data berikut untuk mendapatkan rekomendasi investasi yang tepat!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 1. Usia dengan icon
    st.markdown("### 🎂 Usia Anda")
    usia = st.slider("Berapa usia Anda saat ini?", 17, 70, 25, help="Usia mempengaruhi toleransi risiko investasi Anda")
    
    st.markdown("---")
    
    # 2. Profil Risiko dengan emoji
    st.markdown("### 🎯 Profil Risiko")
    profil_risiko = st.radio(
        "Bagaimana sikap Anda terhadap risiko?",
        ('🛡️ Konservatif', '⚖️ Moderat', '🚀 Aggresif'),
        index=1,
        help="• Aggresif: Berani rugi besar demi untung besar\n• Moderat: Seimbang antara risiko dan return\n• Konservatif: Prioritas keamanan modal"
    )
    # Clean the emoji for processing
    profil_risiko = profil_risiko.split(' ')[1]
    
    st.markdown("---")
    
    # 3. Tujuan Finansial
    st.markdown("### 🎯 Tujuan Investasi")
    tujuan_finansial = st.radio(
        "Berapa lama jangka waktu investasi Anda?",
        ('⏱️ Jangka Pendek', '🏆 Jangka Panjang'),
        index=1,
        help="• Jangka Pendek: 1-3 tahun (misal: dana darurat, liburan)\n• Jangka Panjang: > 5 tahun (misal: pensiun, pendidikan anak)"
    )
    # Clean the emoji
    tujuan_finansial = ' '.join(tujuan_finansial.split(' ')[1:])
    
    st.markdown("---")
    
    # 4. Status Investor
    st.markdown("### 📚 Pengalaman Investasi")
    status_investor = st.radio(
        "Seberapa berpengalaman Anda dalam berinvestasi?",
        ('🌱 Pemula', '⭐ Berpengalaman'),
        index=0,
        help="Pemula: Baru pertama kali atau kurang dari 1 tahun\nBerpengalaman: Sudah lebih dari 1 tahun aktif berinvestasi"
    )
    # Clean the emoji
    status_investor = status_investor.split(' ')[1]
    if status_investor == "Berpengalaman":
        status_investor = "Bukan Pemula"

    st.markdown("---")
    
    # 5. Investable Income
    st.markdown("### 💰 Dana Investasi")
    investable_income = st.number_input(
        "Berapa dana yang siap Anda investasikan? (Rp)",
        min_value=0,
        value=5000000,
        step=500000,
        help="💡 Tip: Pastikan ini adalah dana 'dingin' yang tidak akan Anda butuhkan dalam waktu dekat"
    )
    
    # Format nominal
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
                padding: 15px; 
                border-radius: 10px; 
                text-align: center;
                border: 2px solid #10b981;
                margin-top: 15px;">
        <p style="color: #065f46; font-weight: 600; margin: 0; font-size: 0.9rem;">Total Dana Investasi</p>
        <p style="color: #047857; font-weight: 700; margin: 5px 0 0 0; font-size: 1.5rem;">Rp {investable_income:,.0f}</p>
    </div>
    """, unsafe_allow_html=True)

    # Kumpulkan Data Input
    user_data = {
        "usia": usia,
        "profil_risiko": profil_risiko,
        "tujuan_finansial": tujuan_finansial,
        "status_investor": status_investor,
        "investable_income": investable_income
    }

st.markdown("<br>", unsafe_allow_html=True)

# --- Tombol Inferensi dengan style khusus ---
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analyze_button = st.button("🔍 Analisis & Dapatkan Rekomendasi", use_container_width=True)

if analyze_button:
    
    # Progress bar untuk efek loading
    with st.spinner('🔄 Menganalisis profil investasi Anda...'):
        import time
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
    
    # 1. Panggil fungsi forward_chaining
    hasil_inferensi = forward_chaining(user_data)
    
    # 2. Tampilkan Hasil
    results = hasil_inferensi["results"]

    if results:
        
        # Success message
        st.success("✅ Analisis selesai! Berikut rekomendasi investasi untuk Anda:")
        
        # Pisahkan Rekomendasi Utama (R1-R6) dan Rekomendasi Tambahan (R7+)
        rekomendasi_utama = [r for r in results if r['rule'] in ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']]
        rekomendasi_tambahan = [r for r in results if r['rule'] not in ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']]
        
        # --- BAGIAN HASIL UTAMA ---
        if rekomendasi_utama:
            utama = rekomendasi_utama[0]
            
            # Card besar untuk hasil utama
            with st.container():
                st.markdown('<div class="big-result-card">', unsafe_allow_html=True)
                
                # Icon berdasarkan profil risiko
                risk_icons = {
                    'Konservatif': '🛡️',
                    'Moderat': '⚖️',
                    'Aggresif': '🚀'
                }
                icon = risk_icons.get(user_data['profil_risiko'], '💼')
                
                st.markdown(f"## {icon} Hasil Rekomendasi Alokasi Aset")
                
                # Judul Rekomendasi dengan badge
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                            padding: 20px; 
                            border-radius: 15px; 
                            margin: 20px 0;
                            box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);">
                    <h3 style="color: white; margin: 0; text-align: center; font-weight: 700;">
                        ✅ {utama['rekomendasi']}
                    </h3>
                    <p style="color: #d1fae5; text-align: center; margin: 10px 0 0 0; font-size: 1.1rem;">
                        Tingkat Kepastian (CF): <strong style="color: white; font-size: 1.3rem;">{utama['CF']}</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Tampilkan Alokasi Aset dalam bentuk tabel
                if utama.get('alokasi'):
                    st.markdown("---")
                    
                    # Tampilkan metrik total dana
                    col1_metric, col2_metric, col3_metric = st.columns(3)
                    with col1_metric:
                         st.metric(
                             label="💰 Total Dana", 
                             value=f"Rp {investable_income:,.0f}", 
                             help="Dana yang Anda siapkan untuk investasi"
                         )
                    with col2_metric:
                         st.metric(
                             label="🎯 Profil Risiko", 
                             value=user_data['profil_risiko'],
                             help="Tingkat toleransi risiko Anda"
                         )
                    with col3_metric:
                         st.metric(
                             label="⏰ Jangka Waktu", 
                             value=user_data['tujuan_finansial'],
                             help="Target waktu investasi Anda"
                         )
                         
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 📊 Distribusi Aset Investasi")
                    
                    alokasi_data = []
                    asset_icons = {
                        'Saham': '📈',
                        'Obligasi': '📄',
                        'Reksa Dana': '💼',
                        'Deposito': '🏦',
                        'Emas': '🥇',
                        'Properti': '🏠'
                    }
                    
                    for aset, persen in utama['alokasi'].items():
                        nominal = round(float(persen.replace('%', ''))/100 * investable_income)
                        icon = asset_icons.get(aset, '💎')
                        alokasi_data.append({
                            "Jenis Aset": f"{icon} {aset}",
                            "Persentase": persen,
                            "Nominal (Rp)": f"Rp {nominal:,.0f}"
                        })
                    
                    st.dataframe(
                        alokasi_data, 
                        hide_index=True, 
                        use_container_width=True,
                        height=None
                    )
                    
                    st.markdown("---")
                    st.markdown(f"### 📖 Penjelasan Strategi (`{utama['rule']}`)")
                    st.info(f"💡 {utama['penjelasan']}")
                
                st.markdown('</div>', unsafe_allow_html=True)

        else:
            # Jika tidak ada R1-R6 yang fire
            darurat_atau_usia = [r for r in results if r['rule'] in ['R9', 'R10']]
            if darurat_atau_usia:
                darurat = darurat_atau_usia[0]
                st.error(f"⚠️ **{darurat['rekomendasi']}**")
                st.markdown(f"""
                <div style="background: #fef2f2; padding: 20px; border-radius: 15px; border-left: 5px solid #ef4444;">
                    <p style="color: #991b1b; font-size: 1.1rem; margin: 0;">
                        💬 <strong>Penjelasan:</strong> {darurat['penjelasan']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Tidak ada rekomendasi alokasi spesifik yang cocok dengan profil Anda. Coba cek data input.")


        # --- BAGIAN REKOMENDASI TAMBAHAN / TIPS ---
        if rekomendasi_tambahan:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="text-align: center; margin: 30px 0;">
                <h2 style="color: #065f46; font-weight: 700;">
                    💡 Tips & Pertimbangan Tambahan
                </h2>
                <p style="color: white; font-size: 1.1rem;">
                    Saran tambahan untuk mengoptimalkan strategi investasi Anda
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Tampilkan dalam dua kolom responsif
            col_tips_1, col_tips_2 = st.columns(2)
            
            tips_icons = ['💰', '📚', '🎓', '⚡', '🔔', '🌟', '🎯', '💪']
            
            for i, r_t in enumerate(rekomendasi_tambahan):
                target_col = col_tips_1 if i % 2 == 0 else col_tips_2
                icon = tips_icons[i % len(tips_icons)]
                
                with target_col:
                    with st.expander(f"{icon} **[{r_t['rule']}] {r_t['rekomendasi']}**", expanded=False):
                        st.markdown(f"<div class='tip-card'>{r_t['penjelasan']}</div>", unsafe_allow_html=True)

        # --- BAGIAN TECHNICAL / DEBUG ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        with st.expander("🔬 Detail Teknis & Jalur Penalaran (Developer Mode)", expanded=False):
            col_tech1, col_tech2 = st.columns(2)
            
            with col_tech1:
                st.markdown("#### ✅ Aturan yang Terpenuhi")
                st.code(", ".join(hasil_inferensi['reasoning_path']), language="text")
            
            with col_tech2:
                st.markdown("#### 🧠 Working Memory")
                st.json(hasil_inferensi['working_memory'])
            
    else:
        st.warning("⚠️ Tidak ada aturan yang terpenuhi untuk data input ini. Mohon periksa kembali input Anda dan pastikan `knowledge_base.json` tersedia.")
        st.info("💡 Pastikan semua input sudah terisi dengan benar dan sistem dapat mengakses knowledge base.")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 20px; background: rgba(255, 255, 255, 0.1); border-radius: 15px; margin-top: 30px;">
    <p style="color: white; margin: 0; font-size: 0.9rem;">
        💎 <strong>Sistem Pakar Investasi</strong> | Dibuat dengan ❤️ menggunakan Streamlit<br>
        <em>Investasi Cerdas Dimulai dari Keputusan yang Tepat</em> ✨
    </p>
</div>
""", unsafe_allow_html=True)