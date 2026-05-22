import streamlit as st
import pandas as pd
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
st.set_page_config(layout="wide", page_title="Finansal Takip Portalı")

st.title("📈 Finansal Performans Portalı")
st.write("Hoş geldin! Güncel verilerin ve performans grafiğin aşağıdadır.")

# İnişli çıkışlı grafik için örnek veri oluşturma
# Rastgele 30 günlük değerler (inişli çıkışlı)
veri_sayisi = 30
chart_data = pd.DataFrame(
    np.random.randn(veri_sayisi, 1).cumsum() + 100, 
    columns=['Portföy Değeri ($)']
)

# Çizgi grafiği gösterimi
st.subheader("Portföyün Zaman İçindeki Değişimi")
st.line_chart(chart_data)

# Veri tablosu gösterimi
st.subheader("Güncel Veri Detayları")
st.dataframe(chart_data.style.highlight_max(axis=0))

# Çıkış yapma butonu
if st.button("Çıkış Yap"):
    st.session_state.password_correct = False
    st.rerun()