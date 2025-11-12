## Team 11 CrossAlpha

| 항목 | 내용 |
|---|---|
| **프로젝트명** | 시간과 전문성이 부족한 개인 주식 투자자를 위한,포트폴리오 기반 투자 행동 인사이트 & 학습 서비스 |
| **프로젝트 키워드** | 리스크 관리, 관심종목 추적, 섹터 트렌드, 초보자 질문 해소, 데이터 시각화, GPT 요약 |
| **트랙** | 산학 |
| **프로젝트 멤버** | 이혜령, 유채은, 최지희 |
| **팀지도 교수** | 이민수 교수님 |
| **무엇을 만들고자 하는가** | **CrossAlpha**는 투자자의 인지–판단–행동을 연결하는 AI 대시보드로, 다음 세 가지 기능을 제공합니다.<br><br> ① **정성적 분석 — 섹터별 뉴스 맥락 해석 및 톤 분석**<br>  - Alpha Vantage API로 섹터별 뉴스를 수집하고 감성·관련도·영향도를 분석<br> - ChatGPT API가 뉴스 맥락을 자연어로 요약<br> - 섹터별 톤(긍정/중립/부정) 및 종목 단위의 매수·보류·매도 신호 제공<br> - 매일 오전 9시, 5개 핵심 섹터(Tech&#124;Finance&#124;Retail 등) 업데이트<br><br> ② **정량적 분석 — 포트폴리오 기반 핵심 지표 시각화**<br> - FinanceDataReader로 사용자 포트폴리오 종목 데이터 수집<br> - SMA, RSI, Bollinger 등 주요 기술지표 계산 및 해석 제공<br> - 하단의 RAG 기반 챗봇이 지표 해석을 사용자 눈높이에 맞춰 설명<br> - 모든 대화 내용은 “투자 학습 로그”에 자동 저장<br><br> ③ **투자 행동 학습 로그 — 나의 매매 패턴을 학습하다**<br> - 사용자가 매수/매도 기록 입력 시, 당시 시장 데이터·지표·뉴스 감성을 자동 캡처<br> - 사용자는 “의도” + “확신도 슬라이더” + “행동 유형 태그”를 기록<br> - 일정 개수 이상 쌓이면 AI가 투자 행동 리포트 제공<br> - 자신의 투자 성향(예: 추세추종형&#124;FOMO형 등)을 인식하고 개선 가능 |
| **고객** | 👩 김이화 (29세, 직장인 투자자)<br>- **고객 경험** : 주식 투자 2년 차, 업무로 바빠서 시장을 실시간으로 추적하지 못하고, 매매 후 “왜 샀는지”조차 잊는 경우가 많음. 뉴스나 지표를 봐도 내 종목과의 연결고리를 이해하기 어려움.<br>- **고객 요구** :<br>1. 매매 판단의 근거를 스스로 기록하고 되돌아볼 수 있는 도구<br>2. 뉴스·지표·차트를 내 포트폴리오 맥락으로 자동 연결해주는 설명<br>3. 내 투자 패턴과 편향을 시각적으로 보여주는 개인화 리포트 |
| **Pain Point** | ① **자기 판단 근거 부재** : 매수/매도 결정을 내리지만, “왜 그렇게 했는지”를 기록하지 않아 나중에 같은 실수를 반복함.<br><br>② **정보-행동 간 단절** : 뉴스나 지표를 접해도 자신의 종목과 어떤 관계가 있는지 파악하지 못해, 반응이 감정적·즉흥적으로 이루어짐.<br><br>③ **피드백 구조의 부재** : 투자 후 결과를 돌아볼 기회가 없고, AI 기반 피드백이나 행동 분석이 제공되지 않아 스스로 학습하기 어려움.<br><br>④ **시간 제약** : 직장인은 시장을 실시간으로 추적할 여유가 없고, 매매 타이밍을 놓치거나 리스크 대응이 늦어짐.|
| **사용할 소프트웨어 패키지의 명칭과 핵심기능/용도** | **데이터 분석 및 모델링**<br>- Python: 데이터 처리 및 분석 언어<br>- Pandas: 시계열 데이터 처리 및 지표 계산<br>- NumPy: 수치 계산 라이브러리<br><br>**백엔드**<br>- FastAPI: Python 기반 경량 웹 프레임워크<br>- PostgreSQL: 포트폴리오 및 시계열 데이터 저장용 DB<br><br>**프론트엔드**<br>- React.js: 대시보드 UI 개발용 JS 라이브러리<br>- Plotly: 대화형 차트 및 시각화 라이브러리<br><br>**AI/자연어 처리**<br>- OpenAI GPT API: 뉴스 요약, 리스크 이벤트 설명, 개인화 코멘트 생성<br><br>**외부 데이터 소스**<br>- Alpha Vantage: 금융/경제 데이터 API<br>- Yahoo Finance API (yfinance): 주식/ETF 시세 데이터 |
| **사용할 소프트웨어 패키지의 명칭과 URL** | - Python: https://www.python.org<br>- Pandas: https://pandas.pydata.org<br>- NumPy: https://numpy.org<br>- FastAPI: https://fastapi.tiangolo.com<br>- PostgreSQL: https://www.postgresql.org<br>- React.js: https://react.dev<br>- Plotly: https://plotly.com<br>- OpenAI GPT API: https://platform.openai.com<br>- Alpha Vantage: https://www.alphavantage.co<br>- Yahoo Finance API (yfinance): https://pypi.org/project/yfinance/ |
| **팀그라운드룰** | https://github.com/ahrixxx/Graduation-Project/blob/main/GroundRule.md |
| **최종수정일** | 2025.11.12 |
