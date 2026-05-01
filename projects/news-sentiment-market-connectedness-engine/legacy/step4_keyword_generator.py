import openai
import os
import spacy
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Legacy prototype note: never hardcode API keys in source files.
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# --- GPT method ---
def generate_keywords_gpt(company):
    print(f"\n🔮 GPT-generated keywords for {company}:\n")
    prompt = f"List 10 keywords or phrases relevant to current financial news about {company}. Include product names, people, controversies, and sectors."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial research assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=150
        )
        print(response.choices[0].message.content)
    except Exception as e:
        print("⚠️ GPT API call failed:", e)

# --- spaCy method (uses Wikipedia description) ---
def fetch_wiki_text(company):
    url = f"https://en.wikipedia.org/wiki/{company.strip().replace(' ', '_')}_Inc."
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all('p')
        return ' '.join([p.get_text() for p in paragraphs[:2]])  # Limit to intro
    except:
        return ""

def generate_keywords_spacy(company):
    print(f"\n🧠 spaCy keyword extraction for {company}:\n")
    text = fetch_wiki_text(company)
    if not text:
        print("⚠️ Could not fetch Wikipedia content.")
        return

    doc = nlp(text)
    keywords = set()
    for chunk in doc.noun_chunks:
        if len(chunk.text) > 2:
            keywords.add(chunk.text.strip().lower())

    for kw in list(keywords)[:10]:
        print("-", kw)

# --- Run both ---
if __name__ == "__main__":
    company = input("Enter a company name (e.g., Apple, Tesla): ").strip()
    generate_keywords_gpt(company)
    generate_keywords_spacy(company)
