import streamlit as st
import plotly.graph_objects as go
import time
import datetime
import sqlite3
import pandas as pd
from fetcher import get_data, SYMBOLS

# Veri tabanında tabloyu başlatan fonksiyon (Yoksa otomatik oluşturur)
def init_db():
    conn = sqlite3.connect('finans_verileri.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fiyat_gecmisi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            varlik_turu TEXT NOT NULL,
            fiyat REAL NOT NULL,
            tarih_saat TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Fiyatı veri tabanına kaydeden fonksiyon
def log_to_db(varlik, fiyat):
    anlik_zaman = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('finans_verileri.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO fiyat_gecmisi (varlik_turu, fiyat, tarih_saat)
        VALUES (?, ?, ?)
    ''', (varlik, fiyat, anlik_zaman))
    conn.commit()
    conn.close()

# Başlangıçta veri tabanını kontrol et
init_db()

st.set_page_config(page_title="Finansal Panel", layout="wide")
st.title("📊 Profesyonel Finansal Analiz Terminali")

# Varlık Seçimi
secilen = st.sidebar.selectbox("Varlık Seçin", list(SYMBOLS.keys()))
symbol = SYMBOLS[secilen]

# --- YENİ ÖZELLİK: SQL FİLTRELEME ALANI ---
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 SQL Geçmiş Filtreleme")
merak_edilen_fiyat = st.sidebar.number_input("Fiyat Girin (TL)", min_value=0.0, value=0.0, step=0.1)

if st.sidebar.button("Bu Fiyata Yakın Anları Bul"):
    if merak_edilen_fiyat > 0:
        conn = sqlite3.connect('finans_verileri.db')
        # Girilen fiyatın %0.5 altını ve üstünü tolerans olarak tarar (Hassas yakalama için)
        alt_sinir = merak_edilen_fiyat * 0.995
        ust_sinir = merak_edilen_fiyat * 1.005
        
        sorgu = f"""
            SELECT tarih_saat, fiyat FROM fiyat_gecmisi 
            WHERE varlik_turu = '{secilen}' AND fiyat BETWEEN {alt_sinir} AND {ust_sinir}
            ORDER BY tarih_saat DESC LIMIT 10
        """
        df_sql = pd.read_sql_query(sorgu, conn)
        conn.close()
        
        if not df_sql.empty:
            st.sidebar.success(f"{secilen} için yakın zamanlar bulundu:")
            st.sidebar.dataframe(df_sql, use_container_width=True)
        else:
            st.sidebar.warning("Bu fiyat aralığına uygun geçmiş veri bulunamadı.")
    else:
        st.sidebar.info("Lütfen geçerli bir fiyat girin.")

# Ana Grafik Alanı
placeholder = st.empty()

# Arka planda dakikalık loglama takibi için zaman sayacı
if "son_log_zamani" not in st.session_state:
    st.session_state.son_log_zamani = 0

while True:
    current_time = time.time()
    
    # Kural: Her 60 saniyede bir (dakika başı) arka planda TÜM varlıkları kaydet
    if current_time - st.session_state.son_log_zamani >= 60:
        for isim, simge in SYMBOLS.items():
            fiyat_kayit, _ = get_data(simge)
            if fiyat_kayit is not None:
                log_to_db(isim, fiyat_kayit)
        st.session_state.son_log_zamani = current_time  # Zamanı güncelle

    # Ana ekrandaki grafik güncellenmesi
    with placeholder.container():
        fiyat, df = get_data(symbol)
        
        if fiyat is not None:
            st.metric(f"{secilen} Anlık Fiyat", f"{fiyat:.4f} TL")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df.index, y=df.values, 
                mode='lines', 
                line=dict(color='#00F2FF', width=2, shape='spline')
            ))
            
            fig.update_layout(
                template="plotly_dark",
                margin=dict(l=20, r=20, t=30, b=20),
                height=400,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#222'),
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Veri bekleniyor...")
            
    # --- ALT BİLGİ (FOOTER) ---
    st.markdown("---")
    st.markdown("**Akademik Bölümler:** ESOGÜ - Siyaset Bilimi ve Kamu Yönetimi | AÖF - Yönetim Bilişim Sistemleri")
    
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    with footer_col1:
        st.markdown("**İletişim:**")
        st.markdown("📧 [sonmezburak2007@gmail.com](mailto:sonmezburak2007@gmail.com)")
    with footer_col2:
        st.markdown("**LinkedIn:**")
        st.markdown("🔗 [Burak Sönmez](https://www.linkedin.com/in/buraksönmez/)")
    with footer_col3:
        st.markdown("**GitHub:**")
        st.markdown("💻 [brksnmz657](https://github.com/brksnmz657)")
            
    time.sleep(3)
    st.rerun()
