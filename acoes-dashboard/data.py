import pandas as pd
import streamlit as st
import yfinance as yf

TICKERS = {
    "Itaú (ITUB4)": "ITUB4.SA",
    "Vale (VALE3)": "VALE3.SA",
    "Petrobras (PETR4)": "PETR4.SA",
}
BENCHMARK = "^BVSP"


@st.cache_data(ttl=1800, show_spinner="Baixando cotações...")
def load_prices(tickers: tuple[str, ...], start: str, end: str) -> pd.DataFrame:
    """Retorna OHLCV com colunas MultiIndex (campo, ticker), preços ajustados."""
    df = yf.download(
        list(tickers),
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
        group_by="column",
    )
    if df.empty:
        return df
    return df.dropna(how="all")
