from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI(title="Painel Financeiro API", version="1.0")

# Permitir que o teu frontend na Vercel acesse esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, podes restringir para o URL exato do teu site na Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dicionário auxiliar de mapeamento
TICKERS_MAP = {
    "VALE3": "VALE3.SA",
    "PETR4": "PETR4.SA",
    "ITUB4": "ITUB4.SA",
    "WEGE3": "WEGE3.SA",
    "BBAS3": "BBAS3.SA",
    "BTC": "BTC-BRL"
}

@app.get("/api/cotacao/{ticker}")
def obter_cotacao(ticker: str):
    ticker_upper = ticker.upper()
    if ticker_upper not in TICKERS_MAP:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")
    
    simbolo = TICKERS_MAP[ticker_upper]
    try:
        ativo = yf.Ticker(simbolo)
        # Pega o histórico recente para extrair o preço atual
        hist = ativo.history(period="5d")
        if hist.empty:
            raise HTTPException(status_code=500, detail="Não foi possível obter dados do ativo")
        
        preco_atual = float(hist['Close'].iloc[-1])
        preco_min = float(hist['Low'].min())
        preco_max = float(hist['High'].max())
        preco_medio = float(hist['Close'].mean())

        return {
            "ticker": ticker_upper,
            "preco_atual": round(preco_atual, 2),
            "min_periodo": round(preco_min, 2),
            "max_periodo": round(preco_max, 2),
            "preco_medio": round(preco_medio, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "online", "message": "API do Painel Financeiro a funcionar perfeitamente!"}
