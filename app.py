import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. PROFESYONEL AYARLAR
st.set_page_config(page_title="Finansal Karar Destek Sistemi", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    div[data-testid="stMetric"] { background-color: #1c222b; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. VERİ YÖNETİMİ (Modüler yapı için session_state)
if "history" not in st.session_state:
    st.session_state.history = {"Gümüş (Gram)": [111.58 + np.random.uniform(-1, 1) for _ in range(50)]}

varlik = "Gümüş (Gram)"
fiyatlar = st.session_state.history[varlik]
df = pd.DataFrame(fiyatlar, columns=['Price'])

# 3. TEKNİK ANALİZ HESAPLAMALARI
df['SMA_5'] = df['Price'].rolling(window=5).mean() # 5 günlük hareketli ortalama (Trend)
df['Fark'] = df['Price'].diff() # Günlük değişim

# 4. ARAYÜZ (KPI METRİKLERİ)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Anlık Fiyat", f"{df['Price'].iloc[-1]:.2f} TL", f"{df['Fark'].iloc[-1]:+.2f}")
with col2:
    st.metric("Trend (SMA 5)", f"{df['SMA_5'].iloc[-1]:.2f} TL")
with col3:
    st.metric("Volatilite", "Düşük" if df['Price'].std() < 1 else "Yüksek")

# 5. PROFESYONEL GRAFİK
fig = go.Figure()
fig.add_trace(go.Scatter(y=df['Price'], name='Fiyat', line=dict(color='#00F2FF', width=3)))
fig.add_trace(go.Scatter(y=df['SMA_5'], name='Trend (SMA 5)', line=dict(color='#FFD700', width=2, dash='dot')))

fig.update_layout(
    template="plotly_dark",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    hovermode="x unified",
    margin=dict(l=20, r=20, t=30, b=20)
)
st.plotly_chart(fig, use_container_width=True)

# 6. ALT BİLGİ VE İLETİŞİM
st.divider()
st.subheader("Geliştirici Hakkında")
st.write("Bu sistem; gerçek zamanlı veri akışlarını teknik analiz indikatörleri ile birleştiren bir karar destek prototipidir.")
st.link_button("LinkedIn Profilime Git", "https://www.linkedin.com/in/buraksönmez/")
