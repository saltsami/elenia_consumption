import csv
from datetime import datetime, timedelta
import os
from collections import defaultdict

def read_processed_data(filename):
    filepath = os.path.join('processed', filename)
    data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({
                'date': datetime.strptime(row['Date'], '%Y-%m-%d').date(),
                'hour': row['Hour'],
                'consumption': float(row['Consumption (kW)']),
                'price': float(row['Price (snt/kWh)']),
                'cost': float(row['Cost (EUR)'])
            })
    return data

def calculate_daily_consumption(data):
    daily_consumption = defaultdict(lambda: {'consumption': 0, 'cost': 0})
    for row in data:
        date = row['date']
        daily_consumption[date]['consumption'] += row['consumption']
        daily_consumption[date]['cost'] += row['cost']
    
    return daily_consumption

def save_daily_consumption(daily_consumption, filename='daily_consumption.csv'):
    filepath = os.path.join('processed', filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['Date', 'Consumption (kWh)', 'Cost (EUR)']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for date, values in sorted(daily_consumption.items()):
            writer.writerow({
                'Date': date.strftime('%Y-%m-%d'),
                'Consumption (kWh)': f"{values['consumption']:.2f}",
                'Cost (EUR)': f"{values['cost']:.2f}"
            })
    
    print(f"Daily consumption data saved to {filepath}")

def main():
    # Ensure the processed directory exists
    os.makedirs('processed', exist_ok=True)

    # Read the processed data
    data = read_processed_data('processed_data_2024.csv')

    # Calculate daily consumption
    daily_consumption = calculate_daily_consumption(data)

    # Save daily consumption data
    save_daily_consumption(daily_consumption)

if __name__ == "__main__":
    main()