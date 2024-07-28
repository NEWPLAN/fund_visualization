import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from functools import partial


def Get_html(fund_code, start_date, end_date, type_="lsjz", page=1, per=20):
    """
    获取基金网页数据
    """
    url = "http://fund.eastmoney.com/f10/F10DataApi.aspx?type={}&code={}&page={}&sdate={}&edate={}&per={}".format(
        type_, fund_code, page, start_date, end_date, per
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    }
    HTML = requests.get(url, headers=headers)
    HTML.encoding = "utf-8"

    return HTML


def Get_pages(HTML):
    """
    获取最大页数
    """
    pages = re.findall(r"pages:(.*),", HTML.text)[0]

    return int(pages)


def Get_FundData_history(HTML):
    """
    通过html获取基金历史数据
    """
    soup = BeautifulSoup(HTML.text, "html.parser")
    trs = soup.find_all("tr")
    res = []
    for tr in trs[1:]:
        date = tr.find_all("td")[0].text  # 净值日期
        unit_net = tr.find_all("td")[1].text  # 单位净值
        acc_net = tr.find_all("td")[2].text  # 累计净值
        fund_r = tr.find_all("td")[3].text  # 日增长率
        buy_status = tr.find_all("td")[4].text  # 申购状态
        sell_status = tr.find_all("td")[5].text  # 赎回状态
        res.append([date, unit_net, acc_net, fund_r, buy_status, sell_status])
    df = pd.DataFrame(
        res,
        columns=[
            "净值日期",
            "单位净值",
            "累计净值",
            "日增长率",
            "申购状态",
            "赎回状态",
        ],
    )

    return df


def Get_FundData_main(fund_code, start_date, end_date):
    """
    获取基金数据主函数（仅支持单基金）
    """
    html = Get_html(fund_code, start_date, end_date)
    pages = Get_pages(html)
    res_df = pd.DataFrame()
    for page in range(1, pages + 1):
        html = Get_html(fund_code, start_date, end_date, "lsjz", page)
        df_ = Get_FundData_history(html)
        res_df = pd.concat([res_df, df_])

    res_df.insert(0, "基金代码", fund_code)

    return res_df


if __name__ == "__main__":
    start_date = "2022-09-01"
    end_date = "2022-09-15"
    codes = ["320007", "161725", "012723", "970210", "007195"]  # 基金代码列表
    fund_df = pd.concat(
        list(
            map(
                partial(Get_FundData_main, start_date=start_date, end_date=end_date),
                codes,
            )
        )
    )  # 结合map方法获取多基金数据
    print(fund_df)
