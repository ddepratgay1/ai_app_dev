# Python Programming Concepts

#1. Create variable to sotre the value 500 for sales
sales = 500
print(sales)

#2. Create variable to store serveral values
sales = [500, 475, 625]
print(sales.pop())

integers = list(range(10,1,-1))
print(integers)

#3. Create variable to store names and emails for a number of customers
customers = [
    {'name': 'John', 'email': 'john@some.com'},
    {'name': 'Ann', 'email': 'ann@some.com'},
]

#4. Generate random value based on each of the following

import random

# between 0 and 1
random1 = random.random()
print(random1)

# standard normal deviation
random_dev = round(random.gauss(0,1),2)
print(random_dev)

# value between 1 and 10
random10 = randint(1,10)
print(random10)

# either H or T
random_HT = choice(["H", "T"])
print(random_HT)


#5. Use Python to determine your current working directory
import os
os.getcwd()

#6. Determine how many days until New Year's Day
from datetime import date

today = date.today()
new_year = date(today.year +1, 1, 1)

days_until = (new_year - today).days
print(days_until)

#7. Write a short program that displays the future value of 1,000 earnihng 5% at the end of each year for the next 5 years
principal = 1000
rate = 0.05

for year in range(1, 6):
    future_value = principal * (1 + rate) ** year
    print("Year", year, ":", round(future_value, 2))


