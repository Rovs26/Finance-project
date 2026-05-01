from googlesearch import search
from newspaper import Article
import pandas as pd
from datetime import datetime, timedelta
import time

company = input("Enter company name (e.g., Apple, Tesla): ").strip()
days_back = 10  # You can increase to 30

all_results = []

for i in range(days_back):
    day = datetime.now() - timedelta(days=i)
    date_str = day.strftime('%Y-%m-%d')
    query = f"{company} financial news before:{date_str}"

    print(f"🔍 Searching for: {query}")

    try:
        urls = list(search(query, num_results=5))
        for url in urls:
            try:
                article = Article(url)
                article.download()
                article.parse()

                all_results.append({
                    "date": day.date(),
                    "company": company,
                    "headline": article.title
                })

                print(f"✅ {article.title[:60]}...")

                time.sleep(1)  # Respectful delay
            except:
                print(f"❌ Failed to parse: {url}")
                continue
    except:
        print(f"❌ Google search failed on: {query}")

# Save to CSV
df = pd.DataFrame(all_results)
df.to_csv("scraped_news.csv", index=False)
print("\n✅ Saved multi-day headlines to scraped_news.csv")
