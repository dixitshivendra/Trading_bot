"""Binance Futures Testnet client wrapper."""

import os
import random
import time
from typing import Optional

from binance.client import Client
from binance.exceptions import BinanceAPIException

from .logging_config import get_logger

logger = get_logger("client")

TESTNET_BASE_URL = "https://testnet.binancefuture.com"


class BinanceTestnetClient:
    """Wrapper around Binance client configured for Futures Testnet."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        demo: bool = False,
    ) -> None:
        """
        Initialize the Binance testnet client.

        Args:
            api_key: Binance API key. Falls back to BINANCE_API_KEY env var.
            api_secret: Binance API secret. Falls back to BINANCE_API_SECRET env var.
            demo: If True, run in demo mode without real API calls.

        Raises:
            ValueError: If API credentials are not provided or found in env.
        """
        self.demo = demo
        self.client = None

        if demo:
            logger.info("Running in DEMO mode (no real API calls)")
            return

        self.api_key = api_key or os.environ.get("BINANCE_API_KEY")
        self.api_secret = api_secret or os.environ.get("BINANCE_API_SECRET")

        if not self.api_key or not self.api_secret:
            raise ValueError(
                "API credentials required. Set BINANCE_API_KEY and BINANCE_API_SECRET "
                "environment variables, or pass them directly."
            )

        self.client = Client(
            api_key=self.api_key,
            api_secret=self.api_secret,
            testnet=True,
        )

        self.client.FUTURES_URL = TESTNET_BASE_URL
        logger.info("Binance Futures Testnet client initialized")

    def _generate_demo_response(
        self, symbol: str, side: str, order_type: str, quantity: float,
        price: Optional[float] = None, stop_price: Optional[float] = None,
    ) -> dict:
        """Generate a simulated order response for demo mode."""
        base_prices = {"BTCUSDT": 50000, "ETHUSDT": 3000, "BNBUSDT": 400}
        base_price = base_prices.get(symbol, 100)
        avg_price = base_price + random.uniform(-100, 100)

        return {
            "orderId": random.randint(100000, 999999),
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "status": "FILLED" if order_type == "MARKET" else "NEW",
            "executedQty": str(quantity) if order_type == "MARKET" else "0",
            "avgPrice": f"{avg_price:.2f}" if order_type == "MARKET" else "0",
            "cumulativeQuoteQty": f"{quantity * avg_price:.2f}" if order_type == "MARKET" else "0",
            "stopPrice": str(stop_price) if stop_price else "0",
            "updateTime": int(time.time() * 1000),
        }

    def place_market_order(
        self, symbol: str, side: str, quantity: float
    ) -> dict:
        """
        Place a market order on Binance Futures Testnet.

        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT).
            side: Order side (BUY or SELL).
            quantity: Order quantity.

        Returns:
            Order response dictionary.
        """
        logger.info(
            "Placing MARKET order: symbol=%s, side=%s, quantity=%s",
            symbol,
            side,
            quantity,
        )

        if self.demo:
            response = self._generate_demo_response(symbol, side, "MARKET", quantity)
            logger.debug("Demo market order response: %s", response)
            return response

        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity,
            )
            logger.debug("Market order response: %s", order)
            return order
        except BinanceAPIException as e:
            logger.error("Binance API error placing market order: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error placing market order: %s", e)
            raise

    def place_limit_order(
        self, symbol: str, side: str, quantity: float, price: float
    ) -> dict:
        """
        Place a limit order on Binance Futures Testnet.

        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT).
            side: Order side (BUY or SELL).
            quantity: Order quantity.
            price: Limit price.

        Returns:
            Order response dictionary.
        """
        logger.info(
            "Placing LIMIT order: symbol=%s, side=%s, quantity=%s, price=%s",
            symbol,
            side,
            quantity,
            price,
        )

        if self.demo:
            response = self._generate_demo_response(symbol, side, "LIMIT", quantity, price)
            response["price"] = str(price)
            logger.debug("Demo limit order response: %s", response)
            return response

        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                timeInForce="GTC",
                quantity=quantity,
                price=price,
            )
            logger.debug("Limit order response: %s", order)
            return order
        except BinanceAPIException as e:
            logger.error("Binance API error placing limit order: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error placing limit order: %s", e)
            raise

    def place_stop_market_order(
        self, symbol: str, side: str, quantity: float, stop_price: float
    ) -> dict:
        """
        Place a stop-market order on Binance Futures Testnet.

        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT).
            side: Order side (BUY or SELL).
            quantity: Order quantity.
            stop_price: Trigger price.

        Returns:
            Order response dictionary.
        """
        logger.info(
            "Placing STOP_MARKET order: symbol=%s, side=%s, quantity=%s, stop_price=%s",
            symbol,
            side,
            quantity,
            stop_price,
        )

        if self.demo:
            response = self._generate_demo_response(
                symbol, side, "STOP_MARKET", quantity, stop_price=stop_price
            )
            logger.debug("Demo stop-market order response: %s", response)
            return response

        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP_MARKET",
                quantity=quantity,
                stopPrice=stop_price,
            )
            logger.debug("Stop-market order response: %s", order)
            return order
        except BinanceAPIException as e:
            logger.error("Binance API error placing stop-market order: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error placing stop-market order: %s", e)
            raise

    def place_stop_limit_order(
        self, symbol: str, side: str, quantity: float, price: float, stop_price: float
    ) -> dict:
        """
        Place a stop-limit order on Binance Futures Testnet.

        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT).
            side: Order side (BUY or SELL).
            quantity: Order quantity.
            price: Limit price after trigger.
            stop_price: Trigger price.

        Returns:
            Order response dictionary.
        """
        logger.info(
            "Placing STOP_LIMIT order: symbol=%s, side=%s, quantity=%s, price=%s, stop_price=%s",
            symbol,
            side,
            quantity,
            price,
            stop_price,
        )

        if self.demo:
            response = self._generate_demo_response(
                symbol, side, "STOP_LIMIT", quantity, price, stop_price
            )
            response["price"] = str(price)
            logger.debug("Demo stop-limit order response: %s", response)
            return response

        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP_LIMIT",
                timeInForce="GTC",
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
            )
            logger.debug("Stop-limit order response: %s", order)
            return order
        except BinanceAPIException as e:
            logger.error("Binance API error placing stop-limit order: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error placing stop-limit order: %s", e)
            raise

    def test_connection(self) -> bool:
        """
        Test connection to Binance Futures Testnet.

        Returns:
            True if connection is successful.
        """
        if self.demo:
            logger.info("Demo mode: connection test passed (simulated)")
            return True

        try:
            self.client.futures_ping()
            logger.info("Successfully connected to Binance Futures Testnet")
            return True
        except Exception as e:
            logger.error("Failed to connect to testnet: %s", e)
            return False
