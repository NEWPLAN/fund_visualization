import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import akshare as ak
from mplfinance.original_flavor import candlestick2_ohlc
from matplotlib.ticker import FormatStrFormatter
from typing import Optional
import glog as logger


## ref: https://zhuanlan.zhihu.com/p/18102451465


def draw_kline(
    df: pd.DataFrame, title: str = "中国平安", highlight_extremes: bool = True
) -> Optional[plt.Figure]:
    """
    绘制K线图和移动平均线

    参数:
        df: 包含股票数据的DataFrame
        title: 图表标题
        highlight_extremes: 是否标记最高点和最低点

    返回:
        matplotlib Figure对象
    """
    logger.info("ploting : {}".format(title))
    if df.empty:
        logger.info("空数据，无法绘图")
        return None

    try:
        fig, ax = plt.subplots(figsize=(12, 5), dpi=150)

        # 绘制K线
        candlestick2_ohlc(
            ax,
            opens=df["open"].values,
            highs=df["high"].values,
            lows=df["low"].values,
            closes=df["close"].values,
            width=0.6,  # 调整宽度使K线更清晰
            colorup="red",
            colordown="green",
            alpha=0.8,
        )

        # 计算初始y轴范围
        y_min, y_max = df["low"].min(), df["high"].max()
        y_range = y_max - y_min

        # 标记最高点和最低点
        if highlight_extremes:
            max_idx = df["high"].idxmax()
            min_idx = df["low"].idxmin()

            # 标记最高点
            ax.scatter(max_idx, y_max, color="blue", s=40, zorder=5)
            ax.text(
                max_idx,
                y_max + y_range * 0.02,  # 在最高点上方2%的位置显示文本
                f"最高:{y_max:.2f}",
                ha="center",
                va="bottom",
                fontsize=9,
                bbox=dict(
                    facecolor="white",
                    alpha=0.7,
                    edgecolor="none",
                    boxstyle="round,pad=0.2",
                ),
            )

            # 标记最低点
            ax.scatter(min_idx, y_min, color="blue", s=40, zorder=5)
            ax.text(
                min_idx,
                y_min - y_range * 0.02,  # 在最低点下方2%的位置显示文本
                f"最低:{y_min:.2f}",
                ha="center",
                va="top",
                fontsize=9,
                bbox=dict(
                    facecolor="white",
                    alpha=0.7,
                    edgecolor="none",
                    boxstyle="round,pad=0.2",
                ),
            )

        # 绘制移动平均线
        ax.plot(
            df["MA5"].values,
            label="5日均线",
            linewidth=1.5,
            alpha=0.8,
            color="darkorange",
        )
        ax.plot(
            df["MA10"].values,
            label="10日均线",
            linewidth=1.5,
            alpha=0.8,
            color="purple",
        )

        # 设置图表标题和样式
        ax.set_title(title, fontsize=14, pad=20)
        ax.set_facecolor("whitesmoke")
        ax.grid(True, linestyle="--", alpha=0.5)

        # 设置x轴刻度
        ax.set_xticks(np.arange(0, len(df)))
        ax.set_xticklabels(df["date"].dt.strftime("%m-%d"), rotation=45)
        ax.tick_params(axis="x", labelsize=8)

        # 设置y轴格式和范围
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
        ax.set_ylim(y_min - y_range * 0.1, y_max + y_range * 0.1)  # 扩展10%的空间

        # 添加图例
        ax.legend(
            facecolor="white",
            edgecolor="gray",
            fontsize=9,
            framealpha=0.8,
            loc="upper left",
        )

        # 调整布局
        plt.tight_layout()

        return fig

    except Exception as e:
        logger.info(f"绘图失败: {e}")
        return None


## ref: https://zhuanlan.zhihu.com/p/18102451465


# 全局样式设置
def set_global_style():
    """设置全局绘图样式和中文字体"""
    plt.style.use("ggplot")
    # 中文字体设置（兼容Windows和Mac）
    if plt.get_backend().startswith("Win"):
        plt.rcParams["font.sans-serif"] = ["SimHei"]
    else:
        plt.rcParams["font.sans-serif"] = ["PingFang HK"]  # Mac系统推荐使用苹方字体
    plt.rcParams["axes.unicode_minus"] = False
