import numpy as np
import pandas as pd

TRADING_DAYS = 252


def daily_returns(close: pd.DataFrame) -> pd.DataFrame:
    return close.pct_change().dropna(how="all")


def cumulative_return(close: pd.DataFrame) -> pd.DataFrame:
    """Retorno acumulado em % desde o primeiro pregão do período."""
    return (close / close.bfill().iloc[0] - 1) * 100


def base_100(close: pd.DataFrame) -> pd.DataFrame:
    return close / close.bfill().iloc[0] * 100


def annualized_volatility(returns: pd.DataFrame) -> pd.Series:
    return returns.std() * np.sqrt(TRADING_DAYS) * 100


def max_drawdown(close: pd.DataFrame) -> pd.Series:
    """Maior queda (%) de um pico até o vale seguinte."""
    drawdown = close / close.cummax() - 1
    return drawdown.min() * 100


def moving_average(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window).mean()


def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / window, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / window, adjust=False).mean()
    rs = gain / loss
    return 100 - 100 / (1 + rs)


def summary(close: pd.DataFrame) -> pd.DataFrame:
    """Tabela-resumo por ativo: preço atual, variações e faixa de 52 semanas."""
    last = close.ffill().iloc[-1]
    prev = close.ffill().iloc[-2] if len(close) > 1 else last
    year = close.tail(TRADING_DAYS)
    return pd.DataFrame(
        {
            "Preço atual": last,
            "Variação dia (%)": (last / prev - 1) * 100,
            "Variação período (%)": cumulative_return(close).ffill().iloc[-1],
            "Máx. 52s": year.max(),
            "Mín. 52s": year.min(),
        }
    )
