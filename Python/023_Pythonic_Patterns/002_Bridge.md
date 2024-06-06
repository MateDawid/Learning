# Bridge

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2149946548/posts/2160000213

## Initial code

```python
def main() -> None:
    # symbol we trade on
    symbol = "BTC/USD"
    trade_amount = 10

    # create the exchange
    exchange = Coinbase()
    
    exchange.buy(symbol, trade_amount)
```
* Specific exchange method declared in `main()` function
* No strategy for TradingBot specified yet

## Bridge pattern

```mermaid
classDiagram
    class Abstraction {
        <<abstract>>
    }
    RefinedAbstraction1 --|> Abstraction
    RefinedAbstraction2 --|> Abstraction
    class Implementation {
        <<abstract>>
        +implementation()
    }
    Abstraction o-- Implementation : uses
    Implementation <|-- ConcreteImplementation1
    Implementation <|-- ConcreteImplementation2
    ConcreteImplementation1: +implementation()
    ConcreteImplementation2: +implementation()
```
* `Abstraction` uses `Implementation`
* `RefinedAbstraction` classes are strategies for `Abstraction`
* `ConcreteImplementation` classes are strategies for `Implementation`
* Bridge exists between `Abstraction` and `Implementation`
* `Abstraction` strategies know nothing about `Implementation` subclasses

```mermaid
classDiagram
    class Exchange {
        <<abstract>>
        +int[] get_prices(str symbol)
        +buy(str symbol, int amount)
        +sell(str symbol, int amount)
    }
    Exchange <|-- Binance
    Exchange <|-- Coinbase
    class TradingBot {
        <<abstract>>
        +run()
    }
    TradingBot o-- Exchange : uses
    TradingBot <|-- AvgTradingBot
    TradingBot <|-- MinMaxTradingBot
```
* `TradingBot` uses `Exchange`
* `AvgTradingBot` and `MinMaxTradingBot` classes are strategies for `TradingBot`
* `Binance` and `Coinbase` classes are strategies for `Exchange`
* Bridge exists between `TradingBot` and `Exchange`
* `TradingBot` strategies know nothing about `Exchange` subclasses