# sector_news_single.py
# Alpha Vantage API로 1개 섹터 뉴스 수집 → GPT로 한국어 요약 + 톤 분석(2~3문장) → JSON/Markdown 저장

import os, json, datetime as dt
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI
import time  # 매일 지정된 시각 실행을 위한 time 모듈

# 0. 환경 로드 (.env에 API 키 저장)
load_dotenv()
ALPHA_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not ALPHA_KEY or not OPENAI_KEY:
    raise SystemExit(" .env에 API 키를 확인할 것")

client = OpenAI(api_key=OPENAI_KEY)

# 1. 분석할 섹터 지정
SECTOR_KEY = "financial_markets"
SECTOR_NAME = "Financial Markets"
ALPHA_ENDPOINT = "https://www.alphavantage.co/query"

# 2. Alpha Vantage 뉴스 가져오기
def fetch_sector_news(topic: str, limit: int = 5, days: int = 7):
    time_from = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).strftime("%Y%m%dT%H%M")
    params = {
        "function": "NEWS_SENTIMENT",
        "topics": topic,
        "time_from": time_from,
        "sort": "LATEST",
        "limit": str(limit),
        "apikey": ALPHA_KEY,
    }
    r = requests.get(ALPHA_ENDPOINT, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def compact_article(a: dict):
    return {
        "id": a.get("uuid") or a.get("id") or a.get("url"),
        "title": a.get("title"),
        "summary": a.get("summary"),
        "overall_sentiment_score": a.get("overall_sentiment_score"),
        "overall_sentiment_label": a.get("overall_sentiment_label"),
        "tickers": [
            {
                "ticker": t.get("ticker"),
                "relevance_score": t.get("relevance_score"),
                "ticker_sentiment_score": t.get("ticker_sentiment_score"),
                "ticker_sentiment_label": t.get("ticker_sentiment_label"),
            } for t in (a.get("ticker_sentiment") or [])
        ],
    }

# 3. GPT 출력 구조 정의
class TickerSummary(BaseModel):
    ticker: str
    summary: str = Field(max_length=500)
    tone: str  # "긍정", "중립", "부정"
    confidence: float = Field(ge=0.0, le=1.0)

class SectorOutput(BaseModel):
    sector: str
    sector_display: str
    sector_summary: str = Field(max_length=400)
    tickers: list[TickerSummary]
    evidence_article_ids: list[str]

# 4.  프롬프트 (한국어, 종목 요약 2~3문장으로 강화)
SYSTEM_PROMPT = """
당신은 금융 뉴스 요약가이자 감성(톤) 분류기입니다.

반드시 지켜야 할 것:
- 모든 결과는 한국어로 작성합니다.
- 유효한 JSON만 반환합니다. (앞뒤에 설명 금지)
- 주어진 기사 내용만 근거로 사용합니다.

출력 JSON 필드:
- sector_summary: 한국어 3~4문장으로 섹터 요약 (최대 400자)
- tickers: 각 종목별 요약
    - ticker: 티커 코드
    - summary: 한국어 2~3문장으로 종목의 주요 이슈, 그 의미, 향후 전망을 구체적으로 요약
    - tone: "긍정", "중립", "부정" 중 하나
    - confidence: 0.0 ~ 1.0 (신뢰도)
- evidence_article_ids: 사용한 기사 ID 3개 이상

톤 판정 기준:
- 긍정: 실적·가이던스 상향, 신규 수요, 성장 전망, 긍정적 산업 모멘텀
- 중립: 긍정과 부정 요인이 혼재, 불확실성 높음, 단기 관망세
- 부정: 실적 부진, 리콜·소송, 전망 하향, 수요 감소
"""

USER_PROMPT_TEMPLATE = """
섹터: {sector_display}

아래 기사(JSON)를 근거로, 요구된 형식의 JSON만 반환하세요.

요구사항:
1) sector_summary: 한국어 3~4문장
2) tickers[].summary: 한국어 2~3문장 (핵심 이슈 + 의미 + 전망 포함)
3) tickers[].tone: "긍정" | "중립" | "부정"
4) evidence_article_ids: 사용 기사 ID 3개 이상

기사 목록(JSON):
{articles_json}

반드시 올바른 JSON만 반환하세요.
"""

# 5. GPT 호출
def analyze_with_gpt(sector_key, sector_display, articles):
    prompt = USER_PROMPT_TEMPLATE.format(
        sector_display=sector_display,
        articles_json=json.dumps(articles, ensure_ascii=False)
    )
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    text = resp.choices[0].message.content.strip()
    if not text.startswith("{"):
        s, e = text.find("{"), text.rfind("}")
        text = text[s:e+1]
    data = json.loads(text)
    data["sector"] = sector_key
    data["sector_display"] = sector_display
    return SectorOutput(**data).model_dump()

# 톤 정규화 + 기사 ID 포맷 헬퍼
def _normalize_tone(tone: str) -> str:
    t = (tone or "").strip().lower()
    if t in ("긍정", "positive", "pos", "buy", "매수"):
        return "긍정"
    if t in ("중립", "neutral", "neu", "hold", "보류"):
        return "중립"
    if t in ("부정", "negative", "neg", "sell", "매도"):
        return "부정"
    return "중립"

def _format_evidence_ids(ids: list[str], max_items: int = 5) -> str:
    if not ids:
        return ""
    items = ids[:max_items]
    bullet = "\n".join(f"- {i}" for i in items)
    return f"**근거 기사 IDs**\n{bullet}\n"

# 6. 마크다운 렌더링 (표 깔끔 버전)
def render_markdown(result):
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))
    ts = now.strftime("%Y-%m-%d %H:%M")

    lines = []
    lines.append(f"# 일일 섹터 뉴스 요약 — {ts} KST")
    lines.append("")
    lines.append(f"## {result['sector_display']}")
    lines.append("")
    lines.append("1️. 섹터 요약 ")
    lines.append("")
    lines.append(result["sector_summary"].strip())
    lines.append("")
    lines.append("2️. 종목별 요약 및 톤(긍정/중립/부정)")
    lines.append("")
    lines.append("| 종목 | 톤 | 신뢰도 | 요약 |")
    lines.append("|---|---|---:|---|")

    for t in result.get("tickers", []):
        tone = _normalize_tone(t.get("tone", ""))
        conf = t.get("confidence", 0.0)
        summary = (t.get("summary") or "").replace("\n", " ").strip()
        ticker = t.get("ticker") or "-"
        lines.append(f"| {ticker} | **{tone}** | {conf:.2f} | {summary} |")

    lines.append("")
    ev = _format_evidence_ids(result.get("evidence_article_ids", []))
    if ev:
        lines.append(ev)

    return "\n".join(lines)

# 7. 스케줄러 헬퍼 함수들
def seconds_until(hour: int = 19, minute: int = 5):
    kst = dt.timezone(dt.timedelta(hours=9))
    now = dt.datetime.now(kst)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if now >= target:
        target = target + dt.timedelta(days=1)
    return (target - now).total_seconds()

def run_daily_at_9():
    print("매일 9:00 KST에 섹터 뉴스 요약을 실행합니다.")
    while True:
        wait_sec = seconds_until(19, 5)
        kst = dt.timezone(dt.timedelta(hours=9))
        next_run = dt.datetime.now(kst) + dt.timedelta(seconds=wait_sec)
        print(f"다음 실행 예정: {next_run.strftime('%Y-%m-%d %H:%M:%S')} KST")
        time.sleep(wait_sec)
        try:
            main()
        except Exception as e:
            print("일일 실행 중 오류:", e)

# 8. 메인 실행 함수
def main():
    print(f"\n=== [Sector] {SECTOR_NAME} ===")

    data = fetch_sector_news(SECTOR_KEY)
    if "feed" not in data:
        print(" 뉴스 데이터 없음 또는 호출 제한.")
        return

    articles = [compact_article(a) for a in data["feed"]]
    try:
        result = analyze_with_gpt(SECTOR_KEY, SECTOR_NAME, articles)
    except ValidationError as e:
        print(" JSON 스키마 불일치:", e)
        return
    except Exception as e:
        print(" GPT 오류:", e)
        return

    os.makedirs("out", exist_ok=True)
    stamp = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime("%Y%m%d_%H%M")
    json_path = f"out/sector_summary_{SECTOR_KEY}_{stamp}.json"
    md_path = f"out/sector_summary_{SECTOR_KEY}_{stamp}.md"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(render_markdown(result))

    print(f"\n 결과 저장 완료:\n- {json_path}\n- {md_path}")

# 9. 실행 엔트리포인트
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "once":
        main()
    else:
        run_daily_at_9()
