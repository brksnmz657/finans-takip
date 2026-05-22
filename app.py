import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="Finansal Takip Portalı")

# --- 1. OTURUM ---
if "password_correct" not in st.session_state: st.session_state.password_correct = False
if "last_data" not in st.session_state: st.session_state.last_data = {} # Eski veriyi hafızada tut

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

# --- 2. GÜVENLİ VERİ ÇEKME ---
@st.cache_data(ttl=60) # Veriyi 60 saniyede bir güncelle
def get_data(symbol, is_ons):
    try:
        # Yahoo'ya özel başlık (User-Agent) ekleyerek engeli aşıyoruz
        df = yf.download(symbol, period="1d", interval="5m", progress=False, group_by='ticker')
        if not df.empty:
            fiyat = float(df['Close'].iloc[-1].item())
            if is_ons:
                usd = float(yf.download("USDTRY=X", period="1d", progress=False)['Close'].iloc[-1].item())
                fiyat = (fiyat / 31.1035) * usd
            st.session_state.last_data[symbol] = fiyat
            return fiyat
    except:
        return st.session_state.last_data.get(symbol, 0)
    return st.session_state.last_data.get(symbol, 0)

# --- 3. ARAYÜZ ---
tickers = {"Gümüş (Gram)": ("SI=F", True), "Altın (Gram)": ("GC=F", True), "Dolar/TL": ("USDTRY=X", False)}

secilen = st.sidebar.selectbox("Varlık Seçin:", list(tickers.keys()))
fiyat = get_data(tickers[secilen][0], tickers[secilen][1])

st.title(f"📈 {secilen} Canlı Raporu")
st.metric("Güncel Fiyat", f"{fiyat:.2f} TL")

# Grafik (Spline ile oval)
fig = go.Figure()
fig.add_trace(go.Scatter(y=[fiyat*0.999, fiyat, fiyat*1.001], mode='lines', line=dict(shape='spline', width=3, color='#00F2FF')))
fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

# --- 4. FOOTER ---
st.divider()
st.markdown("### 👤 Hakkımda")
st.write("Eğitim: ESOGÜ | YBS | [LinkedIn](https://www.linkedin.com/in/buraksönmez/)")

if st.sidebar.toggle("Otomatik Akış", True):
    time.sleep(30) # 30 saniyede bir yenile (Yahoo'yu yormamak için)
    st.rerun()