import pandas as pd
import plotly.express as px

# Load the merged JSON file
merged_df = pd.read_json('merged_data.json', lines=True)

# Convert timestamp to datetime
merged_df['date'] = pd.to_datetime(merged_df['date'], unit='ms')

# Group and average sentiment score per date and company
avg_sentiment = merged_df.groupby(['date', 'company'])['sentiment_score'].mean().reset_index()

# Plot interactive line chart
fig = px.line(avg_sentiment, x='date', y='sentiment_score', color='company',
              title='Average Sentiment Score Over Time by Company',
              labels={'date': 'Date', 'sentiment_score': 'Avg Sentiment Score'})
fig.show()
