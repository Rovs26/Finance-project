from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Dummy financial headlines (you can edit or expand these)
headlines = [
    "Apple's earnings soar past Wall Street expectations",
    "Tesla faces backlash over Autopilot safety concerns",
    "Nvidia announces breakthrough in AI chip performance",
    "Market remains flat as investors await Fed decision",
    "Tech stocks tumble after China imposes new tariffs"
]

print("\n🔍 Sentiment Analysis of Sample Financial Headlines\n")

for headline in headlines:
    score = analyzer.polarity_scores(headline)
    compound = score['compound']

    # Interpret compound score into a basic trading signal
    if compound >= 0.3:
        action = "BUY (Positive Sentiment)"
    elif compound <= -0.3:
        action = "SELL (Negative Sentiment)"
    else:
        action = "HOLD (Neutral Sentiment)"

    print(f"📰 Headline: {headline}")
    print(f"   → Compound Score: {compound:.2f} → Suggested Action: {action}")
    print("   (Breakdown:", score, ")")
    print("-" * 80)
