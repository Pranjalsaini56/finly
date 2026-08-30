import random
import csv
from datetime import datetime, timedelta

random.seed(42)

merchants = [
    ("Zomato order", 150, 900),
    ("Zomato Gold membership", 300, 300),
    ("Swiggy order", 120, 850),
    ("Uber ride", 80, 650),
    ("Uber Eats order", 150, 700),
    ("Ola cab ride", 90, 600),
    ("Amazon purchase", 200, 4500),
    ("Amazon Prime subscription", 1499, 1499),
    ("Flipkart purchase", 250, 3800),
    ("Rent payment", 15000, 15000),
    ("Electricity bill", 800, 2500),
    ("Water bill", 200, 500),
    ("Netflix subscription", 649, 649),
    ("Spotify subscription", 119, 119),
    ("Hotstar subscription", 299, 299),
    ("Big Bazaar groceries", 500, 3000),
    ("DMart groceries", 400, 2800),
    ("BigBasket groceries", 350, 2600),
    ("Starbucks coffee", 250, 600),
    ("Cafe Coffee Day", 150, 400),
    ("Domino's Pizza", 300, 900),
    ("McDonald's order", 150, 500),
    ("PVR movie tickets", 400, 1200),
    ("BookMyShow tickets", 300, 1000),
    ("Gym membership", 1500, 1500),
    ("Cult.fit subscription", 999, 999),
    ("Petrol pump fuel", 500, 2000),
    ("Metro card recharge", 100, 500),
    ("Mobile recharge Jio", 199, 799),
    ("Airtel bill payment", 300, 900),
    ("Medical store purchase", 150, 1500),
    ("Apollo Pharmacy", 200, 1800),
    ("Salary credit", -45000, -45000),
    ("ATM cash withdrawal", 500, 5000),
    ("Myntra purchase", 500, 3500),
    ("IKEA furniture purchase", 1000, 8000),
    ("LIC insurance premium", 2000, 2000),
    ("Credit card payment", 3000, 15000),
    ("Zepto grocery delivery", 200, 1200),
    ("Blinkit order", 150, 900),
]

start_date = datetime(2025, 1, 1)
rows = []
num_rows = random.randint(70, 90)

for _ in range(num_rows):
    desc, low, high = random.choice(merchants)
    amount = round(random.uniform(low, high), 2) if low != high else float(low)
    date = start_date + timedelta(days=random.randint(0, 240))
    rows.append((date.strftime("%Y-%m-%d"), desc, amount))

rows.sort(key=lambda r: r[0])

with open("expenses.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Description", "Amount"])
    writer.writerows(rows)

print(f"Generated {len(rows)} rows -> expenses.csv")