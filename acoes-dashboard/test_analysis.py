import pandas as pd
import pytest

import analysis


def test_cumulative_return():
    close = pd.DataFrame({"A": [100.0, 110.0, 121.0]})
    assert analysis.cumulative_return(close)["A"].iloc[-1] == pytest.approx(21.0)


def test_base_100():
    close = pd.DataFrame({"A": [50.0, 100.0]})
    assert analysis.base_100(close)["A"].tolist() == [100.0, 200.0]


def test_max_drawdown():
    close = pd.DataFrame({"A": [100.0, 120.0, 60.0, 90.0]})
    assert analysis.max_drawdown(close)["A"] == pytest.approx(-50.0)


def test_rsi_all_gains_is_100():
    s = pd.Series(range(1, 40), dtype=float)
    assert analysis.rsi(s).iloc[-1] == pytest.approx(100.0)
