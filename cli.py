"""CLI entry point for Binance Futures Testnet Trading Bot."""

import sys

import click
from dotenv import load_dotenv

from trading_bot.bot.client import BinanceTestnetClient
from trading_bot.bot.logging_config import setup_logging
from trading_bot.bot.orders import OrderManager
from trading_bot.bot.validators import ValidationError

load_dotenv()

logger = setup_logging()


@click.group()
@click.version_option(version="1.0.0")
def cli() -> None:
    """Binance Futures Testnet Trading Bot."""
    pass


@cli.command()
@click.option(
    "--symbol",
    "-s",
    required=True,
    help="Trading pair symbol (e.g., BTCUSDT)",
)
@click.option(
    "--side",
    "-S",
    required=True,
    type=click.Choice(["BUY", "SELL"], case_sensitive=False),
    help="Order side: BUY or SELL",
)
@click.option(
    "--order-type",
    "-t",
    required=True,
    type=click.Choice(["MARKET", "LIMIT"], case_sensitive=False),
    help="Order type: MARKET or LIMIT",
)
@click.option(
    "--quantity",
    "-q",
    required=True,
    type=float,
    help="Order quantity",
)
@click.option(
    "--price",
    "-p",
    type=float,
    default=None,
    help="Limit price (required for LIMIT orders)",
)
@click.option(
    "--demo",
    "-d",
    is_flag=True,
    default=False,
    help="Run in demo mode (no real API calls)",
)
def place_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None,
    demo: bool,
) -> None:
    """Place an order on Binance Futures Testnet."""
    try:
        client = BinanceTestnetClient(demo=demo)
        manager = OrderManager(client)
        manager.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )
    except ValidationError as e:
        sys.exit(1)
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


@cli.command()
@click.option(
    "--demo",
    "-d",
    is_flag=True,
    default=False,
    help="Run in demo mode (no real API calls)",
)
def test_connection(demo: bool) -> None:
    """Test connection to Binance Futures Testnet."""
    try:
        client = BinanceTestnetClient(demo=demo)
        if client.test_connection():
            print("Connection successful!")
        else:
            print("Connection failed.")
            sys.exit(1)
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
