import sys

sys.dont_write_bytecode = True
from stock_individual import get_stock_data
from stock_meta import get_all_stock
from stock_plot import set_global_style, draw_kline
import matplotlib.pyplot as plt
import glog as logger

# 1. get meta data of stocks
# 2. plot 30days for a given stocks


# return a list, the first is a symbol and the secnd is
def safe_fetch_meta(type: list):
    all_stock = None
    import time
    import random

    for x in type:
        while True:
            all_stock = get_all_stock(x)
            if all_stock is not None:
                logger.info("getting {}: {}".format(x, all_stock))
                return all_stock
                break
            time.sleep(1)
            time.sleep(random.uniform(1.0, 3.0))
    raise "non-data"


def safe_feta_individual(symbol, market="sh"):
    result = get_stock_data(stock_code=symbol, market=market, days=30)
    logger.info("stock_line: {}".format(len(result)))
    if result is None:
        raise "failed to fetch {symbol}"
    return result
    pass


def main():
    # import ipdb

    # ipdb.set_trace()
    marketing = "sz"
    meta_info = safe_fetch_meta([marketing])
    set_global_style()
    for stock_code, info in meta_info:
        stock_code = marketing + stock_code
        stock_data = safe_feta_individual(symbol=stock_code, market=marketing)
        continue
        if len(stock_data) == 1:
            logger.warn("stock_code is empty: {}|{}".format(stock_code, info))
            continue
        if not stock_data.empty:
            fig = draw_kline(stock_data, title=f"{stock_code}｜{info}")
            if fig:
                plt.show()
                pass


if __name__ == "__main__":
    main()
    pass
