import akshare as ak
import pandas as pd
import sys

# https://blog.csdn.net/2301_77602702/article/details/133816149?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-1-133816149-blog-130668325.235%5Ev43%5Epc_blog_bottom_relevance_base8&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-1-133816149-blog-130668325.235%5Ev43%5Epc_blog_bottom_relevance_base8&utm_relevant_index=2

data = pd.DataFrame()

# symbol = sys.argv[1]
symbol = "000004"
print(f"{symbol}回测开始")

# df = ak.stock_zh_a_hist(
#     symbol=symbol,
#     period="daily",
#     start_date="20000101",
#     end_date="20500101",
#     adjust="qfq",
# )
# # df.to_excel(f'{symbol}.xlsx', index=False)
# print(df)


import pandas as pd
import numpy as np


def ema(data, n):
    # df[f'ema_{n}'] = np.nan
    ema_values = []
    for i in range(len(data)):
        if i == 0 or pd.isnull(data[i - 1]):  # 去掉第一个格子，或上一个格子是空白的格子
            # df.loc[i, f'ema_{n}'] = df.loc[i, column]
            ema_values.append(data[i])  # 直接加入列表
        else:
            # df.loc[i, f'ema_{n}'] = (2 * df.loc[i, column] + (n-1) * df.loc[i-1, f'ema_{n}'])/(n+1)
            ema_values.append(
                (2 * data[i] + (n - 1) * ema_values[i - 1]) / (n + 1)
            )  # #EMA的基础公式：EMA = 前一日EMA x (N-1)/(N+1) + 当日收盘价 x 2/(N+1)
    return ema_values


def mike(df, data_type="d"):  # 主函数，在DataFrame上以增加列的方式保存过程中间的变量
    HIGH = df["最高"]
    LOW = df["最低"]
    CLOSE = df["收盘"]
    df["data1"] = (HIGH + LOW + CLOSE) / 3
    df["HLC"] = ema(df["data1"].values, 10)
    df["HLC"] = df["HLC"].shift(1)
    df.fillna(0)
    df["HHV(HIGH,10)"] = HIGH.rolling(
        10, min_periods=1
    ).max()  # 一段时间最高价翻译过来是这样子
    df["LLV(LOW,10)"] = LOW.rolling(10, min_periods=1).min()  # 如上
    df["HV"] = ema(df["HHV(HIGH,10)"].values, 3)
    df["LV"] = ema(df["LLV(LOW,10)"].values, 3)
    df["HLC*2-LV"] = df["HLC"] * 2 - df["LV"]
    df["WEKR"] = ema(df["HLC*2-LV"].values, 8)
    df["zfyq"] = df["涨跌幅"] - 7
    df["zfyq"] = df["zfyq"].apply(
        lambda x: True if x >= 0 else False
    )  # +-数值转成布林值
    df["WEKR>O"] = df["WEKR"] - df["开盘"]
    df["WEKR>O"] = df["WEKR>O"].apply(lambda x: True if x >= 0 else False)
    df["C>WEKR"] = df["收盘"] - df["WEKR"]
    # df.fillna(0)
    df["C>WEKR"] = df["C>WEKR"].apply(lambda x: True if x >= 0 else False)
    df["On-1<WEKR"] = df["WEKR"] - df["收盘"].shift(1)
    df["On-1<WEKR"] = df["On-1<WEKR"].apply(lambda x: True if x >= 0 else False)
    tj1 = df.filter(items=["WEKR>O", "On-1<WEKR"]).any(axis=1)
    tj2 = df["zfyq"]
    tj3 = df["C>WEKR"]
    if data_type == "d":
        df["冲不冲"] = tj1 & tj2 & tj3
    elif data_type == "m":
        df["冲不冲"] = tj1 & tj3
    else:
        sys.exit()
    df.drop(
        [
            "data1",
            "HLC",
            "HHV(HIGH,10)",
            "LLV(LOW,10)",
            "HV",
            "LV",
            "HLC*2-LV",
            "WEKR>O",
            "C>WEKR",
            "On-1<WEKR",
        ],
        axis=1,
        inplace=True,
    )  # 最后把没用的过程变量去掉


df_monthly = ak.stock_zh_a_hist(
    symbol=symbol,
    period="monthly",
    start_date="20000101",
    end_date="20500101",
    adjust="qfq",
)
mike(df_monthly, "d")
df_monthly["日期"] = pd.to_datetime(df_monthly["日期"])
# df_monthly.to_excel(f'{symbol}.xlsx', index=False)
print(df_monthly)


import sys

rows = df_monthly[df_monthly["冲不冲"] == True].copy()
if rows.size == 0:
    print(f"获得{symbol}回测数据完成，共出现{rows.shape[0]}个信号\n", end="")
    sys.exit(0)
rows.reset_index(inplace=True)
print(rows)


monthly_data = pd.DataFrame(index=range(len(rows)), columns=rows.columns)
monthly_data["日期"] = rows["日期"]
monthly_data.drop(columns=["index"], inplace=True)

# i=2
for i in range(len(rows)):
    the_day = rows.loc[i]
    group = df[df["日期范围"] == the_day["日期范围"]]
    group = group[group["日期"] <= the_day["日期"]]
    group.reset_index(inplace=True)
    if group.size > 0:
        monthly_data.loc[i, "开盘"] = group.head(1)["开盘"].values
        monthly_data.loc[i, "收盘"] = group.tail(1)["收盘"].values
        monthly_data.loc[i, "最高"] = group["最高"].max()
        monthly_data.loc[i, "最低"] = group["最低"].min()
        divisor = df_monthly[df_monthly["日期"] < the_day["日期"]].tail(1)["收盘"]
        if divisor.size > 0 and divisor.values != 0:
            monthly_data.loc[i, "涨跌幅"] = (
                group.tail(1)["收盘"].values / divisor.values - 1
            ) * 100
            monthly_data.loc[i, "涨跌幅"] = monthly_data.loc[i, "涨跌幅"].round(2)
            # monthly_match.loc[i, '上月月线WEKR'] = df_monthly[df_monthly['日期'] < the_day['日期']].tail(1)['WEKR'].values
        # 计算月WEKR,需要将本月月线数据并入股票月线数据表并计算WEKR
        # 日期前所有月线
        df_before_date = df_monthly[df_monthly["日期"] < the_day["日期"]].copy()
        df_insert = pd.DataFrame(monthly_data.loc[i]).transpose()  # 计算出的月线数据
        df_insert.dropna(axis=1, inplace=True)
        if df_insert.size > 0:
            df_before_date = pd.concat(
                [df_before_date, df_insert], axis=0
            )  # 并入本月以前的月线数据
        mike(df_before_date)
        rows.loc[i, "日月穿"] = df_before_date.tail(1)["冲不冲"].values
df_insert.dropna(axis=1)

rows_ryc = rows[rows["日月穿"] == True].copy()
if rows_ryc.size == 0:
    print(f"获得{symbol}回测数据完成，共出现{rows_ryc.shape[0]}个信号\n", end="")
rows_ryc.size
