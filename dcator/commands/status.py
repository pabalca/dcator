import click

from dcator.utils import KrakenAPI, moving_average, medium_price, Color
from dcator.logger import logger


@click.command(context_settings={"show_default": True})
def status():
    api = KrakenAPI()

    balance = api.query("Balance")
    cash = round(float(balance["ZEUR"]))
    btc = round(float(balance["XXBT"]), 6)

    price = round(float(medium_price(api, "XXBTZUSD")))
    price_eur = medium_price(api, "XXBTZEUR")

    total = round(float(cash) + float(btc) * price_eur)

    logger.info(f"{Color.GREEN}{Color.BOLD}BTC = {price_eur} EUR{Color.END}")

    logger.info(
        f"{Color.BOLD}BALANCE = {total} EUR{Color.END}  => {Color.BLUE} {cash} EUR ({round(100*cash/total)}%){Color.END}{Color.ORANGE} {btc} BTC ({round(100*(btc*price_eur)/total)}%) {Color.END}"
    )

    open_orders = api.query("OpenOrders")
    if open_orders["open"]:
        for order in open_orders["open"].items():
            orderid = order[0]
            descr = order[1]["descr"]["order"]
            logger.info(f"{Color.YELLOW}{descr} {Color.END}")
    else:
        logger.info(f"{Color.YELLOW}No open orders.{Color.END}")

    # logger.info(f"4 EUR/HOUR = {round(total/96)} days")

