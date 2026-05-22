import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="Finansal Takip Portalı")

# --- 1. OTURUM VE ŞİFRE ---
if "password_correct" not in st.session_state:
    st.session_state.password_correct = False

def check_password():
    if not st.session_state.password_correct:
        st.title("🔒 Giriş Ekranı")
        user_input = st.text_input("Kullanıcı Adı:", key="user")
        password_input = st.text_input("Şifre:", type="password", key="pass")
        if st.button("Giriş Yap"):
            if user_input == "admin" and password_input == "12345":
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("Hatalı kullanıcı adı veya şifre!")
        return False
    return True

if not check_password(): st.stop()

# --- 2. VERİ ÇEKME FONKSİYONU ---
@st.cache_data(ttl=60)
def get_data(ticker):
    try:
        # download metodu daha kararlı çalışır
        df = yf.download(ticker, period="1d", interval="5m", progress=False)
        if not df.empty:
            return df['Close']
        else:
            return pd.Series([0.0])
    except Exception:
        return pd.Series([0.0])

tickers = {
    "Dolar/TL": "USDTRY=X",
    "Euro/TL": "EURTRY=X",
    "Altın (Ons)": "GC=F",
    "Gümüş (Ons)": "SI=F"
}

# --- 3. ANA PANEL ---
st.sidebar.header("⚙️ Kontrol Paneli")
varlik = st.sidebar.selectbox("Varlık Seçin:", list(tickers.keys()))
otomatik = st.sidebar.toggle("Otomatik Akış", value=True)

st.title(f"📈 {varlik} Canlı Raporu")

fiyatlar = get_data(tickers[varlik])
if not fiyatlar.empty and fiyatlar.iloc[-1] != 0:
    current_price = fiyatlar.iloc[-1]
    degisim = current_price - fiyatlar.iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Güncel Fiyat", f"{current_price:.4f}")
    col2.metric("Günlük Değişim", f"{degisim:+.4f}")
    col3.metric("Yüzdesel Değişim", f"{(degisim/fiyatlar.iloc[0])*100:.3f}%")

    # Ovalleştirilmiş (spline) grafik
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=fiyatlar, 
        mode='lines', 
        line=dict(color='#00F2FF', width=3, shape='spline', smoothing=1.3)
    ))
    fig.update_layout(
        template="plotly_dark", 
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Şu an veri alınamıyor, lütfen bağlantıyı kontrol edin veya başka bir varlık seçin.")

# --- 4. FOOTER ---
st.divider()
st.markdown("### 👤 Hakkımda")
col_a, col_b = st.columns(2)
with col_a:
    st.write("🎓 **Eğitim:**")
    st.write("- **ESOGÜ:** Siyaset Bilimi ve Kamu Yönetimi")
    st.write("- **AÖF:** Yönetim Bilişim Sistemleri (YBS)")
with col_b:
    st.write("📧 **E-posta:** sonmezburak2007@gmail.com")
    st.write("🔗 **LinkedIn:** [Profiline Git](https://www.linkedin.com/in/buraksönmez/)")

if otomatik:
    time.sleep(60) # Dakikada bir yenileme
    st.rerun()