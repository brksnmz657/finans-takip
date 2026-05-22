import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="Finansal Takip Portalı")

# --- 1. OTURUM VE ŞİFRE ---
if "password_correct" not in st.session_state: st.session_state.password_correct = False

def check_password():
    if not st.session_state.password_correct:
        st.title("🔒 Giriş Ekranı")
        user_input = st.text_input("Kullanıcı Adı:", key="username")
        password_input = st.text_input("Şifre:", type="password", key="password")
        if st.button("Giriş Yap"):
            if user_input == "admin" and password_input == "1234":
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("Kullanıcı adı veya şifre hatalı!")
        return False
    return True

if not check_password(): st.stop()

# --- 2. GERÇEK VERİ ÇEKME FONKSİYONU ---
@st.cache_data(ttl=60) # Veriyi 60 saniyede bir günceller
def get_live_data(ticker_symbol):
    try:
        df = yf.download(ticker_symbol, period="1d", interval="5m", progress=False)
        if not df.empty:
            return df['Close'].squeeze() # Tek sütunlu seriye çevir
        return None
    except:
        return None

# Varlık sembolleri
tickers = {
    "Gümüş (Ons)": "SI=F", 
    "Dolar/TL": "USDTRY=X",
    "Euro/TL": "EURTRY=X",
    "Altın (Ons)": "GC=F"
}

# --- 3. ARAYÜZ ---
with st.sidebar:
    st.header("⚙️ Kontrol Paneli")
    varlik_secim = st.selectbox("Varlık Seçin:", list(tickers.keys()))
    otomatik = st.toggle("Otomatik Akış (Canlı Yayın)", value=True)

st.title(f"📈 {varlik_secim} Raporu")

# Veriyi çek
fiyatlar = get_live_data(tickers[varlik_secim])

if fiyatlar is not None and not fiyatlar.empty:
    current_price = float(fiyatlar.iloc[-1])
    ilk_fiyat = float(fiyatlar.iloc[0])
    degisim = current_price - ilk_fiyat
    
    # Metrikler
    col1, col2, col3 = st.columns(3)
    col1.metric("Güncel Fiyat", f"{current_price:.4f}")
    col2.metric("Değişim", f"{degisim:+.4f}")
    col3.metric("Yüzdesel Değişim", f"{(degisim/ilk_fiyat)*100:.3f}%")

    # Grafik (Ovalleştirilmiş çizgiler)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=fiyatlar.values, 
        mode='lines', 
        line=dict(color='#00F2FF', width=3, shape='spline', smoothing=1.3)
    ))
    fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Veri bekleniyor... Lütfen bağlantınızı kontrol edin.")

# --- 4. FOOTER ---
st.divider()
st.markdown("### 👤 Hakkımda")
st.write("🎓 **Eğitim:** ESOGÜ (Siyaset Bilimi) | AÖF (YBS)")
st.write("🔗 [LinkedIn Profilim](https://www.linkedin.com/in/buraksönmez/)")

if otomatik:
    time.sleep(60) # Gerçek veri çok sık değişmediği için 60 saniye idealdir
    st.rerun()