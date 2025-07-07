import pytest
import pytest_asyncio
from defillama import DefiLlama
from defillama import models


@pytest.fixture
def client():
    return DefiLlama()


@pytest_asyncio.fixture
async def async_client():
    client = DefiLlama()
    yield client
    await client.aclose()


def test_get_protocols(client):
    protocols = client.get_protocols()
    assert isinstance(protocols, list)
    assert len(protocols) > 0
    # Check for a well-known protocol to ensure the list is populated
    assert any(p.name == "AAVE V3" for p in protocols)


@pytest.mark.asyncio
async def test_get_protocols_async(async_client):
    protocols = await async_client.get_protocols_async()
    assert isinstance(protocols, list)
    assert len(protocols) > 0
    # Check for a well-known protocol to ensure the list is populated
    assert any(p.name == "AAVE V3" for p in protocols)


def test_get_protocol(client):
    # Test with a well-known protocol slug
    protocol = client.get_protocol("aave-v3")
    assert protocol is not None
    assert protocol.name == "AAVE V3"
    assert isinstance(protocol.tvl, list)
    # Check that the TVL list contains data points
    assert len(protocol.tvl) > 0
    assert "date" in protocol.tvl[0].model_dump()
    assert "totalLiquidityUSD" in protocol.tvl[0].model_dump()


@pytest.mark.asyncio
async def test_get_protocol_async(async_client):
    # Test with a well-known protocol slug
    protocol = await async_client.get_protocol_async("aave-v3")
    assert protocol is not None
    assert protocol.name == "AAVE V3"
    assert isinstance(protocol.tvl, list)
    # Check that the TVL list contains data points
    assert len(protocol.tvl) > 0
    assert "date" in protocol.tvl[0].model_dump()
    assert "totalLiquidityUSD" in protocol.tvl[0].model_dump()


def test_get_nonexistent_protocol(client):
    with pytest.raises(ValueError) as excinfo:
        client.get_protocol("nonexistent-protocol-slug")
    # Check for a 404 or other client/server error status
    assert isinstance(excinfo.value, ValueError)
    assert "HTTP error" in str(excinfo.value)
    assert "400" in str(excinfo.value) or "404" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_nonexistent_protocol_async(async_client):
    with pytest.raises(ValueError) as excinfo:
        await async_client.get_protocol_async("nonexistent-protocol-slug")
    # Check for a 404 or other client/server error status
    assert isinstance(excinfo.value, ValueError)
    assert "HTTP error" in str(excinfo.value)
    assert "400" in str(excinfo.value) or "404" in str(excinfo.value)


def test_get_chains(client):
    chains = client.get_chains()
    assert isinstance(chains, list)
    assert len(chains) > 0
    # Check structure of first chain
    first_chain = chains[0]
    assert hasattr(first_chain, "name")
    assert hasattr(first_chain, "chainId")
    assert hasattr(first_chain, "tvl")


@pytest.mark.asyncio
async def test_get_chains_async(async_client):
    chains = await async_client.get_chains_async()
    assert isinstance(chains, list)
    assert len(chains) > 0
    # Check structure of first chain
    first_chain = chains[0]
    assert hasattr(first_chain, "name")
    assert hasattr(first_chain, "chainId")
    assert hasattr(first_chain, "tvl")


def test_get_current_prices(client):
    prices = client.get_current_prices(coins=["coingecko:ethereum"])
    assert isinstance(prices, models.CoinPrice)
    assert "coins" in prices.model_dump()


@pytest.mark.asyncio
async def test_get_current_prices_async(async_client):
    prices = await async_client.get_current_prices_async(coins=["coingecko:ethereum"])
    assert isinstance(prices, models.CoinPrice)
    assert "coins" in prices.model_dump()


def test_get_historical_prices(client):
    import time

    timestamp = int(time.time()) - 86400  # 24 hours ago
    prices = client.get_historical_prices(
        timestamp=timestamp, coins=["coingecko:ethereum"]
    )
    assert isinstance(prices, models.CoinPrice)
    assert "coins" in prices.model_dump()


@pytest.mark.asyncio
async def test_get_historical_prices_async(async_client):
    import time

    timestamp = int(time.time()) - 86400  # 24 hours ago
    prices = await async_client.get_historical_prices_async(
        timestamp=timestamp, coins=["coingecko:ethereum"]
    )
    assert isinstance(prices, models.CoinPrice)
    assert "coins" in prices.model_dump()


def test_get_first_prices(client):
    prices = client.get_first_prices(coins=["coingecko:ethereum"])
    assert isinstance(prices, models.CoinPrice)
    assert "coins" in prices.model_dump()


@pytest.mark.asyncio
async def test_get_first_prices_async(async_client):
    prices = await async_client.get_first_prices_async(coins=["coingecko:ethereum"])
    assert isinstance(prices, models.CoinPrice)
    assert "coins" in prices.model_dump()


def test_get_block(client):
    from datetime import datetime

    # Use Ethereum chain and a timestamp from a few days ago
    block = client.get_block(
        chain="ethereum",
        timestamp=int(datetime.now().timestamp() - 86400 * 3),  # 3 days ago
    )
    assert isinstance(block, models.Block)
    assert hasattr(block, "height")
    assert hasattr(block, "timestamp")


@pytest.mark.asyncio
async def test_get_block_async(async_client):
    from datetime import datetime

    # Use Ethereum chain and a timestamp from a few days ago
    block = await async_client.get_block_async(
        chain="ethereum",
        timestamp=int(datetime.now().timestamp() - 86400 * 3),  # 3 days ago
    )
    assert isinstance(block, models.Block)
    assert hasattr(block, "height")
    assert hasattr(block, "timestamp")


def test_get_stablecoins(client):
    """Test stablecoins endpoint with proper model validation"""
    stablecoins = client.get_stablecoins()
    assert isinstance(stablecoins, list)
    assert len(stablecoins) > 0
    # Check structure of first stablecoin
    first_stablecoin = stablecoins[0]
    assert hasattr(first_stablecoin, "id")
    assert hasattr(first_stablecoin, "name")
    assert hasattr(first_stablecoin, "symbol")
    assert hasattr(first_stablecoin, "circulating")


@pytest.mark.asyncio
async def test_get_stablecoins_async(async_client):
    """Test stablecoins endpoint with proper model validation"""
    stablecoins = await async_client.get_stablecoins_async()
    assert isinstance(stablecoins, list)
    assert len(stablecoins) > 0
    # Check structure of first stablecoin
    first_stablecoin = stablecoins[0]
    assert hasattr(first_stablecoin, "id")
    assert hasattr(first_stablecoin, "name")
    assert hasattr(first_stablecoin, "symbol")
    assert hasattr(first_stablecoin, "circulating")


def test_get_stablecoin_charts(client):
    """Test stablecoin charts endpoint with proper model validation"""
    charts = client.get_stablecoin_charts()
    assert isinstance(charts, list)
    if len(charts) > 0:
        first_chart = charts[0]
        assert hasattr(first_chart, "date")
        assert hasattr(first_chart, "totalCirculating")
        assert hasattr(first_chart, "totalCirculatingUSD")
        # Check that date is a string and circulating values are dictionaries
        assert isinstance(first_chart.date, str)
        assert isinstance(first_chart.totalCirculating, dict)
        assert isinstance(first_chart.totalCirculatingUSD, dict)


@pytest.mark.asyncio
async def test_get_stablecoin_charts_async(async_client):
    """Test stablecoin charts endpoint with proper model validation"""
    charts = await async_client.get_stablecoin_charts_async()
    assert isinstance(charts, list)
    if len(charts) > 0:
        first_chart = charts[0]
        assert hasattr(first_chart, "date")
        assert hasattr(first_chart, "totalCirculating")
        assert hasattr(first_chart, "totalCirculatingUSD")
        # Check that date is a string and circulating values are dictionaries
        assert isinstance(first_chart.date, str)
        assert isinstance(first_chart.totalCirculating, dict)
        assert isinstance(first_chart.totalCirculatingUSD, dict)


def test_get_stablecoin_chains(client):
    """Test stablecoin chains endpoint with proper model validation"""
    chains = client.get_stablecoin_chains()
    assert isinstance(chains, list)
    if len(chains) > 0:
        first_chain = chains[0]
        assert hasattr(first_chain, "name")
        assert hasattr(first_chain, "totalCirculatingUSD")
        assert hasattr(first_chain, "gecko_id")
        assert hasattr(first_chain, "tokenSymbol")
        # Check that totalCirculatingUSD is a dictionary
        assert isinstance(first_chain.totalCirculatingUSD, dict)


@pytest.mark.asyncio
async def test_get_stablecoin_chains_async(async_client):
    """Test stablecoin chains endpoint with proper model validation"""
    chains = await async_client.get_stablecoin_chains_async()
    assert isinstance(chains, list)
    if len(chains) > 0:
        first_chain = chains[0]
        assert hasattr(first_chain, "name")
        assert hasattr(first_chain, "totalCirculatingUSD")
        assert hasattr(first_chain, "gecko_id")
        assert hasattr(first_chain, "tokenSymbol")
        # Check that totalCirculatingUSD is a dictionary
        assert isinstance(first_chain.totalCirculatingUSD, dict)


def test_get_stablecoin_historical(client):
    """Test stablecoin historical endpoint with proper model validation"""
    # Test with Tether (ID: 1)
    historical = client.get_stablecoin_historical(1)
    assert isinstance(historical, models.StablecoinHistorical)
    assert historical.id == "1"
    assert historical.name == "Tether"
    assert historical.symbol == "USDT"
    assert hasattr(historical, "pegType")
    assert hasattr(historical, "pegMechanism")
    assert hasattr(historical, "chainBalances")


@pytest.mark.asyncio
async def test_get_stablecoin_historical_async(async_client):
    """Test stablecoin historical endpoint with proper model validation"""
    # Test with Tether (ID: 1)
    historical = await async_client.get_stablecoin_historical_async(1)
    assert isinstance(historical, models.StablecoinHistorical)
    assert historical.id == "1"
    assert historical.name == "Tether"
    assert historical.symbol == "USDT"
    assert hasattr(historical, "pegType")
    assert hasattr(historical, "pegMechanism")
    assert hasattr(historical, "chainBalances")


def test_get_pools(client):
    """Test pools endpoint with proper model validation"""
    pools = client.get_pools()
    assert isinstance(pools, list)
    if len(pools) > 0:
        first_pool = pools[0]
        assert hasattr(first_pool, "chain")
        assert hasattr(first_pool, "project")
        assert hasattr(first_pool, "symbol")
        assert hasattr(first_pool, "tvlUsd")
        assert hasattr(first_pool, "apy")


@pytest.mark.asyncio
async def test_get_pools_async(async_client):
    """Test pools endpoint with proper model validation"""
    pools = await async_client.get_pools_async()
    assert isinstance(pools, list)
    if len(pools) > 0:
        first_pool = pools[0]
        assert hasattr(first_pool, "chain")
        assert hasattr(first_pool, "project")
        assert hasattr(first_pool, "symbol")
        assert hasattr(first_pool, "tvlUsd")
        assert hasattr(first_pool, "apy")


def test_get_dexs(client):
    """Test DEXs endpoint with proper model validation"""
    dexs = client.get_dexs()
    assert isinstance(dexs, models.DexOverview)
    assert hasattr(dexs, "allChains")
    assert isinstance(dexs.allChains, list)


@pytest.mark.asyncio
async def test_get_dexs_async(async_client):
    """Test DEXs endpoint with proper model validation"""
    dexs = await async_client.get_dexs_async()
    assert isinstance(dexs, models.DexOverview)
    assert hasattr(dexs, "allChains")
    assert isinstance(dexs.allChains, list)


def test_get_fees(client):
    """Test fees endpoint with proper model validation"""
    fees = client.get_fees()
    assert isinstance(fees, models.FeeOverview)
    assert hasattr(fees, "allChains")
    assert isinstance(fees.allChains, list)


@pytest.mark.asyncio
async def test_get_fees_async(async_client):
    """Test fees endpoint with proper model validation"""
    fees = await async_client.get_fees_async()
    assert isinstance(fees, models.FeeOverview)
    assert hasattr(fees, "allChains")
    assert isinstance(fees.allChains, list)


def test_model_validation_coin_with_confidence(client):
    """Test that Coin model properly validates responses with confidence field"""
    # Test with a coin that should have confidence data
    prices = client.get_current_prices(coins=["coingecko:ethereum"])
    assert isinstance(prices, models.CoinPrice)
    coins_data = prices.coins
    assert isinstance(coins_data, dict)
    if "coingecko:ethereum" in coins_data:
        eth_data = coins_data["coingecko:ethereum"]
        # Confidence field should be present (may be None)
        assert hasattr(eth_data, "confidence")


def test_model_validation_coin_without_confidence(client):
    """Test that Coin model properly validates responses without confidence field"""
    # Test with a coin that might not have confidence data
    prices = client.get_current_prices(coins=["coingecko:bitcoin"])
    assert isinstance(prices, models.CoinPrice)
    coins_data = prices.coins
    assert isinstance(coins_data, dict)
    if "coingecko:bitcoin" in coins_data:
        btc_data = coins_data["coingecko:bitcoin"]
        # Confidence field should be present (may be None)
        assert hasattr(btc_data, "confidence")


@pytest.mark.asyncio
async def test_async_sync_consistency(async_client, client):
    """Test that async and sync methods return the same results"""
    # Test protocols
    sync_protocols = client.get_protocols()
    async_protocols = await async_client.get_protocols_async()

    assert len(sync_protocols) == len(async_protocols)
    # Check that they contain the same protocols (by name)
    sync_names = {p.name for p in sync_protocols}
    async_names = {p.name for p in async_protocols}
    assert sync_names == async_names

    # Test current prices
    sync_prices = client.get_current_prices(coins=["coingecko:ethereum"])
    async_prices = await async_client.get_current_prices_async(
        coins=["coingecko:ethereum"]
    )

    assert sync_prices.model_dump() == async_prices.model_dump()
