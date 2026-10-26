import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import analysis


def comparison_chart(perf: pd.DataFrame, title: str, yaxis: str) -> go.Figure:
    fig = go.Figure()
    for col in perf.columns:
        fig.add_scatter(x=perf.index, y=perf[col], mode="lines", name=col)
    fig.update_layout(title=title, yaxis_title=yaxis, hovermode="x unified")
    return fig


def candlestick_chart(ohlcv: pd.DataFrame, name: str, mas=(20, 50, 200)) -> go.Figure:
    """ohlcv: colunas Open, High, Low, Close, Volume de um único ticker."""
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, row_heights=[0.75, 0.25], vertical_spacing=0.03
    )
    fig.add_trace(
        go.Candlestick(
            x=ohlcv.index,
            open=ohlcv["Open"],
            high=ohlcv["High"],
            low=ohlcv["Low"],
            close=ohlcv["Close"],
            name=name,
        ),
        row=1,
        col=1,
    )
    for w in mas:
        if len(ohlcv) >= w:
            fig.add_scatter(
                x=ohlcv.index,
                y=analysis.moving_average(ohlcv["Close"], w),
                mode="lines",
                name=f"MM{w}",
                line=dict(width=1),
                row=1,
                col=1,
            )
    fig.add_bar(x=ohlcv.index, y=ohlcv["Volume"], name="Volume", row=2, col=1)
    fig.update_layout(title=name, xaxis_rangeslider_visible=False, hovermode="x unified")
    return fig


def rsi_chart(close: pd.Series, name: str) -> go.Figure:
    fig = go.Figure(go.Scatter(x=close.index, y=analysis.rsi(close), name="RSI"))
    fig.add_hline(y=70, line_dash="dash", line_color="red")
    fig.add_hline(y=30, line_dash="dash", line_color="green")
    fig.update_layout(title=f"RSI (14) — {name}", yaxis_range=[0, 100])
    return fig


def correlation_heatmap(returns: pd.DataFrame) -> go.Figure:
    corr = returns.corr()
    fig = go.Figure(
        go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.index,
            zmin=-1,
            zmax=1,
            colorscale="RdBu",
            text=corr.round(2).values,
            texttemplate="%{text}",
        )
    )
    fig.update_layout(title="Correlação dos retornos diários")
    return fig


def drawdown_chart(close: pd.DataFrame) -> go.Figure:
    dd = (close / close.cummax() - 1) * 100
    return comparison_chart(dd, "Drawdown", "%")
