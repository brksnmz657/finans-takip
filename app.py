import streamlit as st
import pandas as pd
import numpy as np

# --- 1. GİRİŞ VE ŞİFRE KONTROLÜ ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
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

if not check_password():
    st.stop()

# --- 2. UYGULAMA İÇERİĞİ ---
st.set_page_config(layout="wide", page_title="Finansal Takip Portalı")

st.title("📈 Finansal Performans Portalı")

# İnişli çıkışlı veri üretimi
np.random.seed(42)
veri_sayisi = 30
degerler = 1000 + np.random.randn(veri_sayisi, 1).cumsum() * 50
df = pd.DataFrame(degerler, columns=['Portföy Değeri ($)'])

# --- ÖZET KARTLARI (KPI) ---
col1, col2, col3 = st.columns(3)

son_deger = df.iloc[-1, 0]
ilk_deger = df.iloc[0, 0]
kar_zarar = son_deger - ilk_deger
yuzde_degisim = (kar_zarar / ilk_deger) * 100

col1.metric("Güncel Portföy Değeri", f"${son_deger:,.2f}")
col2.metric("Toplam Kâr/Zarar", f"${kar_zarar:,.2f}", f"{yuzde_degisim:,.2f}%")
col3.metric("Günlük Değişim", "+$45.20", "1.2%")

# Grafik ve Detay
st.subheader("Performans Grafiği")
st.line_chart(df)

st.subheader("Veri Detayları")
st.dataframe(df.style.format("${:,.2f}"))

if st.button("Çıkış Yap"):
    st.session_state.password_correct = False
    st.rerun()