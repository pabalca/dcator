import click
from itertools import islice

from dcator.utils import KrakenAPI
from dcator.utils import Color
from dcator.logger import logger

from datetime import datetime, timedelta
import pytz


@click.command(context_settings={"show_default": True})
@click.option("-l", "--length", type=int, default=10)
def history(length):

    api = KrakenAPI()

    closed_orders = api.query("ClosedOrders")["closed"]
    for order in islice(closed_orders.items(), length):
        # orderid = order[0]
        status = order[1]["status"]
        cost = order[1]["cost"]
        fee = order[1]["fee"]
        price = order[1]["price"]
        vol_exec = order[1]["vol_exec"]
        side = order[1]["descr"]["type"]
        pair = order[1]["descr"]["pair"]
        close_unix = order[1]["closetm"]

        datetime_obj = datetime.utcfromtimestamp(int(close_unix)) + timedelta(hours=2)
        close_time = datetime_obj.strftime("%d.%m.%y %H:%M:%S")

        message = Color.WHITE + f"[{close_time}]" + Color.END
        text = f" {side} {pair} vol={vol_exec} price={price} cost={cost} fee={fee}"

        if status == "canceled":
            message += Color.GRAY + text + Color.END
        elif side == "buy":
            message += Color.GREEN + text + Color.END
        elif side == "sell":
            message += Color.RED + text + Color.END

        logger.info(message)

