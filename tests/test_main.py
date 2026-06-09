# Tests for Inventory System
import sys, pytest; sys.path.insert(0,'..')
from main import ElectronicsProduct, ClothingProduct, FoodProduct, BookProduct, Inventory

def test_electronics_tax():
    p = ElectronicsProduct('Laptop',80000,5,'Dell',1,65)
    assert p.calculate_tax() == 0.18

def test_book_zero_gst():
    b = BookProduct('Clean Code',2800,10,'Martin','ISBN','Tech')
    assert b.calculate_tax() == 0.0

def test_food_expiry_discount():
    from unittest.mock import patch; from datetime import datetime, timedelta
    f = FoodProduct('Milk',65,50,'Amul',3)
    assert f.calculate_discount() >= 0.30

def test_polymorphic_sell_price():
    products = [
        ElectronicsProduct('Phone',50000,10,'Samsung',1,25),
        ClothingProduct('Shirt',1500,20,'Brand','M','Cotton','Summer'),
        BookProduct('Book',500,5,'Author','ISBN','Tech')
    ]
    prices = [p.get_selling_price() for p in products]
    assert all(p > 0 for p in prices)

def test_inventory_sell():
    inv = Inventory('Test Store')
    e = ElectronicsProduct('TV',40000,5,'LG',1,100)
    inv.add_product(e)
    inv.process_sale(e.id, 2)
    assert e.quantity == 3

def test_insufficient_stock():
    inv = Inventory('Test')
    e = ElectronicsProduct('TV',40000,2,'LG',1,100)
    inv.add_product(e)
    with pytest.raises(ValueError): inv.process_sale(e.id, 5)
