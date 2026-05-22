import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="Finansal Takip Portalı")

# --- 1. GÜNCEL PİYASA DEĞERLERİ (Yedekleme) ---
# Eğer API'den veri çekemezse bu değerleri kullanır
DEFAULT_PRICES = {
    "Dolar/TL": 32.50,
    "Euro/TL": 35.20,
    "Altın (Gram)": 2500.00,
    "Gümüş (Gram)": 30.50
}

# --- 2. GİRİŞ EKRANI ---
if "password_correct" not in st.session_state: st.session_state.password_correct = False
if not st.session_state.password_correct:
    st.title("🔒 Giriş Ekranı")
    if st.text_input("Şifre:", type="password") == "1234":
        st.session_state.password_correct = True
        st.rerun()
    st.stop()

# --- 3. VERİ ÇEKME (EN SAĞLAM YÖNTEM) ---
@st.cache_data(ttl=600)
def get_live_price(varlik_name):
    # Yahoo sembolleri
    symbols = {"Dolar/TL": "USDTRY=X", "Euro/TL": "EURTRY=X", "Altın (Gram)": "GC=F", "Gümüş (Gram)": "SI=F"}
    
    try:
        ticker = yf.Ticker(symbols[varlik_name])
        hist = ticker.history(period="1d")
        price = float(hist['Close'].iloc[-1])
        
        # Grama çevrim (Ons ise)
        if "Gram" in varlik_name:
            usd_try = float(yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1])
            price = (price / 31.1035) * usd_try
            
        return round(price, 2)
    except:
        return DEFAULT_PRICES.get(varlik_name, 1.0)

# --- 4. ARAYÜZ ---
varlik = st.sidebar.selectbox("Varlık Seçin:", list(DEFAULT_PRICES.keys()))
fiyat = get_live_price(varlik)

st.title(f"📈 {varlik} Canlı Takip")
st.metric(label="Güncel Fiyat (TL)", value=f"{fiyat:,.2f} TL")

# Grafik (Spline)
fig = go.Figure(go.Scatter(y=[fiyat*0.99, fiyat, fiyat*1.01], mode='lines', line=dict(shape='spline', color='#00F2FF', width=4)))
fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

# --- 5. FOOTER ---
st.divider()
st.write("Eğitim: ESOGÜ | YBS | [LinkedIn](https://www.linkedin.com/in/buraksönmez/)")

if st.sidebar.toggle("Otomatik Yenile", True):
    time.sleep(30)
    st.rerun()