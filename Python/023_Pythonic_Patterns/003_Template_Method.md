# Template method

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-pythonic-patterns/categories/2149946548/posts/2160000213

## Initial code
```python
# main.py
from bitcoin import BitcoinTradingBot
from ethereum import EthereumTradingBot


def main():
    bitcoin_trader = BitcoinTradingBot()
    bitcoin_trader.trade()

    ethereum_trader = EthereumTradingBot()
    ethereum_trader.trade()

```
```python
# bitcoin.py

class BitcoinTradingBot:
    ...
    def trade(self) -> None:
    prices = self.get_price_data()
    amount = self.get_amount()

    if self.should_buy(prices):
        self.buy(amount)
    if self.should_sell(prices):
        self.sell(amount)
```
```python
# ethereum.py

class EthereumTradingBot:
    ...
    def trade(self) -> None:
    prices = self.get_price_data()
    amount = self.get_amount()

    if self.should_buy(prices):
        self.buy(amount)
    if self.should_sell(prices):
        self.sell(amount)
```
* Two TradingBot classes with some differences, but with the same, crucial `.trade()` method.

## Template method pattern

```mermaid
classDiagram
    class AbstractClass {
        <<abstract>>
        templateMethod()
        primitive1()*
        primitive2()*
        primitive3()*
    }
    class ConcreteClassA {
        primitive1()
        primitive2()
        primitive3()
    }
    class ConcreteClassB {
        primitive1()
        primitive2()
        primitive3()
    }
    AbstractClass <|-- ConcreteClassA
    AbstractClass <|-- ConcreteClassB
```

Algorithms stays the same, components changes.

```mermaid
classDiagram
    class TradingBot {
        <<abstract>>
        trade()
        buy(amount: int)*
        sell(amount)*
        should_buy(prices: list[int])*
        should_sell(prices: list[int])*
        get_price_data()*
        get_amount()*
    }
    class BitcoinTradingBot {
        buy(amount: int)
        sell(amount)
        should_buy(prices: list[int])
        should_sell(prices: list[int])
        get_price_data()
        get_amount()
    }
    class EthereumTradingBot {
        buy(amount: int)
        sell(amount)
        should_buy(prices: list[int])
        should_sell(prices: list[int])
        get_price_data()
        get_amount()
    }
    TradingBot <|-- BitcoinTradingBot
    TradingBot <|-- EthereumTradingBot
```