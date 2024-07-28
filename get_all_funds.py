import requests
import pandas as pd
import re

# ref : https://blog.csdn.net/small__roc/article/details/126871221


def GetAllFund():
    """
    功能：获取所有基金名称、代码、类型，天天基金数据接口：http://fund.eastmoney.com/js/fundcode_search.js
    传入：无
    返回：所有基金基础数据
    """
    url = "http://fund.eastmoney.com/js/fundcode_search.js"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    }
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    list_ = eval(re.findall(r"\[.*\]", res.text)[0])
    df = pd.DataFrame(list_)
    df.columns = ["基金代码", "基金拼音简写", "基金名称", "基金类型", "基金拼音全称"]

    return df


if __name__ == "__main__":
    funds = GetAllFund()
    print(funds)
