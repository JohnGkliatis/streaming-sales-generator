from dataclasses import dataclass
from decimal import Decimal

@dataclass
class SubTotal:
    product_id: str
    event_time: str
    transactions: int
    quantities: int
    sales: Decimal

@dataclass
class Total:
    transactions: int
    quantities: int
    sales: Decimal

@dataclass
class Purchase:
    transaction_id: str
    transaction_time: str
    product_id: str
    is_member: bool
    add_supplements: bool
    quantity: int
    price: Decimal
    member_discount: Decimal
    supplement_price: Decimal
    total_purchase: Decimal

