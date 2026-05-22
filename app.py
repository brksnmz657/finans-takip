import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. OTURUM VE ŞİFRE ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if not st.session_state.password_correct:
        st.title("🔒 Giriş Ekranı")
        if st.button("Giriş Yap") and st.text_input("Şifre:", type="password") == "1234":
            st.session_state.password_correct = True
            st.rerun()
        return False
    return True

if not check_password(): st.stop()

# --- 2. FİYAT SİMÜLASYONU ---
if "fiyat" not in st.session_state:
    st.session_state.fiyat = 111.5746

# Fiyatı rastgele ufak bir miktar değiştir
degisim = np.random.uniform(-0.05, 0.05)
st.session_state.fiyat += degisim

# --- 3. ARAYÜZ ---
st.set_page_config(layout="wide")

with st.sidebar:
    st.header("⚙️ Kontrol Paneli")
    varlik = st.selectbox("Varlık Seçin:", ["Gümüş (Gram)", "Dolar/TL", "Euro/TL"])
    otomatik = st.toggle("Otomatik Akış")

st.title(f"🥈 {varlik} Raporu")

# Metrikleri dinamik yapalım
col1, col2, col3 = st.columns(3)
col1.metric("Güncel Fiyat", f"{st.session_state.fiyat:.4f} TL", f"{degisim:+.4f}")
col2.metric("Anlık Değişim", f"{degisim:+.4f} TL")
col3.metric("Yüzdesel Değişim", f"{(degisim/st.session_state.fiyat)*100:.3f}%")

# Grafik
chart_data = pd.DataFrame([st.session_state.fiyat], columns=['Fiyat'])
st.line_chart(chart_data)

if otomatik:
    time.sleep(2) # 2 saniye bekle
    st.rerun() # Sayfayı otomatik yenile