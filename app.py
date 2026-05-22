
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- 1. GİRİŞ VE ŞİFRE KONTROLÜ ---
def check_password():
    """Basit şifre koruması"""
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        st.title("🔒 Giriş Ekranı")
        st.markdown("Bu finansal takip portalını görüntülemek için lütfen şifrenizi girin.")
        
        # Giriş Bilgileri
        user_input = st.text_input("Kullanıcı Adı:", key="username")
        password_input = st.text_input("Şifre:", type="password", key="password")
        
        if st.button("Giriş Yap"):
            # Kullanıcı adı ve şifre kontrolü
            if user_input == "admin" and password_input == "1234":
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("Kullanıcı adı veya şifre hatalı!")
        return False
    return True

# Şifre kontrolünü en başa koyuyoruz
if not check_password():
    st.stop()

# --- 2. UYGULAMA İÇERİĞİ ---
# Şifre doğruysa burası çalışır

st.set_page_config(layout="wide", page_title="Finansal Takip Portalı")

st.title("⚡ Profesyonel Canlı Finansal Takip Portalı")
st.write("Hoş geldin! Finansal verilerin aşağıda listeleniyor.")

# Örnek bir veri seti (Buraya kendi verilerini ekleyebilirsin)
data = {
    'Varlık': ['Hisse Senedi', 'Altın', 'Döviz', 'Kripto'],
    'Değer': [15000, 25000, 10000, 5000]
}
df = pd.DataFrame(data)

# Tablo gösterimi
st.subheader("Varlık Dağılımı")
st.table(df)

# Grafik gösterimi
fig = go.Figure(data=[go.Pie(labels=df['Varlık'], values=df['Değer'])])
st.plotly_chart(fig)

# Çıkış yapma butonu
if st.button("Çıkış Yap"):
    st.session_state.password_correct = False
    st.rerun()