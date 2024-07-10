#!/usr/bin/env python3

from cash_register import CashRegister  # Import the CashRegister class

import io
import sys
import pytest  # Assuming you are using pytest for testing

class TestCashRegister:
    '''Unit tests for CashRegister class'''

    def setup_method(self):
        '''Setup method to create fresh instances for each test method'''
        self.cash_register = CashRegister()
        self.cash_register_with_discount = CashRegister(20)

    def teardown_method(self):
        '''Teardown method to reset after each test method'''
        self.cash_register.total = 0
        self.cash_register.items = []
        self.cash_register_with_discount.total = 0
        self.cash_register_with_discount.items = []

    def test_discount_attribute(self):
        '''Test discount attribute initialization'''
        assert self.cash_register.discount == 0
        assert self.cash_register_with_discount.discount == 20

    def test_total_attribute(self):
        '''Test total attribute initialization'''
        assert self.cash_register.total == 0
        assert self.cash_register_with_discount.total == 0

    def test_items_attribute(self):
        '''Test items attribute initialization'''
        assert self.cash_register.items == []
        assert self.cash_register_with_discount.items == []

    def test_add_item(self):
        '''Test adding items to CashRegister'''
        self.cash_register.add_item("eggs", 0.98)
        assert self.cash_register.total == 0.98
        assert self.cash_register.items == ["eggs"]

    def test_add_item_optional_quantity(self):
        '''Test adding items with optional quantity'''
        self.cash_register.add_item("book", 5.00, 3)
        assert self.cash_register.total == 15.00
        assert self.cash_register.items == ["book", "book", "book"]

    def test_add_item_with_multiple_items(self):
        '''Test adding multiple items'''
        self.cash_register.add_item("Lucky Charms", 4.5)
        assert self.cash_register.total == 4.5
        self.cash_register.add_item("Ritz Crackers", 5.0)
        assert self.cash_register.total == 9.5
        self.cash_register.add_item("Justin's Peanut Butter Cups", 2.50, 2)
        assert self.cash_register.total == 14.5
        assert self.cash_register.items == ["Lucky Charms", "Ritz Crackers", "Justin's Peanut Butter Cups", "Justin's Peanut Butter Cups"]

    def test_apply_discount(self):
        '''Test applying discount'''
        self.cash_register_with_discount.add_item("macbook air", 1000)
        self.cash_register_with_discount.apply_discount()
        assert self.cash_register_with_discount.total == 800

    def test_apply_discount_success_message(self):
        '''Test success message when applying discount'''
        captured_out = io.StringIO()
        sys.stdout = captured_out
        self.cash_register_with_discount.add_item("macbook air", 1000)
        self.cash_register_with_discount.apply_discount()
        sys.stdout = sys.__stdout__
        assert captured_out.getvalue() == "After the discount, the total comes to $800.\n"

    def test_apply_discount_reduces_total(self):
        '''Test that applying discount reduces the total'''
        self.cash_register_with_discount.add_item("macbook air", 1000)
        self.cash_register_with_discount.apply_discount()
        assert self.cash_register_with_discount.total == 800

    def test_apply_discount_when_no_discount(self):
        '''Test applying discount when there's no discount'''
        captured_out = io.StringIO()
        sys.stdout = captured_out
        self.cash_register.apply_discount()
        sys.stdout = sys.__stdout__
        assert captured_out.getvalue() == "There is no discount to apply.\n"

    def test_items_list_without_multiples(self):
        '''Test items list without multiples'''
        new_register = CashRegister()
        new_register.add_item("eggs", 1.99)
        new_register.add_item("tomato", 1.76)
        assert new_register.items == ["eggs", "tomato"]

    def test_items_list_with_multiples(self):
        '''Test items list with multiples'''
        new_register = CashRegister()
        new_register.add_item("eggs", 1.99, 2)
        new_register.add_item("tomato", 1.76, 3)
        assert new_register.items == ["eggs", "eggs", "tomato", "tomato", "tomato"]

    def test_void_last_transaction(self):
        '''Test voiding last transaction'''
        self.cash_register.add_item("apple", 0.99)
        self.cash_register.add_item("tomato", 1.76)
        self.cash_register.void_last_transaction()
        assert self.cash_register.total == 0.99
        assert self.cash_register.items == ["apple"]

    def test_void_last_transaction_with_multiples(self):
        '''Test voiding last transaction with multiples'''
        self.cash_register.add_item("tomato", 1.76, 2)
        self.cash_register.void_last_transaction()
        assert self.cash_register.total == 0.0
        assert self.cash_register.items == []

