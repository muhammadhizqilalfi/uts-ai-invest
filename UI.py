import streamlit as st
from inference_engine import forward_chaining
from inference_engine import load_knowledge_base

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Sistem Pakar Investasi", page_icon="💰")

# Inject custom CSS untuk tampilan modern dengan warna teal/cyan
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

/* Background putih bersih */
.stApp {
    background-color: #ffffff;
    font-family: 'Inter', sans-serif;
}

/* Hide sidebar completely */
[data-testid="stSidebar"] {
    display: none;
}

/* Header dengan warna teal */
[data-testid="stHeader"] {
    background-color: #f8fafc;
}

/* Container utama */
.main .block-container {
    max-width: 1400px;
    padding: 2rem 3rem;
}

/* Header Section */
.header-section {
    background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
    padding: 2rem 3rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(13, 148, 136, 0.2);
}

.header-title {
    color: white;
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 15px;
}

.header-subtitle {
    color: rgba(255, 255, 255, 0.9);
    font-size: 1.1rem;
    margin-top: 0.5rem;
    font-weight: 400;
}

/* Section Title */
.section-title {
    color: #0f766e;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 3px solid #14b8a6;
}

/* Input Card Container */
.input-cards-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

/* Individual Input Card */
.input-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    border: 2px solid #e0f2f1;
    transition: all 0.3s ease;
}

.input-card:hover {
    box-shadow: 0 8px 25px rgba(13, 148, 136, 0.15);
    border-color: #14b8a6;
    transform: translateY(-2px);
}

.input-card-title {
    color: #0f766e;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Styling untuk input fields */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #14b8a6 0%, #0d9488 100%);
}

.stSlider > label {
    color: #0f766e !important;
    font-weight: 600 !important;
}

.stSelectbox > label {
    color: #0f766e !important;
    font-weight: 600 !important;
}

.stNumberInput > label {
    color: #0f766e !important;
    font-weight: 600 !important;
}

/* Summary Card */
.summary-card {
    background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%);
    padding: 2rem;
    border-radius: 15px;
    border: 3px solid #14b8a6;
    text-align: center;
    margin-top: 1rem;
    box-shadow: 0 4px 15px rgba(13, 148, 136, 0.15);
}

.summary-label {
    color: #0f766e;
    font-size: 1rem;
    font-weight: 600;
    margin: 0;
}

.summary-value {
    color: #0d9488;
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0.5rem 0;
}

.summary-subtitle {
    color: #14b8a6;
    font-size: 0.95rem;
    margin: 0;
}

/* Button Styling */
div.stButton > button {
    background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
    color: white;
    font-weight: 700;
    font-size: 1.2rem;
    border-radius: 12px;
    border: none;
    padding: 1rem 3rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(13, 148, 136, 0.3);
    text-transform: uppercase;
    letter-spacing: 1px;
    width: 100%;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(13, 148, 136, 0.4);
}

/* Result Card */
.result-card {
    background: white;
    padding: 2.5rem;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    margin-bottom: 2rem;
    border: 3px solid #14b8a6;
}

.result-header {
    background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    text-align: center;
}

.result-title {
    color: white;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0;
}

.result-cf {
    color: #ccfbf1;
    font-size: 1rem;
    margin-top: 0.5rem;
}

.result-cf strong {
    color: white;
    font-size: 1.3rem;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: #0d9488 !important;
    font-weight: 700 !important;
    font-size: 1.8rem !important;
}

[data-testid="stMetricLabel"] {
    color: #0f766e !important;
    font-weight: 600 !important;
}

[data-testid="stMetric"] {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
    border: 2px solid #e0f2f1;
}

/* Dataframe */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
}

/* Expander */
.streamlit-expanderHeader {
    background: #f0fdfa;
    border-radius: 10px;
    font-weight: 600;
    color: #0f766e !important;
    border: 2px solid #ccfbf1;
}

.streamlit-expanderHeader:hover {
    background: #ccfbf1;
    border-color: #14b8a6;
}

/* Info/Alert boxes */
.stAlert {
    border-radius: 12px;
    border-left: 4px solid #14b8a6;
}

/* Headings */
h1, h2, h3 {
    color: #0f766e !important;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background-color: #14b8a6;
}

/* Success message */
.stSuccess {
    background-color: #f0fdfa;
    border: 2px solid #14b8a6;
    border-radius: 12px;
    color: #0f766e;
}

/* Divider */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #14b8a6, transparent);
    margin: 2rem 0;
}

/* Responsive */
@media (max-width: 768px) {
    .header-title {
        font-size: 1.8rem;
    }
    .input-cards-container {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="header-section">
    <h1 class="header-title">💰 Sistem Pakar Investasi</h1>
    <p class="header-subtitle">Dapatkan rekomendasi alokasi aset investasi berdasarkan profil risiko dan tujuan finansial Anda</p>
</div>
""", unsafe_allow_html=True)

# Section Title untuk Input
st.markdown('<h2 class="section-title">Masukkan Profil Anda:</h2>', unsafe_allow_html=True)

# Row 1: Usia dan Profil Risiko
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="input-card">
        <div class="input-card-title">🎂 Usia Anda (Tahun)</div>
    </div>
    """, unsafe_allow_html=True)
    usia = st.slider("", 17, 70, 24, label_visibility="collapsed", help="Usia mempengaruhi toleransi risiko investasi")

with col2:
    st.markdown("""
    <div class="input-card">
        <div class="input-card-title">🎯 Profil Risiko</div>
    </div>
    """, unsafe_allow_html=True)
    profil_risiko = st.selectbox(
        "",
        ['Konservatif', 'Moderat', 'Aggresif'],
        index=None,
        placeholder="Pilih Profil Risiko",
        label_visibility="collapsed",
        help="Pilih tingkat toleransi risiko Anda"
    )

# Row 2: Tujuan Investasi dan Pengalaman
col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="input-card">
        <div class="input-card-title">⏰ Tujuan Investasi</div>
    </div>
    """, unsafe_allow_html=True)
    tujuan_finansial = st.selectbox(
        "",
        ['Jangka Pendek', 'Jangka Panjang'],
        index=None,
        placeholder="Pilih Tujuan Investasi",
        label_visibility="collapsed",
        help="Jangka Pendek: 1-3 tahun | Jangka Panjang: > 5 tahun"
    )

with col4:
    st.markdown("""
    <div class="input-card">
        <div class="input-card-title">📚 Pengalaman Investasi</div>
    </div>
    """, unsafe_allow_html=True)
    status_investor = st.selectbox(
        "",
        ['Pemula', 'Bukan Pemula'],
        index=None,
        placeholder="Pilih Pengalaman Investasi",
        label_visibility="collapsed",
        help="Pemula: < 1 tahun | Berpengalaman: > 1 tahun"
    )

# Row 3: Dana Investasi (Full width)
st.markdown("""
<div class="input-card">
    <div class="input-card-title">💵 Dana yang Siap Diinvestasikan</div>
</div>
""", unsafe_allow_html=True)

investable_income = st.number_input(
    "",
    min_value=0,
    value=5000000,
    step=500000,
    label_visibility="collapsed",
    help="Jumlah dana yang siap Anda investasikan"
)

# Summary Card
st.markdown(f"""
<div class="summary-card">
    <p class="summary-label">Total Dana Investasi</p>
    <p class="summary-value">Rp {investable_income:,.0f}</p>
    <p class="summary-subtitle">Siap untuk dialokasikan secara optimal</p>
</div>
""", unsafe_allow_html=True)

# Kumpulkan Data
user_data = {
    "usia": usia,
    "profil_risiko": profil_risiko,
    "tujuan_finansial": tujuan_finansial,
    "status_investor": status_investor,
    "investable_income": investable_income
}

st.markdown("<br>", unsafe_allow_html=True)

# Button Analisis
analyze_button = st.button("🔍 Analisis & Dapatkan Rekomendasi")

if analyze_button:
    # Progress bar
    with st.spinner('Menganalisis profil investasi Anda...'):
        import time
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
    
    # Panggil forward chaining
    hasil_inferensi = forward_chaining(user_data)
    results = hasil_inferensi["results"]

    if results:
        st.success("✅ Analisis selesai! Berikut rekomendasi investasi untuk Anda")
        
        # Pisahkan rekomendasi
        rekomendasi_utama = [r for r in results if r['rule'] in ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']]
        rekomendasi_tambahan = [r for r in results if r['rule'] not in ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']]
        
        # Section Title untuk Hasil
        st.markdown('<br><h2 class="section-title">Hasil Analisis Portofolio</h2>', unsafe_allow_html=True)
        
        if rekomendasi_utama:
            utama = rekomendasi_utama[0]
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            
            # Header hasil dengan CF
            st.markdown(f"""
            <div class="result-header">
                <h3 class="result-title">Hasil Rekomendasi Alokasi Aset 🎯</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Rekomendasi utama
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%); 
                        padding: 1.5rem; 
                        border-radius: 12px; 
                        margin-bottom: 2rem;">
                <h3 style="color: white; margin: 0; font-size: 1.5rem; font-weight: 700;">
                    ✅ {utama['rekomendasi']}
                </h3>
                <p style="color: #ccfbf1; margin: 0.5rem 0 0 0; font-size: 1rem;">
                    CF: <strong style="color: white; font-size: 1.2rem;">{utama['CF']}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if utama.get('alokasi'):
                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Dana Investasi", f"Rp {investable_income:,.0f}")
                with col2:
                    st.metric("Profil Risiko", user_data['profil_risiko'])
                with col3:
                    st.metric("Jangka Waktu", user_data['tujuan_finansial'])
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 📊 Distribusi Aset Investasi")
                
                # Tabel alokasi
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
                        "Nominal": f"Rp {nominal:,.0f}"
                    })
                
                st.dataframe(alokasi_data, hide_index=True, use_container_width=True)
                
                st.markdown("---")
                st.markdown(f"### 📖 Penjelasan Strategi (`{utama['rule']}`)")
                st.info(f"💡 {utama['penjelasan']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            darurat_atau_usia = [r for r in results if r['rule'] in ['R9', 'R10']]
            if darurat_atau_usia:
                darurat = darurat_atau_usia[0]
                st.error(f"⚠️ {darurat['rekomendasi']}")
                st.info(f"💬 {darurat['penjelasan']}")
        
        # Tips tambahan
        if rekomendasi_tambahan:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<h2 class="section-title">💡 Tips & Pertimbangan Tambahan</h2>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            tips_icons = ['💰', '📚', '🎓', '⚡', '🔔', '🌟']
            
            for i, r_t in enumerate(rekomendasi_tambahan):
                target_col = col1 if i % 2 == 0 else col2
                icon = tips_icons[i % len(tips_icons)]
                
                with target_col:
                    with st.expander(f"{icon} [{r_t['rule']}] {r_t['rekomendasi']}"):
                        st.write(r_t['penjelasan'])
        
        # Debug section
        with st.expander("🔬 Detail Teknis (Developer Mode)"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Aturan Terpenuhi:**")
                st.code(", ".join(hasil_inferensi['reasoning_path']))
            with col2:
                st.markdown("**Working Memory:**")
                st.json(hasil_inferensi['working_memory'])
    
    else:
        st.warning("⚠️ Tidak ada rekomendasi. Periksa input Anda.")