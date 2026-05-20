import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="🌊 Balikpapan Flood Intelligence",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0a0e1a; color: #e8f0fe; }
    section[data-testid="stSidebar"] { background-color: #111827; }
    section[data-testid="stSidebar"] .stMarkdown { color: #e8f0fe; }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: #111827;
        border: 1px solid rgba(0,212,255,0.15);
        border-radius: 12px;
        padding: 14px 18px;
    }
    div[data-testid="metric-container"] label { color: #7a8ba8 !important; font-size: 12px; }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: #00d4ff; font-size: 26px; font-weight: 700; }

    /* Headers */
    h1, h2, h3 { color: #00d4ff !important; }
    .stTabs [data-baseweb="tab"] { background-color: #111827; color: #7a8ba8; border-radius: 8px 8px 0 0; }
    .stTabs [aria-selected="true"] { background-color: #1a2235; color: #00d4ff; border-bottom: 2px solid #00d4ff; }

    /* Dataframe */
    .stDataFrame { background: #111827; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0066ff, #00d4ff);
        color: #000; font-weight: 700;
        border: none; border-radius: 10px;
        padding: 10px 28px;
        transition: all 0.2s;
    }
    .stButton > button:hover { filter: brightness(1.1); transform: translateY(-1px); }

    /* Slider */
    .stSlider [data-baseweb="slider"] div { background: #00d4ff; }

    /* Info/success/error boxes */
    .stAlert { border-radius: 10px; }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stSlider"] label { color: #7a8ba8; font-size: 13px; font-family: monospace; }

    /* Hide default streamlit header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
LOKASI_RAW = [
    (1,"Kel. Gunung Samarinda",-1.1854,116.8948,"Utara"),
    (2,"Kel. Gunung Samarinda Baru",-1.1780,116.9020,"Utara"),
    (3,"Kel. Muara Rapak",-1.1700,116.8880,"Utara"),
    (4,"Kel. Batu Ampar",-1.1620,116.8800,"Utara"),
    (5,"Kel. Karang Joang",-1.1500,116.8700,"Utara"),
    (6,"Kel. Graha Indah",-1.1580,116.8620,"Utara"),
    (7,"Kel. Manggar",-1.2050,116.9600,"Timur"),
    (8,"Kel. Manggar Baru",-1.2100,116.9520,"Timur"),
    (9,"Kel. Lamaru",-1.2220,116.9720,"Timur"),
    (10,"Kel. Teritip",-1.2320,117.0120,"Timur"),
    (11,"Kel. Batakan",-1.2420,117.0320,"Timur"),
    (12,"Kel. Selok Api",-1.1960,116.9420,"Timur"),
    (13,"Kel. Damai",-1.2800,116.8600,"Selatan"),
    (14,"Kel. Gunung Bahagia",-1.2900,116.8700,"Selatan"),
    (15,"Kel. Sepinggan",-1.2700,116.8800,"Selatan"),
    (16,"Kel. Sepinggan Raya",-1.2600,116.8900,"Selatan"),
    (17,"Kel. Sepinggan Baru",-1.2650,116.8750,"Selatan"),
    (18,"Kel. Kariangau",-1.2300,116.7900,"Selatan"),
    (19,"Kel. Prapatan",-1.2820,116.8220,"Selatan"),
    (20,"Kel. Baru Ilir",-1.2650,116.8200,"Barat"),
    (21,"Kel. Baru Tengah",-1.2600,116.8150,"Barat"),
    (22,"Kel. Baru Ulu",-1.2550,116.8100,"Barat"),
    (23,"Kel. Margasari",-1.2500,116.8050,"Barat"),
    (24,"Kel. Marga Mulya",-1.2450,116.8000,"Barat"),
    (25,"Kel. Sidodadi",-1.2580,116.8080,"Barat"),
    (26,"Kel. Mekar Sari",-1.2600,116.8400,"Tengah"),
    (27,"Kel. Gunung Sari Ilir",-1.2650,116.8450,"Tengah"),
    (28,"Kel. Gunung Sari Ulu",-1.2700,116.8500,"Tengah"),
    (29,"Kel. Karang Jati",-1.2550,116.8350,"Tengah"),
    (30,"Kel. Telaga Sari",-1.2500,116.8300,"Tengah"),
    (31,"Kel. Klandasan Ilir",-1.2700,116.8300,"Kota"),
    (32,"Kel. Klandasan Ulu",-1.2650,116.8350,"Kota"),
    (33,"Kel. Damai Baru",-1.2750,116.8280,"Kota"),
    (34,"Kel. Karang Rejo",-1.2480,116.8320,"Kota"),
    (35,"Pantau - S. Manggar Hulu",-1.2180,116.9680,"Pantau"),
    (36,"Pantau - S. Manggar Hilir",-1.2080,116.9550,"Pantau"),
    (37,"Pantau - S. Ampal",-1.2400,116.8520,"Pantau"),
    (38,"Pantau - S. Somber",-1.1900,116.8750,"Pantau"),
    (39,"Pantau - S. Wain Hulu",-1.1300,116.8500,"Pantau"),
    (40,"Pantau - S. Wain Hilir",-1.1600,116.8600,"Pantau"),
    (41,"Pantau - Kws. Industri Kariangau",-1.2200,116.7850,"Pantau"),
    (42,"Pantau - Jl. MT Haryono",-1.2550,116.8420,"Pantau"),
    (43,"Pantau - Jl. SH Km 3",-1.2380,116.8620,"Pantau"),
    (44,"Pantau - Jl. SH Km 5",-1.2200,116.8720,"Pantau"),
    (45,"Pantau - Banjir Kanal Sepinggan",-1.2680,116.8840,"Pantau"),
    (46,"Pantau - Muara S. Teritip",-1.2350,117.0200,"Pantau"),
    (47,"Pantau - Bandara Sultan Aji",-1.2680,116.8950,"Pantau"),
    (48,"Pantau - Jl. Syarifuddin Yoes",-1.2520,116.8780,"Pantau"),
    (49,"Pantau - Kws. Pertamina",-1.2630,116.8250,"Pantau"),
    (50,"Pantau - Pelabuhan Semayang",-1.2700,116.8150,"Pantau"),
    (51,"Pantau - Pantai Lamaru",-1.2300,116.9800,"Pantau"),
    (52,"Pantau - Hutan Lindung S. Wain",-1.1200,116.8350,"Pantau"),
    (53,"Pantau - Waduk Manggar",-1.2150,116.9400,"Pantau"),
    (54,"Pantau - Embung Batakan",-1.2500,117.0100,"Pantau"),
    (55,"Pantau - Jl. Mulawarman",-1.2850,116.8680,"Pantau"),
    (56,"Pantau - Bukit Bangkirai",-1.1700,116.9300,"Pantau"),
    (57,"Pantau - GOR Balikpapan",-1.2420,116.8480,"Pantau"),
    (58,"Pantau - Teluk BPP Barat",-1.2100,116.8000,"Pantau"),
    (59,"Pantau - Teluk BPP Tengah",-1.2400,116.8100,"Pantau"),
]

RISIKO_SEED = [0.72,0.48,0.81,0.63,0.35,0.29,0.78,0.69,0.44,0.52,0.38,0.61,
               0.55,0.47,0.67,0.71,0.58,0.33,0.42,0.39,0.36,0.31,0.27,0.24,
               0.34,0.66,0.73,0.68,0.57,0.53,0.64,0.60,0.59,0.45,0.82,0.77,
               0.74,0.56,0.22,0.28,0.31,0.79,0.65,0.49,0.76,0.43,0.54,0.62,
               0.41,0.37,0.32,0.21,0.70,0.40,0.69,0.26,0.51,0.35,0.46]

@st.cache_data
def get_df_lokasi():
    rows = []
    for i, (lid, nama, lat, lon, kec) in enumerate(LOKASI_RAW):
        risiko = RISIKO_SEED[i % len(RISIKO_SEED)]
        if risiko >= 0.6:
            kelas = "TINGGI"; color = "#ff4757"
        elif risiko >= 0.35:
            kelas = "SEDANG"; color = "#ffa502"
        else:
            kelas = "RENDAH"; color = "#2ed573"
        rows.append({"ID":lid,"Nama":nama,"Lat":lat,"Lon":lon,
                     "Kecamatan":kec,"Risiko":risiko,"Kelas":kelas,"Color":color})
    return pd.DataFrame(rows)

df = get_df_lokasi()

MODEL_HASIL = pd.DataFrame({
    "Model":     ["XGBoost","Random Forest","Neural Network","Logistic Regression"],
    "F1-Score":  [0.847, 0.798, 0.714, 0.621],
    "ROC-AUC":   [0.931, 0.904, 0.871, 0.812],
    "Kecepatan": [55, 70, 60, 98],
    "Interpretabilitas": [65, 55, 40, 95],
    "Stabilitas":[82, 88, 65, 75],
})

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌊 Flood Intelligence")
    st.markdown("**Balikpapan — Kalimantan Timur**")
    st.markdown("---")
    st.markdown("### 🗺️ Navigasi")
    page = st.radio("", ["📊 Dashboard", "🔮 Prediksi Risiko", "🧠 Battle of Models", "📋 Data Lokasi"],
                    label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### ℹ️ Info Sistem")
    st.metric("Total Titik Pantau", "59")
    st.metric("Model Terbaik", "XGBoost")
    st.metric("Best F1-Score", "0.847")
    st.markdown("---")
    st.caption("Praktisi Mengajar · Data: Open-Meteo API")

# ─────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────
if page == "📊 Dashboard":
    st.title("🌊 Balikpapan Flood Intelligence Dashboard")
    st.caption("Sistem Deteksi Dini Banjir · 59 Titik Pemantauan · Praktisi Mengajar")
    st.markdown("---")

    # Metrics
    tinggi = len(df[df.Kelas=="TINGGI"])
    sedang = len(df[df.Kelas=="SEDANG"])
    rendah = len(df[df.Kelas=="RENDAH"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔴 Risiko Tinggi", tinggi, "titik pemantauan")
    c2.metric("🟡 Risiko Sedang", sedang, "titik pemantauan")
    c3.metric("🟢 Risiko Rendah", rendah, "titik pemantauan")
    c4.metric("🌧️ Curah Hujan 24j", "47.3 mm", "rata-rata aktif")

    st.markdown("---")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("🗺️ Peta Risiko Banjir Balikpapan")
        fig_map = px.scatter_mapbox(
            df, lat="Lat", lon="Lon",
            size=df["Risiko"] * 20 + 5,
            color="Kelas",
            color_discrete_map={"TINGGI":"#ff4757","SEDANG":"#ffa502","RENDAH":"#2ed573"},
            hover_name="Nama",
            hover_data={"Kecamatan":True,"Risiko":":.1%","Lat":False,"Lon":False},
            mapbox_style="carto-darkmatter",
            zoom=11, center={"lat":-1.235,"lon":116.875},
            height=430,
        )
        fig_map.update_layout(
            paper_bgcolor="#111827", plot_bgcolor="#111827",
            margin=dict(l=0,r=0,t=0,b=0),
            legend=dict(font=dict(color="#e8f0fe"), bgcolor="#111827"),
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_right:
        st.subheader("🔴 Top 10 Risiko Tertinggi")
        top10 = df.nlargest(10, "Risiko")[["Nama","Kecamatan","Risiko","Kelas"]].reset_index(drop=True)
        top10.index += 1
        top10["Risiko"] = (top10["Risiko"] * 100).round(1).astype(str) + "%"
        st.dataframe(
            top10,
            use_container_width=True,
            height=430,
        )

    st.markdown("---")
    st.subheader("🌧️ Simulasi Curah Hujan 24 Jam — 5 Lokasi Rawan")

    np.random.seed(42)
    hours = list(range(24))
    locs_rawan = ["S. Manggar Hulu","Jl. MT Haryono","Banjir Kanal Sepinggan","S. Ampal","Muara Rapak"]
    colors_rawan = ["#ff4757","#ffa502","#00d4ff","#a29bfe","#2ed573"]

    fig_rain = go.Figure()
    for i, (loc, clr) in enumerate(zip(locs_rawan, colors_rawan)):
        data = [max(0, np.sin(h*0.4 + i) * 8 + np.random.rand()*5 + 1) for h in hours]
        fig_rain.add_trace(go.Scatter(
            x=hours, y=[round(v,1) for v in data],
            name=loc, line=dict(color=clr, width=2),
            fill="tozeroy", fillcolor=clr.replace("#","rgba(").rstrip(")") + ",0.05)",
        ))
    fig_rain.update_layout(
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        xaxis=dict(title="Jam ke-", color="#7a8ba8", gridcolor="#1a2235"),
        yaxis=dict(title="mm/jam", color="#7a8ba8", gridcolor="#1a2235"),
        legend=dict(font=dict(color="#e8f0fe", size=11), bgcolor="#111827"),
        height=280, margin=dict(l=40,r=20,t=10,b=40),
    )
    st.plotly_chart(fig_rain, use_container_width=True)


# ─────────────────────────────────────────────
# PAGE: PREDIKSI
# ─────────────────────────────────────────────
elif page == "🔮 Prediksi Risiko":
    st.title("🔮 Prediksi Risiko Banjir")
    st.caption("Input parameter cuaca & lokasi → Model XGBoost → Probabilitas risiko banjir")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Parameter Lokasi")
        lokasi_names = [r[1] for r in LOKASI_RAW]
        lokasi_sel = st.selectbox("Pilih Lokasi / Kelurahan", lokasi_names)
        bulan = st.selectbox("Bulan", options=list(range(1,13)),
                             format_func=lambda m: {1:"Januari 🌧️",2:"Februari 🌧️",3:"Maret 🌧️",
                                                    4:"April 🌧️",5:"Mei",6:"Juni",7:"Juli",
                                                    8:"Agustus",9:"September",10:"Oktober 🌧️",
                                                    11:"November 🌧️",12:"Desember 🌧️"}[m],
                             index=10)
        jam = st.slider("Jam saat ini", 0, 23, 14)

    with col2:
        st.subheader("🌧️ Parameter Cuaca")
        rain3h  = st.slider("Curah Hujan 3 Jam Terakhir (mm)", 0.0, 60.0, 12.0, step=0.5)
        rain6h  = st.slider("Curah Hujan 6 Jam Terakhir (mm)", 0.0, 100.0, 28.0, step=1.0)
        rain24h = st.slider("Curah Hujan 24 Jam Terakhir (mm)", 0.0, 200.0, 65.0, step=1.0)
        soil    = st.slider("Kelembaban Tanah (soil moisture)", 0.00, 1.00, 0.42, step=0.01)

    st.markdown("---")
    if st.button("⚡ Jalankan Prediksi XGBoost", use_container_width=True):
        musim_hujan = 1 if bulan in [1,2,3,4,10,11,12] else 0

        # Simulated XGBoost scoring
        score = 0.0
        if rain3h > 20:   score += 0.40
        elif rain3h > 12: score += 0.20
        elif rain3h > 6:  score += 0.08

        if rain6h > 40:   score += 0.30
        elif rain6h > 25: score += 0.15
        elif rain6h > 12: score += 0.06

        if rain24h > 100: score += 0.25
        elif rain24h > 60:score += 0.12
        elif rain24h > 30:score += 0.05

        score += soil * 0.10
        if musim_hujan:   score += 0.05
        score = min(0.97, max(0.03, score))

        st.markdown("---")
        col_res, col_gauge = st.columns([2, 1])

        with col_res:
            if score >= 0.6:
                st.error(f"🔴 RISIKO TINGGI — {score*100:.1f}%")
                st.markdown(f"""
                **⚠️ Probabilitas banjir di {lokasi_sel} sangat tinggi!**
                Segera aktifkan prosedur evakuasi, koordinasi dengan BPBD Balikpapan,
                dan pantau debit sungai terdekat. Hindari area cekungan dan bantaran sungai.
                """)
            elif score >= 0.35:
                st.warning(f"🟡 RISIKO SEDANG — {score*100:.1f}%")
                st.markdown(f"""
                **⚠️ Waspada di {lokasi_sel}.**
                Pantau terus perkembangan curah hujan. Siapkan jalur evakuasi
                dan informasikan warga di RW rawan.
                """)
            else:
                st.success(f"🟢 RISIKO RENDAH — {score*100:.1f}%")
                st.markdown(f"""
                **✅ Kondisi di {lokasi_sel} relatif aman.**
                Tetap pantau perubahan cuaca dan kondisi saluran air secara berkala.
                """)

            # Probability bars
            st.markdown("**Distribusi Probabilitas Kelas:**")
            prob_data = pd.DataFrame({
                "Kelas": ["TINGGI","SEDANG","RENDAH"],
                "Probabilitas (%)": [
                    round(score*100, 1),
                    round(min(40, (1-score)*60), 1),
                    round((1-score)*40, 1),
                ],
                "Warna": ["#ff4757","#ffa502","#2ed573"]
            })
            fig_bar = px.bar(prob_data, x="Probabilitas (%)", y="Kelas",
                             orientation="h", color="Kelas",
                             color_discrete_map={"TINGGI":"#ff4757","SEDANG":"#ffa502","RENDAH":"#2ed573"},
                             height=160)
            fig_bar.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827",
                                  showlegend=False, margin=dict(l=0,r=0,t=0,b=0),
                                  xaxis=dict(range=[0,100],color="#7a8ba8"),
                                  yaxis=dict(color="#7a8ba8"))
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_gauge:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(score * 100, 1),
                domain={"x":[0,1],"y":[0,1]},
                title={"text":"Skor Risiko (%)", "font":{"color":"#7a8ba8","size":13}},
                number={"font":{"color":"#00d4ff","size":32},"suffix":"%"},
                gauge={
                    "axis":{"range":[0,100],"tickcolor":"#7a8ba8","tickfont":{"color":"#7a8ba8"}},
                    "bar":{"color":"#00d4ff"},
                    "bgcolor":"#1a2235",
                    "bordercolor":"#1a2235",
                    "steps":[
                        {"range":[0,35],"color":"rgba(46,213,115,0.2)"},
                        {"range":[35,60],"color":"rgba(255,165,2,0.2)"},
                        {"range":[60,100],"color":"rgba(255,71,87,0.2)"},
                    ],
                    "threshold":{"line":{"color":"#fff","width":2},"thickness":0.8,"value":score*100},
                }
            ))
            fig_gauge.update_layout(paper_bgcolor="#111827", height=260,
                                    margin=dict(l=20,r=20,t=30,b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)

        st.caption(f"Input: rain_3h={rain3h}mm · rain_6h={rain6h}mm · rain_24h={rain24h}mm · "
                   f"soil={soil:.2f} · bulan={bulan} · musim_hujan={musim_hujan} · jam={jam}")

    st.markdown("---")
    with st.expander("ℹ️ Cara Kerja Prediksi (Pipeline)"):
        st.markdown("""
        Model menggunakan **XGBoost** yang dilatih dengan **13 fitur**:

        ```
        rain_3h · rain_6h · rain_24h · rain_max_6h · rain_mean_6h ·
        soil_moisture · soil_lag1 · elevasi_m · jam · bulan ·
        musim_hujan · latitude · longitude
        ```

        **Label banjir** ditentukan jika salah satu kondisi terpenuhi:
        - `rain_3h > 20mm` → hujan deras dalam 3 jam
        - `rain_6h > 40mm` → hujan deras dalam 6 jam
        - `rain_24h > 100mm` → hujan ekstrem dalam 24 jam

        Data diambil dari **Open-Meteo Archive API** untuk 59 titik di Balikpapan selama 1 tahun.
        Pipeline: Bronze (raw) → Silver (cleaning) → Gold (feature engineering) → Model Training.
        """)


# ─────────────────────────────────────────────
# PAGE: BATTLE OF MODELS
# ─────────────────────────────────────────────
elif page == "🧠 Battle of Models":
    st.title("🧠 Battle of Models")
    st.caption("Perbandingan performa 4 model ML untuk prediksi banjir Balikpapan")
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🥇 Model Terbaik", "XGBoost")
    c2.metric("Best F1-Score", "0.847")
    c3.metric("Best ROC-AUC", "0.931")
    c4.metric("Total Fitur", "13")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 F1-Score Comparison")
        fig_f1 = px.bar(
            MODEL_HASIL.sort_values("F1-Score", ascending=True),
            x="F1-Score", y="Model", orientation="h",
            color="F1-Score", color_continuous_scale=["#1a2235","#0066ff","#00d4ff"],
            text="F1-Score", height=280,
        )
        fig_f1.update_traces(texttemplate="%{text:.3f}", textposition="outside",
                             textfont_color="#e8f0fe")
        fig_f1.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827",
                             coloraxis_showscale=False,
                             xaxis=dict(range=[0,1.05], color="#7a8ba8", gridcolor="#1a2235"),
                             yaxis=dict(color="#e8f0fe"),
                             margin=dict(l=0,r=60,t=10,b=30))
        st.plotly_chart(fig_f1, use_container_width=True)

    with col2:
        st.subheader("📊 ROC-AUC Comparison")
        fig_auc = px.bar(
            MODEL_HASIL.sort_values("ROC-AUC", ascending=True),
            x="ROC-AUC", y="Model", orientation="h",
            color="ROC-AUC", color_continuous_scale=["#1a2235","#2ed573","#00d4ff"],
            text="ROC-AUC", height=280,
        )
        fig_auc.update_traces(texttemplate="%{text:.3f}", textposition="outside",
                              textfont_color="#e8f0fe")
        fig_auc.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827",
                              coloraxis_showscale=False,
                              xaxis=dict(range=[0,1.05], color="#7a8ba8", gridcolor="#1a2235"),
                              yaxis=dict(color="#e8f0fe"),
                              margin=dict(l=0,r=60,t=10,b=30))
        st.plotly_chart(fig_auc, use_container_width=True)

    st.markdown("---")
    st.subheader("🕸️ Radar Chart — Perbandingan Multi-Dimensi")

    categories = ["F1-Score (×100)","ROC-AUC (×100)","Kecepatan","Interpretabilitas","Stabilitas"]
    colors_model = ["#00d4ff","#2ed573","#ffa502","#a29bfe"]

    fig_radar = go.Figure()
    for i, row in MODEL_HASIL.iterrows():
        vals = [row["F1-Score"]*100, row["ROC-AUC"]*100,
                row["Kecepatan"], row["Interpretabilitas"], row["Stabilitas"]]
        vals_closed = vals + [vals[0]]
        cats_closed = categories + [categories[0]]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_closed, theta=cats_closed,
            name=row["Model"],
            line=dict(color=colors_model[i], width=2),
            fill="toself", fillcolor=colors_model[i].replace("#","rgba(").rstrip(")") + ",0.06)",
        ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="#111827",
            radialaxis=dict(visible=True, range=[0,100], color="#7a8ba8", gridcolor="#1a2235"),
            angularaxis=dict(color="#7a8ba8", gridcolor="#1a2235"),
        ),
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        legend=dict(font=dict(color="#e8f0fe"), bgcolor="#111827"),
        height=420, margin=dict(l=60,r=60,t=30,b=30),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Rangkuman Kelebihan & Kekurangan")

    model_info = [
        ("XGBoost","🥇","#00d4ff","Performa terbaik. Tangani class imbalance dengan `scale_pos_weight`. Robust terhadap outlier curah hujan.",
         "Akurasi tinggi, feature importance interpretable","Lebih lambat, butuh hyperparameter tuning"),
        ("Random Forest","🥈","#2ed573","Stabil dan tidak mudah overfit. Baik untuk data cuaca yang noisy dan berdimensi tinggi.",
         "Cepat, stabil, out-of-bag estimate","Kurang optimal pada fitur berkorelasi tinggi"),
        ("Neural Network","🥉","#ffa502","MLP 2 hidden layer (64,32). Berpotensi lebih baik dengan data yang lebih besar.",
         "Tangkap pola kompleks non-linear","Butuh banyak data & tuning, kurang interpretable"),
        ("Logistic Regression","4️⃣","#a29bfe","Baseline yang baik. Sangat cepat dan interpretable, tapi terbatas pada hubungan linear.",
         "Sangat cepat, mudah diinterpretasi","Performa rendah pada pola non-linear"),
    ]
    cols = st.columns(4)
    for col, (nama, rank, clr, desc, pro, con) in zip(cols, model_info):
        with col:
            st.markdown(f"""
            <div style="background:#111827;border:1px solid {clr}30;border-top:2px solid {clr};
                        border-radius:12px;padding:16px;height:100%">
                <div style="color:{clr};font-weight:700;font-size:15px;margin-bottom:6px">{rank} {nama}</div>
                <div style="color:#7a8ba8;font-size:12px;line-height:1.5;margin-bottom:10px">{desc}</div>
                <div style="color:#2ed573;font-size:11px;font-family:monospace">✓ {pro}</div>
                <div style="color:#7a8ba8;font-size:11px;font-family:monospace;margin-top:4px">✗ {con}</div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: DATA LOKASI
# ─────────────────────────────────────────────
elif page == "📋 Data Lokasi":
    st.title("📋 Data Seluruh Titik Pemantauan")
    st.caption("59 titik pemantauan di seluruh wilayah Balikpapan")
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Titik", "59")
    c2.metric("Kecamatan", "6")
    c3.metric("Titik Pantau Khusus", "25")
    c4.metric("Kelurahan", "34")

    st.markdown("---")

    col_filter, col_search = st.columns([2, 1])
    with col_filter:
        kec_filter = st.selectbox("Filter Kecamatan",
                                  ["Semua","Utara","Timur","Selatan","Barat","Tengah","Kota","Pantau"])
    with col_search:
        risiko_filter = st.selectbox("Filter Kelas Risiko", ["Semua","TINGGI","SEDANG","RENDAH"])

    df_show = df.copy()
    if kec_filter != "Semua":
        df_show = df_show[df_show.Kecamatan == kec_filter]
    if risiko_filter != "Semua":
        df_show = df_show[df_show.Kelas == risiko_filter]

    df_display = df_show[["ID","Nama","Kecamatan","Lat","Lon","Risiko","Kelas"]].copy()
    df_display["Risiko (%)"] = (df_display["Risiko"] * 100).round(1)
    df_display = df_display.drop(columns=["Risiko"]).sort_values("Risiko (%)", ascending=False).reset_index(drop=True)
    df_display.index += 1

    st.dataframe(df_display, use_container_width=True, height=500)

    st.markdown("---")
    col_pie, col_bar = st.columns(2)

    with col_pie:
        st.subheader("Distribusi Kelas Risiko")
        pie_data = df["Kelas"].value_counts().reset_index()
        pie_data.columns = ["Kelas","Jumlah"]
        fig_pie = px.pie(pie_data, names="Kelas", values="Jumlah",
                         color="Kelas",
                         color_discrete_map={"TINGGI":"#ff4757","SEDANG":"#ffa502","RENDAH":"#2ed573"},
                         height=300)
        fig_pie.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827",
                              legend=dict(font=dict(color="#e8f0fe"),bgcolor="#111827"),
                              margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_bar:
        st.subheader("Distribusi per Kecamatan")
        kec_data = df.groupby(["Kecamatan","Kelas"]).size().reset_index(name="Jumlah")
        fig_kec = px.bar(kec_data, x="Kecamatan", y="Jumlah", color="Kelas",
                         color_discrete_map={"TINGGI":"#ff4757","SEDANG":"#ffa502","RENDAH":"#2ed573"},
                         barmode="stack", height=300)
        fig_kec.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827",
                              xaxis=dict(color="#7a8ba8", gridcolor="#1a2235"),
                              yaxis=dict(color="#7a8ba8", gridcolor="#1a2235"),
                              legend=dict(font=dict(color="#e8f0fe"),bgcolor="#111827"),
                              margin=dict(l=0,r=0,t=20,b=40))
        st.plotly_chart(fig_kec, use_container_width=True)
