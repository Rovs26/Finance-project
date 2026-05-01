# Interview Talking Points

## 1. What does this project do?

It cleans a recovered financial news sentiment prototype, scores headlines, merges sentiment with market data, and creates a connectedness view with clear limitations.

## 2. Why did you add OpenAI structured scoring?

The recovered sentiment log had headline text. Structured scoring made the output more useful by returning company, ticker, score, label, confidence, rationale, risk flags, and a research signal in a consistent schema.

## 3. How did you handle the API key safely?

The project reads local settings from `.env`, keeps `.env` ignored, provides `.env.example` with placeholders, and avoids printing or saving credentials.

## 4. What happens if OpenAI scoring is unavailable?

The workflow falls back to transparent keyword-based scoring. That keeps the project runnable without external model access.

## 5. How are signal labels created?

Signals are based on sentiment score thresholds: `SELL` for scores at or below `-0.25`, `BUY` for scores at or above `0.25`, and `HOLD` otherwise. They are research labels only, not trading advice.

## 6. Why was formal GFEVD not used?

The recovered merged dataset has only two observations and incomplete market values. Running formal GFEVD on that would be misleading.

## 7. What connectedness method did you use instead?

I used an absolute-correlation fallback to show the connectedness workflow shape while documenting that it is exploratory.

## 8. What are the main data limitations?

The scraped news file is empty, the sentiment log has only 11 rows, and the merged market dataset has only two rows with incomplete market data.

## 9. What would you improve next?

I would rebuild the scraped news dataset, expand tickers and dates, validate sentiment labels manually, rebuild market returns, and only then run formal GFEVD.

## 10. How is this relevant to finance roles?

It shows practical research engineering: cleaning a prototype, preserving legacy logic, handling credentials safely, producing reproducible outputs, and refusing to overstate weak data.
