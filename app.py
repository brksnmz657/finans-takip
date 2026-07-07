
  
import streamlit as st
import plotly.graph_objects as go
import time
import datetime
import sqlite3
import pandas as pd
from fetcher import get_data, SYMBOLS

# Veri tabanında tabloyu başlayan fonksiyon
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

# Günlük özet istatistiklerini SQL ile çeken fonksiyon
def get_daily_stats(varlik):
    bugun = datetime.datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('finans_verileri.db')
    sorgu = f"""
        SELECT MAX(fiyat), MIN(fiyat), AVG(fiyat) FROM fiyat_gecmisi 
        WHERE varlik_turu = '{varlik}' AND tarih_saat LIKE '{bugun}%'
    """
    cursor = conn.cursor()
    cursor.execute(sorgu)
    res = cursor.fetchone()
    conn.close()
    return res if res else (None, None, None)

# Başlangıçta veri tabanını kontrol et
init_db()

st.set_page_config(page_title="Finansal Panel", layout="wide")
st.title("📊 Profesyonel Finansal Analiz Terminali")

# Varlık Seçimi
secilen = st.sidebar.selectbox("Varlık Seçin", list(SYMBOLS.keys()))
symbol = SYMBOLS[secilen]

# --- ÖZELLİK 1: FİYAT ALARM SİSTEMİ (SIDEBAR) ---
st.sidebar.markdown("---")
st.sidebar.subheader("🚨 Fiyat Alarm Sistemi")
alarm_tipi = st.sidebar.radio("Alarm Koşulu", ["Şunun Üzerine Çıkınca:", "Şunun Altına Düşünce:"])
alarm_hedef_fiyat = st.sidebar.number_input("Hedef Fiyat (TL)", min_value=0.0, value=0.0, step=0.1)
alarm_aktif = st.sidebar.checkbox("Alarmı Aktif Et")

# --- SQL GEÇMİŞ FİLTRELEME (SIDEBAR) ---
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 SQL Geçmiş Filtreleme")
merak_edilen_fiyat = st.sidebar.number_input("Geçmiş Fiyat Ara (TL)", min_value=0.0, value=0.0, step=0.1)

if st.sidebar.button("Bu Fiyata Yakın Anları Bul"):
    if merak_edilen_fiyat > 0:
        conn = sqlite3.connect('finans_verileri.db')
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

# Ana Ekran Düzeni
placeholder = st.empty()

# Zaman takip sayacı
if "son_log_zamani" not in st.session_state:
    st.session_state.son_log_zamani = 0

while True:
    current_time = time.time()
    
    # Her 60 saniyede bir arka planda TÜM varlıkları kaydet
    if current_time - st.session_state.son_log_zamani >= 60:
        for isim, simge in SYMBOLS.items():
            fiyat_kayit, _ = get_data(simge)
            if fiyat_kayit is not None:
                log_to_db(isim, fiyat_kayit)
        st.session_state.son_log_zamani = current_time

    with placeholder.container():
        fiyat, df = get_data(symbol)
        
        if fiyat is not None:
            # --- ÖZELLİK 2: ALARM KONTROLÜ ---
            if alarm_aktif and alarm_hedef_fiyat > 0:
                if alarm_tipi == "Şunun Üzerine Çıkınca:" and fiyat >= alarm_hedef_fiyat:
                    st.audio("https://www.soundjay.com/buttons/sounds/button-3.mp3")
                    st.error(f"🚨 ALARM: {secilen} fiyatı hedeflediğin {alarm_hedef_fiyat:.2f} TL seviyesinin üzerine çıktı! Anlık: {fiyat:.4f} TL")
                elif alarm_tipi == "Şunun Altına Düşünce:" and fiyat <= alarm_hedef_fiyat:
                    st.audio("https://www.soundjay.com/buttons/sounds/button-3.mp3")
                    st.warning(f"🚨 ALARM: {secilen} fiyatı hedeflediğin {alarm_hedef_fiyat:.2f} TL seviyesinin altına düştü! Anlık: {fiyat:.4f} TL")

            # --- ÖZELLİK 3: GÜNLÜK ÖZET KARTLARI ---
            max_f, min_f, avg_f = get_daily_stats(secilen)
            
            col_anlik, col_max, col_min, col_avg = st.columns(4)
            with col_anlik:
                st.metric(f"Anlık {secilen}", f"{fiyat:.4f} TL")
            with col_max:
                st.metric("Bugün En Yüksek (SQL)", f"{max_f:.4f} TL" if max_f else "Veri bekleniyor...")
            with col_min:
                st.metric("Bugün En Düşük (SQL)", f"{min_f:.4f} TL" if min_f else "Veri bekleniyor...")
            with col_avg:
                st.metric("Bugün Ortalama (SQL)", f"{avg_f:.4f} TL" if avg_f else "Veri bekleniyor...")

            # --- ÖZELLİK 4: HAREKETLİ ORTALAMA (SMA) HESAPLAMA VE GRAFİK ---
            fig = go.Figure()
            
            # Orijinal Fiyat Çizgisi
            fig.add_trace(go.Scatter(
                x=df.index, y=df.values, 
                name="Anlık Fiyat",
                mode='lines', 
                line=dict(color='#00F2FF', width=2, shape='spline')
            ))
            
            # Son 10 veri noktasının hareketli ortalamasını alıyoruz (SMA 10)
            if len(df) >= 10:
                df_sma = df.rolling(window=10).mean()
                fig.add_trace(go.Scatter(
                    x=df_sma.index, y=df_sma.values,
                    name="10 Periyotluk Ort. (SMA)",
                    mode='lines',
                    line=dict(color='#FFD700', width=1.5, dash='dash')
                ))
            
            fig.update_layout(
                template="plotly_dark",
                margin=dict(l=20, r=20, t=10, b=20),
                height=400,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#222'),
                hovermode="x unified",
                legend=dict(orientation="h", y=1.02, x=0)
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
        st.markdown("🔗 [Burak Sönmez](https://www.linkedin.com/in/buraks%C3%B6nmez/)")
    with footer_col3:
        st.markdown("**GitHub:**")
        st.markdown("💻 [brksnmz657](https://github.com/brksnmz657)")
            
    time.sleep(3)
    st.rerun()
