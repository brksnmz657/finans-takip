import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# Sayfa ayarları
st.set_page_config(layout="wide", page_title="Finansal Takip Portalı")

# --- 1. OTURUM VE ŞİFRE ---
if "login" not in st.session_state: st.session_state.login = False

def check_password():
    if not st.session_state.login:
        st.title("🔒 Giriş Ekranı")
        user = st.text_input("Kullanıcı Adı:", key="u")
        pwd = st.text_input("Şifre:", type="password", key="p")
        if st.button("Giriş Yap"):
            if user == "admin" and pwd == "1234":
                st.session_state.login = True
                st.rerun()
            else:
                st.error("Kullanıcı adı veya şifre hatalı!")
        return False
    return True

if not check_password(): st.stop()

# --- 2. VERİ HAFIZASI ---
if "history" not in st.session_state:
    st.session_state.history = {
        "Dolar/TL": [45.74], 
        "Euro/TL": [53.05], 
        "Altın (Gram)": [6640.05], 
        "Gümüş (Gram)": [111.58]
    }

# --- 3. ARAYÜZ ---
with st.sidebar:
    st.header("⚙️ Kontrol Paneli")
    varlik = st.selectbox("Grafikte Görmek İstediğiniz Varlık:", list(st.session_state.history.keys()))
    st.divider()
    st.info("Sistem gerçek zamanlı simülasyon modunda çalışmaktadır.")

# --- 4. SİMÜLASYON ALGORİTMASI ---
last_price = st.session_state.history[varlik][-1]
# %0.1 civarında rastgele değişim
change = last_price * np.random.uniform(-0.001, 0.001)
new_price = last_price + change
st.session_state.history[varlik].append(new_price)

# Hafızayı 50 kayıtla sınırla
if len(st.session_state.history[varlik]) > 50: st.session_state.history[varlik].pop(0)

# --- 5. ANA EKRAN VE GRAFİK ---
st.title(f"📈 {varlik} Canlı Takip")

col1, col2 = st.columns([1, 4])
col1.metric("Anlık Fiyat", f"{new_price:.4f} TL", f"{change:+.4f} TL")

fig = go.Figure(go.Scatter(
    y=st.session_state.history[varlik], 
    mode='lines',
    line=dict(shape='spline', color='#00F2FF', width=4)
))
fig.update_layout(
    template="plotly_dark", 
    plot_bgcolor='rgba(0,0,0,0)', 
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig, use_container_width=True)

# --- 6. HAKKIMDA (FOOTER) ---
st.divider()
st.markdown("### 👤 Hakkımda")

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("""
    🎓 **Eğitim Bilgileri**
    * **Eskişehir Osmangazi Üniversitesi (ESOGÜ)**
        * Siyaset Bilimi ve Kamu Yönetimi
    * **Anadolu Üniversitesi (AÖF)**
        * Yönetim Bilişim Sistemleri (YBS)
    """)

with col_b:
    st.markdown("""
    📧 **İletişim & Sosyal**
    * **E-posta:** sonmezburak2007@gmail.com
    * **LinkedIn:** [Profilime Git](https://www.linkedin.com/in/buraksönmez/)
    """)

st.caption("© 2026 Burak Sönmez - Finansal Takip ve Analiz Portalı")

# --- 7. OTOMATİK YENİLEME ---
time.sleep(1)
st.rerun()