import streamlit as st
import plotly.graph_objects as go
import time
from fetcher import get_data, SYMBOLS

st.set_page_config(page_title="Finansal Panel", layout="wide")

st.title("📊 Profesyonel Finansal Analiz Terminali")

# Varlık Seçimi
secilen = st.sidebar.selectbox("Varlık Seçin", list(SYMBOLS.keys()))
symbol = SYMBOLS[secilen]

# Ana Grafik Alanı
placeholder = st.empty()

while True:
    with placeholder.container():
        fiyat, df = get_data(symbol)
        
        if fiyat is not None:
            st.metric(f"{secilen} Anlık Fiyat", f"{fiyat:.4f} TL")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df.index, y=df.values, 
                mode='lines', 
                line=dict(color='#00F2FF', width=2, shape='spline')
            ))
            
            fig.update_layout(
                template="plotly_dark",
                margin=dict(l=20, r=20, t=30, b=20),
                height=400,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#222'),
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Veri bekleniyor...")
            
    # --- ALT BİLGİ (FOOTER) ---
    st.markdown("---")
    
    # Bölümler
    st.markdown("**Akademik Bölümler:** ESOGÜ - Siyaset Bilimi ve Kamu Yönetimi | AÖF - Yönetim Bilişim Sistemleri")
    
    # İletişim ve Hesaplar
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    with footer_col1:
        st.markdown("**İletişim:**")
        st.markdown("📧 [sonmezburak2007@gmail.com](mailto:sonmezburak2007@gmail.com)")
    with footer_col2:
        st.markdown("**LinkedIn:**")
        st.markdown("🔗 [Burak Sönmez](https://www.linkedin.com/in/buraksönmez/)")
    with footer_col3:
        st.markdown("**GitHub:**")
        st.markdown("💻 [brksnmz657](https://github.com/brksnmz657)")
            
    time.sleep(3)
    st.rerun()
