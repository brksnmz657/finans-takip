import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Finansal Takip")

# --- 1. FONKSİYON: GRAM HESAPLAMA ---
@st.cache_data(ttl=300) # 5 dakikada bir güncelle
def get_live_price(symbol, is_ons=False):
    try:
        data = yf.download(symbol, period="1d", interval="5m", progress=False)
        fiyat = float(data['Close'].iloc[-1].item())
        
        if is_ons:
            # Dolar/TL'yi çekip grama çevirme
            usd_try = float(yf.download("USDTRY=X", period="1d", progress=False)['Close'].iloc[-1].item())
            return (fiyat / 31.1035) * usd_try
        return fiyat
    except:
        return None

# --- 2. ARAYÜZ ---
varliklar = {
    "Gümüş (Gram)": {"symbol": "SI=F", "ons": True},
    "Altın (Gram)": {"symbol": "GC=F", "ons": True},
    "Dolar/TL": {"symbol": "USDTRY=X", "ons": False}
}

secilen = st.sidebar.selectbox("Varlık Seçin:", list(varliklar.keys()))
st.title(f"📈 {secilen} Canlı")

info = varliklar[secilen]
fiyat = get_live_price(info['symbol'], info['ons'])

if fiyat:
    st.metric("Güncel Fiyat", f"{fiyat:.2f} TL")
    # Grafiği spline ile oval yaptık
    # (Buraya geçmiş veriyi getiren bir döngü eklenebilir)
else:
    st.error("Veri çekilemedi.")