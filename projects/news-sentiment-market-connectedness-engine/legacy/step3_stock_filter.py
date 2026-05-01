import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# 🔍 Set target company and keywords
target_company = "Apple"
keywords = ['apple', 'aapl', 'iphone', 'macbook', 'app store', 'tim cook']

def scrape_yahoo_headlines():
    url = "https://finance.yahoo.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    headline_tags = soup.find_all('h3')
    
    headlines = []
    for tag in headline_tags:
        text = tag.get_text(strip=True)
        if text and len(text) > 10:
            headlines.append(text)
    return headlines

def is_relevant(headline, keywords):
    return any(kw.lower() in headline.lower() for kw in keywords)

def analyze_headline_sentiment(headline, analyzer):
    score = analyzer.polarity_scores(headline)['compound']
    if score >= 0.3:
        return score, "BUY"
    elif score <= -0.3:
        return score, "SELL"
    else:
        return score, "HOLD"

# 🔧 Run the pipeline
if __name__ == "__main__":
    headlines = scrape_yahoo_headlines()
    analyzer = SentimentIntensityAnalyzer()

    print(f"\n📈 Sentiment for {target_company} Related Headlines:\n")

    # Filter for headlines matching keywords
    filtered = [h for h in headlines if is_relevant(h, keywords)]

    if not filtered:
        print("No headlines matched your filter.")
    else:
        # Limit to 5 headlines max
        for headline in filtered[:5]:
            score, action = analyze_headline_sentiment(headline, analyzer)
            print(f"📰 {headline}")
            print(f"   → Sentiment: {score:.2f} → Suggested Action: {action}")
            print("-" * 80)
