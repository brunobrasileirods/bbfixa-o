# Dashboard de ações: Itaú, Vale e Petrobras

Site em Python (Streamlit + Plotly) com gráficos de performance de ITUB4, VALE3 e PETR4.

## Como rodar
1. Instale o Python 3.10+ (https://www.python.org/downloads/, marque "Add to PATH").
2. No terminal, dentro desta pasta:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```
3. Testes: `pytest`

## Estrutura
- `app.py`: interface
- `data.py`: download e cache (yfinance)
- `analysis.py`: retornos, volatilidade, drawdown, RSI
- `charts.py`: gráficos Plotly

Dados do Yahoo Finance, com atraso. Não é recomendação de investimento.
