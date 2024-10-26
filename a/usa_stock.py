import akshare as ak
import pandas as pd
import datetime

stock_zh_a_hist_df = ak.stock_zh_a_hist(
    symbol="000001",
    period="daily",
    start_date="20170301",
    end_date="20231022",
    adjust="",
)

print(stock_zh_a_hist_df)


import akshare as ak
import mplfinance as mpf  # Please install mplfinance as follows: pip install mplfinance

# print(dir(ak))
stock_us_daily_df = ak.stock_us_daily(symbol="AAPL", adjust="qfq")
# stock_us_daily_df = ak.stock_zh_a_daily(symbol="159995", adjust="qfq")
# print(type(stock_us_daily_df["date"][0]))
stock_us_daily_df = stock_us_daily_df.set_index(["date"])
# print(type(stock_us_daily_df["date"][0]))
stock_us_daily_df = stock_us_daily_df["2020-04-01":"2020-04-29"]

mc = mpf.make_marketcolors(up="red", down="green")
s = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(
    stock_us_daily_df,
    type="candle",
    mav=(3, 6, 9),
    volume=True,
    show_nontrading=False,
    # style=s,
)
