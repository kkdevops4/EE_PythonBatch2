portfolio = []

print("=" * 60)
print("            STOCK PORTFOLIO TRACKER")
print("=" * 60)

num_stocks = int(input("Enter number of stocks: "))

for i in range(num_stocks):

    print(f"\nEnter details for Stock {i + 1}")

    symbol = input("Stock name: ").upper()
    buy_price = float(input("Buy Price: "))
    quantity = int(input("Quantity: "))
    current_price = float(input("Current Price: "))

    investment_value = buy_price * quantity
    current_value = current_price * quantity
    profit_loss = current_value - investment_value

    if investment_value != 0:
        profit_loss_percent = (profit_loss / investment_value) * 100
    else:
        profit_loss_percent = 0

    stock = {
        "symbol": symbol,
        "buy_price": buy_price,
        "quantity": quantity,
        "current_price": current_price,
        "investment_value": investment_value,
        "current_value": current_value,
        "profit_loss": profit_loss,
        "profit_loss_percent": profit_loss_percent
    }

    portfolio.append(stock)

total_investment = 0
total_current_value = 0

for stock in portfolio:
    total_investment += stock["investment_value"]
    total_current_value += stock["current_value"]

total_profit_loss = total_current_value - total_investment

if total_investment != 0:
    total_return_percent = (total_profit_loss / total_investment) * 100
else:
    total_return_percent = 0

print("\n" + "=" * 100)
print("                      STOCK PORTFOLIO REPORT")
print("=" * 100)

print(
    f"{'name':<10}"
    f"{'Buy Price':<15}"
    f"{'Qty':<10}"
    f"{'Current':<15}"
    f"{'Investment':<15}"
    f"{'P/L':<15}"
    f"{'P/L %':<10}"
    f"{'Allocation %':<15}"
)

print("-" * 100)

for stock in portfolio:

    if total_current_value != 0:
        allocation_percent = (
            stock["current_value"] / total_current_value
        ) * 100
    else:
        allocation_percent = 0

    print(
        f"{stock['symbol']:<10}"
        f"{stock['buy_price']:<15.2f}"
        f"{stock['quantity']:<10}"
        f"{stock['current_price']:<15.2f}"
        f"{stock['investment_value']:<15.2f}"
        f"{stock['profit_loss']:<15.2f}"
        f"{stock['profit_loss_percent']:<10.2f}"
        f"{allocation_percent:<15.2f}"
    )

print("-" * 100)

print(f"Total Investment     : ₹{total_investment:.2f}")
print(f"Current Portfolio    : ₹{total_current_value:.2f}")
print(f"Total Profit/Loss    : ₹{total_profit_loss:.2f}")
print(f"Portfolio Return %   : {total_return_percent:.2f}%")

print("=" * 100)