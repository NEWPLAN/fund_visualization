# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import akshare as ak
# from mplfinance.original_flavor import candlestick2_ohlc
# from matplotlib.ticker import FormatStrFormatter

# # 设置中文字体
# # for window
# plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
# # for mac
# plt.rcParams["font.family"] = "Heiti TC"  # 替换为你选择的字体
# plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号


# def getStoneData():
#     pingan = ak.stock_zh_a_daily(symbol="sh601318", adjust="qfq")
#     df3 = pingan.reset_index().iloc[-30:, :6]  # 取过去30天数据
#     df3 = df3.dropna(how="any").reset_index(drop=True)  # 去除空值且从零开始编号索引
#     df3 = df3.sort_values(by="date", ascending=True)
#     print(df3.info())

#     # 均线数据
#     df3["5"] = df3.close.rolling(5).mean()
#     df3["10"] = df3.close.rolling(10).mean()

#     print(df3.tail())
#     return df3


# def drawKLine(df3):
#     plt.style.use("ggplot")
#     fig, ax = plt.subplots(1, 1, figsize=(8, 3), dpi=200)
#     # 绘制 K线
#     candlestick2_ohlc(
#         ax,
#         opens=df3["open"].values,
#         highs=df3["high"].values,
#         lows=df3["low"].values,
#         closes=df3["close"].values,
#         width=0.75,
#         colorup="r",
#         colordown="g",
#     )

#     # 显示最高点和最低点
#     ax.text(df3.high.idxmax(), df3.high.max(), s=df3.high.max(), fontsize=8)
#     ax.text(df3.high.idxmin(), df3.high.min() - 2, s=df3.high.min(), fontsize=8)
#     # 显示中文
#     plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]

#     ax.set_facecolor("white")
#     ax.set_title("中国平安")

#     # 画均线
#     plt.plot(df3["5"].values, alpha=0.5, label="MA5")
#     plt.plot(df3["10"].values, alpha=0.5, label="MA10")

#     ax.legend(facecolor="white", edgecolor="white", fontsize=6)
#     # date 为 object 数据类型，通过 pd.to_datetime将该列数据转换为时间类型，即datetime
#     df3.date = pd.to_datetime(df3.date, format="%Y-%m-%d")
#     # 修改x轴坐标
#     plt.xticks(
#         ticks=np.arange(0, len(df3)), labels=df3.date.dt.strftime("%Y-%m-%d").to_numpy()
#     )
#     plt.xticks(rotation=90, size=8)
#     # 修改y轴坐标
#     ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
#     # x轴坐标显示不全，整理
#     plt.subplots_adjust(bottom=0.25)
#     plt.show()


# data = getStoneData()
# drawKLine(data)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import akshare as ak
from mplfinance.original_flavor import candlestick2_ohlc
from matplotlib.ticker import FormatStrFormatter
from typing import Optional
import glog as logger


## ref: https://zhuanlan.zhihu.com/p/18102451465

# 全局样式设置
def set_global_style():
    """设置全局绘图样式和中文字体"""
    plt.style.use("ggplot")
    # 中文字体设置（兼容Windows和Mac）
    if plt.get_backend().startswith('Win'):
        plt.rcParams["font.sans-serif"] = ["SimHei"]
    else:
        plt.rcParams["font.sans-serif"] = ["PingFang HK"]  # Mac系统推荐使用苹方字体
    plt.rcParams["axes.unicode_minus"] = False

def get_stock_data(stock_code: str = "sh601318", type:str ='sh', days: int = 30) -> pd.DataFrame:
    """
    获取股票数据并计算移动平均线
    
    参数:
        stock_code: 股票代码，默认为中国平安
        days: 获取的天数，默认为30天
        
    返回:
        处理后的DataFrame
    """
    try:
        # 获取股票数据
        if type == 'kc':
            stock_data=ak.stock_zh_kcb_daily(symbol=stock_code, adjust="hfq")
        else:
            stock_data = ak.stock_zh_a_daily(symbol=stock_code, adjust="qfq")
        
        # 数据清洗和处理
        df = (
            stock_data
            .reset_index()
            .iloc[-days:, :6]  # 取指定天数数据
            .dropna(how="any")  # 去除空值
            .sort_values(by="date", ascending=True)
            .reset_index(drop=True)
        )
        
        # 计算移动平均线
        df["MA5"] = df.close.rolling(5).mean()
        df["MA10"] = df.close.rolling(10).mean()
        
        # 转换日期格式
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
        
        logger.info("\n{}".format(df.info()))
        logger.info("\n{}".format(df.tail()))
        
        return df
        
    except Exception as e:
        logger.info(f"获取数据失败: {e}")
        return pd.DataFrame()

def draw_kline(
    df: pd.DataFrame, 
    title: str = "中国平安",
    highlight_extremes: bool = True
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
    if df.empty:
        logger.info("空数据，无法绘图")
        return None
    
    try:
        fig, ax = plt.subplots(figsize=(12,5), dpi=150)
        
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
            alpha=0.8
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
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2')
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
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2')
            )
        
        # 绘制移动平均线
        ax.plot(df["MA5"].values, label="5日均线", linewidth=1.5, alpha=0.8, color='darkorange')
        ax.plot(df["MA10"].values, label="10日均线", linewidth=1.5, alpha=0.8, color='purple')
        
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
            loc='upper left'
        )
        
        # 调整布局
        plt.tight_layout()
        
        return fig
        
    except Exception as e:
        logger.info(f"绘图失败: {e}")
        return None
    


def get_all_stock(type:str ="sh"):
    allow_stock=["sh","sz","bj",'cy','kc',"all"]
    assert type in allow_stock,"Invalid type={}, must be one of {}...".format(type,'/'.join(allow_stock))
    import akshare as ak
    # https://akshare.akfamily.xyz/data/stock/stock.html
    stock_zh_a_spot_em_df=None
    try:
        if type=="sh":
            stock_zh_a_spot_em_df = ak.stock_sh_a_spot_em()
        elif type == "sz":
            stock_zh_a_spot_em_df = ak.stock_sz_a_spot_em()
        elif type == 'bj':
            stock_zh_a_spot_em_df = ak.stock_bj_a_spot_em()
        elif type == 'cy':
            stock_zh_a_spot_em_df = ak.stock_cy_a_spot_em()
        elif type == 'kc':
            stock_zh_a_spot_em_df = ak.stock_kc_a_spot_em()
        else:
            stock_zh_a_spot_em_df = ak.stock_zh_a_spot()
            
    except Exception as e:
        logger.info("Error: {} when getting type={}".format(e,type))
        return None

    # logger.info("ret@{}: {}".format(type,stock_zh_a_spot_em_df))
    if stock_zh_a_spot_em_df is None:
        logger.info("WARNING: no data for type={}".format(type))
        return None
    # Print basic info (optional)
    logger.info(f"Fetched {len(stock_zh_a_spot_em_df)} stocks as: {stock_zh_a_spot_em_df[['代码', '名称']].head()}")

    # just return the code and name of stocks
    # Convert to list of tuples (code, name) without index
    stock_list = stock_zh_a_spot_em_df[['代码', '名称']].to_records(index=False).tolist()
    return stock_list

import time
import random
for x in  ['all']:
    while True:
        all_stock = get_all_stock(x)
        if all_stock is not None:
            logger.info("getting {}: {}".format(x,all_stock))
            break
        time.sleep(1)
        time.sleep(random.uniform(1.0, 3.0))
    

if __name__ == "__main__":
    set_global_style()
    
    # 获取数据并绘图
    stock_code = "sh688256"#"sh601318"  # 中国平安
    stock_data = get_stock_data(stock_code=stock_code, days=30)
    
    if not stock_data.empty:
        fig = draw_kline(stock_data, title=f"{stock_code} 寒武纪")
        if fig:
            plt.show()
            pass