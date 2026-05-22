import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="Finansal Takip Portalı")

# --- 1. OTURUM VE GİRİŞ ---
if "login" not in st.session_state: st.session_state.login = False
if not st.session_state.login:
    st.title("🔒 Giriş Ekranı")
    if st.text_input("Şifre:", type="password") == "1234":
        st.session_state.login = True
        st.rerun()
    st.stop()

# --- 2. HATA VERMEYEN DİNAMİK HAFIZA ---
if "history" not in st.session_state:
    st.session_state.history = {
        "Dolar/TL": [45.74], "Euro/TL": [53.05], 
        "Altın (Gram)": [6640.05], "Gümüş (Gram)": [111.58]
    }

# --- 3. ARAYÜZ ---
with st.sidebar:
    st.header("⚙️ Kontrol Paneli")
    varlik = st.selectbox("Varlık Seçin:", list(st.session_state.history.keys()))
    st.divider()
    st.info("Sistem canlı simülasyon modunda çalışmaktadır.")

# --- 4. AKILLI SİMÜLASYON ---
# Fiyatı sadece %0.1 civarında değiştir (daha gerçekçi)
last_price = st.session_state.history[varlik][-1]
change = last_price * np.random.uniform(-0.001, 0.001)
new_price = last_price + change

st.session_state.history[varlik].append(new_price)
if len(st.session_state.history[varlik]) > 50: st.session_state.history[varlik].pop(0)

# --- 5. GÖRSELLEŞTİRME ---
st.title(f"📈 {varlik} Canlı Takip")
col1, col2 = st.columns([1, 3])
col1.metric("Anlık Fiyat", f"{new_price:.4f} TL", f"{change:+.4f} TL")

fig = go.Figure(go.Scatter(
    y=st.session_state.history[varlik], 
    mode='lines',
    line=dict(shape='spline', color='#00F2FF', width=4)
))
fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

# Footer
st.divider()
st.write("Eğitim: ESOGÜ | YBS | [LinkedIn](https://www.linkedin.com/in/buraksönmez/)")

# --- 6. OTOMATİK AKIŞ ---
time.sleep(1) # Saniyede bir güncelle
st.rerun()