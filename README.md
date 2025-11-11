# 📊 CrossAlpha – 개인 포트폴리오 맞춤형 금융 리스크&인사이트 대시보드

## 📝 팀 주제  
시간과 전문성이 부족한 개인 투자자를 위한,  
거시경제·산업 뉴스가 내 포트폴리오에 미치는 리스크와 인사이트를  
**한눈에 보여주는 금융 대시보드 프로젝트**  

<br>

## 👩‍💻 팀원 소개  

| 학번 | 이름 | 역할 |
|------|------|------|
| 2376175 | **유채은** | Backend / AI |
| 2276256 | **이혜령** | Frontend / AI / 팀장 |
| 2376302 | **최지희** | Backend / AI |

📌 [팀 그라운드룰 보기](https://github.com/ahrixxx/Graduation-Project/blob/main/GroundRule.md)  

<br>

## 🚀 프로젝트 개요  
많은 개인 투자자들은 뉴스, 경제 지표, 차트를 접해도  
**"내 종목과 무슨 관련이 있는지"** 이해하기 어렵습니다.  
또한 바쁜 직장인은 관심종목을 꾸준히 확인하지 못해  
기회를 놓치거나 리스크 대응이 늦어지곤 합니다.  

**CrossAlpha**는 이런 문제를 해결하기 위해:  
- 📌 **관심종목 리스크 이벤트 추적 및 알림**  
- 📰 **시장/섹터 트렌드 요약 카드 제공**  
- 📉 **이동평균선 이탈·변동성 급등·최대 낙폭 초과 등 객관적 리스크 신호 제공**  

을 통해 투자자가 스스로 판단할 수 있도록 돕는 **웹 대시보드 서비스**입니다.  

<br>

## 🔑 주요 기능
- **리스크 이벤트 자동 감지**  
  - 이동평균선 이탈, 변동성 급등, 최대 낙폭 초과 신호 제공  
- **AI 차트 분석 & 주요 뉴스 요약**  
  - AI가 차트의 기술적 분석과 각 종목의 주요 뉴스 요약을 제공
- **차트를 같이 보는 AI 챗봇**  
  - 차트 지표가 잘 해석이 안된다면? PER, RSI, 이동평균선 등 차트 지표를 초보자 친화적으로 설명하는 RAG 기반 챗봇에게 질문!
- **투자 행동 학습 로그**
 - 사용자가 매매 이유 기록시, AI가 당시 시장 지표를 자동으로 캡처 → 투자 결정의 맥락과 감정적 요인을 함께 분석
 - -> 사용자의 반복되는 판단 패턴과 편향을 시각화함으로써 사용자가 스스로 인식하고 학습할 수 있도록 피드백
<br>

## 🛠 기술 스택  

### 📊 데이터 분석 및 모델링
- [Python](https://www.python.org) – 데이터 처리 및 분석  
- [Pandas](https://pandas.pydata.org) – 시계열 데이터 처리 및 지표 계산  
- [NumPy](https://numpy.org) – 수치 계산  

### ⚙️ 백엔드
- [FastAPI](https://fastapi.tiangolo.com) – Python 기반 경량 웹 프레임워크  
- [PostgreSQL](https://www.postgresql.org) – 포트폴리오 및 시계열 데이터 저장  

### 💻 프론트엔드
- [React.js](https://react.dev) – 대시보드 UI 개발  
- [Plotly](https://plotly.com) – 대화형 차트 및 데이터 시각화  

### 🤖 AI / NLP
- [OpenAI GPT API](https://platform.openai.com) – 뉴스 요약, 리스크 이벤트 설명, 개인화 코멘트  

### 📡 외부 데이터 소스
- [Alpha Vantage](https://www.alphavantage.co) – 금융/경제 데이터 API  
- [Yahoo Finance API (yfinance)](https://pypi.org/project/yfinance/) – 주식/ETF 시세 데이터  
