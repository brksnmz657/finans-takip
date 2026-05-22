import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="Finansal Takip Portalı")

# --- 1. OTURUM VE ŞİFRE ---
def check_password():
    if "password_correct" not in st.session_state: st.session_state.password_correct = False
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

# --- 2. VERİ HAFIZASI ---
if "fiyatlar" not in st.session_state: 
    st.session_state.fiyatlar = [111.5746]
if "otomatik" not in st.session_state:
    st.session_state.otomatik = True 

# Fiyat simülasyonu
degisim = np.random.uniform(-0.05, 0.05)
st.session_state.fiyatlar.append(st.session_state.fiyatlar[-1] + degisim)
if len(st.session_state.fiyatlar) > 50: st.session_state.fiyatlar.pop(0)

# --- 3. ARAYÜZ ---
with st.sidebar:
    st.header("⚙️ Kontrol Paneli")
    varlik = st.selectbox("Grafikte Görmek İstediğiniz Varlık:", ["Gümüş (Gram)", "Dolar/TL", "Euro/TL", "Altın (Gram)"])
    st.session_state.otomatik = st.toggle("Otomatik Akış (Canlı Yayın)", value=st.session_state.otomatik)
    
    st.divider()
    st.subheader("📊 Son Piyasa Durumu")
    st.write("Gümüş (Gram): 111.58 TL")
    st.write("Dolar/TL: 45.74 TL")
    st.write("Euro/TL: 53.05 TL")
    st.write("Altın (Gram): 6640.05 TL")

st.title(f"📈 {varlik} Raporu")

# Metrikler
col1, col2, col3 = st.columns(3)
col1.metric("Güncel Fiyat", f"{st.session_state.fiyatlar[-1]:.4f} TL", f"{degisim:+.4f}")
col2.metric("Anlık Değişim", f"{degisim:+.4f} TL")
col3.metric("Yüzdesel Değişim", f"{(degisim/st.session_state.fiyatlar[-1])*100:.3f}%")

# Grafik
fig = go.Figure()
fig.add_trace(go.Scatter(y=st.session_state.fiyatlar, mode='lines', line=dict(color='#00F2FF', width=3)))
fig.update_layout(yaxis=dict(range=[110, 113]), template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig, use_container_width=True)

# --- 4. SAYFA ALTI (FOOTER) ---
st.divider()
st.markdown("### 👤 Hakkımda")
col_a, col_b = st.columns(2)
with col_a:
    st.write("**Eğitim:** ESOGÜ / AÖF - Yönetim Bilişim Sistemleri (YBS)")
    st.write("📧 **E-posta:** sonmezburak2007@gmail.com")
with col_b:
    st.write("🔗 **LinkedIn:** [Profiline Git](https://www.linkedin.com/in/buraksönmez/)")

if st.session_state.otomatik:
    time.sleep(1)
    st.rerun()