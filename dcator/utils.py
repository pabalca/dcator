import datetime
import sys
import krakenex
import os

from dcator.logger import logger


PRIVATE_METHODS = {"AddOrder", "CancelAll", "CancelOrder", "Balance",
                   "OpenOrders", "ClosedOrders", "DepositAddresses",
                   "DepositStatus", "WithdrawInfo", "WithdrawStatus",
                   "Withdraw"}
PUBLIC_METHODS = {"Balance", "Depth", "Time", "SystemStatus", "OHLC"}


class KrakenAPI:
    def __init__(self):
        self.api = krakenex.API()
        self.load_key()

    def load_key(self, path=os.environ.get('KRAKEN_API_FILE')):
        with open(path, "r") as f:
            self.api.key = f.readline().strip()
            self.api.secret = f.readline().strip()

    def query(self, method, data=None):
        if data is None:
            data = {}
        try:
            if method in PRIVATE_METHODS:
                r = self.api.query_private(method, data)
            elif method in PUBLIC_METHODS:
                r = self.api.query_public(method, data)
            else:
                logger.error(f"Unsupported method: {method}")
                sys.exit(1)
        except Exception as error:
            logger.error(error)
            sys.exit(1)

        if len(r["error"]) > 0:
            logger.error(r["error"])
            sys.exit(1)

        return r["result"]


def moving_average(api, ticker, n):
    from_date = (
        datetime.datetime.now()
        - datetime.timedelta(weeks=300)
        - datetime.datetime(1970, 1, 1)
    )
    unix = int(from_date.total_seconds())

    r = api.query("OHLC", {"pair": ticker, "interval": 10080, "since": unix})

    closes = [float(ohlc[4]) for ohlc in r[ticker]]
    days = closes[len(closes) - n - 1: len(closes) - 1]
    average = int(sum(days) / len(days))

    return average


def medium_price(api, ticker):
    r = api.query(
        "Depth",
        {
            "pair": ticker,
            "count": 1
        }
    )

    ob = r[ticker]
    price = (float(ob["asks"][0][0]) + float(ob["bids"][0][0])) / 2

    return price


class Color:
    WHITE = '\033[80m'
    GRAY = '\033[37m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ORANGE = '\033[33m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
