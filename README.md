# 🥠 오늘의 마음쿠키
중1 학생이 감정 단어를 최대 2개 고르고, 150자 이내 이야기를 적으면 Gemini 또는 GPT가 답합니다.

## GitHub → Streamlit 실행
1. 새 GitHub 저장소에 `app.py`와 `requirements.txt`를 올립니다. 기존 앱을 유지하려면 별도 저장소를 만드세요.
2. Streamlit Community Cloud https://share.streamlit.io/ 에서 Create app을 선택합니다.
3. 해당 저장소와 브랜치를 고르고 Main file path를 `app.py`로 지정합니다.
4. Advanced settings의 Secrets에 아래 중 사용할 서비스의 설정을 넣습니다. 이미 배포했다면 앱 Settings → Secrets에서 설정합니다.
5. Deploy를 누릅니다. 두 키를 모두 설정하면 학생 화면에서 Gemini/GPT를 선택할 수 있습니다. 키가 없으면 체험만 가능합니다.

Gemini:
```toml
GEMINI_API_KEY = "여기에 실제 Gemini API 키"
GEMINI_MODEL = "gemini-2.5-flash"
```
키 발급: https://aistudio.google.com/apikey

GPT:
```toml
OPENAI_API_KEY = "여기에 실제 OpenAI API 키"
OPENAI_MODEL = "gpt-5-mini"
```
키 발급: https://platform.openai.com/api-keys

실제 키는 GitHub나 학생 입력창, 채팅에 올리지 마세요. Secrets에서만 설정합니다. `secrets.example.toml`은 형식 참고용이며 이 파일을 올리는 것만으로 키가 적용되지는 않습니다. 모델 이용 가능 여부에 따라 Secrets의 모델명을 변경할 수 있습니다. 제공사 API 계정의 이용 한도와 과금 설정을 확인하세요.

## 파일
- app.py: 전체 앱. 이 파일 하나에 감정 목록·디자인·API 호출 포함
- requirements.txt: 필수 패키지
- .streamlit/config.toml: 선택 사항인 색상 테마
- secrets.example.toml: 키 설정 예시(실제 키 없음)
- .gitignore: 로컬 비밀 파일 제외

## 동작과 데이터
- 제공된 대화의 감정 목록 124개를 사용합니다(원본 사진은 이번 실행 환경에서 열 수 없어, 대화에 전사된 목록 기준).
- 감정 선택, 검색, 혼합 감정, 선택적 이야기 입력, 재생성, 초기화 제공.
- 선택한 서비스에만 감정·이야기를 전달합니다. API 키는 서버에서만 사용합니다.
- 대화는 현재 브라우저 연결의 Streamlit 세션 메모리에만 유지하며 앱은 파일·DB에 저장하지 않습니다. 외부 API 제공사의 데이터 처리 정책은 별도로 적용됩니다. OpenAI 호출은 store=false입니다.
- 체험 문구를 실제 AI 답변으로 표시하지 않습니다. AI 호출 실패 시 오류를 표시합니다.
- 응답은 HTML 이스케이프하여 표시합니다. 타임아웃·키 오류·이용 한도·형식 오류를 처리합니다.
- 세션별 재요청 간격 8초를 적용합니다. 이는 전역 과금 한도나 강력한 남용 방지는 아닙니다.
- 위기 표현 시 안전한 장소·믿을 수 있는 어른의 도움을 권하도록 프롬프트를 설정했습니다. 자동 감지나 전문 상담 기능은 아닙니다.

## 로컬 실행
Python 3.11 이상 권장.
```sh
pip install -r requirements.txt
streamlit run app.py
```
로컬 키는 `.streamlit/secrets.toml`에 저장합니다.

## 확인 범위
Python 구문 검사 및 Streamlit AppTest로 화면 로딩·선택·체험·초기화 확인. 제공사별 HTTP 응답을 모의하여 요청 구성과 결과 파싱 확인. 실제 API 키가 제공되지 않아 Gemini/GPT의 실응답과 실제 과금은 검증하지 않았습니다.

공식 안내:
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
