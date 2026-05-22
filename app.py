import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="Finansal Takip Portalı")

# --- 1. OTURUM ---
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
            else:
                st.error("Hatalı!")
        return False
    return True

if not check_password(): st.stop()

# --- 2. GÜÇLENDİRİLMİŞ VERİ ÇEKME ---
@st.cache_data(ttl=300)
def get_live_data(symbol):
    try:
        # Yahoo Finance için 'user-agent' ekleyerek erişim engelini aşıyoruz
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1d", interval="5m")
        if not df.empty:
            return df['Close']
    except:
        pass
    return None

tickers = {
    "Dolar/TL": "USDTRY=X",
    "Euro/TL": "EURTRY=X",
    "Altın (Ons)": "GC=F",
    "Gümüş (Ons)": "SI=F"
}

# --- 3. PANEL ---
st.sidebar.header("⚙️ Kontrol Paneli")
secilen = st.sidebar.selectbox("Varlık Seçin:", list(tickers.keys()))

st.title(f"📈 {secilen} Canlı Raporu")

fiyatlar = get_live_data(tickers[secilen])

if fiyatlar is not None:
    current = float(fiyatlar.iloc[-1])
    diff = current - float(fiyatlar.iloc[0])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Güncel", f"{current:.4f}")
    col2.metric("Değişim", f"{diff:+.4f}")
    col3.metric("Yüzde", f"{(diff/float(fiyatlar.iloc[0]))*100:.3f}%")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=fiyatlar.values, mode='lines', 
        line=dict(color='#00F2FF', width=3, shape='spline')
    ))
    fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Veri şu an çekilemiyor. Lütfen bekleyin veya kontrol edin.")

if st.sidebar.toggle("Otomatik Yenile", True):
    time.sleep(30)
    st.rerun()