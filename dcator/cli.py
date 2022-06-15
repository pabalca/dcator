import click
import collections
from dcator.commands import order, cancel, status, history, wallet, ticker


class OrderedGroup(click.Group):
    """
    https://stackoverflow.com/questions/47972638/how-can-i-define-the-order-of-click-sub-commands-in-help
    """
    def __init__(self, name=None, commands=None, **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return self.commands


@click.group(cls=OrderedGroup, help="Kraken CLI (v1.0.0) @ pabalca")
def cli():
    pass


cli.add_command(status.status)
cli.add_command(order.order)
cli.add_command(cancel.cancel)
cli.add_command(history.history)
cli.add_command(wallet.wallet)
cli.add_command(ticker.ticker)



if __name__ == '__main__':
    cli()
