# Avoid flags

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset-complete-extension/categories/2149347727/posts/2154129460

```python
from dataclasses import dataclass

@dataclass
class BitcoinWallet:
    balance: int = 0  # in satoshi

    def place_order(self, amount: int, sell: bool = False) -> None:
        if sell:
            if amount > self.balance:
                raise NotEnoughFundsError(amount, self.balance)
            print(f"Selling {amount * SATOSHI_TO_BTC_RATE} BTC.")
            self.balance -= amount
        else:
            print(f"Buying {amount * SATOSHI_TO_BTC_RATE} BTC.")
            self.balance += amount
```
Using flag like `sell` in example above indicates, that functions tries to do too many things. It's better to split it 
into many functions focused on particular action.

```python
@dataclass
class BitcoinWallet:
    balance: int = 0  # in satoshi

    def buy(self, amount: int) -> None:
        print(f"Buying {amount * SATOSHI_TO_BTC_RATE} BTC.")
        self.balance += amount

    def sell(self, amount: int) -> None:
        if amount > self.balance:
            raise NotEnoughFundsError(amount, self.balance)
        print(f"Selling {amount * SATOSHI_TO_BTC_RATE} BTC.")
        self.balance -= amount
```