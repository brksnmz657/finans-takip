import yfinance as yf

SYMBOLS = {
    "Dolar/TL": "USDTRY=X",
    "Euro/TL": "EURTRY=X",
    "Gram Altın": "GC=F",
    "Gümüş": "SI=F",
    "Bitcoin": "BTC-USD"
}

def get_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # 1.4.1 sürümü için en stabil yöntem history
        df = ticker.history(period="5d", interval="1h")
        
        if not df.empty:
            current_price = df['Close'].iloc[-1]
            # Gram altın/gümüş dönüşümü
            if symbol in ["GC=F", "SI=F"]:
                current_price = (current_price / 31.1) * 45.85 # Anlık dolar kuru ile çarpan
            return round(float(current_price), 4), df['Close']
        return None, None
    except:
        return None, None
