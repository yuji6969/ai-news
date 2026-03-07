import yfinance as yf
import requests
import datetime

NEWS_API_KEY = "a8b54719948048b596a75cc1e2cd00d8"

STOCKS = [
    {"ticker": "GOOGL", "name": "Google (Alphabet)", "query": "Google Alphabet AI", "points": "GeminiとGoogle Cloudの競争力"},
    {"ticker": "META",  "name": "Meta",              "query": "Meta AI investment",   "points": "AI投資額・広告収益・LLaMAの進捗"},
    {"ticker": "AMZN",  "name": "Amazon",             "query": "Amazon AWS AI",        "points": "AWS（クラウド）のAI需要"},
    {"ticker": "AAPL",  "name": "Apple",              "query": "Apple AI features",    "points": "Apple Intelligence・製品サイクル"},
    {"ticker": "NVDA",  "name": "NVIDIA",             "query": "NVIDIA GPU AI",        "points": "AI半導体需要・データセンター向け売上"},
    {"ticker": "MSFT",  "name": "Microsoft",          "query": "Microsoft OpenAI Azure","points": "OpenAI投資・Azure AIの成長"},
]

def translate(text):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {"client": "gtx", "sl": "en", "tl": "ja", "dt": "t", "q": text}
    try:
        res = requests.get(url, params=params, timeout=5)
        return res.json()[0][0][0]
    except:
        return text

today = datetime.date.today()
results = []

for stock in STOCKS:
    ticker = yf.Ticker(stock["ticker"])
    hist = ticker.history(period="2d")
    info = ticker.info

    latest = hist["Close"].iloc[-1]
    prev = hist["Close"].iloc[-2]
    change = (latest - prev) / prev * 100
    change_icon = "📈" if change >= 0 else "📉"

    next_earnings = info.get("earningsDate", None)
    if next_earnings:
        try:
            earnings_str = datetime.datetime.fromtimestamp(next_earnings[0]).strftime("%Y-%m-%d")
        except:
            earnings_str = "不明"
    else:
        earnings_str = "不明"

    news_items = []
    url = f"https://newsapi.org/v2/everything?q={stock['query']}&language=en&sortBy=publishedAt&pageSize=3&apiKey={NEWS_API_KEY}"
    try:
        res = requests.get(url)
        articles = res.json().get("articles", [])
        for a in articles:
            title_ja = translate(a.get("title", ""))
            published = a.get("publishedAt", "")[:10]
            news_items.append(f"[{published}] {title_ja}")
    except:
        news_items.append("ニュース取得失敗")

    results.append({
        "name": stock["name"],
        "price": f"${latest:.2f}",
        "change": f"{change:+.2f}%",
        "change_icon": change_icon,
        "earnings": earnings_str,
        "points": stock["points"],
        "news": news_items
    })

lines = [f"=== AI・ビッグテック チェック {today} ===\n"]
for r in results:
    lines.append(f"【{r['name']}】 {r['change_icon']} {r['price']}  前日比: {r['change']}")
    lines.append(f"  次回決算: {r['earnings']}")
    lines.append(f"  注目ポイント: {r['points']}")
    lines.append(f"  📰 最新ニュース:")
    for n in r["news"]:
        lines.append(f"    ・{n}")
    lines.append("")
lines.append("=== チェック完了 ===")

with open("result.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("\n".join(lines))
