import openai
import os
import spacy
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from urllib.request import urlopen
from fuzzywuzzy import fuzz

# Legacy prototype note: never hardcode API keys in source files.
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🧠 spaCy setup
nlp = spacy.load("en_core_web_sm")

# Sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# 🧠 GPT keyword generator
def generate_keywords_gpt(company):
    prompt = f"""
    List 10 short keywords (1 to 2 words max) commonly used in financial news headlines about {company}.
    Only include:
    - Stock symbols (e.g., AAPL),
    - Executive names,
    - Product categories,
    - Common macro topics affecting the company (e.g., trade war, tariffs),
    - Abbreviations or sector names (e.g., tech, EV).

    Do not include long phrases or detailed explanations — just compact, headline-relevant terms.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=150
        )
        raw = response.choices[0].message.content
        keywords = []

        for line in raw.strip().split('\n'):
            line = line.strip("0123456789.-• ").lower().replace('"', '').replace("'", "")
            if line:
                # Strip to 1–3 word keywords only
                phrase = line.split(" - ")[0].strip()
                word_count = len(phrase.split())
                if 1 <= word_count <= 3:
                    keywords.append(phrase)
        return keywords
    except Exception as e:
        print("⚠️ GPT failed, falling back to spaCy. Error:", e)
        return []

# 🧠 spaCy keyword fallback
def fetch_wiki_text(company):
    url = f"https://en.wikipedia.org/wiki/{company.strip().replace(' ', '_')}_Inc."
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all('p')
        return ' '.join([p.get_text() for p in paragraphs[:2]])
    except:
        return ""

def generate_keywords_spacy(company):
    text = fetch_wiki_text(company)
    doc = nlp(text)
    keywords = set()
    for chunk in doc.noun_chunks:
        if len(chunk.text) > 2:
            keywords.add(chunk.text.strip().lower())
    return list(keywords)[:10]

# 🌐 Scrape Yahoo headlines
def scrape_yahoo_headlines():
    url = "https://finance.yahoo.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all('h3')
    headlines = [tag.get_text(strip=True) for tag in tags if tag.get_text(strip=True)]
    return headlines

# 🧠 Relevance check
def is_relevant(headline, keywords):
    headline_lower = headline.lower()
    return any(fuzz.partial_ratio(kw, headline_lower) > 80 for kw in keywords)

# 🧪 Sentiment scoring
def analyze_sentiment(headline):
    score = analyzer.polarity_scores(headline)['compound']
    if score >= 0.3:
        return score, "BUY"
    elif score <= -0.3:
        return score, "SELL"
    else:
        return score, "HOLD"

# 🚀 Main
if __name__ == "__main__":
    company = input("Enter a company name (e.g., Apple, Tesla): ").strip()

    print(f"\n🔍 Generating keywords for {company}...\n")
    keywords = generate_keywords_gpt(company)

    if not keywords:
        keywords = generate_keywords_spacy(company)
        print(f"\n🧠 spaCy fallback keywords:\n{keywords}")
    else:
        print(f"\n🔮 GPT keywords:\n{keywords}")

    print("\n🌐 Scraping headlines...\n")
    headlines = scrape_yahoo_headlines()
    filtered = [h for h in headlines if is_relevant(h, keywords)]

    if not filtered:
        print("⚠️ No relevant headlines found.")
    else:
        print(f"\n📈 Sentiment Analysis for {company}:\n")
        for h in filtered[:5]:
            score, action = analyze_sentiment(h)
            print(f"📰 {h}")
            print(f"→ Sentiment Score: {score:.2f} → Suggested Action: {action}")
            print("-" * 80)
