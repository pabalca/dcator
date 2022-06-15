import click
from datetime import datetime
from collections import defaultdict

from dcator.utils import KrakenAPI
from dcator.logger import logger


@click.command(context_settings={"show_default": True})
@click.option("--ticker", "-t", type=str, default="XBT")
@click.option("--deposit", "-d", is_flag=True)
@click.option("--withdraw", "-w", is_flag=True)
@click.option("--value", "-v", type=str)
def wallet(ticker, deposit, withdraw, value):

    ticker = ticker.upper()

    if ticker == "XBT":
        method = "Bitcoin"
        address = "cold"
    elif ticker == "EUR":
        method = "Clear Junction (SEPA)"
        address = "ABN INSTANT"
    else:
        logger.error(f"Asset {ticker} is not supported.")
        return

    api = KrakenAPI()

    if deposit:
        r = api.query("DepositAddresses", {"asset": ticker, "method": method})
        address = r[0]["address"]
        logger.info(f"{method} = {address}")
    elif withdraw:
        r = api.query("Withdraw", {"asset": ticker, "key": address, "amount": value})
        logger.info(f"{r}")
    else:
        movements = defaultdict(dict)

        r = api.query("WithdrawStatus", {"asset": ticker})
        for transfer in r:
            status = transfer["status"]
            amount = float(transfer["amount"])
            time = datetime.fromtimestamp(transfer["time"])
            movements[time]["amount"] = -1 * amount
            movements[time]["status"] = status

        r = api.query("DepositStatus", {"asset": ticker})
        for transfer in r:
            status = transfer["status"]
            amount = float(transfer["amount"])
            time = datetime.fromtimestamp(transfer["time"])
            movements[time]["amount"] = amount
            movements[time]["status"] = status

        for timestamp, movement in sorted(movements.items(), reverse=True):
            logger.info(
                f"{timestamp} {str(round(movement['amount'], 1)).rjust(10, ' ')} {ticker} = {movement['status']}"
            )
