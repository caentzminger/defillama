# DefiLlama Python Client

A Python client for the DefiLlama API with full type safety and Pydantic validation. Supports both synchronous and asynchronous operations.

## Features

- **Full API Coverage**: All DefiLlama API endpoints are supported
- **Type Safety**: Complete type hints and Pydantic model validation
- **Async Support**: Both synchronous and asynchronous methods available
- **Error Handling**: Proper HTTP error handling with meaningful exceptions
- **Validation**: Automatic response validation using Pydantic models

## Installation

```bash
# Using uv (recommended)
uv add git+https://github.com/caentzminger/defillama.git

# Using pip
pip install git+https://github.com/caentzminger/defillama.git
```

## Quick Start

### Synchronous Usage

```python
from defillama import DefiLlama

# Create a client
client = DefiLlama()

# Get all protocols
protocols = client.get_protocols()
print(f"Found {len(protocols)} protocols")

# Get current prices
prices = client.get_current_prices(coins=["coingecko:ethereum", "coingecko:bitcoin"])
eth_price = prices.coins["coingecko:ethereum"].price
btc_price = prices.coins["coingecko:bitcoin"].price
print(f"ETH: ${eth_price:.2f}, BTC: ${btc_price:.2f}")

# Get protocol details
aave = client.get_protocol("aave-v3")
print(f"AAVE V3 TVL: ${aave.tvl[0].totalLiquidityUSD:,.0f}")

# Close the client
client.close()
```

### Asynchronous Usage

```python
import asyncio
from defillama import DefiLlama

async def main():
    # Create a client
    client = DefiLlama()
    
    try:
        # Get all protocols asynchronously
        protocols = await client.get_protocols_async()
        print(f"Found {len(protocols)} protocols")
        
        # Get current prices asynchronously
        prices = await client.get_current_prices_async(coins=["coingecko:ethereum"])
        eth_price = prices.coins["coingecko:ethereum"].price
        print(f"ETH: ${eth_price:.2f}")
        
        # Get protocol details asynchronously
        aave = await client.get_protocol_async("aave-v3")
        print(f"AAVE V3 TVL: ${aave.tvl[0].totalLiquidityUSD:,.0f}")
        
    finally:
        # Always close the async client
        await client.aclose()

# Run the async function
asyncio.run(main())
```

### Concurrent Async Operations

```python
import asyncio
from defillama import DefiLlama

async def main():
    client = DefiLlama()
    
    try:
        # Run multiple operations concurrently
        protocols_task = client.get_protocols_async()
        prices_task = client.get_current_prices_async(coins=["coingecko:ethereum"])
        chains_task = client.get_chains_async()
        
        # Wait for all tasks to complete
        protocols, prices, chains = await asyncio.gather(
            protocols_task, prices_task, chains_task
        )
        
        print(f"Protocols: {len(protocols)}")
        print(f"ETH Price: ${prices.coins['coingecko:ethereum'].price:.2f}")
        print(f"Chains: {len(chains)}")
        
    finally:
        await client.aclose()

asyncio.run(main())
```

## Available Methods

### Protocol Methods
- `get_protocols()` / `get_protocols_async()` - Get all protocols
- `get_protocol(slug)` / `get_protocol_async(slug)` - Get specific protocol details
- `get_protocol_tvl(slug)` / `get_protocol_tvl_async(slug)` - Get protocol TVL

### Chain Methods
- `get_chains()` / `get_chains_async()` - Get all chains
- `get_historical_chain_tvl(chain_slug)` / `get_historical_chain_tvl_async(chain_slug)` - Get historical chain TVL

### Price Methods
- `get_current_prices(coins)` / `get_current_prices_async(coins)` - Get current prices
- `get_historical_prices(timestamp, coins)` / `get_historical_prices_async(timestamp, coins)` - Get historical prices
- `get_first_prices(coins)` / `get_first_prices_async(coins)` - Get first recorded prices
- `get_price_chart(coins, start, end, span, period)` / `get_price_chart_async(coins, start, end, span, period)` - Get price charts
- `get_price_percentage_change(coins, timestamp, look_forward, period)` / `get_price_percentage_change_async(coins, timestamp, look_forward, period)` - Get percentage changes
- `get_batch_historical_prices(coins, search_width)` / `get_batch_historical_prices_async(coins, search_width)` - Get batch historical prices
- `get_block(chain, timestamp)` / `get_block_async(chain, timestamp)` - Get block information

### Stablecoin Methods
- `get_stablecoins(include_prices)` / `get_stablecoins_async(include_prices)` - Get all stablecoins
- `get_stablecoin_charts(chain, stablecoin)` / `get_stablecoin_charts_async(chain, stablecoin)` - Get stablecoin charts
- `get_stablecoin_historical(asset_id)` / `get_stablecoin_historical_async(asset_id)` - Get stablecoin historical data
- `get_stablecoin_chains()` / `get_stablecoin_chains_async()` - Get stablecoin chains
- `get_stablecoin_prices()` / `get_stablecoin_prices_async()` - Get stablecoin prices

### Yield Methods
- `get_pools()` / `get_pools_async()` - Get all pools
- `get_pool_chart(pool_id)` / `get_pool_chart_async(pool_id)` - Get pool chart data

### DEX Methods
- `get_dexs(chain, exclude_total_data_chart, exclude_total_data_chart_breakdown)` / `get_dexs_async(chain, exclude_total_data_chart, exclude_total_data_chart_breakdown)` - Get DEX overview
- `get_dex_summary(protocol_slug, exclude_total_data_chart, exclude_total_data_chart_breakdown)` / `get_dex_summary_async(protocol_slug, exclude_total_data_chart, exclude_total_data_chart_breakdown)` - Get DEX summary
- `get_options_dexs(chain, exclude_total_data_chart, exclude_total_data_chart_breakdown, data_type)` / `get_options_dexs_async(chain, exclude_total_data_chart, exclude_total_data_chart_breakdown, data_type)` - Get options DEX overview
- `get_options_dex_summary(protocol_slug, data_type)` / `get_options_dex_summary_async(protocol_slug, data_type)` - Get options DEX summary

### Fee Methods
- `get_fees(chain, exclude_total_data_chart, exclude_total_data_chart_breakdown, data_type)` / `get_fees_async(chain, exclude_total_data_chart, exclude_total_data_chart_breakdown, data_type)` - Get fees overview
- `get_fee_summary(protocol_slug, data_type)` / `get_fee_summary_async(protocol_slug, data_type)` - Get fee summary

## Error Handling

The client raises `ValueError` with HTTP error details when API requests fail:

```python
try:
    protocol = client.get_protocol("nonexistent-protocol")
except ValueError as e:
    print(f"API Error: {e}")
```

## Development

### Setup

```bash
# Clone the repository
gh repo clone caentzminger/defillama
cd defillama

# Install dependencies
uv sync

# Install in development mode
uv pip install -e .
```

### Running Tests

```bash
# Run all tests
make test

# Run async tests only
uv run pytest -k "async"

# Run with coverage
uv run pytest --cov=defillama
```

### Type Checking

```bash
make typecheck
```

## License

This project is licensed under the MIT License.
