"""Input validation for trading bot."""

import re
from typing import Optional

from .logging_config import get_logger

logger = get_logger("validators")

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET", "STOP_LIMIT"}
SYMBOL_PATTERN = re.compile(r"^[A-Z0-9]{5,20}$")


class ValidationError(Exception):
    """Raised when input validation fails."""


def validate_symbol(symbol: str) -> str:
    """
    Validate trading pair symbol format.

    Args:
        symbol: Trading pair symbol to validate.

    Returns:
        Validated uppercase symbol.

    Raises:
        ValidationError: If symbol format is invalid.
    """
    symbol = symbol.upper().strip()
    if not SYMBOL_PATTERN.match(symbol):
        raise ValidationError(
            f"Invalid symbol format: '{symbol}'. "
            "Expected 5-20 uppercase alphanumeric characters (e.g., BTCUSDT)."
        )
    logger.debug("Symbol validated: %s", symbol)
    return symbol


def validate_side(side: str) -> str:
    """
    Validate order side.

    Args:
        side: Order side to validate.

    Returns:
        Validated uppercase side.

    Raises:
        ValidationError: If side is not BUY or SELL.
    """
    side = side.upper().strip()
    if side not in VALID_SIDES:
        raise ValidationError(
            f"Invalid side: '{side}'. Must be one of: {', '.join(sorted(VALID_SIDES))}"
        )
    logger.debug("Side validated: %s", side)
    return side


def validate_order_type(order_type: str) -> str:
    """
    Validate order type.

    Args:
        order_type: Order type to validate.

    Returns:
        Validated uppercase order type.

    Raises:
        ValidationError: If order type is not supported.
    """
    order_type = order_type.upper().strip()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type: '{order_type}'. "
            "Must be one of: {', '.join(sorted(VALID_ORDER_TYPES))}"
        )
    logger.debug("Order type validated: %s", order_type)
    return order_type


def validate_quantity(quantity: float) -> float:
    """
    Validate order quantity.

    Args:
        quantity: Order quantity to validate.

    Returns:
        Validated quantity.

    Raises:
        ValidationError: If quantity is not positive.
    """
    if quantity <= 0:
        raise ValidationError(
            f"Invalid quantity: {quantity}. Must be a positive number."
        )
    logger.debug("Quantity validated: %s", quantity)
    return quantity


def validate_stop_price(stop_price: Optional[float]) -> Optional[float]:
    """
    Validate stop price (required for STOP orders).

    Args:
        stop_price: Stop price to validate.

    Returns:
        Validated stop price or None.

    Raises:
        ValidationError: If stop price is not positive.
    """
    if stop_price is None:
        return None
    if stop_price <= 0:
        raise ValidationError(
            f"Invalid stop price: {stop_price}. Must be a positive number."
        )
    logger.debug("Stop price validated: %s", stop_price)
    return stop_price


def validate_price(price: Optional[float]) -> Optional[float]:
    """
    Validate order price (required for LIMIT orders).

    Args:
        price: Order price to validate.

    Returns:
        Validated price or None.

    Raises:
        ValidationError: If price is not positive.
    """
    if price is None:
        return None
    if price <= 0:
        raise ValidationError(
            f"Invalid price: {price}. Must be a positive number."
        )
    logger.debug("Price validated: %s", price)
    return price


def validate_order_input(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
    stop_price: Optional[float] = None,
) -> dict:
    """
    Validate all order inputs and return validated values.

    Args:
        symbol: Trading pair symbol.
        side: Order side (BUY/SELL).
        order_type: Order type (MARKET/LIMIT/STOP_MARKET/STOP_LIMIT).
        quantity: Order quantity.
        price: Limit price (required for LIMIT orders).
        stop_price: Stop price (required for STOP orders).

    Returns:
        Dictionary with validated inputs.

    Raises:
        ValidationError: If any validation fails.
    """
    logger.info(
        "Validating order input: symbol=%s, side=%s, type=%s, qty=%s, price=%s, stop_price=%s",
        symbol,
        side,
        order_type,
        quantity,
        price,
        stop_price,
    )

    validated_symbol = validate_symbol(symbol)
    validated_side = validate_side(side)
    validated_type = validate_order_type(order_type)
    validated_quantity = validate_quantity(quantity)
    validated_price = validate_price(price)
    validated_stop_price = validate_stop_price(stop_price)

    if validated_type == "LIMIT" and validated_price is None:
        raise ValidationError("Price is required for LIMIT orders.")

    if validated_type == "STOP_LIMIT" and validated_price is None:
        raise ValidationError("Price is required for STOP_LIMIT orders.")

    if validated_type in ("STOP_MARKET", "STOP_LIMIT") and validated_stop_price is None:
        raise ValidationError("Stop price is required for STOP orders.")

    result = {
        "symbol": validated_symbol,
        "side": validated_side,
        "order_type": validated_type,
        "quantity": validated_quantity,
        "price": validated_price,
        "stop_price": validated_stop_price,
    }

    logger.info("All inputs validated successfully")
    return result
