import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="Finansal Takip Portalı")

# --- CSS İLE KARANLIK MOD VE LAMBA EFEKTİ ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .login-box { 
        padding: 20px; 
        border-radius: 15px; 
        background-color: #1c1f24; 
        border: 1px solid #333;
        transition: all 0.5s ease;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. OTURUM VE GİRİŞ EKRANI (LAMBA MANTIĞI) ---
if "password_correct" not in st.session_state:
    st.session_state.password_correct = False

def login_screen():
    st.markdown("<h1 style='text-align: center;'>💡 Login Lamp</h1>", unsafe_allow_html=True)
    st.write("Giriş formunu görmek için lambayı aç!")
    
    # Lamba anahtarı
    lamba_acik = st.toggle("Lambayı Aç/Kapat")
    
    if lamba_acik:
        with st.container():
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            user_input = st.text_input("Kullanıcı Adı:")
            password_input = st.text_input("Şifre:", type="password")
            
            if st.button("Giriş Yap"):
                if user_input == "admin" and password_input == "12345":
                    st.session_state.password_correct = True
                    st.rerun()
                else:
                    st.error("Kullanıcı adı veya şifre hatalı!")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("*(Lamba kapalı, karanlık mod aktif)*")

if not st.session_state.password_correct:
    login_screen()
    st.stop()

# --- 2. VERİ HAFIZASI ---
if "fiyatlar" not in st.session_state: 
    st.session_state.fiyatlar = [111.5746]
if "otomatik" not in st.session_state:
    st.session_state.otomatik = True 

degisim = np.random.uniform(-0.05, 0.05)
st.session_state.fiyatlar.append(st.session_state.fiyatlar[-1] + degisim)
if len(st.session_state.fiyatlar) > 50: st.session_state.fiyatlar.pop(0)

# --- 3. ANA UYGULAMA PANELİ ---
with st.sidebar:
    st.header("⚙️ Kontrol Paneli")
    varlik = st.selectbox("Grafikte Görmek İstediğiniz Varlık:", ["Gümüş (Gram)", "Dolar/TL", "Euro/TL", "Altın (Gram)"])
    st.session_state.otomatik = st.toggle("Otomatik Akış (Canlı Yayın)", value=st.session_state.otomatik)

st.title(f"📈 {varlik} Raporu")

col1, col2, col3 = st.columns(3)
col1.metric("Güncel Fiyat", f"{st.session_state.fiyatlar[-1]:.4f} TL", f"{degisim:+.4f}")
col2.metric("Anlık Değişim", f"{degisim:+.4f} TL")
col3.metric("Yüzdesel Değişim", f"{(degisim/st.session_state.fiyatlar[-1])*100:.3f}%")

fig = go.Figure()
fig.add_trace(go.Scatter(y=st.session_state.fiyatlar, mode='lines', line=dict(color='#00F2FF', width=3)))
fig.update_layout(yaxis=dict(range=[110, 113]), template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig, use_container_width=True)

# --- 4. SAYFA ALTI ---
st.divider()
st.markdown("### 👤 Hakkımda")
st.write("🎓 **Eğitim:**")
st.write("- **ESOGÜ:** Siyaset Bilimi ve Kamu Yönetimi")
st.write("- **AÖF:** Yönetim Bilişim Sistemleri (YBS)")
st.write("📧 **E-posta:** sonmezburak2007@gmail.com")
st.write("🔗 **LinkedIn:** [Profiline Git](https://www.linkedin.com/in/buraksönmez/)")

if st.session_state.otomatik:
    time.sleep(1)
    st.rerun()