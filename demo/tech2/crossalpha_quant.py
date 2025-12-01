import os
import json
from datetime import datetime, timedelta

import FinanceDataReader as fdr
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# 0. 환경 설정

load_dotenv()  # .env에서 환경변수 로드
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY가 .env 파일에 설정되어 있지 않습니다.")

client = OpenAI(api_key=API_KEY)


# 1. 주가 데이터 로드 + 기술 지표 계산

def load_price(symbol, period=365):

    #오늘 기준 최근 period일 주가 데이터 로드.
    #FinanceDataReader 사용.

    end = datetime.today().date()
    start = end - timedelta(days=period)

    df = fdr.DataReader(symbol, start=start, end=end)
    df = df.rename(
        columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    )
    return df[["open", "high", "low", "close", "volume"]]


def calc_rsi(close, period=14):

    #기본형 RSI 계산 (단순 이동평균 기반).

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calc_indicators(df):

    #SMA20/50/120, RSI14, Bollinger Bands, Bollinger Width 계산.

    out = df.copy()

    # 이동평균 (SMA)
    out["sma_20"] = out["close"].rolling(20).mean()
    out["sma_50"] = out["close"].rolling(50).mean()
    out["sma_120"] = out["close"].rolling(120).mean()

    # RSI(14)
    out["rsi_14"] = calc_rsi(out["close"], 14)

    # Bollinger Band (20일 기준, ±2표준편차)
    mid = out["close"].rolling(20).mean()
    std = out["close"].rolling(20).std()
    out["bb_mid"] = mid
    out["bb_upper"] = mid + 2 * std
    out["bb_lower"] = mid - 2 * std

    # Bollinger Width
    out["bollinger_width"] = (out["bb_upper"] - out["bb_lower"]) / out["bb_mid"]

    return out.dropna()


def categorize_volatility(width_value, low_th, high_th):
    """
    볼린저 폭 분위수를 기준으로 변동성 구간 라벨링.
    - 상위 33% 이상: '높음'
    - 하위 33% 이하: '낮음'
    - 나머지: '보통'
    """
    if width_value >= high_th:
        return "높음"
    elif width_value <= low_th:
        return "낮음"
    return "보통"


def calc_support_resistance(df_calc, window=60):
    """
    최근 window일 종가 기준:
    - 최저가 = 지지선
    - 최고가 = 저항선
    """
    recent = df_calc.tail(window)
    support = float(recent["close"].min())
    resistance = float(recent["close"].max())
    return support, resistance


# 2. Snapshot 구성 - GPT에 넘길 요약 데이터 구조 (JSON 형태)

def make_snapshot(symbol, df_calc, display_name=None):
    """
    GPT에 전달할 Snapshot 생성.
    - symbol / name
    - date / price
    - volatility (낮음/보통/높음)
    - support / resistance
    - indicators (SMA20/50/120, RSI14, Bollinger Width)
    """
    last = df_calc.iloc[-1]

    # 변동성 분위수 계산
    width_series = df_calc["bollinger_width"].dropna()
    low_th = float(width_series.quantile(0.33))
    high_th = float(width_series.quantile(0.66))

    volatility = categorize_volatility(float(last["bollinger_width"]), low_th, high_th)
    support, resistance = calc_support_resistance(df_calc)

    name = display_name if display_name is not None else symbol

    snapshot = {
        "symbol": symbol,
        "name": name,
        "date": last.name.strftime("%Y-%m-%d"),
        "price": float(last["close"]),
        "volatility": volatility,
        "support": support,
        "resistance": resistance,
        "indicators": {
            "sma_20": float(last["sma_20"]),
            "sma_50": float(last["sma_50"]),
            "sma_120": float(last["sma_120"]),
            "rsi_14": float(last["rsi_14"]),
            "bollinger_width": float(last["bollinger_width"]),
        },
    }
    return snapshot

# 3. 프롬프트 설계

SYSTEM_PROMPT = """
당신은 초보 개인 투자자를 위한 기술적 지표 해설 전문가입니다.

반드시 지켜야 할 것:
- 모든 결과는 한국어로 작성합니다.
- 매수/매도, 종목 추천 등 직접적인 투자 조언을 하지 않습니다.
- 미래 가격을 단정적으로 예측하지 않습니다.
- 주어진 스냅샷(JSON)에 포함된 정보만 근거로 사용합니다.
- 초보자도 이해할 수 있도록, 전문 용어는 필요 시 괄호로 간단히 풀어서 설명합니다.

톤:
- 중립적이고 차분한 톤
- "확실하다", "반드시 오른다/내린다"와 같은 표현은 사용하지 않습니다.
""".strip()

USER_PROMPT_TEMPLATE = """
아래는 사용자가 선택한 종목에 대한 기술적 지표 스냅샷(JSON)입니다.

요구사항:
1) "주요 신호" 섹션을 작성하세요.
   - SMA20/50/120, RSI14, Bollinger 폭 등을 기반으로
     핵심 신호를 3~4개 불릿 포인트로 정리합니다.
   - 단순 숫자 나열이 아니라, '해당 지표 상태가 무엇을 의미하는지'를 중심으로 설명합니다.

   예시:
     - 20일선이 50일선 위에 있어 단기 상승 흐름을 유지하고 있습니다.
     - 현재가 120일선 위에 위치해 장기 우상향 기조를 나타냅니다.
     - RSI가 50대 중반으로, 과열되지 않은 범위 내에서 상승 모멘텀이 이어지고 있습니다.
     - 볼린저 밴드 폭이 최근 확대되어 단기 변동성이 증가한 상황입니다.

2) "차트 요약" 섹션을 작성하세요.
   - 변동성, 지지선, 저항선 값을 활용하여
     현재 차트 상황을 2~4문장으로 종합적으로 설명합니다.
   - 예측이 아니라, 현재 상태를 기반으로 작성하세요.
   - 예시:
       - 최근 변동성이 확대되며 가격 움직임이 커진 상황입니다.
       - 현재 가격은 주요 지지선 위에 있어 단기적으로 방어력이 있는 위치입니다.
       - 다만 저항선과의 가격 차이가 좁아져 주의 깊은 관찰이 필요합니다.

형식 예시는 다음과 같습니다:

주요 신호:
- ...

차트 요약:
- ...

스냅샷(JSON):
{snapshot_json}

위 두 개 섹션만 출력하세요.
JSON, 코드 블록, 추가 설명 문구는 포함하지 마세요.
""".strip()


def build_user_prompt(snapshot):

    #Snapshot(dict)를 JSON 문자열로 직렬화해서 USER_PROMPT_TEMPLATE에 삽입.

    snapshot_json = json.dumps(snapshot, ensure_ascii=False, indent=2)
    prompt = USER_PROMPT_TEMPLATE.format(snapshot_json=snapshot_json)
    return prompt


def explain_with_gpt(user_prompt):

    #OpenAI GPT API 호출하여 SYSTEM_PROMPT + USER_PROMPT로 차트 해석 텍스트 생성.

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=600,
    )
    return response.choices[0].message.content

# 4. 데모 엔트리포인트

def demo(symbol="005930", name="삼성전자"):
    """
    1) 가격 데이터 로드
    2) 지표 계산
    3) Snapshot 생성
    4) GPT 해설 생성
    5) Snapshot / GPT 결과 출력
    """
    df = load_price(symbol)
    df_calc = calc_indicators(df)
    snapshot = make_snapshot(symbol, df_calc, display_name=name)
    user_prompt = build_user_prompt(snapshot)
    explanation = explain_with_gpt(user_prompt)

    print("=== Snapshot (입력) ===")
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    print("\n=== GPT 해석 (출력) ===\n")
    print(explanation)


if __name__ == "__main__":
    demo()
