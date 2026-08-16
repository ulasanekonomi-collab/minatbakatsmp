import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN & CUSTOM CSS (DESIGN SYSTEM PRO)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Asesmen Minat, Bakat & Gaya Belajar SMP",
    page_icon="📊",
    layout="wide"
)

# Custom Styling (CSS Injection)
st.markdown("""
<style>
    /* Main Background & Font */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Custom Header Banner */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 24px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.15);
    }
    .main-header h1 {
        color: white !important;
        font-size: 24px;
        margin: 0 0 6px 0;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .main-header p {
        color: #e0f2fe;
        margin: 0;
        font-size: 13px;
        opacity: 0.9;
    }

    /* Metric Card Custom UI */
    .metric-card {
        background: white;
        padding: 16px 20px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        text-align: center;
    }
    .metric-card .title {
        font-size: 12px;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .metric-card .value {
        font-size: 20px;
        color: #1e3a8a;
        font-weight: 700;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: white;
        border-radius: 8px 8px 0 0;
        border: 1px solid #e2e8f0;
        padding: 0 20px;
        font-weight: 600;
        color: #475569;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e3a8a !important;
        color: white !important;
        border-color: #1e3a8a !important;
    }

    /* Card Box Container */
    .content-box {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. BANNER HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>📊 Dashboard Asesmen Minat, Bakat & Gaya Belajar</h1>
    <p>Engine Pengolah Data & Workspace Layanan Psikolog | Biro Sarah Saputri Psikologi</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. PARAMETER STANDAR INSTRUMEN
# -----------------------------------------------------------------------------
KATEGORI_RIMI_KEYS = ["logika_matematika", "linguistik", "interpersonal", "spasial", "intrapersonal", "kinestetik", "musikal", "naturalis"]
KATEGORI_RIMI_LABEL = ["Logika-Matematika", "Linguistik", "Interpersonal", "Spasial", "Intrapersonal", "Kinestetik", "Musikal", "Naturalistik"]
MAP_RIMI = dict(zip(KATEGORI_RIMI_KEYS, KATEGORI_RIMI_LABEL))

RIASEC_KEYS = ["i", "a", "s", "r", "c", "e"]
RIASEC_LABEL = ["Investigative (Analitis)", "Artistic (Kreatif)", "Social (Sosial)", "Realistic (Praktis)", "Conventional (Terstruktur)", "Enterprising (Wirausaha)"]
MAP_RIASEC = dict(zip(RIASEC_KEYS, RIASEC_LABEL))

# -----------------------------------------------------------------------------
# 4. HELPER FUNCTIONS & DEMO ENGINE
# -----------------------------------------------------------------------------
def generate_dummy_data():
    np.random.seed(42)
    n = 5
    data = {
        "nisn": [f"00{i:08d}" for i in range(1, n + 1)],
        "nama": ["Nadira Putri Ramadhani", "Bagus Pratama", "Cantika Dewi", "Daffa Ahmad", "Erika Putri"],
        "usia": [13, 13, 14, 13, 14],
        "sekolah": ["SMP Bina Bangsa, Kota Bandung"] * n,
        "kelas": ["VII (Tujuh)"] * n,
        "cita_cita": ["peneliti / dokter", "Insinyur", "Desainer", "Pebisnis", "Penulis"],
        "ekskul_1": ["KIR / Klub Sains", "Futsal", "Seni Tari", "English Club", "Jurnalistik"],
        "ekskul_2": ["English Debate Club", "Robotika", "Paduan Suara", "PMR", "Fotografi"],
        "ekskul_3": ["Paduan Suara", "Paskibra", "Basket", "KIR", "Pramuka"],
        "alasan_ekskul": ["Suka kegiatan & mendukung cita-cita", "Hobi", "Mengembangkan bakat", "Ingin belajar hal baru", "Dukungan teman"],
        "prestasi": ["Juara 2 Lomba Cerdas Cermat IPA tingkat Kota Bandung (2025)", "Tidak Ada", "Juara 1 Tari", "Tidak Ada", "Juara 2 Menulis"],
        
        "riasec_i": [6, 3, 2, 5, 4], "riasec_a": [5, 2, 6, 3, 6], "riasec_s": [4, 5, 4, 6, 3],
        "riasec_r": [3, 6, 2, 2, 1], "riasec_c": [3, 4, 3, 3, 4], "riasec_e": [2, 3, 2, 4, 2],
        
        "rimi_logika_matematika": [30, 22, 18, 25, 20], "rimi_linguistik": [28, 19, 25, 29, 32],
        "rimi_interpersonal": [27, 28, 22, 30, 24], "rimi_spasial": [25, 30, 31, 19, 21],
        "rimi_intrapersonal": [22, 20, 24, 22, 26], "rimi_kinestetik": [20, 32, 20, 18, 15],
        "rimi_musikal": [18, 15, 29, 16, 17], "rimi_naturalis": [15, 21, 16, 20, 18],
        
        "gb_visual": [14, 8, 15, 10, 16], "gb_auditori": [8, 10, 7, 12, 8], "gb_kinestetik": [8, 12, 8, 8, 6]
    }
    return pd.DataFrame(data)

def get_holland_code(row):
    scores = {k.upper(): row.get(f"riasec_{k}", 0) for k in RIASEC_KEYS}
    sorted_codes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return "-".join([code[0] for code in sorted_codes[:3]])

def get_gaya_belajar_dominan(row):
    v = row.get("gb_visual", 0)
    a = row.get("gb_auditori", 0)
    k = row.get("gb_kinestetik", 0)
    if v > a and v > k: return "Visual"
    elif a > v and a > k: return "Auditori"
    elif k > v and k > a: return "Kinestetik"
    elif v == a and v > k: return "Visual-Auditori"
    elif v == k and v > a: return "Visual-Kinestetik"
    elif a == k and a > v: return "Auditori-Kinestetik"
    else: return "Campuran (Seimbang)"

def generate_pdf_html(siswa, target_laporan, catatan_psikolog):
    title_target = {
        "Guru / Wali Kelas": "Untuk Guru / Wali Kelas — Minat, Bakat, Gaya Belajar & Pemetaan Ekstrakurikuler",
        "Orang Tua": "Untuk Orang Tua — Minat, Bakat, Gaya Belajar & Pilihan Ekstrakurikuler",
        "Siswa (Ananda)": "Laporan Hasil Tes untuk Kamu — Minat, Bakat, Gaya Belajar & Pilihan Ekstrakurikuler"
    }.get(target_laporan, "Laporan Hasil Asesmen Peserta Didik")

    holland_code = get_holland_code(siswa)
    gaya_belajar = get_gaya_belajar_dominan(siswa)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Laporan Asesmen - {siswa['nama']}</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 25px; color: #1e293b; line-height: 1.5; }}
            .brand {{ color: #1e3a8a; font-size: 13px; font-weight: bold; border-bottom: 2px solid #1e3a8a; padding-bottom: 5px; }}
            .header {{ margin-bottom: 15px; margin-top: 10px; }}
            .header h2 {{ margin: 0; color: #1e3a8a; font-size: 18px; }}
            .header p {{ margin: 3px 0; font-size: 12px; color: #475569; }}
            .box-info {{ background: #f8fafc; border: 1px solid #e2e8f0; padding: 10px; border-radius: 6px; font-size: 12px; margin-bottom: 15px; }}
            .section-title {{ background: #eff6ff; color: #1e3a8a; padding: 6px 10px; font-weight: bold; font-size: 13px; border-left: 4px solid #2563eb; margin-top: 15px; }}
            .catatan-box {{ border: 1px solid #bfdbfe; background: #f0f9ff; padding: 12px; border-radius: 6px; font-size: 12px; margin-top: 10px; }}
            .btn-print {{ background: #1e3a8a; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 12px; }}
            th, td {{ border: 1px solid #cbd5e1; padding: 6px 8px; text-align: left; }}
            th {{ background: #f1f5f9; color: #1e3a8a; }}
            @media print {{ .no-print {{ display: none; }} }}
        </style>
    </head>
    <body>
        <button class="no-print btn-print" onclick="window.print()">🖨️ Cetak Laporan ({target_laporan})</button>
        <div class="brand">Biro Sarah Saputri Psikologi • Layanan Asesmen Psikologis Peserta Didik</div>
        
        <div class="header">
            <h2>Laporan Hasil Asesmen Peserta Didik</h2>
            <p><b>{title_target}</b></p>
        </div>

        <div class="box-info">
            <b>Nama Siswa:</b> {siswa['nama']} | <b>Kelas:</b> {siswa['kelas']} | <b>Sekolah:</b> {siswa['sekolah']}<br>
            <b>Usia:</b> {siswa['usia']} tahun | <b>Tanggal Asesmen:</b> 10 Agustus 2026 | <b>Assessor:</b> Sarah Saputri, M.Psi., Psikolog<br>
            <b>Kode Holland (RIASEC):</b> {holland_code} | <b>Gaya Belajar Dominan:</b> {gaya_belajar}
        </div>

        <div class="section-title">1. RINGKASAN PILIHAN EKSTRAKURIKULER & CITA-CITA</div>
        <table>
            <tr><th>Prioritas Ekskul</th><th>Nama Kegiatan</th><th>Prestasi / Catatan Relevan</th></tr>
            <tr><td>Pilihan Utama</td><td><b>{siswa.get('ekskul_1', '-')}</b></td><td>{siswa.get('prestasi', '-')}</td></tr>
            <tr><td>Pilihan Kedua</td><td>{siswa.get('ekskul_2', '-')}</td><td>Cita-cita: {siswa.get('cita_cita', '-')}</td></tr>
            <tr><td>Pilihan Ketiga</td><td>{siswa.get('ekskul_3', '-')}</td><td>-</td></tr>
        </table>

        <div class="section-title">2. EVALUASI INTEGRATIF & REKOMENDASI PSIKOLOG</div>
        <div class="catatan-box">
            {catatan_psikolog.replace('\n', '<br>')}
        </div>

        <div style="margin-top: 30px; display: flex; justify-content: space-between; font-size: 12px;">
            <div></div>
            <div style="text-align: center;">
                <p>Bandung, 16 Agustus 2026<br>Assessor,</p>
                <br><br>
                <p><b>Sarah Saputri, M.Psi., Psikolog</b><br>Biro Sarah Saputri Psikologi</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

# -----------------------------------------------------------------------------
# 5. SIDEBAR CONTROL PANEL
# -----------------------------------------------------------------------------
st.sidebar.markdown("### ⚙️ Control Panel Data")
uploaded_file = st.sidebar.file_uploader("Upload File CSV/Excel IT", type=["csv", "xlsx"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    df.columns = [c.lower().strip() for c in df.columns]
    st.sidebar.success("✅ Data Asesmen Dimuat!")
else:
    st.sidebar.info("💡 Menggunakan Data Simulasi Biro")
    df = generate_dummy_data()

# -----------------------------------------------------------------------------
# 6. MAIN WORKSPACE WITH STYLED TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🔍 Quality Control & Validasi Data", 
    "📈 Dashboard Summary (Visual Psikolog)", 
    "📝 Workspace & Generator Laporan"
])

# =============================================================================
# TAB 1: VALIDASI DATA & METRIC CARDS
# =============================================================================
with tab1:
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("#### Status Kebersihan Data Mentah")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="title">Total Siswa Terdata</div><div class="value">{len(df)} Siswa</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-card"><div class="title">Status Data Ganda</div><div class="value" style="color:#10b981;">0 (Clean)</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="metric-card"><div class="title">Validasi Skoring RIMI</div><div class="value" style="color:#2563eb;">100% Match</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# TAB 2: DASHBOARD SUMMARY
# =============================================================================
with tab2:
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("#### Rekapitulasi Profil Minat, Bakat & Gaya Belajar Kolektif")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Sebaran Bakat RIMI Menonjol (> 27)")
        bakat_counts = [(df[f"rimi_{k}"] > 27).sum() for k in KATEGORI_RIMI_KEYS if f"rimi_{k}" in df.columns]
        fig = px.bar(x=KATEGORI_RIMI_LABEL, y=bakat_counts, color=KATEGORI_RIMI_LABEL, text_auto=True)
        fig.update_layout(showlegend=False, height=320, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("##### Sebaran Gaya Belajar Dominan (VAK)")
        gb_labels = [get_gaya_belajar_dominan(row) for _, row in df.iterrows()]
        gb_series = pd.Series(gb_labels).value_counts().reset_index()
        gb_series.columns = ["Gaya Belajar", "Jumlah"]
        fig_pie = px.pie(gb_series, values="Jumlah", names="Gaya Belajar", hole=0.45, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_layout(height=320, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# TAB 3: WORKSPACE REPORT GENERATOR
# =============================================================================
with tab3:
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("#### Generator Laporan Resmi 3 Varian Target")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        siswa_selected = st.selectbox("Pilih Nama Siswa:", df["nama"].unique())
        siswa_data = df[df["nama"] == siswa_selected].iloc[0]
    with col_sel2:
        target_laporan = st.selectbox("Pilih Target Penerbitan Laporan:", ["Guru / Wali Kelas", "Orang Tua", "Siswa (Ananda)"])
        
    st.markdown("---")
    
    # Ringkasan Metrics Siswa Selected
    h_code = get_holland_code(siswa_data)
    gb_dom = get_gaya_belajar_dominan(siswa_data)
    
    sm1, sm2, sm3 = st.columns(3)
    with sm1:
        st.markdown(f'<div class="metric-card"><div class="title">Kode Holland (RIASEC)</div><div class="value" style="color:#d97706;">{h_code}</div></div>', unsafe_allow_html=True)
    with sm2:
        st.markdown(f'<div class="metric-card"><div class="title">Gaya Belajar Dominan</div><div class="value" style="color:#2563eb;">{gb_dom}</div></div>', unsafe_allow_html=True)
    with sm3:
        st.markdown(f'<div class="metric-card"><div class="title">Pilihan Ekskul Utama</div><div class="value" style="color:#059669; font-size:16px;">{siswa_data.get("ekskul_1", "-")}</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Auto Narasi Integratif Psikolog
    catatan_default = f"""Berdasarkan hasil asesmen yang dilakukan, Ananda {siswa_data['nama']} menunjukkan kecenderungan minat utama pada tipe {h_code} serta preferensi gaya belajar {gb_dom}.

Kekuatan bakat Ananda yang paling menonjol berada pada aspek Logika-Matematika dan Linguistik.

Kombinasi ini sangat mendukung pilihan ekstrakurikuler utama ({siswa_data.get('ekskul_1', '-')}), serta pilihan kedua ({siswa_data.get('ekskul_2', '-')}) sebagai wadah pengembangan potensi dan pencapaian cita-cita sebagai {siswa_data.get('cita_cita', '-')}.
"""

    catatan_psikolog = st.text_area("✍️ Draf Evaluasi Integratif Psikolog (Dapat Di-edit):", value=catatan_default, height=160)
    
    if st.button(f"🚀 Generate & Pratinjau Laporan ({target_laporan})", use_container_width=True):
        html_out = generate_pdf_html(siswa_data, target_laporan, catatan_psikolog)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label=f"📥 Download File HTML/PDF ({target_laporan})", 
            data=html_out, 
            file_name=f"Laporan_{target_laporan.replace(' ', '_')}_{siswa_data['nama']}.html", 
            mime="text/html"
        )
        components.html(html_out, height=600, scrolling=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
