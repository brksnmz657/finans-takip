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

# --- 2. VERİ HAFIZASI ---
if "fiyatlar" not in st.session_state:
    st.session_state.fiyatlar = [111.5746] # Başlangıç fiyatı

# Rastgele değişim
degisim = np.random.uniform(-0.05, 0.05)
yeni_fiyat = st.session_state.fiyatlar[-1] + degisim
st.session_state.fiyatlar.append(yeni_fiyat)

# Hafıza dolmasın diye son 50 veriyi tutalım
if len(st.session_state.fiyatlar) > 50:
    st.session_state.fiyatlar.pop(0)

# --- 3. ARAYÜZ ---
st.set_page_config(layout="wide")

with st.sidebar:
    st.header("⚙️ Kontrol Paneli")
    varlik = st.selectbox("Varlık Seçin:", ["Gümüş (Gram)", "Dolar/TL", "Euro/TL"])
    otomatik = st.toggle("Otomatik Akış")

st.title(f"🥈 {varlik} Raporu")

# Metrikler
col1, col2, col3 = st.columns(3)
col1.metric("Güncel Fiyat", f"{yeni_fiyat:.4f} TL", f"{degisim:+.4f}")
col2.metric("Anlık Değişim", f"{degisim:+.4f} TL")
col3.metric("Yüzdesel Değişim", f"{(degisim/yeni_fiyat)*100:.3f}%")

# Grafik: Listeyi DataFrame'e çevirip çizdiriyoruz
df = pd.DataFrame(st.session_state.fiyatlar, columns=['Fiyat'])
st.line_chart(df)

if otomatik:
    time.sleep(1) # Hızını buradan ayarlayabilirsin (1 saniye)
    st.rerun()