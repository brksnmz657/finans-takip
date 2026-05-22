import streamlit as st
import pandas as pd
import numpy as np

# --- 1. ŞİFRE KORUMASI ---
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
                st.error("Hatalı giriş!")
        return False
    return True

if not check_password():
    st.stop()

# --- 2. UYGULAMA PANELİ ---
st.set_page_config(layout="wide", page_title="Finansal Takip")

# Kenar Çubuğu (Sidebar)
with st.sidebar:
    st.header("⚙️ Kontrol Paneli")
    varlik = st.selectbox("Grafikte Görmek İstediğiniz Varlık:", ["Gümüş (Gram)", "Dolar/TL", "Euro/TL", "Altın (Gram)"])
    otomatik_akis = st.toggle("Otomatik Akış (Canlı Yayın)")
    
    st.divider()
    st.subheader("📊 Son Piyasa Durumu")
    st.write("Gümüş (Gram): 111.58 TL")
    st.write("Dolar/TL: 45.74 TL")
    st.write("Euro/TL: 53.05 TL")
    st.write("Altın (Gram): 6640.05 TL")

# Ana Ekran
st.title(f"🥈 {varlik} Raporu")

# Metrikler
col1, col2, col3 = st.columns(3)
col1.metric("Güncel Fiyat", "111.5746 TL", "-0.0094 TL")
col2.metric("Anlık Değişim", "-0.0094 TL")
col3.metric("Yüzdesel Değişim", "-0.01%")

# Grafik (İnişli çıkışlı)
chart_data = pd.DataFrame(np.random.randn(20).cumsum() + 111, columns=['Fiyat'])
st.line_chart(chart_data)

if otomatik_akis:
    st.rerun() # Otomatik yenileme özelliği