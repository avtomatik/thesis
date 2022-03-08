# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 16:03:35 2021

@author: Mastermind
"""
"""Depreciation Types"""

def print_out(stock):
    for i,  value in enumerate(stock):
        print('Year {:2n}: {:, .2f}'.format(i,  value))

"""Linear Depreciation"""
value = 1000000
life = 50
rate = 1

stock = [value]
for year in range(life):
    delta = value*rate/life
    stock.append(stock[year]-delta)

print_out(stock = stock)

"""Geomertic Depreciation"""
value = 1000000
life = 50
rate = 2

stock = [value]
for year in range(life):
    delta = value*rate/life*(1-rate/life)**(year-1)
    stock.append(stock[year]-delta)

print_out(stock = stock)

"""Hyperbolic Depreciation"""
value = 1000000
life = 50
rate = 0.1

stock = [value]
for year in range(life):
    delta = value*((life-(year-1))/(life-rate*(year-1))-(life-year)/(life-rate*year))
    stock.append(stock[year]-delta)

print_out(stock = stock)

"""Ivashkevich,  Page 145,  Depreciation"""
value = 70000
life = 7
initial = 16000

stock = [value]
for year in range(life):
    delta = 2*(0-value+initial*life)/(life*(life-1))
    stock.append(stock[year]-delta)

print_out(stock = stock)