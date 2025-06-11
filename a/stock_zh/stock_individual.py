import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import akshare as ak
from mplfinance.original_flavor import candlestick2_ohlc
from matplotlib.ticker import FormatStrFormatter
from typing import Optional
import glog as logger


## ref: https://zhuanlan.zhihu.com/p/18102451465
## ref: https://gitlab.eduxiji.net/githubexcellent/akshare/-/blob/cc6790f5f5c2aa983a60dac3db69948b662578d3/akshare/stock/zh_stock_kcb_sina.py


def get_stock_data(
    stock_code: str = "sh601318", type: str = "sh", days: int = 30
) -> pd.DataFrame:
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
        logger.info(f"type={type}")
        if type == "kc":
            logger.info(f"stock_code={stock_code}")
            stock_data = ak.stock_zh_kcb_daily(symbol=stock_code, adjust="hfq")
            logger.info("done...")
        else:
            stock_data = ak.stock_zh_a_daily(symbol=stock_code, adjust="qfq")

        # 数据清洗和处理
        df = (
            stock_data.reset_index()
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
