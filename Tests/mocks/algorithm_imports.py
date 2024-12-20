from unittest.mock import MagicMock
import datetime as dt  # Import as dt to avoid naming conflicts
from dataclasses import dataclass, field
from typing import List, Union, Optional
from datetime import time  # Add this import

# At the top of the file, add List to be exported
List = List  # This makes List available for import from our mock

# Create datetime class with all needed components
datetime = dt.datetime
timedelta = dt.timedelta
date = dt.date

class Symbol:
    def __init__(self, ticker=None, security_type=None, market=None):
        self.Value = ticker
        self.SecurityType = security_type
        self.ID = MagicMock(market=market)

    @staticmethod
    def Create(symbol_str):
        mock = Symbol(symbol_str)
        return mock

    @staticmethod
    def create_option(underlying_symbol, market, option_style, right, strike_price, expiry_date):
        """Mock implementation of create_option"""
        mock = Symbol()
        mock.ID = MagicMock(
            underlying=MagicMock(symbol=underlying_symbol),
            market=market,
            option_style=option_style,
            option_right=right,
            strike_price=strike_price,
            date=expiry_date
        )
        mock.Value = f"{underlying_symbol}_{strike_price}_{right}_{expiry_date}"
        return mock

    @staticmethod
    def create_canonical_option(underlying_symbol, target_option, market=None, alias=None):
        """Mock implementation of create_canonical_option matching QC's implementation
        
        Args:
            underlying_symbol: The underlying symbol
            target_option: The target option ticker (e.g. SPXW)
            market: The market (defaults to underlying's market)
            alias: Optional alias for symbol cache
        """
        mock = Symbol()
        mock.ID = MagicMock(
            underlying=MagicMock(symbol=underlying_symbol),
            market=market or Market.USA,
            option_style="European",  # Default for index options
            date=None
        )
        mock.Value = f"{target_option}_CANONICAL_{market or Market.USA}"
        mock.Underlying = underlying_symbol
        return mock

    # Make create_canonical_option also available as a class attribute for testing
    create_canonical_option = MagicMock(side_effect=create_canonical_option.__func__)

class InsightDirection:
    """Mock of QuantConnect's InsightDirection enum"""
    Up = 1
    Down = -1
    Flat = 0

@dataclass
class Insight:
    """Mock of QuantConnect's Insight class"""
    Symbol: Union[str, Symbol] = None
    Type: str = "Price"
    Direction: float = InsightDirection.Up
    Period: timedelta = timedelta(days=1)
    Magnitude: float = 0.0
    Confidence: float = 0.0
    SourceModel: str = "MockModel"
    Weight: float = 0.0
    Id: str = "test_insight_id"

    def __post_init__(self):
        if isinstance(self.Symbol, str):
            self.Symbol = Symbol(self.Symbol)

    @staticmethod
    def Price(symbol, period, direction):
        """Mock implementation of static Price method"""
        return Insight(
            Symbol=symbol,
            Period=period,
            Direction=direction
        )

    @staticmethod
    def Group(insights):
        """Mock implementation of static Group method"""
        return insights if insights else []

@dataclass
class PortfolioTarget:
    """Mock of QuantConnect's PortfolioTarget class"""
    Symbol: Union[str, Symbol]
    Quantity: float
    Tag: str = ""

    def __post_init__(self):
        if isinstance(self.Symbol, str):
            self.Symbol = Symbol(self.Symbol)

    @staticmethod
    def percent(algorithm: 'QCAlgorithm', 
                symbol: Union['Symbol', str], 
                percent: float,
                return_delta_quantity: bool = False,
                tag: str = "") -> 'PortfolioTarget':
        """Mock implementation of percent method"""
        # Simple mock implementation
        mock_quantity = 100.0 * percent  # Simplified calculation
        return PortfolioTarget(symbol, mock_quantity, tag)

    def __str__(self) -> str:
        return f"PortfolioTarget({self.Symbol}, {self.Quantity}, {self.Tag})"

class Resolution:
    Minute = "Minute"
    Hour = "Hour"
    Daily = "Daily"

class OptionRight:
    """Mock of QuantConnect's OptionRight enum"""
    Call = "Call"
    Put = "Put"
    CALL = "Call"  # Add uppercase versions
    PUT = "Put"    # Add uppercase versions

    @staticmethod
    def create(right_str):
        """Helper method to create OptionRight from string"""
        right_str = right_str.lower()
        if right_str == "call":
            return OptionRight.Call
        elif right_str == "put":
            return OptionRight.Put
        return None

class Market:
    USA = "USA"

class Security:
    """Mock of QuantConnect's Security class"""
    def __init__(self, symbol=None):
        self.Symbol = symbol or Symbol.Create("TEST")
        self.Type = SecurityType.Equity
        self.Price = 100.0
        self.BidPrice = 0.95
        self.AskPrice = 1.05
        self.Close = 100.0
        self.IsTradable = True
        self.HasData = True
        self.Holdings = MagicMock(Quantity=0)
        self.VolatilityModel = None
        self.Expiry = datetime.now() + timedelta(days=30)
        
        # Greeks for options
        self.delta = None
        self.gamma = None
        self.theta = None
        self.vega = None
        self.rho = None
        self.iv = None

    def SetDataNormalizationMode(self, mode):
        pass

    def SetMarketPrice(self, price):
        self.Price = price

    def SetBuyingPowerModel(self, model):
        pass

    def SetFillModel(self, model):
        pass

    def SetFeeModel(self, model):
        pass

    def SetOptionAssignmentModel(self, model):
        pass

    def PriceModel(self, model):
        pass

class SecurityType:
    """Mock of QuantConnect's SecurityType enum"""
    Equity = "Equity"
    Option = "Option"
    IndexOption = "IndexOption"
    Index = "Index"
    Future = "Future"
    FutureOption = "FutureOption"

class TradeBar:
    """Mock of QuantConnect's TradeBar class"""
    def __init__(self, time, symbol, open_price, high, low, close, volume):
        self.Time = time
        self.Symbol = symbol
        self.Open = open_price
        self.High = high
        self.Low = low
        self.Close = close
        self.Volume = volume
        self.Value = close  # Usually the closing price is used as the value
        self.Period = timedelta(minutes=1)  # Default period

    def Update(self, price, volume=0):
        self.Close = price
        self.Value = price
        self.Volume += volume

class DataNormalizationMode:
    """Mock of QuantConnect's DataNormalizationMode enum"""
    Raw = "Raw"
    Adjusted = "Adjusted"
    SplitAdjusted = "SplitAdjusted"
    TotalReturn = "TotalReturn"

class BrokerageName:
    """Mock of QuantConnect's BrokerageName enum"""
    InteractiveBrokersBrokerage = "InteractiveBrokersBrokerage"
    TradierBrokerage = "TradierBrokerage"
    OandaBrokerage = "OandaBrokerage"

class AccountType:
    """Mock of QuantConnect's AccountType enum"""
    Margin = "Margin"
    Cash = "Cash"

class Securities(dict):
    """Mock of QuantConnect's Securities dictionary"""
    def __init__(self):
        super().__init__()
        self._default_security = MagicMock(
            BidPrice=0.95,
            AskPrice=1.05,
            Price=100.0,
            Close=100.0,
            IsTradable=True,
            Volume=1000,
            OpenInterest=100,
            symbol=MagicMock(
                ID=MagicMock(
                    StrikePrice=100.0,
                    Date=datetime.now() + timedelta(days=30)
                ),
                Value="TEST"
            )
        )
        # Configure the MagicMock to return actual values
        type(self._default_security).Volume = property(lambda x: 1000)
        type(self._default_security).OpenInterest = property(lambda x: 100)
        
        # Pre-populate with TEST symbol
        self["TEST"] = self._default_security
    
    def items(self):
        """Return a list of items to allow safe iteration"""
        return list(super().items())
    
    def clear(self):
        """Clear all items including default security"""
        super().clear()

    def __getitem__(self, key):
        if hasattr(key, 'Value'):
            key = key.Value
        return super().__getitem__(key)

    def __delitem__(self, key):
        if hasattr(key, 'Value'):
            key = key.Value
        if key in self:
            super().__delitem__(key)

    def __contains__(self, key):
        if hasattr(key, 'Value'):
            key = key.Value
        return super().__contains__(key)

class QCAlgorithm:
    def __init__(self):
        self.Securities = Securities()
        self.Portfolio = MagicMock(
            SetPositions=MagicMock()
        )
        self.Time = datetime.now()
        self.StartDate = datetime.now() - timedelta(days=30)
        self.EndDate = datetime.now() + timedelta(days=30)
        self.logLevel = 0
        self.Resolution = Resolution
        self.Log = MagicMock()
        self.Plot = MagicMock()
        self.openPositions = MagicMock(Count=0)
        self.timeResolution = Resolution.Minute
        self.optionContractsSubscriptions = []
        
        # Add missing attributes
        self.universe_settings = MagicMock(resolution=None)
        self.LiveMode = False
        self.strategies = []
        self._benchmark = None  # Add private benchmark variable
        
        # Add mocked methods for DataHandler tests
        self.AddEquity = MagicMock()
        self.AddIndex = MagicMock()
        self.AddOption = MagicMock()
        self.AddIndexOption = MagicMock()
        self.AddOptionContract = MagicMock()
        self.AddIndexOptionContract = MagicMock()
        self.SetBrokerageModel = MagicMock()
        self.RemoveSecurity = MagicMock()
        
        # Add new attributes
        self.charting = MagicMock(updateStats=MagicMock())
        self.TradingCalendar = MagicMock()
        
        # Add market order methods
        self.MarketOrder = MagicMock()
        self.ComboMarketOrder = MagicMock(return_value=[MagicMock(OrderId="123")])
        
        # Make SetBenchmark a MagicMock instead of a method
        self.SetBenchmark = MagicMock()

    @property
    def Benchmark(self):
        """Mock implementation of Benchmark property"""
        return self._benchmark

    def lastTradingDay(self, expiry):
        """Mock implementation of lastTradingDay"""
        if isinstance(expiry, datetime):
            return expiry.date()
        return expiry

    def GetLastKnownPrice(self, security):
        return MagicMock(Price=100.0)

    def AddChart(self, chart):
        pass

    def SetBrokerageModel(self, brokerage_name, account_type):
        """Mock implementation of SetBrokerageModel"""
        pass

    def RemoveSecurity(self, symbol):
        """Mock implementation of RemoveSecurity"""
        if symbol in self.Securities:
            del self.Securities[symbol]

class Greeks:
    """Mock of QuantConnect's Greeks class"""
    def __init__(self):
        self.delta = 0.0
        self.gamma = 0.0
        self.theta = 0.0
        self.vega = 0.0
        self.rho = 0.0

class OptionContract:
    """Mock of QuantConnect's OptionContract class"""
    def __init__(self, symbol=None, security=None):
        self._symbol = symbol or Symbol.Create("TEST")
        self._strike = 100.0
        self._expiry = datetime.now() + timedelta(days=30)
        self._right = OptionRight.Call
        self._greeks = Greeks()
        self._time = datetime.now()
        self._theoretical_price = 1.0
        self._implied_volatility = 0.2
        self._open_interest = 100
        self._last_price = 100.0
        self._volume = 1000
        self._bid_price = 0.95
        self._bid_size = 10
        self._ask_price = 1.05
        self._ask_size = 10
        self._underlying_last_price = 100.0
        self._underlying_symbol = "TEST"
        self._bsm_greeks = None  # Add BSM Greeks storage
        
        # Add symbol property structure
        self.symbol = MagicMock()
        self.symbol.ID = MagicMock()
        self.symbol.ID.StrikePrice = self._strike
        self.symbol.ID.Date = self._expiry
        self.symbol.Value = "TEST"
        self.symbol.Underlying = self._underlying_symbol

    @property
    def BSMGreeks(self):
        """Mock BSMGreeks property that persists"""
        if self._bsm_greeks is None:
            # Create a mock with Delta property that returns the stored delta
            self._bsm_greeks = MagicMock()
            self._bsm_greeks.Delta = self._greeks.delta
        return self._bsm_greeks

    @BSMGreeks.setter
    def BSMGreeks(self, value):
        """Allow setting BSMGreeks directly"""
        self._bsm_greeks = value

    # Properties with correct casing
    @property
    def greeks(self) -> Greeks:
        return self._greeks

    @property
    def implied_volatility(self) -> float:
        return self._implied_volatility

    # Keep other properties as they are...

    @property
    def Symbol(self) -> 'Symbol':
        return self.symbol

    @property
    def Strike(self) -> float:
        return self._strike

    @property
    def Expiry(self) -> datetime:
        return self._expiry

    @property
    def Right(self) -> 'OptionRight':
        return self._right

    @property
    def Time(self) -> datetime:
        return self._time

    @property
    def OpenInterest(self) -> int:
        return self._open_interest

    @property
    def Volume(self) -> int:
        return self._volume

    @property
    def BidPrice(self) -> float:
        return self._bid_price

    @property
    def AskPrice(self) -> float:
        return self._ask_price

    @property
    def Price(self) -> float:
        return self._last_price

    @property
    def UnderlyingSymbol(self) -> str:
        return self._underlying_symbol

    @property
    def UnderlyingLastPrice(self) -> float:
        return self._underlying_last_price

    @property
    def Underlying(self):
        """Returns the underlying symbol - this matches the actual implementation"""
        return self.symbol.Underlying

    def __str__(self) -> str:
        return f"OptionContract({self.Symbol}, {self.Strike}, {self.Expiry}, {self.Right})"

class OrderStatus:
    """Mock of QuantConnect's OrderStatus enum"""
    Invalid = "Invalid"
    CancelPending = "CancelPending"
    Canceled = "Canceled"
    Filled = "Filled"
    PartiallyFilled = "PartiallyFilled"
    Submitted = "Submitted"
    None_ = "None"

class SeriesType:
    Line = "Line"
    Scatter = "Scatter"
    Bar = "Bar"
    Candlestick = "Candlestick"

class Color:
    Red = "Red"
    Green = "Green"

class ScatterMarkerSymbol:
    Triangle = "Triangle"
    TriangleDown = "TriangleDown"

class Series:
    def __init__(self, name, series_type, unit, color=None, symbol=None):
        self.Name = name
        self.SeriesType = series_type
        self.Unit = unit
        self.Color = color
        self.Symbol = symbol

class CandlestickSeries(Series):
    def __init__(self, name, unit):
        super().__init__(name, SeriesType.Candlestick, unit)

class Chart:
    def __init__(self, name):
        self.Name = name
        self.Series = []

    def AddSeries(self, series):
        self.Series.append(series)

class BuyingPowerModel:
    """Mock of QuantConnect's BuyingPowerModel"""
    NULL = None
    
    def __init__(self):
        pass

    def GetMaximumOrderQuantityForTargetBuyingPower(self, *args, **kwargs):
        return MagicMock(Quantity=100)

    def GetLeverage(self, *args, **kwargs):
        return 1.0

    def GetReservedBuyingPowerForPosition(self, *args, **kwargs):
        return 0.0

class ImmediateFillModel:
    """Mock of QuantConnect's ImmediateFillModel"""
    def __init__(self):
        pass

    def MarketFill(self, order, security):
        return MagicMock(
            OrderEvent=MagicMock(
                OrderId=order.Id,
                Symbol=order.Symbol,
                Status=OrderStatus.Filled,
                FillPrice=security.Price,
                FillQuantity=order.Quantity
            )
        )

    def StopMarketFill(self, order, security):
        return self.MarketFill(order, security)

    def StopLimitFill(self, order, security):
        return self.MarketFill(order, security)

    def LimitFill(self, order, security):
        return self.MarketFill(order, security)

    def MarketOnCloseFill(self, order, security):
        return self.MarketFill(order, security)

    def MarketOnOpenFill(self, order, security):
        return self.MarketFill(order, security)

class SecurityPositionGroupModel:
    """Mock of QuantConnect's SecurityPositionGroupModel"""
    Null = None

class OptionPriceModels:
    """Mock of QuantConnect's OptionPriceModels"""
    @staticmethod
    def CrankNicolsonFD():
        return MagicMock()

class StandardDeviationOfReturnsVolatilityModel:
    """Mock of QuantConnect's StandardDeviationOfReturnsVolatilityModel"""
    def __init__(self, periods):
        self.periods = periods

    def Update(self, security, trade_bar):
        pass

class RiskManagementModel:
    """Mock of QuantConnect's RiskManagementModel class"""
    def __init__(self):
        pass

    def ManageRisk(self, algorithm: 'QCAlgorithm', targets: List['PortfolioTarget']) -> List['PortfolioTarget']:
        return targets

    def OnSecuritiesChanged(self, algorithm: 'QCAlgorithm', changes: 'SecurityChanges') -> None:
        pass

class SecurityChanges:
    """Mock of QuantConnect's SecurityChanges class"""
    def __init__(self, added_securities=None, removed_securities=None):
        self.AddedSecurities = added_securities or []
        self.RemovedSecurities = removed_securities or []

# Add this class with the other mock classes:

class PythonIndicator:
    """Mock of QuantConnect's PythonIndicator class"""
    def __init__(self, name):
        self.Name = name
        self.Current = MagicMock()
        self.IsReady = False
        self.WarmUpPeriod = 0

    def Update(self, input):
        pass

    def Reset(self):
        pass

    def BullLevels(self):
        return [100.0, 101.0, 102.0]  # Mock values

    def BearLevels(self):
        return [98.0, 97.0, 96.0]  # Mock values

# Add this class with other mock classes:

class SecuritiesDict(dict):
    """Mock of QuantConnect's Securities dictionary with special lookup behavior"""
    def ContainsKey(self, key):
        return str(key) in self
        
    def __getitem__(self, key):
        key_str = str(key)
        for k, v in self.items():
            if str(k) == key_str:
                return v
        return super().__getitem__(key)

# Add this class with the other mock classes:

class AlphaModel:
    """Mock of QuantConnect's AlphaModel base class"""
    def __init__(self):
        pass

    def Update(self, algorithm, data):
        """Mock implementation of Update method"""
        return []

    def OnSecuritiesChanged(self, algorithm, changes):
        """Mock implementation of OnSecuritiesChanged method"""
        pass

# Add this class with the other mock classes:

class Slice:
    """Mock of QuantConnect's Slice class"""
    def __init__(self):
        self.OptionChains = {}
        self.Bars = {}
        self.QuoteBars = {}
        self.Ticks = {}
        self.CustomData = {}
        self.Time = datetime.now()
        self.HasData = True
        self.ContainsKey = MagicMock(return_value=True)

    def __getitem__(self, key):
        """Allow dictionary-style access to data"""
        if key in self.Bars:
            return self.Bars[key]
        if key in self.OptionChains:
            return self.OptionChains[key]
        if key in self.QuoteBars:
            return self.QuoteBars[key]
        if key in self.Ticks:
            return self.Ticks[key]
        return None

    def ContainsKey(self, key):
        """Mock implementation of ContainsKey"""
        return key in self.Bars or key in self.OptionChains or key in self.QuoteBars or key in self.Ticks

class PythonData:
    """Mock of QuantConnect's PythonData base class"""
    def __init__(self):
        self.Symbol = None
        self.Time = datetime.now()
        self.Value = 0.0
        self.Price = 0.0
        self.EndTime = datetime.now()

    def GetSource(self, config, date, isLiveMode):
        """Mock implementation of GetSource"""
        return None, False

    def Reader(self, config, line, date, isLiveMode):
        """Mock implementation of Reader"""
        return None

    def DefaultResolution(self):
        """Mock implementation of DefaultResolution"""
        return Resolution.Minute

# Add this class with the other mock classes:

class ExecutionModel:
    """Mock of QuantConnect's ExecutionModel base class"""
    def __init__(self):
        pass

    def Execute(self, algorithm, targets):
        """Mock implementation of Execute method"""
        pass

    def OnSecuritiesChanged(self, algorithm, changes):
        """Mock implementation of OnSecuritiesChanged method"""
        pass

# Add this class with the other mock classes:

class PortfolioTargetCollection:
    """Mock of QuantConnect's PortfolioTargetCollection class"""
    def __init__(self):
        self._targets = []
        self.IsEmpty = True

    def AddRange(self, targets):
        """Mock implementation of AddRange"""
        if targets:
            self._targets.extend(targets)
            self.IsEmpty = len(self._targets) == 0

    def ClearFulfilled(self, algorithm):
        """Mock implementation of ClearFulfilled"""
        pass

    def __iter__(self):
        return iter(self._targets)

    def __len__(self):
        return len(self._targets)

# Add this class with the other mock classes:
class Leg:
    """Mock of QuantConnect's Leg class"""
    def __init__(self, symbol=None, ratio=1):
        self.Symbol = symbol
        self.Ratio = ratio

    @staticmethod
    def Create(symbol, ratio=1):
        """Mock implementation of Create method"""
        return Leg(symbol, ratio)

# Add this class with the other mock classes:
class UpdateOrderFields:
    """Mock of QuantConnect's UpdateOrderFields class"""
    def __init__(self):
        self.LimitPrice = None
        self.StopPrice = None
        self.Quantity = None
        self.Tag = None

    def __str__(self):
        return f"UpdateOrderFields(LimitPrice={self.LimitPrice}, StopPrice={self.StopPrice}, Quantity={self.Quantity}, Tag={self.Tag})"

class PortfolioConstructionModel:
    """Mock of QuantConnect's PortfolioConstructionModel class"""
    def __init__(self):
        pass

    def CreateTargets(self, algorithm, insights):
        """Mock implementation of CreateTargets method"""
        return []

class Futures:
    """Mock of QuantConnect's Futures class"""
    class Indices:
        SP_500_E_MINI = "ES"  # E-mini S&P 500 Future

# Export all the mocks
__all__ = [
    'Resolution',
    'OptionRight',
    'Market',
    'Symbol',
    'Security',
    'SecurityType',
    'TradeBar',
    'DataNormalizationMode',
    'BrokerageName',
    'AccountType',
    'QCAlgorithm',
    'Insight',
    'InsightDirection',
    'PortfolioTarget',
    'OptionContract',
    'datetime',
    'timedelta',
    'date',
    'time',
    'OrderStatus',
    'SeriesType',
    'Color',
    'ScatterMarkerSymbol',
    'Series',
    'CandlestickSeries',
    'Chart',
    'BuyingPowerModel',
    'ImmediateFillModel',
    'SecurityPositionGroupModel',
    'OptionPriceModels',
    'StandardDeviationOfReturnsVolatilityModel',
    'RiskManagementModel',
    'List',
    'SecurityChanges',
    'PythonIndicator',
    'SecuritiesDict',
    'AlphaModel',
    'Slice',
    'PythonData',
    'ExecutionModel',
    'PortfolioTargetCollection',
    'Leg',
    'UpdateOrderFields',
    'PortfolioConstructionModel',
    'Futures'
] 