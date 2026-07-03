"""Order placement logic for trading bot."""

from typing import Optional

from binance.exceptions import BinanceAPIException

from .client import BinanceTestnetClient
from .logging_config import get_logger
from .validators import ValidationError, validate_order_input

logger = get_logger("orders")


class OrderManager:
    """Manages order placement and formatting on Binance Futures Testnet."""

    def __init__(self, client: BinanceTestnetClient) -> None:
        """
        Initialize OrderManager with a Binance client.

        Args:
            client: Initialized BinanceTestnetClient instance.
        """
        self.client = client
        logger.info("OrderManager initialized")

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
    ) -> dict:
        """
        Place an order with validation and error handling.

        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT).
            side: Order side (BUY or SELL).
            order_type: Order type (MARKET or LIMIT).
            quantity: Order quantity.
            price: Limit price (required for LIMIT orders).

        Returns:
            Formatted order response dictionary.
        """
        try:
            validated = validate_order_input(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
            )

            self._print_request_summary(validated)

            if validated["order_type"] == "MARKET":
                response = self.client.place_market_order(
                    symbol=validated["symbol"],
                    side=validated["side"],
                    quantity=validated["quantity"],
                )
            else:
                response = self.client.place_limit_order(
                    symbol=validated["symbol"],
                    side=validated["side"],
                    quantity=validated["quantity"],
                    price=validated["price"],
                )

            formatted = self._format_response(response)
            self._print_response(formatted)

            logger.info(
                "Order placed successfully: orderId=%s, status=%s",
                formatted["orderId"],
                formatted["status"],
            )
            return formatted

        except ValidationError as e:
            logger.error("Validation error: %s", e)
            print(f"\nValidation Error: {e}")
            raise

        except BinanceAPIException as e:
            logger.error("Binance API error: %s", e)
            print(f"\nBinance API Error: {e.status_code} - {e.message}")
            raise

        except Exception as e:
            logger.error("Unexpected error placing order: %s", e)
            print(f"\nError: {e}")
            raise

    def _print_request_summary(self, validated: dict) -> None:
        """Print formatted order request summary."""
        print("\n" + "=" * 50)
        print("Order Request Summary:")
        print("=" * 50)
        print(f"  Symbol:     {validated['symbol']}")
        print(f"  Side:       {validated['side']}")
        print(f"  Type:       {validated['order_type']}")
        print(f"  Quantity:   {validated['quantity']}")
        if validated["price"] is not None:
            print(f"  Price:      {validated['price']}")
        print("=" * 50)

    def _format_response(self, response: dict) -> dict:
        """Format raw API response into clean structure."""
        return {
            "orderId": response.get("orderId"),
            "symbol": response.get("symbol"),
            "side": response.get("side"),
            "type": response.get("type"),
            "status": response.get("status"),
            "executedQty": response.get("executedQty", "0"),
            "avgPrice": response.get("avgPrice", "N/A"),
            "cumulativeQuoteQty": response.get("cumulativeQuoteQty", "N/A"),
            "time": response.get("updateTime") or response.get("time"),
        }

    def _print_response(self, formatted: dict) -> None:
        """Print formatted order response."""
        print("\n" + "=" * 50)
        print("Order Response:")
        print("=" * 50)
        print(f"  Order ID:       {formatted['orderId']}")
        print(f"  Symbol:         {formatted['symbol']}")
        print(f"  Status:         {formatted['status']}")
        print(f"  Executed Qty:   {formatted['executedQty']}")
        print(f"  Avg Price:      {formatted['avgPrice']}")
        print(f"  Cumulative:     {formatted['cumulativeQuoteQty']}")
        print("=" * 50)

        if formatted["status"] == "FILLED":
            print("\nOrder placed successfully!")
        elif formatted["status"] == "NEW":
            print("\nLimit order placed and waiting to be filled!")
        else:
            print(f"\nOrder status: {formatted['status']}")
