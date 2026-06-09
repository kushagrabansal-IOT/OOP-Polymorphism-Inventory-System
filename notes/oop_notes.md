# Polymorphism Notes
## Types
- Compile-time (Method Overloading) → Python uses *args/**kwargs
- Runtime (Method Overriding) → Subclass overrides parent method
- Duck Typing → 'If it quacks like a duck...'

## Abstract Methods
@abstractmethod forces subclasses to implement.
Cannot instantiate abstract class.
Defines the interface/contract.

## Runtime Polymorphism Example
for product in [Electronics, Clothing, Food]:
    product.get_selling_price()  # Different behavior, same call!

## Duck Typing in Python
Python doesn't check type — checks behavior.
Any object with get_selling_price() works in inventory.

## Interview Questions
1. What is polymorphism? Types?
2. Difference between overloading and overriding?
3. What is runtime polymorphism? Example?
4. What is duck typing?
5. How does abstract method enforce a contract?
