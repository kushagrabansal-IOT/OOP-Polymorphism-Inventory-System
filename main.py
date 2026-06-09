"""
OOP-Polymorphism-Inventory-System
Concepts: Method Overriding, Runtime Polymorphism, Duck Typing, Abstract Methods
Author  : Kushagra Bansal — Project Lab India
Run     : python main.py
"""
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum

class Category(Enum):
    ELECTRONICS="Electronics"; CLOTHING="Clothing"
    FOOD="Food"; BOOKS="Books"; MEDICINE="Medicine"


class Product(ABC):
    """Abstract base — defines interface all products must follow"""
    _id_counter = 1000

    def __init__(self, name, price, quantity, category):
        Product._id_counter += 1
        self._id        = f"PRD{Product._id_counter:05d}"
        self._name      = name
        self._price     = price
        self._quantity  = quantity
        self._category  = category
        self._created   = datetime.now()

    @property
    def id(self):       return self._id
    @property
    def name(self):     return self._name
    @property
    def price(self):    return self._price
    @property
    def quantity(self): return self._quantity
    @property
    def category(self): return self._category

    # ── Abstract Methods — MUST override in subclass ─────────
    @abstractmethod
    def calculate_discount(self) -> float:
        """Each product type has different discount logic"""
        pass

    @abstractmethod
    def get_selling_price(self) -> float:
        """Final price after all adjustments"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Availability logic differs per product type"""
        pass

    @abstractmethod
    def get_product_details(self) -> dict:
        """Type-specific details"""
        pass

    # ── Concrete Methods ─────────────────────────────────────
    def calculate_tax(self) -> float:
        return 0.0

    def get_total_value(self) -> float:
        return self.get_selling_price() * self._quantity

    def restock(self, qty):
        self._quantity += qty
        print(f"  📦 Restocked {self._name}: +{qty} units (Total: {self._quantity})")

    def sell(self, qty):
        if qty > self._quantity:
            raise ValueError(f"Insufficient stock. Available: {self._quantity}")
        self._quantity -= qty
        revenue = qty * self.get_selling_price()
        print(f"  🛒 Sold {qty}x {self._name} @ ₹{self.get_selling_price():,.2f} = ₹{revenue:,.2f}")
        return revenue

    def __str__(self):
        return (f"[{self._id}] {self._name:<25} | "
                f"₹{self.get_selling_price():>8,.2f} | "
                f"Qty:{self._quantity:>4} | "
                f"{self._category.value}")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._id!r}, name={self._name!r})"

    def __lt__(self, other):  return self.get_selling_price() < other.get_selling_price()
    def __eq__(self, other):  return isinstance(other,Product) and self._id == other._id


class ElectronicsProduct(Product):
    """Runtime polymorphism: overrides all abstract methods"""

    def __init__(self, name, price, quantity, brand, warranty_years, wattage):
        super().__init__(name, price, quantity, Category.ELECTRONICS)
        self._brand     = brand
        self._warranty  = warranty_years
        self._wattage   = wattage

    def calculate_discount(self) -> float:
        """Electronics: 10% on items > ₹5000, 5% otherwise"""
        return 0.10 if self._price > 5000 else 0.05

    def calculate_tax(self) -> float:
        """Electronics GST: 18%"""
        return 0.18

    def get_selling_price(self) -> float:
        """Price - discount + tax"""
        discounted = self._price * (1 - self.calculate_discount())
        return round(discounted * (1 + self.calculate_tax()), 2)

    def is_available(self) -> bool:
        return self._quantity > 0

    def get_product_details(self) -> dict:
        return {
            "brand":    self._brand,
            "warranty": f"{self._warranty} year(s)",
            "wattage":  f"{self._wattage}W",
            "gst":      "18%",
            "discount": f"{self.calculate_discount()*100:.0f}%"
        }


class ClothingProduct(Product):
    """Polymorphic override — different pricing logic"""

    SIZE_MULTIPLIER = {"XS":0.95,"S":1.0,"M":1.0,"L":1.05,"XL":1.10,"XXL":1.15}

    def __init__(self, name, price, quantity, brand, size, material, season):
        super().__init__(name, price, quantity, Category.CLOTHING)
        self._brand    = brand
        self._size     = size
        self._material = material
        self._season   = season

    def calculate_discount(self) -> float:
        """Off-season items get 30% discount"""
        current_month = datetime.now().month
        is_summer = current_month in [3,4,5,6]
        is_winter = current_month in [10,11,12,1]
        if (self._season == "Summer" and is_winter) or (self._season == "Winter" and is_summer):
            return 0.30
        return 0.05

    def calculate_tax(self) -> float:
        """Clothing GST: 12% if price > 1000, else 5%"""
        return 0.12 if self._price > 1000 else 0.05

    def get_selling_price(self) -> float:
        base = self._price * self.SIZE_MULTIPLIER.get(self._size, 1.0)
        return round(base * (1 - self.calculate_discount()) * (1 + self.calculate_tax()), 2)

    def is_available(self) -> bool:
        return self._quantity > 0 and self._size in self.SIZE_MULTIPLIER

    def get_product_details(self) -> dict:
        return {"brand":self._brand,"size":self._size,
                "material":self._material,"season":self._season,
                "discount":f"{self.calculate_discount()*100:.0f}%"}


class FoodProduct(Product):
    """Perishable product — availability depends on expiry"""

    def __init__(self, name, price, quantity, brand, expiry_days, unit="kg"):
        super().__init__(name, price, quantity, Category.FOOD)
        self._brand      = brand
        self._expiry_date= datetime.now() + timedelta(days=expiry_days)
        self._unit       = unit

    @property
    def days_to_expiry(self):
        return (self._expiry_date - datetime.now()).days

    def calculate_discount(self) -> float:
        """Perishables near expiry get increasing discounts"""
        days = self.days_to_expiry
        if days <= 2:  return 0.50
        if days <= 5:  return 0.30
        if days <= 10: return 0.10
        return 0.0

    def calculate_tax(self) -> float:
        """Food: 5% GST"""
        return 0.05

    def get_selling_price(self) -> float:
        return round(self._price * (1 - self.calculate_discount()) * (1 + self.calculate_tax()), 2)

    def is_available(self) -> bool:
        return self._quantity > 0 and self.days_to_expiry > 0

    def get_product_details(self) -> dict:
        return {"brand":self._brand,"unit":self._unit,
                "expiry":self._expiry_date.strftime("%Y-%m-%d"),
                "days_left":self.days_to_expiry,
                "discount":f"{self.calculate_discount()*100:.0f}%"}


class BookProduct(Product):
    """Books — simple pricing with author/ISBN"""

    def __init__(self, name, price, quantity, author, isbn, genre):
        super().__init__(name, price, quantity, Category.BOOKS)
        self._author = author
        self._isbn   = isbn
        self._genre  = genre

    def calculate_discount(self) -> float:
        """Books: 20% flat — promote reading"""
        return 0.20

    def calculate_tax(self) -> float:
        """Books: 0% GST (exempt in India)"""
        return 0.0

    def get_selling_price(self) -> float:
        return round(self._price * (1 - self.calculate_discount()), 2)

    def is_available(self) -> bool:
        return self._quantity > 0

    def get_product_details(self) -> dict:
        return {"author":self._author,"isbn":self._isbn,"genre":self._genre,"gst":"0%"}


class Inventory:
    """Manages all products — demonstrates polymorphism in action"""

    def __init__(self, store_name):
        self.store_name = store_name
        self._products  = {}

    def add_product(self, product: Product):
        self._products[product.id] = product
        print(f"  ✅ Added: {product}")

    def remove_product(self, product_id):
        del self._products[product_id]

    def get_product(self, product_id) -> Product:
        return self._products.get(product_id)

    def process_sale(self, product_id, qty) -> float:
        """POLYMORPHISM: same method call, different behavior"""
        product = self._products[product_id]
        if not product.is_available():
            raise ValueError(f"{product.name} is not available")
        return product.sell(qty)

    def get_available_products(self):
        """POLYMORPHISM: is_available() behaves differently for each type"""
        return [p for p in self._products.values() if p.is_available()]

    def get_total_inventory_value(self) -> float:
        return sum(p.get_total_value() for p in self._products.values())

    def apply_bulk_discount(self, product_id, extra_pct):
        """Demonstrates extension of base behavior"""
        p = self._products[product_id]
        # Duck typing — any product with _price works
        p._price *= (1 - extra_pct)
        print(f"  🏷️  Bulk discount {extra_pct*100:.0f}% applied to {p.name}")

    def generate_report(self):
        """Polymorphic report — each product's get_product_details differs"""
        print(f"\n{'═'*75}")
        print(f"  📊 INVENTORY REPORT | {self.store_name}")
        print(f"{'═'*75}")
        print(f"  {'ID':<12} {'PRODUCT':<28} {'MRP':>8} {'SELL PRICE':>11} {'QTY':>5} {'VALUE':>12}")
        print(f"  {'─'*72}")
        total = 0
        for p in sorted(self._products.values()):
            val = p.get_total_value()
            total += val
            avail = "✅" if p.is_available() else "❌"
            print(f"  {p.id:<12} {p.name:<28} ₹{p.price:>7,.0f} ₹{p.get_selling_price():>10,.2f} {p.quantity:>5} ₹{val:>11,.2f} {avail}")
        print(f"  {'─'*72}")
        print(f"  {'TOTAL INVENTORY VALUE':>52} ₹{total:>11,.2f}")
        print(f"{'═'*75}")


if __name__ == "__main__":
    print("═"*75)
    print("  OOP Polymorphism — Inventory Management System")
    print("  Project Lab India")
    print("═"*75)

    inv = Inventory("Project Lab India Store")

    # Create different product types
    laptop  = ElectronicsProduct("Dell Laptop XPS 15",   85000, 10, "Dell",     2, 65)
    phone   = ElectronicsProduct("Samsung Galaxy S24",   70000, 25, "Samsung",  1, 25)
    jeans   = ClothingProduct("Levis Slim Fit 511",       2500,  50, "Levis",  "M", "Denim","Winter")
    apple   = FoodProduct("Organic Apples",                200,  100, "Fresh",  7, "kg")
    milk    = FoodProduct("Full Cream Milk",                 65,  200, "Amul",   3, "litre")
    dsa_book= BookProduct("Cracking the Coding Interview", 3500,  30,"McDowell","978-0984782857","Tech")
    cleancode=BookProduct("Clean Code",                    2800,  20, "Martin", "978-0132350884","Tech")

    for p in [laptop, phone, jeans, apple, milk, dsa_book, cleancode]:
        inv.add_product(p)

    print("\n── Polymorphism Demo — Same call, different behavior ──")
    for p in [laptop, jeans, apple, dsa_book]:
        print(f"  {p.__class__.__name__:<22}: discount={p.calculate_discount()*100:>5.1f}%  "
              f"tax={p.calculate_tax()*100:>4.0f}%  "
              f"sell_price=₹{p.get_selling_price():>10,.2f}")

    print("\n── Processing Sales ──")
    inv.process_sale(laptop.id, 2)
    inv.process_sale(dsa_book.id, 5)
    inv.process_sale(apple.id, 10)

    inv.generate_report()

    print("\n── Product Details (Type-Specific) ──")
    for p in [laptop, jeans, apple, dsa_book]:
        print(f"  {p.__class__.__name__}: {p.get_product_details()}")
