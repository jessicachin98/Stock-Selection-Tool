import functions as fn

def main():
    print("Welcome to the Stock Selection Tool!")
    while True:
        # User Authentication Menu
        choice = input("\n1. Register\n2. Login\n3. Exit\nChoose an option: ").strip()
        if choice == '1':  # Register
            handle_registration()
        elif choice == '2':  # Login
            if handle_login():
                main_menu()  # Navigate to Main Menu after successful login
        elif choice == '3':  # Exit
            print("\nThank you for using the Stock Selection Tool! Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

def handle_registration():
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()
    print(fn.register_user(email, password))

def handle_login():
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()
    success, message = fn.authenticate_user(email, password)
    print(message)
    return success

def main_menu():
    while True:
        # Main Menu
        choice = input("\nMain Menu\n1. Analyze Stock Data\n2. View Stored Data\n3. Logout\nChoose an option: ").strip()
        if choice == '1':  # Analyze Stock Data
            analyze_stock_data()
        elif choice == '2':  # View Stored Data
            view_stored_data()
        elif choice == '3':  # Logout
            print("\nLogging out...")
            break
        else:
            print("Invalid option. Please try again.")

def analyze_stock_data():
    ticker = input("Enter Stock Ticker (e.g.: 1155.KL): ").strip()
    start_date = input("Start date (YYYY-MM-DD): ").strip()
    end_date = input("End date (YYYY-MM-DD): ").strip()
    
    # Fetch closing prices
    closing_prices = fn.get_closing_prices(ticker, start_date, end_date)
    if isinstance(closing_prices, str):  # If error message is returned
        print(closing_prices)
        return

    # Analyze closing prices
    analysis = fn.analyze_closing_prices(closing_prices)
    if isinstance(analysis, str):  # If no data available
        print(analysis)
    else:
        print(f"\nAnalyze Stock Data for {ticker}")
        print(f"Start date: {start_date}")
        print(f"End date: {end_date}")
        print(f"Average Price: RM{analysis['Average Price']}")
        print(f"Percentage Change: {analysis['Percentage Change']}%")
        print(f"Highest Price: RM{analysis['Highest Price']}")
        print(f"Lowest Price: RM{analysis['Lowest Price']}")

        # Save results to CSV
        data_to_save = [ticker, start_date, end_date, 
                        f"RM{analysis['Average Price']}", 
                        f"{analysis['Percentage Change']}%", 
                        f"RM{analysis['Highest Price']}", 
                        f"RM{analysis['Lowest Price']}"]
        fn.save_to_csv(data_to_save, "analysis_results.csv")
        print("\n*These data have been saved to 'analysis_results.csv'")

def print_analysis_results(ticker, start_date, end_date, analysis):
    print(f"\nAnalyze Stock Data for {ticker}")
    print(f"Start date: {start_date}")
    print(f"End date: {end_date}")
    print(f"Average Price: {analysis['Average Closing Price']}")
    print(f"Percentage Change: {analysis['Percentage Change']:.2f}%")
    print(f"Highest Price: {analysis['Highest Closing Price']}")
    print(f"Lowest Price: {analysis['Lowest Closing Price']}")

def view_stored_data():
    print("\nStored Data:")
    data = fn.read_from_csv("analysis_results.csv")
    if not data:  # If data is empty or file not found
        print("No stored data available.\n")
    else:
        print("\n{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
            "Ticker", "Start Date", "End Date", "Avg Price", "Change %", "High Price", "Low Price"
        ))
        print("-" * 90)
        for row in data:
            print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(*row))
        print()

if __name__ == "__main__":
    main()
