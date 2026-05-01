import pandas as pd
import yfinance as yf
from datetime import timedelta

# Load sentiment data
sentiment_df = pd.read_csv('sentiment_log.csv')

# Standardize and fix column casing
sentiment_df.columns = sentiment_df.columns.str.lower()
sentiment_df['date'] = pd.to_datetime(sentiment_df['date']).dt.date

# Group sentiment by date (average score per day)
daily_sentiment = sentiment_df.groupby('date').agg({
    'sentiment_score': 'mean',
    'company': lambda x: ', '.join(set(x)),  # Combine companies if needed
    'headline': 'count',  # Optional: number of headlines
    'action': lambda x: x.mode()[0] if not x.mode().empty else 'HOLD'
}).reset_index()

# Input ticker
ticker = input("Enter the stock ticker symbol (e.g., AAPL, TSLA): ").upper()

# Define date range
start_date = daily_sentiment['date'].min() - timedelta(days=30)
end_date = daily_sentiment['date'].max() + timedelta(days=1)

# Download stock data
stock_data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)

# Flatten columns if MultiIndex
if isinstance(stock_data.columns, pd.MultiIndex):
    stock_data.columns = [' '.join(col).strip() for col in stock_data.columns.values]

# Reset index and convert date
stock_data.reset_index(inplace=True)
stock_data['date'] = pd.to_datetime(stock_data['Date']).dt.date

# Merge on date
merged_df = pd.merge(daily_sentiment, stock_data, on='date', how='left')

# Save as JSON
merged_df.to_json('merged_data.json', orient='records', lines=True)
print("✅ Merged and grouped data saved to 'merged_data.json'")
