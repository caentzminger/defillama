from __future__ import annotations

import httpx
from typing import List, Optional, Dict, Any, Literal

from . import models


class DefiLlama:
    """
    A Python client for the DefiLlama API.

    DefiLlama provides comprehensive data about DeFi protocols, including TVL (Total Value Locked),
    token prices, stablecoins, yields, DEX volumes, and fees/revenue data.

    The client supports both synchronous and asynchronous operations for all API endpoints.

    Base URLs:
    - Main API: https://api.llama.fi
    - Coins API: https://coins.llama.fi
    - Stablecoins API: https://stablecoins.llama.fi
    - Yields API: https://yields.llama.fi
    """

    def __init__(self):
        self.client = httpx.Client()
        self.async_client = httpx.AsyncClient()
        self.BASE_URL = "https://api.llama.fi"
        self.COINS_URL = "https://coins.llama.fi"
        self.STABLECOINS_URL = "https://stablecoins.llama.fi"
        self.YIELDS_URL = "https://yields.llama.fi"

    def _request(self, method: str, url: str, params: Optional[Dict[str, Any]] = None):
        try:
            res = self.client.request(method=method, url=url, params=params)
            res.raise_for_status()
            return res.json()
        except httpx.HTTPStatusError as e:
            raise ValueError(f"HTTP error: {e}") from e

    async def _async_request(
        self, method: str, url: str, params: Optional[Dict[str, Any]] = None
    ):
        try:
            res = await self.async_client.request(method=method, url=url, params=params)
            res.raise_for_status()
            return res.json()
        except httpx.HTTPStatusError as e:
            raise ValueError(f"HTTP error: {e}") from e

    def get_protocols(self) -> List[models.Protocol]:
        """
        List all protocols on DefiLlama along with their TVL.

        Returns:
            List[models.Protocol]: List of all protocols with their current TVL data

        API Endpoint: GET /protocols
        """
        data = self._request("GET", f"{self.BASE_URL}/protocols")
        return models.Protocols.validate_python(data)

    async def get_protocols_async(self) -> List[models.Protocol]:
        """
        List all protocols on DefiLlama along with their TVL (async).

        Returns:
            List[models.Protocol]: List of all protocols with their current TVL data

        API Endpoint: GET /protocols
        """
        data = await self._async_request("GET", f"{self.BASE_URL}/protocols")
        return models.Protocols.validate_python(data)

    def get_protocol(self, protocol_slug: str) -> models.ProtocolDetails:
        """
        Get historical TVL of a protocol and breakdowns by token and chain.

        Args:
            protocol_slug (str): Protocol slug (e.g., "aave", "uniswap")

        Returns:
            models.ProtocolDetails: Detailed protocol information including historical TVL data

        API Endpoint: GET /protocol/{protocol}
        """
        data = self._request("GET", f"{self.BASE_URL}/protocol/{protocol_slug}")
        return models.ProtocolDetails.model_validate(data)

    async def get_protocol_async(self, protocol_slug: str) -> models.ProtocolDetails:
        """
        Get historical TVL of a protocol and breakdowns by token and chain (async).

        Args:
            protocol_slug (str): Protocol slug (e.g., "aave", "uniswap")

        Returns:
            models.ProtocolDetails: Detailed protocol information including historical TVL data

        API Endpoint: GET /protocol/{protocol}
        """
        data = await self._async_request(
            "GET", f"{self.BASE_URL}/protocol/{protocol_slug}"
        )
        return models.ProtocolDetails.model_validate(data)

    def get_historical_chain_tvl(
        self, chain_slug: Optional[str] = None
    ) -> List[models.HistoricalTvl]:
        """
        Get historical TVL (excludes liquid staking and double counted TVL) of DeFi on all chains or a specific chain.

        Args:
            chain_slug (Optional[str]): Chain slug (e.g., "Ethereum", "BSC"). If None, returns data for all chains.

        Returns:
            List[models.HistoricalTvl]: Historical TVL data points

        API Endpoint: GET /v2/historicalChainTvl or GET /v2/historicalChainTvl/{chain}
        """
        endpoint = "/v2/historicalChainTvl"
        if chain_slug:
            endpoint = f"{endpoint}/{chain_slug}"
        data = self._request("GET", f"{self.BASE_URL}{endpoint}")
        return models.HistoricalTvls.validate_python(data)

    async def get_historical_chain_tvl_async(
        self, chain_slug: Optional[str] = None
    ) -> List[models.HistoricalTvl]:
        """
        Get historical TVL (excludes liquid staking and double counted TVL) of DeFi on all chains or a specific chain (async).

        Args:
            chain_slug (Optional[str]): Chain slug (e.g., "Ethereum", "BSC"). If None, returns data for all chains.

        Returns:
            List[models.HistoricalTvl]: Historical TVL data points

        API Endpoint: GET /v2/historicalChainTvl or GET /v2/historicalChainTvl/{chain}
        """
        endpoint = "/v2/historicalChainTvl"
        if chain_slug:
            endpoint = f"{endpoint}/{chain_slug}"
        data = await self._async_request("GET", f"{self.BASE_URL}{endpoint}")
        return models.HistoricalTvls.validate_python(data)

    def get_protocol_tvl(self, protocol_slug: str) -> float:
        """
        Get simplified current TVL of a protocol.

        Args:
            protocol_slug (str): Protocol slug (e.g., "uniswap", "aave")

        Returns:
            float: Current TVL value as a number

        API Endpoint: GET /tvl/{protocol}
        """
        return self._request("GET", f"{self.BASE_URL}/tvl/{protocol_slug}")

    async def get_protocol_tvl_async(self, protocol_slug: str) -> float:
        """
        Get simplified current TVL of a protocol (async).

        Args:
            protocol_slug (str): Protocol slug (e.g., "uniswap", "aave")

        Returns:
            float: Current TVL value as a number

        API Endpoint: GET /tvl/{protocol}
        """
        return await self._async_request("GET", f"{self.BASE_URL}/tvl/{protocol_slug}")

    def get_chains(self) -> List[models.Chain]:
        """
        Get current TVL of all chains.

        Returns:
            List[models.Chain]: List of all chains with their current TVL data

        API Endpoint: GET /v2/chains
        """
        data = self._request("GET", f"{self.BASE_URL}/v2/chains")
        return models.Chains.validate_python(data)

    async def get_chains_async(self) -> List[models.Chain]:
        """
        Get current TVL of all chains (async).

        Returns:
            List[models.Chain]: List of all chains with their current TVL data

        API Endpoint: GET /v2/chains
        """
        data = await self._async_request("GET", f"{self.BASE_URL}/v2/chains")
        return models.Chains.validate_python(data)

    def get_current_prices(
        self, coins: List[str], search_width: str = "4h"
    ) -> models.CoinPrice:
        """
        Get current prices of tokens by contract address.

        The API prices tokens through multiple methods including bridged token pricing,
        specialized adapters for LP tokens, and liquidity-based pricing for exotic tokens.

        Args:
            coins (List[str]): List of tokens in format {chain}:{address} or coingecko:{id}
                              Examples: ["ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1", "coingecko:ethereum"]
            search_width (str): Time range on either side to find price data (default: "4h")

        Returns:
            models.CoinPrice: Current price data for the requested tokens

        API Endpoint: GET /prices/current/{coins}
        """
        coins_str = ",".join(coins)
        params = {"searchWidth": search_width}
        data = self._request(
            "GET", f"{self.COINS_URL}/prices/current/{coins_str}", params=params
        )
        return models.CoinPrice.model_validate(data)

    async def get_current_prices_async(
        self, coins: List[str], search_width: str = "4h"
    ) -> models.CoinPrice:
        """
        Get current prices of tokens by contract address (async).

        The API prices tokens through multiple methods including bridged token pricing,
        specialized adapters for LP tokens, and liquidity-based pricing for exotic tokens.

        Args:
            coins (List[str]): List of tokens in format {chain}:{address} or coingecko:{id}
                              Examples: ["ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1", "coingecko:ethereum"]
            search_width (str): Time range on either side to find price data (default: "4h")

        Returns:
            models.CoinPrice: Current price data for the requested tokens

        API Endpoint: GET /prices/current/{coins}
        """
        coins_str = ",".join(coins)
        params = {"searchWidth": search_width}
        data = await self._async_request(
            "GET", f"{self.COINS_URL}/prices/current/{coins_str}", params=params
        )
        return models.CoinPrice.model_validate(data)

    def get_historical_prices(
        self, timestamp: int, coins: List[str], search_width: str = "4h"
    ) -> models.CoinPrice:
        """
        Get historical prices of tokens by contract address at a specific timestamp.

        Args:
            timestamp (int): UNIX timestamp of time when you want historical prices
            coins (List[str]): List of tokens in format {chain}:{address} or coingecko:{id}
                              Examples: ["ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1", "coingecko:ethereum"]
            search_width (str): Time range on either side to find price data (default: "4h")

        Returns:
            models.CoinPrice: Historical price data for the requested tokens at the specified timestamp

        API Endpoint: GET /prices/historical/{timestamp}/{coins}
        """
        coins_str = ",".join(coins)
        params = {"searchWidth": search_width}
        data = self._request(
            "GET",
            f"{self.COINS_URL}/prices/historical/{timestamp}/{coins_str}",
            params=params,
        )
        return models.CoinPrice.model_validate(data)

    async def get_historical_prices_async(
        self, timestamp: int, coins: List[str], search_width: str = "4h"
    ) -> models.CoinPrice:
        """
        Get historical prices of tokens by contract address at a specific timestamp (async).

        Args:
            timestamp (int): UNIX timestamp of time when you want historical prices
            coins (List[str]): List of tokens in format {chain}:{address} or coingecko:{id}
                              Examples: ["ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1", "coingecko:ethereum"]
            search_width (str): Time range on either side to find price data (default: "4h")

        Returns:
            models.CoinPrice: Historical price data for the requested tokens at the specified timestamp

        API Endpoint: GET /prices/historical/{timestamp}/{coins}
        """
        coins_str = ",".join(coins)
        params = {"searchWidth": search_width}
        data = await self._async_request(
            "GET",
            f"{self.COINS_URL}/prices/historical/{timestamp}/{coins_str}",
            params=params,
        )
        return models.CoinPrice.model_validate(data)

    def get_batch_historical_prices(
        self, coins: Dict[str, List[int]], search_width: Optional[str] = None
    ) -> models.BatchHistoricalPrices:
        """
        Get historical prices for multiple tokens at multiple different timestamps.

        Args:
            coins (Dict[str, List[int]]): Dictionary where keys are coins in format {chain}:{address},
                                        and values are arrays of requested timestamps
                                        Example: {"avax:0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e": [1666876743, 1666862343]}
            search_width (Optional[str]): Time range on either side to find price data (default: 6 hours)

        Returns:
            models.BatchHistoricalPrices: Historical price data for multiple tokens at multiple timestamps

        API Endpoint: GET /batchHistorical
        """
        params = {"coins": str(coins)}
        if search_width:
            params["searchWidth"] = search_width
        data = self._request("GET", f"{self.COINS_URL}/batchHistorical", params=params)
        return models.BatchHistoricalPrices.model_validate(data)

    async def get_batch_historical_prices_async(
        self, coins: Dict[str, List[int]], search_width: Optional[str] = None
    ) -> models.BatchHistoricalPrices:
        """
        Get historical prices for multiple tokens at multiple different timestamps (async).

        Args:
            coins (Dict[str, List[int]]): Dictionary where keys are coins in format {chain}:{address},
                                        and values are arrays of requested timestamps
                                        Example: {"avax:0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e": [1666876743, 1666862343]}
            search_width (Optional[str]): Time range on either side to find price data (default: 6 hours)

        Returns:
            models.BatchHistoricalPrices: Historical price data for multiple tokens at multiple timestamps

        API Endpoint: GET /batchHistorical
        """
        params = {"coins": str(coins)}
        if search_width:
            params["searchWidth"] = search_width
        data = await self._async_request(
            "GET", f"{self.COINS_URL}/batchHistorical", params=params
        )
        return models.BatchHistoricalPrices.model_validate(data)

    def get_price_chart(
        self,
        coins: List[str],
        start: Optional[int] = None,
        end: Optional[int] = None,
        span: Optional[int] = None,
        period: Optional[str] = None,
        search_width: Optional[str] = None,
    ) -> models.PriceChart:
        """
        Get token prices at regular time intervals.

        Args:
            coins (List[str]): List of tokens in format {chain}:{address} or coingecko:{id}
                              Examples: ["ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1", "coingecko:ethereum"]
            start (Optional[int]): UNIX timestamp of earliest data point requested
            end (Optional[int]): UNIX timestamp of latest data point requested
            span (Optional[int]): Number of data points returned (default: 0)
            period (Optional[str]): Duration between data points (default: "24h")
                                  Can use chart candle notation like '4h', '2d', '1w', '1M'
            search_width (Optional[str]): Time range on either side to find price data (default: 10% of period)

        Returns:
            models.PriceChart: Chart data with prices at regular intervals

        API Endpoint: GET /chart/{coins}
        """
        coins_str = ",".join(coins)
        params = {}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        if span:
            params["span"] = span
        if period:
            params["period"] = period
        if search_width:
            params["searchWidth"] = search_width
        data = self._request(
            "GET", f"{self.COINS_URL}/chart/{coins_str}", params=params
        )
        return models.PriceChart.model_validate(data)

    async def get_price_chart_async(
        self,
        coins: List[str],
        start: Optional[int] = None,
        end: Optional[int] = None,
        span: Optional[int] = None,
        period: Optional[str] = None,
        search_width: Optional[str] = None,
    ) -> models.PriceChart:
        """
        Get token prices at regular time intervals (async).

        Args:
            coins (List[str]): List of tokens in format {chain}:{address} or coingecko:{id}
                              Examples: ["ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1", "coingecko:ethereum"]
            start (Optional[int]): UNIX timestamp of earliest data point requested
            end (Optional[int]): UNIX timestamp of latest data point requested
            span (Optional[int]): Number of data points returned (default: 0)
            period (Optional[str]): Duration between data points (default: "24h")
                                  Can use chart candle notation like '4h', '2d', '1w', '1M'
            search_width (Optional[str]): Time range on either side to find price data (default: 10% of period)

        Returns:
            models.PriceChart: Chart data with prices at regular intervals

        API Endpoint: GET /chart/{coins}
        """
        coins_str = ",".join(coins)
        params = {}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        if span:
            params["span"] = span
        if period:
            params["period"] = period
        if search_width:
            params["searchWidth"] = search_width
        data = await self._async_request(
            "GET", f"{self.COINS_URL}/chart/{coins_str}", params=params
        )
        return models.PriceChart.model_validate(data)

    def get_price_percentage_change(
        self,
        coins: List[str],
        timestamp: Optional[int] = None,
        look_forward: bool = False,
        period: str = "24h",
    ) -> models.PercentageChange:
        """
        Get percentage change in price over time.

        Args:
            coins (List[str]): List of tokens in format {chain}:{address} or coingecko:{id}
                              Examples: ["ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1", "coingecko:ethereum"]
            timestamp (Optional[int]): Timestamp of data point requested (default: current time)
            look_forward (bool): Whether to look forward from timestamp or backward (default: False)
            period (str): Duration for percentage calculation (default: "24h")
                         Can use chart candle notation like '4h', '2d', '1w', '1M'

        Returns:
            models.PercentageChange: Percentage change data for the requested tokens

        API Endpoint: GET /percentage/{coins}
        """
        coins_str = ",".join(coins)
        params = {"lookForward": look_forward, "period": period}
        if timestamp:
            params["timestamp"] = timestamp
        data = self._request(
            "GET", f"{self.COINS_URL}/percentage/{coins_str}", params=params
        )
        return models.PercentageChange.model_validate(data)

    async def get_price_percentage_change_async(
        self,
        coins: List[str],
        timestamp: Optional[int] = None,
        look_forward: bool = False,
        period: str = "24h",
    ) -> models.PercentageChange:
        """
        Get percentage change in price over time (async).

        Args:
            coins (List[str]): List of tokens in format {chain}:{address} or coingecko:{id}
                              Examples: ["ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1", "coingecko:ethereum"]
            timestamp (Optional[int]): Timestamp of data point requested (default: current time)
            look_forward (bool): Whether to look forward from timestamp or backward (default: False)
            period (str): Duration for percentage calculation (default: "24h")
                         Can use chart candle notation like '4h', '2d', '1w', '1M'

        Returns:
            models.PercentageChange: Percentage change data for the requested tokens

        API Endpoint: GET /percentage/{coins}
        """
        coins_str = ",".join(coins)
        params = {"lookForward": look_forward, "period": period}
        if timestamp:
            params["timestamp"] = timestamp
        data = await self._async_request(
            "GET", f"{self.COINS_URL}/percentage/{coins_str}", params=params
        )
        return models.PercentageChange.model_validate(data)

    def get_first_prices(self, coins: List[str]) -> models.CoinPrice:
        """
        Get earliest timestamp price record for coins.

        Args:
            coins (List[str]): List of tokens in format {chain}:{address} or coingecko:{id}
                              Examples: ["ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1", "coingecko:ethereum"]

        Returns:
            models.CoinPrice: First available price data for the requested tokens

        API Endpoint: GET /prices/first/{coins}
        """
        coins_str = ",".join(coins)
        data = self._request("GET", f"{self.COINS_URL}/prices/first/{coins_str}")
        return models.CoinPrice.model_validate(data)

    async def get_first_prices_async(self, coins: List[str]) -> models.CoinPrice:
        """
        Get earliest timestamp price record for coins (async).

        Args:
            coins (List[str]): List of tokens in format {chain}:{address} or coingecko:{id}
                              Examples: ["ethereum:0xdF574c24545E5FfEcb9a659c229253D4111d87e1", "coingecko:ethereum"]

        Returns:
            models.CoinPrice: First available price data for the requested tokens

        API Endpoint: GET /prices/first/{coins}
        """
        coins_str = ",".join(coins)
        data = await self._async_request(
            "GET", f"{self.COINS_URL}/prices/first/{coins_str}"
        )
        return models.CoinPrice.model_validate(data)

    def get_block(self, chain: str, timestamp: int) -> models.Block:
        """
        Get the closest block to a timestamp.

        Runs binary search over a blockchain's blocks to get the closest one to a timestamp.
        Every time this is run, new data is added to the database, so each query permanently
        speeds up future queries.

        Args:
            chain (str): Chain which you want to get the block from
            timestamp (int): UNIX timestamp of the block you are searching for

        Returns:
            models.Block: Block information with height and timestamp

        API Endpoint: GET /block/{chain}/{timestamp}
        """
        data = self._request(
            "GET", f"{self.COINS_URL}/block/{chain.lower()}/{timestamp}"
        )
        return models.Block.model_validate(data)

    async def get_block_async(self, chain: str, timestamp: int) -> models.Block:
        """
        Get the closest block to a timestamp (async).

        Runs binary search over a blockchain's blocks to get the closest one to a timestamp.
        Every time this is run, new data is added to the database, so each query permanently
        speeds up future queries.

        Args:
            chain (str): Chain which you want to get the block from
            timestamp (int): UNIX timestamp of the block you are searching for

        Returns:
            models.Block: Block information with height and timestamp

        API Endpoint: GET /block/{chain}/{timestamp}
        """
        data = await self._async_request(
            "GET", f"{self.COINS_URL}/block/{chain}/{timestamp}"
        )
        return models.Block.model_validate(data)

    def get_stablecoins(self, include_prices: bool = True) -> List[models.Stablecoin]:
        """
        List all stablecoins along with their circulating amounts.

        Args:
            include_prices (bool): Whether to include current stablecoin prices (default: True)

        Returns:
            List[models.Stablecoin]: List of all stablecoins with their circulating amounts

        API Endpoint: GET /stablecoins
        """
        params = {"includePrices": include_prices}
        data = self._request(
            "GET", f"{self.STABLECOINS_URL}/stablecoins", params=params
        )
        # The API returns {"peggedAssets": [...]}
        if isinstance(data, dict) and "peggedAssets" in data:
            return models.Stablecoins.validate_python(data["peggedAssets"])
        return models.Stablecoins.validate_python(data)

    async def get_stablecoins_async(
        self, include_prices: bool = True
    ) -> List[models.Stablecoin]:
        """
        List all stablecoins along with their circulating amounts (async).

        Args:
            include_prices (bool): Whether to include current stablecoin prices (default: True)

        Returns:
            List[models.Stablecoin]: List of all stablecoins with their circulating amounts

        API Endpoint: GET /stablecoins
        """
        params = {"includePrices": include_prices}
        data = await self._async_request(
            "GET", f"{self.STABLECOINS_URL}/stablecoins", params=params
        )
        # The API returns {"peggedAssets": [...]}
        if isinstance(data, dict) and "peggedAssets" in data:
            return models.Stablecoins.validate_python(data["peggedAssets"])
        return models.Stablecoins.validate_python(data)

    def get_stablecoin_charts(
        self, chain: Optional[str] = None, stablecoin: Optional[int] = None
    ) -> List[models.StablecoinChart]:
        """
        Get historical market cap sum of all stablecoins or stablecoins in a specific chain.

        Args:
            chain (Optional[str]): Chain slug (e.g., "Ethereum"). If None, returns data for all chains.
            stablecoin (Optional[int]): Stablecoin ID from /stablecoins endpoint. If None, returns data for all stablecoins.

        Returns:
            List[models.StablecoinChart]: Historical market cap data for stablecoins

        API Endpoint: GET /stablecoincharts/all or GET /stablecoincharts/{chain}
        """
        endpoint = "/stablecoincharts/all"
        if chain:
            endpoint = f"/stablecoincharts/{chain}"
        params = {}
        if stablecoin:
            params["stablecoin"] = stablecoin
        data = self._request("GET", f"{self.STABLECOINS_URL}{endpoint}", params=params)
        # The API returns a list of chart data points
        return models.StablecoinCharts.validate_python(data)

    async def get_stablecoin_charts_async(
        self, chain: Optional[str] = None, stablecoin: Optional[int] = None
    ) -> List[models.StablecoinChart]:
        """
        Get historical market cap sum of all stablecoins or stablecoins in a specific chain (async).

        Args:
            chain (Optional[str]): Chain slug (e.g., "Ethereum"). If None, returns data for all chains.
            stablecoin (Optional[int]): Stablecoin ID from /stablecoins endpoint. If None, returns data for all stablecoins.

        Returns:
            List[models.StablecoinChart]: Historical market cap data for stablecoins

        API Endpoint: GET /stablecoincharts/all or GET /stablecoincharts/{chain}
        """
        endpoint = "/stablecoincharts/all"
        if chain:
            endpoint = f"/stablecoincharts/{chain}"
        params = {}
        if stablecoin:
            params["stablecoin"] = stablecoin
        data = await self._async_request(
            "GET", f"{self.STABLECOINS_URL}{endpoint}", params=params
        )
        # The API returns a list of chart data points
        return models.StablecoinCharts.validate_python(data)

    def get_stablecoin_historical(self, asset_id: int) -> models.StablecoinHistorical:
        """
        Get historical market cap and historical chain distribution of a stablecoin.

        Args:
            asset_id (int): Stablecoin ID from /stablecoins endpoint

        Returns:
            models.StablecoinHistorical: Historical data for the specified stablecoin

        API Endpoint: GET /stablecoin/{asset}
        """
        data = self._request("GET", f"{self.STABLECOINS_URL}/stablecoin/{asset_id}")
        return models.StablecoinHistorical.model_validate(data)

    async def get_stablecoin_historical_async(
        self, asset_id: int
    ) -> models.StablecoinHistorical:
        """
        Get historical market cap and historical chain distribution of a stablecoin (async).

        Args:
            asset_id (int): Stablecoin ID from /stablecoins endpoint

        Returns:
            models.StablecoinHistorical: Historical data for the specified stablecoin

        API Endpoint: GET /stablecoin/{asset}
        """
        data = await self._async_request(
            "GET", f"{self.STABLECOINS_URL}/stablecoin/{asset_id}"
        )
        return models.StablecoinHistorical.model_validate(data)

    def get_stablecoin_chains(self) -> List[models.StablecoinChainData]:
        """
        Get current market cap sum of all stablecoins on each chain.

        Returns:
            List[models.StablecoinChainData]: Market cap data for stablecoins on each chain

        API Endpoint: GET /stablecoinchains
        """
        data = self._request("GET", f"{self.STABLECOINS_URL}/stablecoinchains")
        # The API returns a list of chain data
        return models.StablecoinChains.validate_python(data)

    async def get_stablecoin_chains_async(self) -> List[models.StablecoinChainData]:
        """
        Get current market cap sum of all stablecoins on each chain (async).

        Returns:
            List[models.StablecoinChainData]: Market cap data for stablecoins on each chain

        API Endpoint: GET /stablecoinchains
        """
        data = await self._async_request(
            "GET", f"{self.STABLECOINS_URL}/stablecoinchains"
        )
        # The API returns a list of chain data
        return models.StablecoinChains.validate_python(data)

    def get_stablecoin_prices(self) -> List[models.StablecoinPrice]:
        """
        Get historical prices of all stablecoins.

        Returns:
            List[models.StablecoinPrice]: Historical price data for all stablecoins

        API Endpoint: GET /stablecoinprices
        """
        data = self._request("GET", f"{self.STABLECOINS_URL}/stablecoinprices")
        # The API returns a list of price data
        return models.StablecoinPrices.validate_python(data)

    async def get_stablecoin_prices_async(self) -> List[models.StablecoinPrice]:
        """
        Get historical prices of all stablecoins (async).

        Returns:
            List[models.StablecoinPrice]: Historical price data for all stablecoins

        API Endpoint: GET /stablecoinprices
        """
        data = await self._async_request(
            "GET", f"{self.STABLECOINS_URL}/stablecoinprices"
        )
        # The API returns a list of price data
        return models.StablecoinPrices.validate_python(data)

    def get_pools(self) -> List[models.Pool]:
        """
        Retrieve the latest data for all pools, including enriched information such as predictions.

        Returns:
            List[models.Pool]: List of all yield farming pools with their current data

        API Endpoint: GET /pools
        """
        data = self._request("GET", f"{self.YIELDS_URL}/pools")
        # The API returns {"data": [...], "status": "success"}
        if isinstance(data, dict) and "data" in data:
            return models.Pools.validate_python(data["data"])
        return models.Pools.validate_python(data)

    async def get_pools_async(self) -> List[models.Pool]:
        """
        Retrieve the latest data for all pools, including enriched information such as predictions (async).

        Returns:
            List[models.Pool]: List of all yield farming pools with their current data

        API Endpoint: GET /pools
        """
        data = await self._async_request("GET", f"{self.YIELDS_URL}/pools")
        # The API returns {"data": [...], "status": "success"}
        if isinstance(data, dict) and "data" in data:
            return models.Pools.validate_python(data["data"])
        return models.Pools.validate_python(data)

    def get_pool_chart(self, pool_id: str) -> List[models.PoolChart]:
        """
        Get historical APY and TVL of a pool.

        Args:
            pool_id (str): Pool ID, can be retrieved from /pools (property is called pool)

        Returns:
            List[models.PoolChart]: Historical APY and TVL data for the specified pool

        API Endpoint: GET /chart/{pool}
        """
        data = self._request("GET", f"{self.YIELDS_URL}/chart/{pool_id}")
        return models.PoolCharts.validate_python(data)

    async def get_pool_chart_async(self, pool_id: str) -> List[models.PoolChart]:
        """
        Get historical APY and TVL of a pool (async).

        Args:
            pool_id (str): Pool ID, can be retrieved from /pools (property is called pool)

        Returns:
            List[models.PoolChart]: Historical APY and TVL data for the specified pool

        API Endpoint: GET /chart/{pool}
        """
        data = await self._async_request("GET", f"{self.YIELDS_URL}/chart/{pool_id}")
        return models.PoolCharts.validate_python(data)

    # TODO: fix this. it's not returning all the data.
    def get_dexs(
        self,
        chain: Optional[str] = None,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
    ) -> models.DexOverview:
        """
        List all DEXs along with summaries of their volumes and dataType history data.

        Args:
            chain (Optional[str]): Chain name to filter by. List of supported chains can be found
                                  under allChains attribute in /overview/dexs response.
            exclude_total_data_chart (bool): True to exclude aggregated chart from response (default: True)
            exclude_total_data_chart_breakdown (bool): True to exclude broken down chart from response (default: True)

        Returns:
            models.DexOverview: Overview of all DEXs with their volume data

        API Endpoint: GET /overview/dexs or GET /overview/dexs/{chain}
        """
        endpoint = "/overview/dexs"
        if chain:
            endpoint = f"{endpoint}/{chain}"
        params = {
            "excludeTotalDataChart": exclude_total_data_chart,
            "excludeTotalDataChartBreakdown": exclude_total_data_chart_breakdown,
        }
        data = self._request("GET", f"{self.BASE_URL}{endpoint}", params=params)
        # The API returns a summary object, not a list
        return models.DexOverview.model_validate(data)

    # TODO: fix this. it's not returning all the data.
    async def get_dexs_async(
        self,
        chain: Optional[str] = None,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
    ) -> models.DexOverview:
        """
        List all DEXs along with summaries of their volumes and dataType history data (async).

        Args:
            chain (Optional[str]): Chain name to filter by. List of supported chains can be found
                                  under allChains attribute in /overview/dexs response.
            exclude_total_data_chart (bool): True to exclude aggregated chart from response (default: True)
            exclude_total_data_chart_breakdown (bool): True to exclude broken down chart from response (default: True)

        Returns:
            models.DexOverview: Overview of all DEXs with their volume data

        API Endpoint: GET /overview/dexs or GET /overview/dexs/{chain}
        """
        endpoint = "/overview/dexs"
        if chain:
            endpoint = f"{endpoint}/{chain}"
        params = {
            "excludeTotalDataChart": exclude_total_data_chart,
            "excludeTotalDataChartBreakdown": exclude_total_data_chart_breakdown,
        }
        data = await self._async_request(
            "GET", f"{self.BASE_URL}{endpoint}", params=params
        )
        # The API returns a summary object, not a list
        return models.DexOverview.model_validate(data)

    # TODO: fix this. it's failing to validate the data.
    def get_dex_summary(
        self,
        protocol_slug: str,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
    ) -> models.Dex:
        """
        Get summary of DEX volume with historical data.

        Args:
            protocol_slug (str): Protocol slug (e.g., "uniswap", "sushiswap")
            exclude_total_data_chart (bool): True to exclude aggregated chart from response (default: True)
            exclude_total_data_chart_breakdown (bool): True to exclude broken down chart from response (default: True)

        Returns:
            models.Dex: Summary of DEX volume with historical data

        API Endpoint: GET /summary/dexs/{protocol}
        """
        params = {
            "excludeTotalDataChart": exclude_total_data_chart,
            "excludeTotalDataChartBreakdown": exclude_total_data_chart_breakdown,
        }
        data = self._request(
            "GET", f"{self.BASE_URL}/summary/dexs/{protocol_slug}", params=params
        )
        return models.Dex.model_validate(data)

    # TODO: fix this. it's failing to validate the data.
    async def get_dex_summary_async(
        self,
        protocol_slug: str,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
    ) -> models.Dex:
        """
        Get summary of DEX volume with historical data (async).

        Args:
            protocol_slug (str): Protocol slug (e.g., "uniswap", "sushiswap")
            exclude_total_data_chart (bool): True to exclude aggregated chart from response (default: True)
            exclude_total_data_chart_breakdown (bool): True to exclude broken down chart from response (default: True)

        Returns:
            models.Dex: Summary of DEX volume with historical data

        API Endpoint: GET /summary/dexs/{protocol}
        """
        params = {
            "excludeTotalDataChart": exclude_total_data_chart,
            "excludeTotalDataChartBreakdown": exclude_total_data_chart_breakdown,
        }
        data = await self._async_request(
            "GET", f"{self.BASE_URL}/summary/dexs/{protocol_slug}", params=params
        )
        return models.Dex.model_validate(data)

    def get_options_dexs(
        self,
        chain: Optional[str] = None,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        data_type: str = "dailyNotionalVolume",
    ) -> models.DexOverview:
        """
        List all options DEXs along with summaries of their volumes and dataType history data.

        Args:
            chain (Optional[str]): Chain name to filter by. List of supported chains can be found
                                  under allChains attribute in /overview/options response.
            exclude_total_data_chart (bool): True to exclude aggregated chart from response (default: True)
            exclude_total_data_chart_breakdown (bool): True to exclude broken down chart from response (default: True)
            data_type (str): Desired data type (default: "dailyNotionalVolume")
                           Options: "dailyPremiumVolume", "dailyNotionalVolume"

        Returns:
            models.DexOverview: Overview of all options DEXs with their volume data

        API Endpoint: GET /overview/options or GET /overview/options/{chain}
        """
        endpoint = "/overview/options"
        if chain:
            endpoint = f"{endpoint}/{chain}"
        params = {
            "excludeTotalDataChart": exclude_total_data_chart,
            "excludeTotalDataChartBreakdown": exclude_total_data_chart_breakdown,
            "dataType": data_type,
        }
        data = self._request("GET", f"{self.BASE_URL}{endpoint}", params=params)
        # The API returns a summary object, not a list
        return models.DexOverview.model_validate(data)

    async def get_options_dexs_async(
        self,
        chain: Optional[str] = None,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        data_type: str = "dailyNotionalVolume",
    ) -> models.DexOverview:
        """
        List all options DEXs along with summaries of their volumes and dataType history data (async).

        Args:
            chain (Optional[str]): Chain name to filter by. List of supported chains can be found
                                  under allChains attribute in /overview/options response.
            exclude_total_data_chart (bool): True to exclude aggregated chart from response (default: True)
            exclude_total_data_chart_breakdown (bool): True to exclude broken down chart from response (default: True)
            data_type (str): Desired data type (default: "dailyNotionalVolume")
                           Options: "dailyPremiumVolume", "dailyNotionalVolume"

        Returns:
            models.DexOverview: Overview of all options DEXs with their volume data

        API Endpoint: GET /overview/options or GET /overview/options/{chain}
        """
        endpoint = "/overview/options"
        if chain:
            endpoint = f"{endpoint}/{chain}"
        params = {
            "excludeTotalDataChart": exclude_total_data_chart,
            "excludeTotalDataChartBreakdown": exclude_total_data_chart_breakdown,
            "dataType": data_type,
        }
        data = await self._async_request(
            "GET", f"{self.BASE_URL}{endpoint}", params=params
        )
        # The API returns a summary object, not a list
        return models.DexOverview.model_validate(data)

    def get_options_dex_summary(
        self, protocol_slug: str, data_type: str = "dailyNotionalVolume"
    ) -> models.Dex:
        """
        Get summary of options DEX volume with historical data.

        Args:
            protocol_slug (str): Protocol slug (e.g., "derive", "lyra")
            data_type (str): Desired data type (default: "dailyNotionalVolume")
                           Options: "dailyPremiumVolume", "dailyNotionalVolume"

        Returns:
            models.Dex: Summary of options DEX volume with historical data

        API Endpoint: GET /summary/options/{protocol}
        """
        params = {"dataType": data_type}
        data = self._request(
            "GET", f"{self.BASE_URL}/summary/options/{protocol_slug}", params=params
        )
        return models.Dex.model_validate(data)

    async def get_options_dex_summary_async(
        self, protocol_slug: str, data_type: str = "dailyNotionalVolume"
    ) -> models.Dex:
        """
        Get summary of options DEX volume with historical data (async).

        Args:
            protocol_slug (str): Protocol slug (e.g., "derive", "lyra")
            data_type (str): Desired data type (default: "dailyNotionalVolume")
                           Options: "dailyPremiumVolume", "dailyNotionalVolume"

        Returns:
            models.Dex: Summary of options DEX volume with historical data

        API Endpoint: GET /summary/options/{protocol}
        """
        params = {"dataType": data_type}
        data = await self._async_request(
            "GET", f"{self.BASE_URL}/summary/options/{protocol_slug}", params=params
        )
        return models.Dex.model_validate(data)

    def get_fees(
        self,
        chain: Optional[str] = None,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        data_type: Literal["dailyFees", "dailyRevenue"] = "dailyFees",
    ) -> models.FeeOverview:
        """
        List all protocols along with summaries of their fees and revenue and dataType history data.

        Args:
            chain (Optional[str]): Chain name to filter by. List of supported chains can be found
                                  under allChains attribute in /overview/fees response.
            exclude_total_data_chart (bool): True to exclude aggregated chart from response (default: True)
            exclude_total_data_chart_breakdown (bool): True to exclude broken down chart from response (default: True)
            data_type (Literal["dailyFees", "dailyRevenue"]): Desired data type (default: "dailyFees")
                           Options: "dailyFees", "dailyRevenue"

        Returns:
            models.FeeOverview: Overview of all protocols with their fees and revenue data

        API Endpoint: GET /overview/fees or GET /overview/fees/{chain}
        """
        endpoint = "/overview/fees"
        if chain:
            endpoint = f"{endpoint}/{chain}"
        params = {
            "excludeTotalDataChart": exclude_total_data_chart,
            "excludeTotalDataChartBreakdown": exclude_total_data_chart_breakdown,
            "dataType": data_type,
        }
        data = self._request("GET", f"{self.BASE_URL}{endpoint}", params=params)
        # The API returns a summary object, not a list
        return models.FeeOverview.model_validate(data)

    async def get_fees_async(
        self,
        chain: Optional[str] = None,
        exclude_total_data_chart: bool = True,
        exclude_total_data_chart_breakdown: bool = True,
        data_type: Literal["dailyFees", "dailyRevenue"] = "dailyFees",
    ) -> models.FeeOverview:
        """
        List all protocols along with summaries of their fees and revenue and dataType history data (async).

        Args:
            chain (Optional[str]): Chain name to filter by. List of supported chains can be found
                                  under allChains attribute in /overview/fees response.
            exclude_total_data_chart (bool): True to exclude aggregated chart from response (default: True)
            exclude_total_data_chart_breakdown (bool): True to exclude broken down chart from response (default: True)
            data_type (Literal["dailyFees", "dailyRevenue"]): Desired data type (default: "dailyFees")
                           Options: "dailyFees", "dailyRevenue"

        Returns:
            models.FeeOverview: Overview of all protocols with their fees and revenue data

        API Endpoint: GET /overview/fees or GET /overview/fees/{chain}
        """
        endpoint = "/overview/fees"
        if chain:
            endpoint = f"{endpoint}/{chain}"
        params = {
            "excludeTotalDataChart": exclude_total_data_chart,
            "excludeTotalDataChartBreakdown": exclude_total_data_chart_breakdown,
            "dataType": data_type,
        }
        data = await self._async_request(
            "GET", f"{self.BASE_URL}{endpoint}", params=params
        )
        # The API returns a summary object, not a list
        return models.FeeOverview.model_validate(data)

    def get_fee_summary(
        self,
        protocol_slug: str,
        data_type: Literal["dailyFees", "dailyRevenue"] = "dailyFees",
    ) -> models.Fee:
        """
        Get summary of protocol fees and revenue with historical data.

        Args:
            protocol_slug (str): Protocol slug (e.g., "uniswap", "aave")
            data_type (Literal["dailyFees", "dailyRevenue"]): Desired data type (default: "dailyFees")
                           Options: "dailyFees", "dailyRevenue"

        Returns:
            models.Fee: Summary of protocol fees and revenue with historical data

        API Endpoint: GET /summary/fees/{protocol}
        """
        params = {"dataType": data_type}
        data = self._request(
            "GET", f"{self.BASE_URL}/summary/fees/{protocol_slug}", params=params
        )
        return models.Fee.model_validate(data)

    async def get_fee_summary_async(
        self,
        protocol_slug: str,
        data_type: Literal["dailyFees", "dailyRevenue"] = "dailyFees",
    ) -> models.Fee:
        """
        Get summary of protocol fees and revenue with historical data (async).

        Args:
            protocol_slug (str): Protocol slug (e.g., "uniswap", "aave")
            data_type (Literal["dailyFees", "dailyRevenue"]): Desired data type (default: "dailyFees")
                           Options: "dailyFees", "dailyRevenue"

        Returns:
            models.Fee: Summary of protocol fees and revenue with historical data

        API Endpoint: GET /summary/fees/{protocol}
        """
        params = {"dataType": data_type}
        data = await self._async_request(
            "GET", f"{self.BASE_URL}/summary/fees/{protocol_slug}", params=params
        )
        return models.Fee.model_validate(data)

    def close(self):
        """
        Close the synchronous HTTP client.

        This method should be called when you're done using the client to properly
        clean up resources and close the underlying HTTP connection.
        """
        self.client.close()

    async def aclose(self):
        """
        Close the asynchronous HTTP client.

        This method should be called when you're done using the client to properly
        clean up resources and close the underlying HTTP connection.
        """
        await self.async_client.aclose()
