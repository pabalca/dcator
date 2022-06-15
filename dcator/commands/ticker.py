import click

from dcator.utils import KrakenAPI, moving_average, medium_price, Color
from dcator.logger import logger


@click.command(context_settings={"show_default": True})
def ticker():
    api = KrakenAPI()

    price = round(float(medium_price(api, "XXBTZUSD")))
    logger.info(Color.GREEN + Color.BOLD + f"1 BTC = {price} USD" + Color.END)
