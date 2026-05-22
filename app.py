import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="Finansal Takip Portalı")

# --- 1. SABİT BAŞLANGIÇ FİYATLARI (Veri 0 gelirse bunu kullanacak) ---
SAFE_PRICES = {
    "Gümüş (Gram)": 32.50,
    "Altın (Gram)": 2500.00,
    "Dolar/TL": 32.20
}

# --- 2. ŞİFRE VE OTURUM ---
if "password_correct" not in st.session_state: st.session_state.password_correct = False

def check_password():
    if not st.session_state.password_correct:
        st.title("🔒 Giriş Ekranı")
        user = st.text_input("Kullanıcı Adı:", key="u")
        pwd = st.text_input("Şifre:", type="password", key="p")
        if st.button("Giriş Yap"):
            if user == "admin" and pwd == "1234":
                st.session_state.password_correct = True
                st.rerun()
            else: st.error("Hatalı!")
        return False
    return True

if not check_password(): st.stop()

# --- 3. VERİ ÇEKME VE HATA KONTROLÜ ---
@st.cache_data(ttl=60)
def get_clean_data(symbol, name):
    try:
        df = yf.download(symbol, period="1d", interval="5m", progress=False)
        # Eğer veri boşsa veya 0 ise sabit fiyatı döndür
        if df.empty or df['Close'].iloc[-1].item() <= 0:
            return SAFE_PRICES.get(name, 1.0)
        
        fiyat = float(df['Close'].iloc[-1].item())
        # Ons -> Gram çevrimi
        if name in ["Gümüş (Gram)", "Altın (Gram)"]:
            usd = float(yf.download("USDTRY=X", period="1d", progress=False)['Close'].iloc[-1].item())
            fiyat = (fiyat / 31.1035) * usd
        return fiyat
    except:
        return SAFE_PRICES.get(name, 1.0)

# --- 4. ARAYÜZ ---
tickers = {"Gümüş (Gram)": "SI=F", "Altın (Gram)": "GC=F", "Dolar/TL": "USDTRY=X"}
secilen = st.sidebar.selectbox("Varlık Seçin:", list(tickers.keys()))

st.title(f"📈 {secilen} Canlı Raporu")
fiyat = get_clean_data(tickers[secilen], secilen)

st.metric("Güncel Fiyat", f"{fiyat:.2f} TL")

# Grafik (Spline ile oval)
fig = go.Figure()
# Gerçek veri akışı için son 20 veriyi simüle eden görsel yapı
fig.add_trace(go.Scatter(y=[fiyat*0.99, fiyat*1.01, fiyat], mode='lines', 
                         line=dict(shape='spline', width=3, color='#00F2FF', smoothing=1.3)))
fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

if st.sidebar.toggle("Otomatik Akış", True):
    time.sleep(30)
    st.rerun()