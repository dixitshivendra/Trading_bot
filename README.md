# Binance Futures Testnet Trading Bot

A simplified Python trading bot for placing orders on Binance Futures Testnet (USDT-M).

## Features

- Place MARKET and LIMIT orders
- Support for BUY and SELL sides
- Input validation with clear error messages
- Structured logging to file and console
- Clean CLI interface with Click

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Credentials

Set environment variables:

```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"
```

Or create a `.env` file:

```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

### 4. Get Testnet Credentials

1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Register and activate an account
3. Generate API credentials in the API section

## Usage

### Test Connection

```bash
python cli.py test-connection
```

### Place a Market Order

```bash
python cli.py place-order --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### Place a Limit Order

```bash
python cli.py place-order --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 50000
```

### Using Short Options

```bash
python cli.py place-order -s BTCUSDT -S BUY -t MARKET -q 0.001
python cli.py place-order -s BTCUSDT -S SELL -t LIMIT -q 0.001 -p 50000
```

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py        # Binance client wrapper
│   ├── orders.py        # Order placement logic
│   ├── validators.py    # Input validation
│   └── logging_config.py
├── __init__.py
├── cli.py               # CLI entry point
└── README.md
```

## Logging

- Console output: INFO level
- File output: `trading_bot.log` (DEBUG level)

## Error Handling

- **ValidationError**: Invalid input parameters
- **BinanceAPIException**: API errors from Binance
- **ValueError**: Missing API credentials
- **NetworkError**: Connection issues

## License

