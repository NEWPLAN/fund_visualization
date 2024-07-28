import re
import json
import requests
import pandas as pd


def GetFundInfoNow(FundCode):
    """
    功能：获取基金实时信息，天天基金数据接口：http://fundgz.1234567.com.cn/js/基金代码.js
    传入：基金代码
    输出：基金实时信息 --> dict
            fundcode -- 基金代码
            name     -- 基金名称
            jzrqv    -- 上一交易日
            dwjz     -- 基金净值（截止上一交易日）
            gsz      -- 估算净值（实时）
            gszzl    -- 估算涨幅（实时）
            gztime   -- 更新时间（实时）
    """
    url = "http://fundgz.1234567.com.cn/js/%s.js" % FundCode
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    }
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    js_data = json.loads(re.findall(r"jsonpgz\((.*)\)", res.text)[0])  # 正则匹配

    return js_data


if __name__ == "__main__":
    codes = ["320007", "161725", "012723", "007195"]  # 基金代码列表
    res_df = pd.DataFrame(list(map(GetFundInfoNow, codes)))
    print(res_df)
