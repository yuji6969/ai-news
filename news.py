import yfinance as yf
import requests
import datetime
import json

NEWS_API_KEY = "a8b54719948048b596a75cc1e2cd00d8"

STOCKS = [
    {"ticker": "GOOGL", "name": "Google (Alphabet)", "query": "Google Alphabet AI", "points": "Gemini（AI）とGoogle Cloudの競争力"},
    {"ticker": "META",  "name": "Meta",              "query": "Meta AI investment",   "points": "AI投資額・広告収益・LLaMAの進捗"},
    {"ticker": "AMZN",  "name": "Amazon",             "query": "Amazon AWS AI",        "points": "AWS（クラウド）のAI需要"},
    {"ticker": "AAPL",  "name": "Apple",              "query": "Apple AI features",    "points": "Apple Intelligence・製品サイクル"},
    {"ticker": "NVDA",  "name": "NVIDIA",             "query": "NVIDIA GPU AI",        "points": "AI半導体需要・データセンター向け売上"},
    {"ticker": "MSFT",  "name": "Microsoft",          "query": "Microsoft OpenAI Azure","points": "OpenAI投資・Azure AIの成長"},
]

today = datetime.date.today()
lines = []
lines.append(f"=== AI・ビッグテック チェック {today} ===\n")

for stock in STOCKS:
    ticker = yf.Ticker(stock["ticker"])
    hist = ticker.history(period="2d")
    info = ticker.info

    latest = hist["Close"].iloc[-1]
    prev = hist["Close"].iloc[-2]
    change = (latest - prev) / prev * 100

    next_earnings = info.get("earningsDate", None)
    if next_earnings:
        try:
            earnings_str = datetime.datetime.fromtimestamp(next_earnings[0]).strftime("%Y-%m-%d")
        except:
            earnings_str = "不明"
    else:
        earnings_str = "不明"

    lines.append(f"【{stock['name']}】")
    lines.append(f"  株価: ${latest:.2f}  前日比: {change:+.2f}%")
    lines.append(f"  次回決算: {earnings_str}")
    lines.append(f"  注目ポイント: {stock['points']}")

    # ニュース取得
    url = f"https://newsapi.org/v2/everything?q={stock['query']}&language=en&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
    try:
        res = requests.get(url)
        articles = res.json().get("articles", [])
        lines.append("  📰 最新ニュース:")
        for a in articles:
            title = a.get("title", "")
            published = a.get("publishedAt", "")[:10]
            lines.append(f"    [{published}] {title}")
    except:
        lines.append("  📰 ニュース取得失敗")

    lines.append("")

lines.append("=== チェック完了 ===")

with open("result.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("\n".join(lines))
