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
    stock_code: str = "sh601318", market: str = "sh", days: int = 30
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
        logger.info(f"type={market}")
        if market == "kc":
            logger.info(f"stock_code={stock_code}")
            stock_data = ak.stock_zh_kcb_daily(symbol=stock_code, adjust="hfq")
            logger.info("done...")
        else:
            stock_data = ak.stock_zh_a_daily(symbol=stock_code, adjust="qfq")

        from datetime import datetime, timezone, timedelta
        import pytz

        # Get today's date (naive)
        today_naive = datetime.today()
        # Assign UTC timezone first
        today_utc = today_naive.replace(tzinfo=timezone.utc)
        # Convert to Asia/Shanghai
        shanghai_tz = pytz.timezone("Asia/Shanghai")
        today_shanghai = today_naive  # today_utc.astimezone(shanghai_tz)
        formatted_date = today_shanghai.strftime("%Y-%m-%d")
        today = formatted_date
        yesterday = today_shanghai - timedelta(days=1)  # 计算昨天

        # 数据清洗和处理
        df = (
            stock_data.reset_index()
            .iloc[-days:, :6]  # 取指定天数数据
            .dropna(how="any")  # 去除空值
            # .query("date != @today")  # 排除今天的数据
            .sort_values(by="date", ascending=True)
            .reset_index(drop=True)
        )

        # 计算移动平均线
        df["MA5"] = df.close.rolling(5).mean()
        df["MA10"] = df.close.rolling(10).mean()

        # 转换日期格式
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
        import os

        if int(os.environ.get("REMOVE_TODAY", 0)):
            # Filter out today and invalid dates
            today = datetime.now().date()
            logger.info(f"Removing today's data: {today}")
            df = df[df["date"].dt.date != today].dropna(subset=["date"])

        # np_data = df.to_numpy()
        np_data = df[["open", "high", "low", "close"]].to_numpy()

        def is_continue_desc(data, max_depth):
            if len(data) < max_depth:
                return False
            for x in range(max_depth):
                current_line = data[-1 - x]
                open_idx, high_idx, low_idx, close_idx = 0, 1, 2, 3
                if current_line[open_idx] < current_line[close_idx]:
                    return False
            return True
            pass

        result = is_continue_desc(np_data, 4)

        logger.info("\n{}".format(df.info()))
        logger.info("\n{}".format(df.tail()))
        logger.info(f"\nnp_data: \n{np_data}")
        logger.info(
            "\n today: {} stock_code={} is matched? {}".format(
                today, stock_code, result
            )
        )
        if result is True:
            with open("abc.txt", "a+") as f:
                f.writelines(f"stock_code: {stock_code}\n")

        return df

    except Exception as e:
        logger.info(f"获取{stock_code}数据失败: {e}")
        return pd.DataFrame()
