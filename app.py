import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="Finansal Takip Portalı - Giriş")

# --- CSS İLE ÖZEL LAMBA EFEKTİ (Görselden Esinlenildi) ---
st.markdown("""
    <style>
    /* Tüm Uygulama Arka Planını Koru */
    .stApp { background-color: #0e1117; color: white; }

    /* Lamba Kapalıyken Karanlık ve Belirsiz Arka Plan */
    [data-test="stAppViewContainer"] {
        background-color: #0e1117;
        transition: background-color 0.8s ease;
    }

    /* Lamba Açıkken Görseldeki Gibi Hafifçe Aydınlık ve Renkli Arka Plan */
    [data-test="stAppViewContainer"][data-data-on="True"] {
        background-color: #1c1f24; /* Görseldeki açık arka plan rengine yakın */
    }

    /* Giriş Kutusunun Tasarımı (Işık Alan Bölge) */
    .login-box { 
        padding: 30px; 
        border-radius: 20px; 
        background-color: transparent; 
        border: 2px solid transparent; /* Varsayılan olarak gizli */
        transition: all 1.2s ease;
    }

    /* Lamba Açıkken Giriş Kutusu Belirsin */
    [data-test="stAppViewContainer"][data-data-on="True"] .login-box {
        border-color: #00F2FF; /* Gümüş grafiğinin rengiyle uyumlu */
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.4);
    }

    /* Başlık Stilize Et */
    h1.lamp-title { text-align: center; color: white; font-weight: 300; }
    
    /* Toggle Tasarımını Düzenle */
    .stToggle { margin: 20px auto; display: block; width: 100%; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. OTURUM VE GİRİŞ EKRANI (LAMBA MANTIĞI) ---
if "password_correct" not in st.session_state:
    st.session_state.password_correct = False

def login_screen():
    # Görseldeki gibi bir başlık
    st.markdown("<h1 class='lamp-title'>L o g i n   L a m p</h1>", unsafe_allow_html=True)
    
    # CSS efektlerini tetikleyen Toggle (Lamba) anahtarı
    # 'key' ve CSS seçicileri ile state'i bağlıyoruz
    lamba_state = st.session_state.get("lamba_on", False)
    lamba_acik = st.toggle("Giriş Yapmak İçin Lambayı Aç/Kapat", key="lamba_on", value=lamba_state)
    
    # CSS'in algılaması için data-on attribute'unu konteynıra ekliyoruz
    if lamba_acik:
        st.markdown('<div data-test="stAppViewContainer" data-data-on="True">', unsafe_allow_html=True)
    else:
        st.markdown('<div data-test="stAppViewContainer">', unsafe_allow_html=True)

    with st.container():
        # Giriş Kutusunun CSS ile tetiklenen efekti
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        # Form içerikleri (Sadece lamba açıkken etkili)
        if lamba_acik:
            user_input = st.text_input("Kullanıcı Adı (admin):")
            password_input = st.text_input("Şifre (12345):", type="password")
            
            if st.button("Giriş Yap", use_container_width=True):
                # Güncellenmiş kullanıcı adı ve şifre kontrolü
                if user_input == "admin" and password_input == "12345":
                    st.session_state.password_correct = True
                    # Doğru şifre girildiğinde lamba state'ini sıfırlıyoruz ki
                    # tekrar giriş yapıldığında kapalı başlasın
                    st.session_state.lamba_on = False
                    st.rerun()
                else:
                    st.error("Kullanıcı adı veya şifre hatalı!")
        else:
            st.write("---")
            st.info("Formun bir ışık hüzmesi gibi belirmesi için lambayı (yukarıdaki anahtarı) açmanız gerekiyor.")
            st.write("---")
            
        st.markdown('</div>', unsafe_allow_html=True) # login-box bitiş
    
    st.markdown('</div>', unsafe_allow_html=True) # data-on attribute'u bitiş

if not st.session_state.password_correct:
    login_screen()
    st.stop() # Doğru şifre girilmediği sürece sitenin geri kalanını gösterme

# --- 2. VERİ HAFIZASI ---
if "fiyatlar" not in st.session_state: 
    st.session_state.fiyatlar = [111.5746]
if "otomatik" not in st.session_state:
    st.session_state.otomatik = True 

# Fiyat simülasyonu
degisim = np.random.uniform(-0.05, 0.05)
st.session_state.fiyatlar.append(st.session_state.fiyatlar[-1] + degisim)
if len(st.session_state.fiyatlar) > 50: st.session_state.fiyatlar.pop(0)

# --- 3. ANA UYGULAMA PANELİ ---
# (Buradaki kodlar aynı kalıyor, sadece başlık ve renkler entegre edildi)
with st.sidebar:
    st.header("⚙️ Kontrol Paneli")
    varlik = st.selectbox("Grafikte Görmek İstediğiniz Varlık:", ["Gümüş (Gram)", "Dolar/TL", "Euro/TL", "Altın (Gram)"])
    st.session_state.otomatik = st.toggle("Otomatik Akış (Canlı Yayın)", value=st.session_state.otomatik)
    
    st.divider()
    st.subheader("📊 Son Piyasa Durumu")
    st.write("Gümüş (Gram): 111.58 TL")
    st.write("Dolar/TL: 45.74 TL")
    st.write("Euro/TL: 53.05 TL")
    st.write("Altın (Gram): 6640.05 TL")

st.title(f"📈 {varlik} Raporu")

# Metrikler
col1, col2, col3 = st.columns(3)
col1.metric("Güncel Fiyat", f"{st.session_state.fiyatlar[-1]:.4f} TL", f"{degisim:+.4f}")
col2.metric("Anlık Değişim", f"{degisim:+.4f} TL")
col3.metric("Yüzdesel Değişim", f"{(degisim/st.session_state.fiyatlar[-1])*100:.3f}%")

# Grafik (Gümüş rengi ile uyumlu mavi hat)
fig = go.Figure()
fig.add_trace(go.Scatter(y=st.session_state.fiyatlar, mode='lines', line=dict(color='#00F2FF', width=3)))
fig.update_layout(yaxis=dict(range=[110, 113]), template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig, use_container_width=True)

# --- 4. SAYFA ALTI (FOOTER) ---
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