# 📊 CrossAlpha – 금융 리스크 인사이트 대시보드  



## 📝 팀 주제  
시간과 전문성이 부족한 개인 투자자를 위한,  
거시경제·산업 뉴스가 내 포트폴리오에 미치는 리스크와 인사이트를  
**한눈에 보여주는 금융 대시보드 프로젝트**  

<br><br>  

## 👩‍💻 팀원 소개  

| 학번 | 이름 | 역할 |
|------|------|------|
| 2376175 | **유채은** | Backend / AI |
| 2276256 | **이혜령** | Frontend / AI / 팀장 |
| 2376302 | **최지희** | Backend / AI |

📌 [팀 그라운드룰 보기](https://github.com/ahrixxx/Graduation-Project/blob/main/GroundRule.md)  

<br><br>  

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

<br><br>  

## 🔑 주요 기능
- **리스크 이벤트 자동 감지**  
  - 이동평균선 이탈, 변동성 급등, 최대 낙폭 초과 신호 제공  
- **뉴스-포트폴리오 연결 설명**  
  - "환율 상승 → IT 업종 위험", "유가 하락 → 항공사 수혜" 등 종목·섹터 영향 해설  
- **투자 지표 해설**  
  - PER, RSI, 이동평균선 등 차트 지표를 초보자 친화적으로 설명  
- **시장/섹터 트렌드 요약 카드**  
  - 하루 1분 만에 확인 가능한 거시경제·산업 이벤트 요약  
- **관심종목 알림 시스템**  
  - 등록만 해두면 리스크 이벤트 발생 시 즉시 푸시 알림  

<br><br>  

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
