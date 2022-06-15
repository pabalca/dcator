# Kraken CLI to interact with the exchange.

```
 $ kraken
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

  Kraken CLI (v1.0.0) @ pabalca

Options:
  --help  Show this message and exit.

Commands:
  status
  order
  cancel
  history
  deposit
```

Installation.
```
python3 -m virtualenv venv
source venv/bin/activate
pip install -e .
```

How to run periodic commands using crontab.
```
# DCA Bitcoin buys
0 * * * * python3 /home/umbrel/dcator/dcator/cli.py order -v 4 -x --max_price 30000 
```

Examples:
```
# Place market buy of 5 euros.
kraken order -s buy -v 5 -x

# Place limit order
kraken order -s buy -v 5 -l2000

# Insert order at 200 week moving average.
kraken order -s buy -v 5 -w200
```
