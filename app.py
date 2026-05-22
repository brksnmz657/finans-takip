import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide")

# --- 1. OTURUM VE ŞİFRE ---
def check_password():
    if "password_correct" not in st.session_state: st.session_state.password_correct = False
    if not st.session_state.password_correct:
        st.title("🔒 Giriş Ekranı")
        if st.button("Giriş Yap") and st.text_input("Şifre:", type="password") == "1234":
            st.session_state.password_correct = True
            st.rerun()
        return False
    return True

if not check_password(): st.stop()

# --- 2. VERİ HAFIZASI ---
if "fiyatlar" not in st.session_state: 
    st.session_state.fiyatlar = [111.5746]
# Site açıldığında otomatik aksın diye 'otomatik' değişkenini True yapıyoruz
if "otomatik" not in st.session_state:
    st.session_state.otomatik = True 

# Rastgele değişim
degisim = np.random.uniform(-0.05, 0.05)
st.session_state.fiyatlar.append(st.session_state.fiyatlar[-1] + degisim)
if len(st.session_state.fiyatlar) > 50: st.session_state.fiyatlar.pop(0)

# --- 3. ARAYÜZ ---
with st.sidebar:
    st.header("⚙️ Kontrol Paneli")
    varlik = st.selectbox("Varlık Seçin:", ["Gümüş (Gram)", "Dolar/TL", "Euro/TL"])
    st.session_state.otomatik = st.toggle("Otomatik Akış", value=st.session_state.otomatik)

st.title(f"📈 {varlik} Portalı")

# Metrikler
col1, col2, col3 = st.columns(3)
col1.metric("Güncel Fiyat", f"{st.session_state.fiyatlar[-1]:.4f} TL", f"{degisim:+.4f}")
col2.metric("Anlık Değişim", f"{degisim:+.4f} TL")
col3.metric("Yüzdesel Değişim", f"{(degisim/st.session_state.fiyatlar[-1])*100:.3f}%")

# Plotly ile titremeyen sabit grafik
fig = go.Figure()
fig.add_trace(go.Scatter(y=st.session_state.fiyatlar, mode='lines', line=dict(color='#00F2FF', width=3)))
fig.update_layout(
    yaxis=dict(range=[111, 112.5]), # Y-eksenini sabitledik, zoom yapmaz
    template="plotly_dark",
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig, use_container_width=True)

if st.session_state.otomatik:
    time.sleep(1)
    st.rerun()