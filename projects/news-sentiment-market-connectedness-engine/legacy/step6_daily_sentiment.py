import csv
import datetime
from step5_dynamic_filtering import (
    generate_keywords_gpt,
    generate_keywords_spacy,
    scrape_yahoo_headlines,
    is_relevant,
    analyze_sentiment
)

# 📍 Where to save results
CSV_FILE = "sentiment_log.csv"

def save_to_csv(rows, csv_file):
    header = ["date", "company", "headline", "sentiment_score", "action"]
    
    # Create file with header if it doesn't exist
    try:
        with open(csv_file, 'x', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    except FileExistsError:
        pass  # File already exists

    # Append new rows
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

if __name__ == "__main__":
    company = input("Enter a company name: ").strip()
    today = datetime.date.today()

    print(f"\n🔍 Generating keywords for {company}...\n")
    keywords = generate_keywords_gpt(company)
    if not keywords:
        keywords = generate_keywords_spacy(company)
        print(f"🧠 spaCy fallback keywords:\n{keywords}")
    else:
        print(f"🔮 GPT keywords:\n{keywords}")

    print("\n🌐 Scraping headlines...\n")
    headlines = scrape_yahoo_headlines()
    filtered = [h for h in headlines if is_relevant(h, keywords)]

    rows = []
    print(f"\n📈 Sentiment Log for {company} - {today}:\n")
    for h in filtered[:5]:
        score, action = analyze_sentiment(h)
        print(f"📰 {h}")
        print(f"→ Sentiment Score: {score:.2f} → Suggested Action: {action}")
        print("-" * 80)
        rows.append([today, company, h, round(score, 4), action])

    if rows:
        save_to_csv(rows, CSV_FILE)
        print(f"\n✅ Saved {len(rows)} rows to '{CSV_FILE}'")
    else:
        print("⚠️ No relevant headlines found.")
