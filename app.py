import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

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

# --- 2. GERÇEK VERİ ÇEKME (HATA TOLERANSLI) ---
@st.cache_data(ttl=600) # Veriyi 10 dakikada bir güncelle (API limitini aşmamak için)
def get_real_data(symbol):
    try:
        # Yahoo Finance'ten veri çek
        df = yf.download(symbol, period="1d", interval="15m", progress=False)
        if not df.empty:
            return df['Close']
    except Exception:
        return None
    return None

tickers = {
    "Dolar/TL": "USDTRY=X",
    "Euro/TL": "EURTRY=X",
    "Altın (Ons)": "GC=F",
    "Gümüş (Ons)": "SI=F"
}

# --- 3. ARAYÜZ ---
st.sidebar.header("⚙️ Kontrol Paneli")
secilen = st.sidebar.selectbox("Varlık Seçin:", list(tickers.keys()))

st.title(f"📈 {secilen} Güncel Piyasa Verisi")

data = get_real_data(tickers[secilen])

if data is not None:
    current = float(data.iloc[-1])
    change = current - float(data.iloc[0])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Son Fiyat", f"{current:.4f}")
    col2.metric("Günlük Değişim", f"{change:+.4f}")
    col3.metric("Yüzde", f"{(change/float(data.iloc[0]))*100:.3f}%")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=data.values, mode='lines', 
        line=dict(color='#00F2FF', width=3, shape='spline', smoothing=1.3)
    ))
    fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    st.success("Veriler Yahoo Finance üzerinden gerçek zamanlı çekilmiştir.")
else:
    st.error("Veri sunucudan alınamadı. Lütfen daha sonra tekrar deneyin.")

# --- 4. CV İÇİN FOOTER ---
st.divider()
st.markdown("### 👤 Hakkımda")
st.write("Bu uygulama, Python, Streamlit, Pandas ve yfinance API'si kullanılarak geliştirilmiş gerçek zamanlı bir finansal takip portalıdır.")