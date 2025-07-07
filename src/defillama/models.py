from __future__ import annotations

from pydantic import BaseModel, Field, TypeAdapter, AnyHttpUrl
from typing import List, Dict, Optional, Union, Any
from datetime import datetime


class Protocol(BaseModel):
    """Protocol model for /protocols endpoint"""

    id: str
    name: str
    address: Optional[str] = None
    symbol: str
    url: Optional[AnyHttpUrl | str] = Field(None)
    description: Optional[str] = None
    chain: Optional[str] = None
    logo: Optional[str] = None
    chains: List[str]
    gecko_id: Optional[str] = Field(None)
    cmcId: Optional[str] = None
    category: str
    tvl: Optional[float] = None
    chainTvls: Dict[str, float]
    change_1h: Optional[float] = Field(None)
    change_1d: Optional[float] = Field(None)
    change_7d: Optional[float] = Field(None)


Protocols = TypeAdapter(List[Protocol])


class Coin(BaseModel):
    """Coin model for price endpoints"""

    decimals: Optional[int] = None
    price: Optional[float] = None
    symbol: Optional[str] = None
    timestamp: Optional[int] = None
    confidence: Optional[float] = None


class CoinPrice(BaseModel):
    """Response model for /prices/current/{coins} and /prices/historical/{timestamp}/{coins}"""

    coins: Dict[str, Coin]


class HistoricalPrice(BaseModel):
    """Historical price data point"""

    timestamp: int
    price: float
    confidence: Optional[float] = None


class CoinHistoricalData(BaseModel):
    """Historical data for a coin in batch responses"""

    symbol: str
    prices: List[HistoricalPrice]


class BatchHistoricalPrices(BaseModel):
    """Response model for /batchHistorical"""

    coins: Dict[str, CoinHistoricalData]


class CoinChartData(BaseModel):
    """Chart data for a coin"""

    decimals: Optional[int] = None
    confidence: Optional[float] = None
    prices: List[HistoricalPrice]
    symbol: str


class PriceChart(BaseModel):
    """Response model for /chart/{coins}"""

    coins: Dict[str, CoinChartData]


class PercentageChange(BaseModel):
    """Response model for /percentage/{coins}"""

    coins: Dict[str, float]


class Block(BaseModel):
    """Response model for /block/{chain}/{timestamp}"""

    height: int
    timestamp: int


class HistoricalTvl(BaseModel):
    """Historical TVL data point"""

    date: datetime
    tvl: float


HistoricalTvls = TypeAdapter(List[HistoricalTvl])


class TokenHistory(BaseModel):
    """Token history data point"""

    date: int
    tokens: Dict[str, float]


class ChainTvlDetails(BaseModel):
    """Chain TVL details"""

    tvl: List[HistoricalTvl]
    tokens: Optional[List[TokenHistory]] = None
    tokensInUsd: Optional[List[TokenHistory]] = None


class ProtocolDetails(Protocol):
    """Protocol details model for /protocol/{protocol}"""

    class ProtocolHistoricalTvl(BaseModel):
        """Protocol historical TVL data point"""

        date: datetime
        totalLiquidityUSD: float

    class ProtocolChainTvlDetails(BaseModel):
        """Protocol chain TVL details"""

        tvl: List["ProtocolDetails.ProtocolHistoricalTvl"] = Field(
            default_factory=list, alias="tvl"
        )
        tokens: Optional[List[TokenHistory]] = Field(default=None)
        tokensInUsd: Optional[List[TokenHistory]] = Field(default=None)

    tvl: List[ProtocolHistoricalTvl] = Field(default_factory=list, alias="tvl")
    tokens: Optional[List[TokenHistory]] = Field(default=None)
    tokensInUsd: Optional[List[TokenHistory]] = Field(default=None)
    chainTvls: Dict[str, ProtocolChainTvlDetails]


class Chain(BaseModel):
    """Chain model for /v2/chains"""

    gecko_id: Optional[str] = Field(None)
    tvl: Optional[float] = None
    tokenSymbol: Optional[str] = None
    cmcId: Optional[str] = None
    name: str
    chainId: Optional[int] = None


Chains = TypeAdapter(List[Chain])


class Stablecoin(BaseModel):
    """Stablecoin model for /stablecoins"""

    id: str
    name: str
    symbol: str
    gecko_id: Optional[str] = Field(None)
    pegType: str
    priceSource: Optional[str] = None
    pegMechanism: str
    circulating: Dict[str, float]
    circulatingPrevDay: Optional[Union[Dict[str, float], int]] = None
    circulatingPrevWeek: Optional[Union[Dict[str, float], int]] = None
    circulatingPrevMonth: Optional[Union[Dict[str, float], int]] = None
    price: Optional[float] = None
    chainCirculating: Optional[Dict[str, Dict[str, Union[Dict[str, float], int]]]] = (
        None
    )


Stablecoins = TypeAdapter(List[Stablecoin])


class StablecoinChart(BaseModel):
    """Stablecoin chart data point"""

    date: str  # API returns date as string
    totalCirculating: Dict[str, float]
    totalCirculatingUSD: Dict[str, float]


StablecoinCharts = TypeAdapter(List[StablecoinChart])


class StablecoinHistorical(BaseModel):
    """Stablecoin historical data"""

    id: str
    name: str
    address: Optional[str] = None
    symbol: str
    url: Optional[str] = None
    description: Optional[str] = None
    mintRedeemDescription: Optional[str] = None
    onCoinGecko: Optional[str] = None
    gecko_id: Optional[str] = None
    cmcId: Optional[str] = None
    pegType: str
    pegMechanism: str
    priceSource: Optional[str] = None
    auditLinks: Optional[List[str]] = None
    twitter: Optional[str] = None
    wiki: Optional[str] = None
    chainBalances: Optional[Dict[str, Dict[str, Any]]] = None


class StablecoinChainData(BaseModel):
    """Stablecoin chain data"""

    gecko_id: Optional[str] = None
    totalCirculatingUSD: Dict[str, float]
    tokenSymbol: Optional[str] = None
    name: str


StablecoinChains = TypeAdapter(List[StablecoinChainData])


class StablecoinPrice(BaseModel):
    """Stablecoin price data"""

    id: str
    price: float
    timestamp: int


StablecoinPrices = TypeAdapter(List[StablecoinPrice])


class Pool(BaseModel):
    """Pool model for /pools"""

    chain: str
    project: str
    symbol: str
    tvlUsd: float
    apyBase: Optional[float] = None
    apyReward: Optional[float] = None
    apy: float
    rewardTokens: Optional[List[Optional[str]]] = None
    pool: str
    apyPct1D: Optional[float] = None
    apyPct7D: Optional[float] = None
    apyPct30D: Optional[float] = None
    stablecoin: bool
    ilRisk: Optional[str] = None
    exposure: Optional[str] = None
    predictions: Optional[Dict[str, Any]] = None


Pools = TypeAdapter(List[Pool])


class PoolChart(BaseModel):
    """Pool chart data point"""

    timestamp: int
    apy: float
    tvlUsd: float


PoolCharts = TypeAdapter(List[PoolChart])


class Volume(BaseModel):
    """Volume data point"""

    totalVolume: float
    dailyVolume: Optional[float] = None
    timestamp: int


class Dex(BaseModel):
    """DEX model for volume endpoints"""

    name: str
    category: str
    totalVolume: float
    dailyVolume: Optional[float] = None
    monthlyVolume: Optional[float] = None
    chains: Optional[List[str]] = None
    methodologyURL: Optional[str] = None
    methodology: Optional[Dict[str, str]] = None
    allChains: Optional[List[str]] = None
    totalDataChart: Optional[List[List[Union[int, float]]]] = None
    totalDataChartBreakdown: Optional[List[List[Union[int, float]]]] = None


class DexOverview(BaseModel):
    """DEX overview model for /overview/dexs"""

    totalDataChart: List[List[Union[int, float]]]
    totalDataChartBreakdown: List[List[Union[int, float]]]
    breakdown24h: Optional[Dict[str, Any]] = None
    breakdown30d: Optional[Dict[str, Any]] = None
    chain: Optional[str] = None
    allChains: List[str]


Dexes = TypeAdapter(List[Dex])


class Fee(BaseModel):
    """Fee model for fees and revenue endpoints"""

    name: str
    category: str
    dailyFees: Optional[float] = None
    dailyRevenue: Optional[float] = None
    totalFees: float
    totalRevenue: float
    chains: Optional[List[str]] = None
    methodologyURL: Optional[str] = None
    methodology: Optional[Dict[str, str]] = None
    allChains: Optional[List[str]] = None
    totalDataChart: Optional[List[List[Union[int, float]]]] = None
    totalDataChartBreakdown: Optional[List[List[Union[int, float]]]] = None


class FeeOverview(BaseModel):
    """Fee overview model for /overview/fees"""

    totalDataChart: List[List[Union[int, float]]]
    totalDataChartBreakdown: List[List[Union[int, float]]]
    breakdown24h: Optional[Dict[str, Any]] = None
    breakdown30d: Optional[Dict[str, Any]] = None
    chain: Optional[str] = None
    allChains: List[str]


Fees = TypeAdapter(List[Fee])


class Yield(BaseModel):
    """Yield model (alias for Pool)"""

    chain: str
    project: str
    symbol: str
    tvlUsd: float
    apyBase: Optional[float] = None
    apyReward: Optional[float] = None
    apy: float
    rewardTokens: Optional[List[Optional[str]]] = None
    pool: str
    apyPct1D: Optional[float] = None
    apyPct7D: Optional[float] = None
    apyPct30D: Optional[float] = None
    stablecoin: bool
    ilRisk: Optional[str] = None
    exposure: Optional[str] = None
    predictions: Optional[Dict[str, Any]] = None
    poolMeta: Optional[str] = None
    mu: Optional[float] = None
    sigma: Optional[float] = None
    underlyingTokens: Optional[List[str]] = None
    il7d: Optional[float] = None
    apyBase7d: Optional[float] = None
