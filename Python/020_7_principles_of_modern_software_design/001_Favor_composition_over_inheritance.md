# Composition over inheritance

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150529699/posts/2153184357

## Example of calculating salary for employees

```python
from dataclasses import dataclass


@dataclass
class HourlyEmployee:
    name: str
    id: int
    commission: int = 10000
    contracts_landed: float = 0
    pay_rate: int = 0
    hours_worked: float = 0
    employer_cost: int = 100000

    def compute_pay(self) -> int:
        return int(
            self.pay_rate * self.hours_worked
            + self.employer_cost
            + self.commission * self.contracts_landed
        )


@dataclass
class SalariedEmployee:

    name: str
    id: int
    commission: int = 10000
    contracts_landed: float = 0
    monthly_salary: int = 0
    percentage: float = 1

    def compute_pay(self) -> int:
        return int(
            self.monthly_salary * self.percentage
            + self.commission * self.contracts_landed
        )


@dataclass
class Freelancer:

    name: str
    id: int
    commission: int = 10000
    contracts_landed: float = 0
    pay_rate: int = 0
    hours_worked: float = 0
    vat_number: str = ""

    def compute_pay(self) -> int:
        return int(
            self.pay_rate * self.hours_worked + self.commission * self.contracts_landed
        )


def main() -> None:

    henry = HourlyEmployee(name="Henry", id=12346, pay_rate=5000, hours_worked=100)
    print(f"{henry.name} earned ${(henry.compute_pay() / 100):.2f}.")

    sarah = SalariedEmployee(
        name="Sarah", id=47832, monthly_salary=500000, contracts_landed=10
    )
    print(f"{sarah.name} earned ${(sarah.compute_pay() / 100):.2f}.")


if __name__ == "__main__":
    main()
```

In this case we have three separate classes for three types of employees - `HourlyEmployee`, `SalariedEmployee` and `Freelancer`.

All of them has `compute_pay()` method defined and demands specific fields for pay calculation.

## Usual refactoring using inheritance

```python
from dataclasses import dataclass


@dataclass
class HourlyEmployee:
    name: str
    id: int
    pay_rate: int
    hours_worked: float = 0
    employer_cost: int = 100000

    def compute_pay(self) -> int:
        return int(self.pay_rate * self.hours_worked + self.employer_cost)


@dataclass
class SalariedEmployee:
    name: str
    id: int
    monthly_salary: int
    percentage: float = 1

    def compute_pay(self) -> int:
        return int(self.monthly_salary * self.percentage)


@dataclass
class Freelancer:
    name: str
    id: int
    pay_rate: int
    hours_worked: float = 0
    vat_number: str = ""

    def compute_pay(self) -> int:
        return int(self.pay_rate * self.hours_worked)


@dataclass
class SalariedEmployeeWithCommission(SalariedEmployee):
    commission: int = 10000
    contracts_landed: float = 0

    def compute_pay(self) -> int:
        return super().compute_pay() + int(self.commission * self.contracts_landed)


@dataclass
class HourlyEmployeeWithCommission(HourlyEmployee):
    commission: int = 10000
    contracts_landed: float = 0

    def compute_pay(self) -> int:
        return super().compute_pay() + int(self.commission * self.contracts_landed)


@dataclass
class FreelancerWithCommission(Freelancer):
    commission: int = 10000
    contracts_landed: float = 0

    def compute_pay(self) -> int:
        return super().compute_pay() + int(self.commission * self.contracts_landed)


def main() -> None:

    henry = HourlyEmployee(name="Henry", id=12346, pay_rate=5000, hours_worked=100)
    print(f"{henry.name} earned ${(henry.compute_pay() / 100):.2f}.")

    sarah = SalariedEmployeeWithCommission(
        name="Sarah", id=47832, monthly_salary=500000, contracts_landed=10
    )
    print(f"{sarah.name} earned ${(sarah.compute_pay() / 100):.2f}.")


if __name__ == "__main__":
    main()
```

In this way of refactoring initial code calculation of commission (that was common for all employees classes) was moved to separate classes that inherit from "base" class respectively:
* HourlyEmployee -> HourlyEmployeeWithCommission
* SalariedEmployee -> SalariedEmployeeWithCommission
* Freelancer -> FreelancerWithCommission

All `WithCommision` child classes do their job, but they provide exactly the same functionality, so it ends up with code duplication.

## Refactoring using composition

```python
from dataclasses import dataclass, field
from typing import Protocol


class PaymentSource(Protocol):
    def compute_pay(self) -> int:
        ...


@dataclass
class DealBasedCommission:
    commission: int = 10000
    deals_landed: int = 0

    def compute_pay(self) -> int:
        return self.commission * self.deals_landed


@dataclass
class HourlyContract:
    hourly_rate: int
    hours_worked: float = 0.0
    employer_cost: int = 100000

    def compute_pay(self) -> int:
        return int(self.hourly_rate * self.hours_worked + self.employer_cost)


@dataclass
class SalariedContract:
    monthly_salary: int
    percentage: float = 1

    def compute_pay(self) -> int:
        return int(self.monthly_salary * self.percentage)


@dataclass
class FreelanceContract:
    pay_rate: int
    hours_worked: float = 0
    vat_number: str = ""

    def compute_pay(self) -> int:
        return int(self.pay_rate * self.hours_worked)


@dataclass
class Employee:
    name: str
    id: int
    payment_sources: list[PaymentSource] = field(default_factory=list)

    def add_payment_source(self, payment_source: PaymentSource):
        self.payment_sources.append(payment_source)

    def compute_pay(self) -> int:
        return sum(source.compute_pay() for source in self.payment_sources)


def main() -> None:
    henry_contract = HourlyContract(hourly_rate=5000, hours_worked=100)
    henry = Employee(name="Henry", id=12346, payment_sources=[henry_contract])
    print(f"{henry.name} earned ${(henry.compute_pay() / 100):.2f}.")

    sarah_contract = SalariedContract(monthly_salary=500000)
    sarah_commission = DealBasedCommission(deals_landed=10)
    sarah = Employee(
        name="Sarah", id=47832, payment_sources=[sarah_contract, sarah_commission]
    )
    print(f"{sarah.name} earned ${(sarah.compute_pay() / 100):.2f}.")


if __name__ == "__main__":
    main()
```

In that case payment source is provided as separate object that is a part of employee object. It enables more flexibility as every single employee may have custom combination of payment sources.

Protocol `PaymentSource` defines, how payment source should look like for typing system. `DealBasedCommission`, `HourlyContract`, `SalariedContract`, `FreelanceContract` meet the requirements of protocol and handle commission case.

`Employee` object represents all employees, that may have many payment sources.

Computing pay in `compute_pay()` method works for all payment sources as according to defined protocol they share the same interface.