import re
import pandas as pd
import yfinance as yf
import csv
import os

# Register a new user
def register_user(email, password):
    """
    Register a new user and save their credentials in a CSV file.
    """
    if len(password) < 6:
        return "Password must be at least 6 characters long."

    # Append user credentials to CSV file
    with open("registered_users.csv", mode="a+", newline="") as file:
        file.seek(0)
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == email:  # Check for duplicate email
                return "Email already registered. Please login."
        writer = csv.writer(file)
        writer.writerow([email, password])
    
    return "Registration successful! Please login."

def is_valid_email(email):
    # Regular expression for a valid email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Authenticate user login
def authenticate_user(email, password, user_file='users.csv'):
    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Invalid email format."
    
    # Check password length
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    # Verify credentials from file
    if not os.path.exists(user_file):
        return False, "No users registered yet."
    with open(user_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Email"] == email and row["Password"] == password:
                return True, "Login successful."
    return False, "Invalid email or password."

def get_closing_prices(ticker, start_date, end_date):
    """
    Fetch historical closing prices for a given stock ticker and date range.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            return "No data available for the given ticker and date range."
        return data['Close']
    except Exception as e:
        return f"Error fetching data: {str(e)}"

def analyze_closing_prices(data):
    """
    Analyze closing prices: calculate average, percentage change, highest, and lowest prices.
    """
    if data.empty:
        return "No data available for analysis."

    average_price = data.mean()
    percentage_change = ((data.iloc[-1] - data.iloc[0]) / data.iloc[0]) * 100
    highest_price = data.max()
    lowest_price = data.min()

    return {
        "Average Price": round(average_price.item(), 2),  # Extract scalar value
        "Percentage Change": round(percentage_change.item(), 2),  # Extract scalar value
        "Highest Price": round(highest_price.item(), 2),
        "Lowest Price": round(lowest_price.item(), 2)
    }

def save_to_csv(data, filename):
    """
    Save data to a CSV file.
    """
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

def read_from_csv(filename="analysis_results.csv"):
    """
    Read data from a CSV file and return it as a list.
    """
    data = []
    try:
        with open(filename, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"No data found. The file '{filename}' does not exist yet.")
    return data