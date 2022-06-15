import click

from dcator.utils import KrakenAPI
from dcator.logger import logger


@click.command(no_args_is_help=True, context_settings={'show_default': True})
@click.option("--execute", "-x", is_flag=True)
@click.option("-t", "--txid", type=str, required=False)
def cancel(execute, txid):

    api = KrakenAPI()

    if txid:
        orders = api.query("CancelOrder", {"txid": txid})
    elif execute:
        orders = api.query("CancelAll")

    orders_cancelled = orders["count"]
    logger.info(f"{orders_cancelled} orders were cancelled")
