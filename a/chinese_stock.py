import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import akshare as ak
from mplfinance.original_flavor import candlestick2_ohlc
from matplotlib.ticker import FormatStrFormatter

# 设置中文字体
# for window
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
# for mac
plt.rcParams["font.family"] = "Heiti TC"  # 替换为你选择的字体
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号


def getStoneData():
    pingan = ak.stock_zh_a_daily(symbol="sh601318", adjust="qfq")
    df3 = pingan.reset_index().iloc[-30:, :6]  # 取过去30天数据
    df3 = df3.dropna(how="any").reset_index(drop=True)  # 去除空值且从零开始编号索引
    df3 = df3.sort_values(by="date", ascending=True)
    print(df3.info())

    # 均线数据
    df3["5"] = df3.close.rolling(5).mean()
    df3["10"] = df3.close.rolling(10).mean()

    print(df3.tail())
    return df3


def drawKLine(df3):
    plt.style.use("ggplot")
    fig, ax = plt.subplots(1, 1, figsize=(8, 3), dpi=200)
    # 绘制 K线
    candlestick2_ohlc(
        ax,
        opens=df3["open"].values,
        highs=df3["high"].values,
        lows=df3["low"].values,
        closes=df3["close"].values,
        width=0.75,
        colorup="r",
        colordown="g",
    )

    # 显示最高点和最低点
    ax.text(df3.high.idxmax(), df3.high.max(), s=df3.high.max(), fontsize=8)
    ax.text(df3.high.idxmin(), df3.high.min() - 2, s=df3.high.min(), fontsize=8)
    # 显示中文
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]

    ax.set_facecolor("white")
    ax.set_title("中国平安")

    # 画均线
    plt.plot(df3["5"].values, alpha=0.5, label="MA5")
    plt.plot(df3["10"].values, alpha=0.5, label="MA10")

    ax.legend(facecolor="white", edgecolor="white", fontsize=6)
    # date 为 object 数据类型，通过 pd.to_datetime将该列数据转换为时间类型，即datetime
    df3.date = pd.to_datetime(df3.date, format="%Y-%m-%d")
    # 修改x轴坐标
    plt.xticks(
        ticks=np.arange(0, len(df3)), labels=df3.date.dt.strftime("%Y-%m-%d").to_numpy()
    )
    plt.xticks(rotation=90, size=8)
    # 修改y轴坐标
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
    # x轴坐标显示不全，整理
    plt.subplots_adjust(bottom=0.25)
    plt.show()


data = getStoneData()
drawKLine(data)
