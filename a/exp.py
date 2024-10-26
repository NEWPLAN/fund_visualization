import akshare as ak
import matplotlib.pyplot as plt
import pandas as pd
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import numpy as np

print(dir(ak))

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号

stock_code = "603228"
start_date = "20240601"
end_date = "20240702"
print(f"正在获取股票 {stock_code} 从 {start_date} 到 {end_date} 的历史行情数据...")
stock_data = ak.stock_zh_a_hist(
    symbol=stock_code, start_date=start_date, end_date=end_date, adjust="qfq"
)
print("数据获取成功！")
print(stock_data)
# 重新排列列顺序以适应 mplfinance 的格式

stock_data = stock_data[["日期", "开盘", "最高", "最低", "收盘", "成交量"]]
print(type(stock_data["日期"][0]))
print(stock_data)

# 计算布林线
stock_data["中轨"] = stock_data["收盘"].rolling(window=20).mean()
stock_data["上轨"] = (
    stock_data["中轨"] + 2 * stock_data["收盘"].rolling(window=20).std()
)
stock_data["下轨"] = (
    stock_data["中轨"] - 2 * stock_data["收盘"].rolling(window=20).std()
)

# 计算 MACD
exp1 = stock_data["收盘"].ewm(span=12, adjust=False).mean()
exp2 = stock_data["收盘"].ewm(span=26, adjust=False).mean()
stock_data["MACD"] = exp1 - exp2
stock_data["信号线"] = stock_data["MACD"].ewm(span=9, adjust=False).mean()
stock_data["MACD柱"] = stock_data["MACD"] - stock_data["信号线"]

# 绘制K线图

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(14, 10))
# 绘制K线

candlestick_ohlc(
    ax1,
    stock_data[["日期", "开盘", "最高", "最低", "收盘"]].values,
    width=0.6,
    colorup="red",
    colordown="green",
)

ax1.plot(stock_data["日期"], stock_data["中轨"], label="中轨")
ax1.plot(stock_data["日期"], stock_data["上轨"], label="上轨")
ax1.plot(stock_data["日期"], stock_data["下轨"], label="下轨")
ax1.xaxis_date()
ax1.legend()
ax1.set_title("景旺电子 K线图与布林线")

# 绘制MACD
ax2.plot(stock_data["日期"], stock_data["MACD"], label="MACD")
ax2.plot(stock_data["日期"], stock_data["信号线"], label="信号线")
ax2.bar(stock_data["日期"], stock_data["MACD柱"], label="MACD柱")
ax2.xaxis_date()
ax2.legend()
ax2.set_title("景旺电子 MACD")
plt.tight_layout()
plt.show()
