import yfinance as yf
import pandas as pd


class InvestmentCalculator:
    def __init__(self, stock_symbol, start_year, end_year, coffee_type):
        """
        Manages stock and investment calculations.

        stock_symbol: Stock ticker symbol
        start_year: Investment start year
        end_year: Investment end year
        coffee_type: Coffee type (e.g., "Small", "Cappuccino", "Fancy Latte")
        """
        self.stock_symbol = stock_symbol
        self.start_year = start_year
        self.end_year = end_year
        self.coffee_type = coffee_type
        self.coffee_prices = {"Small": 2.5, "Cappuccino": 3.5, "Fancy Latte": 4.5}

    def get_stock_data(self):
        """
        Fetches historical stock data for the given stock symbol.
        """
        try:
            start_date = f"{self.start_year}-01-01"
            end_date = f"{self.end_year}-12-31"

            stock_data = yf.download(
                self.stock_symbol, start=start_date, end=end_date, interval="1mo"
            )
            if stock_data.empty:
                raise ValueError(
                    f"No data found for {self.stock_symbol} between {start_date} and {end_date}."
                )

            # Filter closing prices and drop NaN values
            monthly_closing_prices = stock_data["Close"].dropna()
            return pd.DataFrame(
                {
                    "Date": monthly_closing_prices.index,
                    "Close": monthly_closing_prices.values.ravel(),
                }
            )
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_coffee_price(self):
        """
        Returns the price of the selected coffee type.
        """
        return self.coffee_prices.get(self.coffee_type, None)

    def calculate_investment(self, stock_data, working_days=20):
        """
        Calculates the total value of an investment made with daily coffee savings.

        stock_data: DataFrame containing stock prices (Date and Close columns)
        working_days: Number of working days per month (default: 20 days)
        """
        daily_coffee_price = self.get_coffee_price()
        if daily_coffee_price is None:
            raise ValueError("Invalid coffee type selected!")

        monthly_investment = (
            daily_coffee_price * working_days
        )  # Monthly investment amount
        total_shares = 0
        total_investment = 0

        for _, row in stock_data.iterrows():
            price = row["Close"]
            if price > 0:  # Avoid negative or zero prices
                shares_bought = monthly_investment / price
                total_shares += shares_bought
                total_investment += monthly_investment

        final_price = stock_data["Close"].iloc[-1]
        investment_value = total_shares * final_price

        return {
            "Total Investment": round(total_investment, 2),
            "Final Investment Value": round(investment_value, 2),
            "Total Shares Bought": round(total_shares, 4),
        }


# Usage Example
if __name__ == "__main__":
    # Get user input
    stock_symbol = input("Enter the stock symbol: ").strip()
    coffee_type = input(
        "Select a coffee type (Small, Cappuccino, Fancy Latte): "
    ).strip()
    start_year = int(
        input("Enter the start year of the investment (YYYY format): ").strip()
    )
    end_year = int(
        input("Enter the end year of the investment (YYYY format): ").strip()
    )

    # Initialize the calculator
    calculator = InvestmentCalculator(stock_symbol, start_year, end_year, coffee_type)

    # Fetch stock data
    stock_data = calculator.get_stock_data()
    if stock_data is None:
        print("Failed to retrieve stock data.")
    else:
        # Calculate investment
        try:
            investment_result = calculator.calculate_investment(stock_data)
            print("\nInvestment Results:")
            print(f"Total Investment: {investment_result['Total Investment']} USD")
            print(
                f"Final Investment Value: {investment_result['Final Investment Value']} USD"
            )
            print(f"Total Shares Bought: {investment_result['Total Shares Bought']}")
        except ValueError as e:
            print(f"Error: {e}")
