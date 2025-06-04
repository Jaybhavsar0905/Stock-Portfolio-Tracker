import yfinance as yf
from tabulate import tabulate

portfolio = {}

def add_stock(ticker, shares, purchase_price):
    ticker = ticker.upper()
    if ticker in portfolio:
        portfolio[ticker]['shares'] += shares
    else:
        portfolio[ticker] = {'shares': shares, 'purchase_price': purchase_price}

def remove_stock(ticker):
    ticker = ticker.upper()
    if ticker in portfolio:
        del portfolio[ticker]
    else:
        print("Stock not found in portfolio.")

def fetch_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        return round(data['Close'].iloc[-1], 2)
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def show_portfolio():
    if not portfolio:
        print("Portfolio is empty.")
        return

    total_value = 0
    total_cost = 0
    table_data = []

    for ticker, info in portfolio.items():
        shares = info['shares']
        purchase_price = info['purchase_price']
        current_price = fetch_stock_price(ticker)
        if current_price is None:
            continue
        current_value = round(shares * current_price, 2)
        invested_amount = round(shares * purchase_price, 2)
        profit_loss = round(current_value - invested_amount, 2)
        total_value += current_value
        total_cost += invested_amount

        table_data.append([
            ticker,
            shares,
            purchase_price,
            current_price,
            current_value,
            profit_loss
        ])

    print(tabulate(table_data, headers=["Ticker", "Shares", "Buy Price", "Current Price", "Value", "P/L"]))
    print(f"\nTotal Invested: ${total_cost:.2f} | Current Value: ${total_value:.2f} | Net P/L: ${total_value - total_cost:.2f}")

def main():
    while True:
        print("\n--- Stock Portfolio Tracker ---")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Show Portfolio")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            ticker = input("Enter stock ticker: ").upper()
            shares = float(input("Enter number of shares: "))
            purchase_price = float(input("Enter purchase price per share: "))
            add_stock(ticker, shares, purchase_price)
        elif choice == '2':
            ticker = input("Enter stock ticker to remove: ").upper()
            remove_stock(ticker)
        elif choice == '3':
            show_portfolio()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
