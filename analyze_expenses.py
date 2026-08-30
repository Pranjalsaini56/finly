import pandas as pd

# 1. Load the CSV
df = pd.read_csv("expenses.csv")


# 2. Categorization function based on keywords in Description
def categorize(description):
    desc = description.lower()

    keyword_map = {
        "Food & Dining": ["zomato", "swiggy", "domino", "mcdonald", "cafe", "starbucks", "pizza"],
        "Groceries": ["big bazaar", "dmart", "bigbasket", "zepto", "blinkit", "grocery", "groceries"],
        "Transport": ["uber", "ola", "petrol", "metro", "fuel"],
        "Shopping": ["amazon", "flipkart", "myntra", "ikea"],
        "Housing & Utilities": ["rent", "electricity", "water bill"],
        "Subscriptions": ["netflix", "spotify", "hotstar", "prime subscription", "gold membership",
                           "cult.fit", "gym membership"],
        "Bills & Recharge": ["mobile recharge", "airtel", "jio", "credit card payment"],
        "Health": ["pharmacy", "medical store", "apollo"],
        "Insurance": ["lic", "insurance"],
        "Entertainment": ["pvr", "bookmyshow", "movie"],
        "Income": ["salary"],
        "Cash Withdrawal": ["atm", "cash withdrawal"],
    }

    for category, keywords in keyword_map.items():
        if any(kw in desc for kw in keywords):
            return category

    return "Other"


# 3. Apply categorization
df["Category"] = df["Description"].apply(categorize)

# 4. Group by category and print total spend
category_totals = (
    df.groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

print("=== Total Spend by Category ===\n")
for category, total in category_totals.items():
    print(f"{category:22s}: Rs. {total:>12,.2f}")

print("\n=== Overall Net (Spend - Income) ===")
print(f"Rs. {df['Amount'].sum():,.2f}")

expenses_only = df[df["Category"] != "Income"]["Amount"].sum()
print(f"Total Expenses: Rs. {expenses_only:,.2f}")

# Save results
df.to_csv("expenses_categorized.csv", index=False)
category_totals.to_csv("category_totals.csv", header=["Total Amount"])

duplicates = df[df.duplicated(subset=["Date", "Description", "Amount"], keep=False)]
print(f"\n=== Possible Duplicate Entries: {len(duplicates)} ===")
print(duplicates)

df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M")

monthly_cat = df[df["Category"] != "Income"].groupby(["Month", "Category"])["Amount"].sum().reset_index()
avg_per_cat = monthly_cat.groupby("Category")["Amount"].mean()

# Flag months where spend is 50%+ above that category's average
monthly_cat["Average"] = monthly_cat["Category"].map(avg_per_cat)
monthly_cat["Overspend"] = monthly_cat["Amount"] > (monthly_cat["Average"] * 1.5)

flagged = monthly_cat[monthly_cat["Overspend"]]
print("\n=== Overspending Alerts ===")
print(flagged[["Month", "Category", "Amount", "Average"]])
