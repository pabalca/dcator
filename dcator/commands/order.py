import click

from dcator.utils import KrakenAPI
from dcator.utils import moving_average, medium_price
from dcator.logger import logger


@click.command(no_args_is_help=True, context_settings={'show_default': True})
@click.option("--ticker", "-t", type=str, default="XXBTZEUR")
@click.option("--side", "-s", type=click.Choice(["buy", "sell"]), default="buy")
@click.option("--value", "-v", type=float, required=True)
@click.option("--price", "-p", type=float, required=False)
@click.option("--execute", "-x", is_flag=True)
@click.option("--max_price", default=100000)
@click.option("--weekly", "-w", type=int)
@click.option("--down", "-d", type=int)
def order(ticker, side, value, price, execute, max_price, weekly, down):

    api = KrakenAPI()

    # Calculate order type and assign a price.
    if price:
        price = price
    elif weekly:
        price = moving_average(api, ticker, weekly)
    elif down:
        price = (100-down) * medium_price(api, ticker) / 100
    else:
        price = medium_price(api, ticker)

    # Check limits.
    if price > max_price:
        logger.info(
            f"Current price > max_price ({price} > {max_price}). Not buying."
        )

    # Send order.
    o = api.query(
        "AddOrder",
        {
            "pair": ticker,
            "type": side,
            "ordertype": "market" if execute else "limit",
            "price": round(price, 1),
            "volume": value / price,
        },
    )

    # Log results.
    txid = o["txid"][0]
    descr = o["descr"]["order"]
    logger.info(f"Order {txid} = {descr} {price}")
