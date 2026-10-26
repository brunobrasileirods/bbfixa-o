from datetime import date, timedelta

import pandas as pd
import streamlit as st

import analysis
import charts
from data import BENCHMARK, TICKERS, load_prices

st.set_page_config(page_title="Ações: Itaú, Vale e Petrobras", layout="wide")
st.title("📈 Performance: Itaú, Vale e Petrobras")

PERIODS = {"1M": 30, "6M": 182, "1A": 365, "5A": 1825}

with st.sidebar:
    st.header("Filtros")
    selected = st.multiselect("Ações", list(TICKERS), default=list(TICKERS))
    period = st.radio("Período", [*PERIODS, "Personalizado"], index=2, horizontal=True)
    if period == "Personalizado":
        start = st.date_input("Início", date.today() - timedelta(days=365))
        end = st.date_input("Fim", date.today())
    else:
        end = date.today()
        start = end - timedelta(days=PERIODS[period])
    use_bench = st.checkbox("Comparar com Ibovespa", value=True)

if not selected:
    st.info("Selecione ao menos uma ação.")
    st.stop()
if start >= end:
    st.error("A data de início deve ser anterior à data final.")
    st.stop()

names = {TICKERS[n]: n for n in selected}
tickers = tuple(names) + ((BENCHMARK,) if use_bench else ())
# MM200 precisa de histórico anterior ao período exibido
raw = load_prices(tickers, str(start - timedelta(days=300)), str(end + timedelta(days=1)))
if raw.empty:
    st.error("Não foi possível obter cotações agora. Tente novamente em instantes.")
    st.stop()

labels = {**names, BENCHMARK: "Ibovespa"}
close_full = raw["Close"].rename(columns=labels)
close = close_full.loc[str(start):]
stocks = [n for n in selected if n in close.columns]
returns = analysis.daily_returns(close[stocks])

# Cards de resumo
summ = analysis.summary(close[stocks])
cols = st.columns(len(stocks))
for col, name in zip(cols, stocks):
    row = summ.loc[name]
    col.metric(
        name,
        f"R$ {row['Preço atual']:.2f}",
        f"{row['Variação dia (%)']:+.2f}% no dia",
    )

tab_over, tab_comp, tab_risk = st.tabs(["Visão Geral", "Comparação", "Risco"])

with tab_over:
    ticker_name = st.selectbox("Ação", stocks)
    ticker = TICKERS[ticker_name]
    ohlcv = pd.DataFrame(
        {f: raw[f][ticker] for f in ["Open", "High", "Low", "Close", "Volume"]}
    ).dropna()
    # as médias usam o histórico completo; o gráfico mostra só o período
    fig = charts.candlestick_chart(ohlcv, ticker_name)
    fig.update_xaxes(range=[str(start), str(end)])
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(
        charts.rsi_chart(close_full[ticker_name].dropna().loc[str(start):], ticker_name),
        use_container_width=True,
    )
    st.dataframe(summ.style.format("{:.2f}"), use_container_width=True)

with tab_comp:
    mode = st.radio("Visualização", ["Retorno acumulado (%)", "Base 100"], horizontal=True)
    cols_cmp = [c for c in close.columns]
    if mode.startswith("Retorno"):
        perf = analysis.cumulative_return(close[cols_cmp])
        st.plotly_chart(
            charts.comparison_chart(perf, "Retorno acumulado", "%"), use_container_width=True
        )
    else:
        perf = analysis.base_100(close[cols_cmp])
        st.plotly_chart(
            charts.comparison_chart(perf, "Performance (base 100)", "Base 100"),
            use_container_width=True,
        )

with tab_risk:
    c1, c2 = st.columns(2)
    risk = pd.DataFrame(
        {
            "Volatilidade anualizada (%)": analysis.annualized_volatility(returns),
            "Drawdown máximo (%)": analysis.max_drawdown(close[stocks]),
        }
    )
    c1.dataframe(risk.style.format("{:.2f}"), use_container_width=True)
    if len(stocks) > 1:
        c2.plotly_chart(charts.correlation_heatmap(returns), use_container_width=True)
    st.plotly_chart(charts.drawdown_chart(close[stocks]), use_container_width=True)

st.caption(
    "Dados via Yahoo Finance (podem ter atraso de ~15 min). "
    "Conteúdo informativo; não é recomendação de investimento."
)
