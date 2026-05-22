
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="Finansal Takip Portalı")

# --- 1. ŞİFRE KONTROLÜ ---
def check_password():
    if "password_correct" not in st.session_state: st.session_state.password_correct = False
    if not st.session_state.password_correct:
        st.title("🔒 Giriş Ekranı")
        user = st.text_input("Kullanıcı Adı:", key="u")
        pwd = st.text_input("Şifre:", type="password", key="p")
        if st.button("Giriş Yap"):
            if user == "admin" and pwd == "1234":
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("Kullanıcı adı veya şifre hatalı!")
        return False
    return True

if not check_password(): st.stop()

# --- 2. GERÇEK VERİ VE GRAM HESAPLAMA ---
@st.cache_data(ttl=300)
def get_data(symbol, is_ons=False):
    try:
        df = yf.download(symbol, period="1d", interval="15m", progress=False)
        fiyat = float(df['Close'].iloc[-1].item())
        
        if is_ons:
            # Dolar kurunu çek ve grama çevir
            usd_df = yf.download("USDTRY=X", period="1d", progress=False)
            usd_try = float(usd_df['Close'].iloc[-1].item())
            fiyat = (fiyat / 31.1035) * usd_try
        
        # Grafik için geçmiş veriyi de alalım (spline için)
        history = df['Close']
        if is_ons: history = (history / 31.1035) * usd_try
        
        return fiyat, history
    except:
        return None, None

varliklar = {
    "Gümüş (Gram)": {"symbol": "SI=F", "ons": True},
    "Altın (Gram)": {"symbol": "GC=F", "ons": True},
    "Dolar/TL": {"symbol": "USDTRY=X", "ons": False}
}

# --- 3. ARAYÜZ ---
with st.sidebar:
    st.header("⚙️ Kontrol Paneli")
    secilen = st.selectbox("Varlık Seçin:", list(varliklar.keys()))
    otomatik = st.toggle("Otomatik Akış", True)

st.title(f"📈 {secilen} Canlı Raporu")

fiyat, history = get_data(varliklar[secilen]['symbol'], varliklar[secilen]['ons'])

if fiyat:
    st.metric("Güncel Fiyat", f"{fiyat:.2f} TL")
    
    # Ovalleştirilmiş grafik
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=history.values.flatten(), mode='lines',
        line=dict(color='#00F2FF', width=3, shape='spline', smoothing=1.3)
    ))
    fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Veri alınamadı.")

# --- 4. FOOTER VE HAKKIMDA ---
st.divider()
st.markdown("### 👤 Hakkımda")
col_a, col_b = st.columns(2)
with col_a:
    st.write("🎓 **Eğitim:** ESOGÜ (Siyaset Bilimi) | AÖF (YBS)")
with col_b:
    st.write("📧 **E-posta:** sonmezburak2007@gmail.com")
    st.write("🔗 [LinkedIn Profiline Git](https://www.linkedin.com/in/buraksönmez/)")

if otomatik:
    time.sleep(60)
    st.rerun()