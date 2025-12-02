# 🚀 LangGraph 멀티에이전트 실습 - 설치 및 실행 가이드

LLM 기반 에이전트 실전·응용 (중급) 과정을 위한 실습 프로젝트입니다.

## 📋 목차
1. [사전 준비사항](#1-사전-준비사항)
2. [프로젝트 다운로드](#2-프로젝트-다운로드)
3. [환경 설정](#3-환경-설정)
4. [Google OAuth 2.0 설정](#4-google-oauth-20-설정)
5. [실행](#5-실행)
6. [문제 해결](#6-문제-해결)

---

## 1. 사전 준비사항

### 필수 소프트웨어 설치

#### Windows 사용자

1. **Python 3.10 이상** 설치
   - https://www.python.org/downloads/ 에서 다운로드
   - 설치 시 **"Add Python to PATH"** 체크 필수!

2. **Git** 설치
   - https://git-scm.com/download/win 에서 다운로드
   - 기본 설정으로 설치

3. **설치 확인** (명령 프롬프트 또는 PowerShell에서 실행)
   ```bash
   python --version
   git --version
   ```

#### macOS 사용자

1. **Homebrew 설치** (터미널에서 실행)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Python & Git 설치**
   ```bash
   brew install python@3.11 git
   ```

3. **설치 확인**
   ```bash
   python3 --version
   git --version
   ```

---

## 2. 프로젝트 다운로드

### 방법 1: Git Clone (권장)

터미널 또는 명령 프롬프트에서 실행:

```bash
# 원하는 폴더로 이동
cd C:\Users\YourName\Documents  # Windows
cd ~/Documents                   # macOS/Linux

# 저장소 클론
git clone https://github.com/Shawn-CAIO/event-calendar-agent-langgraph.git

# 프로젝트 폴더로 이동
cd event-calendar-agent-langgraph
```

### 방법 2: ZIP 파일 다운로드

1. GitHub 페이지에서 **Code** → **Download ZIP** 클릭
2. 다운로드한 ZIP 파일 압축 해제
3. 터미널에서 압축 해제한 폴더로 이동

---

## 3. 환경 설정

### 1) 가상환경 생성 (권장)

**Windows (명령 프롬프트):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

가상환경이 활성화되면 프롬프트 앞에 `(venv)`가 표시됩니다.

### 2) 패키지 설치

```bash
pip install -r requirements.txt
```

**설치되는 주요 패키지:**
- `langgraph` - LangGraph 워크플로우 엔진
- `langchain` - LangChain 프레임워크
- `openai` - OpenAI API 클라이언트
- `google-api-python-client` - Google API 클라이언트
- `gspread` - Google Sheets API

### 3) 환경 변수 설정

1. `.env.example` 파일을 `.env`로 복사:

   **Windows:**
   ```bash
   copy .env.example .env
   ```

   **macOS/Linux:**
   ```bash
   cp .env.example .env
   ```

2. `.env` 파일을 텍스트 에디터로 열어 수정:

   ```env
   # OpenAI API Key (필수)
   OPENAI_API_KEY=sk-proj-여기에_실제_API_키_입력

   # Google Sheets Configuration (필수)
   GOOGLE_SHEET_ID=여기에_구글_시트_ID_입력
   GOOGLE_SHEET_NAME=Sheet1

   # Google Calendar Configuration
   GOOGLE_CALENDAR_ID=primary
   ```

#### 📝 각 항목 설정 방법

**OPENAI_API_KEY:**
1. https://platform.openai.com/api-keys 접속
2. 로그인 후 "Create new secret key" 클릭
3. 생성된 키를 복사하여 붙여넣기

**GOOGLE_SHEET_ID:**
1. Google Sheets에서 새 스프레드시트 생성
2. URL에서 ID 부분 복사:
   ```
   https://docs.google.com/spreadsheets/d/1abc...xyz/edit
                                          ↑ 이 부분이 SHEET_ID
   ```

---

## 4. Google OAuth 2.0 설정

### 1) Google Cloud Console 설정

1. **Google Cloud Console 접속**
   - https://console.cloud.google.com/

2. **새 프로젝트 생성**
   - 프로젝트 선택 → 새 프로젝트
   - 프로젝트 이름: `event-calendar-agent` (또는 원하는 이름)

3. **API 활성화**
   - 좌측 메뉴: API 및 서비스 → 라이브러리
   - 검색하여 다음 API 활성화:
     - ✅ Google Sheets API
     - ✅ Google Calendar API
     - ✅ Google Drive API

4. **OAuth 동의 화면 구성**
   - API 및 서비스 → OAuth 동의 화면
   - User Type: **외부** 선택 → 만들기
   - 앱 이름: `Event Calendar Agent`
   - 사용자 지원 이메일: 본인 이메일
   - 개발자 연락처: 본인 이메일
   - 저장 후 계속

5. **OAuth 2.0 클라이언트 ID 생성**
   - API 및 서비스 → 사용자 인증 정보
   - + 사용자 인증 정보 만들기 → OAuth 클라이언트 ID
   - 애플리케이션 유형: **데스크톱 앱**
   - 이름: `Desktop Client`
   - 만들기 클릭
   - **JSON 다운로드** 클릭

6. **JSON 파일 저장**
   - 다운로드한 JSON 파일을 프로젝트 폴더에 저장
   - 파일 이름을 `oauth_credentials.json`으로 변경

### 2) Google Sheets 준비

1. **헤더 설정**
   - Google Sheets를 열고 첫 번째 행에 다음 헤더 입력:

   | A | B | C | D | E | F | G | H |
   |---|---|---|---|---|---|---|---|
   | 원본 텍스트 | 제목 | 날짜 | 시간 | 장소 | 설명 | 메모 | 처리 상태 |

2. **테스트 데이터 입력**
   - `test_messages.txt` 파일의 샘플 메시지를 A열에 복사
   - 각 메시지를 별도 행에 붙여넣기

---

## 5. 실행

### 1) 프로그램 실행

```bash
python main.py
```

### 2) 첫 실행 시 OAuth 인증

1. 브라우저가 자동으로 열립니다
2. Google 계정으로 로그인
3. "앱이 확인되지 않음" 경고 화면:
   - **고급** 클릭
   - **Event Calendar Agent(안전하지 않음)로 이동** 클릭
4. 권한 요청 화면에서 **계속** 클릭
5. 인증 완료 후 터미널로 돌아옵니다

**⚠️ 주의:** "앱이 확인되지 않음" 경고는 정상입니다. 본인이 만든 앱이므로 안전합니다.

### 3) 실행 결과 확인

터미널 출력 예시:
```
============================================================
🤖 LangGraph 멀티에이전트 이벤트 처리 시작
============================================================
✅ Google Sheets 인증 성공
✅ Google Calendar 인증 성공

📊 [Sheets Agent] 구글 시트에서 미처리 이벤트 읽기...
처리 대기 중인 이벤트: 5개

============================================================
[1/5] 행 2 처리 시작
============================================================

🤖 [Parser Agent] 행 2 텍스트 파싱 중...
  📌 제목: 연세자연애치과
  📅 날짜: 2025-11-22
  🕐 시간: 12:30
  📍 장소: 서울특별시 서초구...

✓ [Parser Agent] 데이터 검증 중...
  ✅ 검증 통과

📝 [Sheets Agent] 파싱 결과 작성 중...
✅ 작성 완료

📅 [Calendar Agent] 캘린더 등록 중...
✅ 캘린더에 이벤트 등록 완료!
```

---

## 6. 문제 해결

### ❌ `ModuleNotFoundError: No module named 'langgraph'`

**해결 방법:**
```bash
# 가상환경이 활성화되어 있는지 확인
# (venv)가 프롬프트 앞에 표시되어야 함

pip install -r requirements.txt
```

### ❌ `FileNotFoundError: oauth_credentials.json`

**해결 방법:**
1. Google Cloud Console에서 OAuth 클라이언트 ID 다운로드
2. 파일 이름을 `oauth_credentials.json`으로 변경
3. 프로젝트 루트 폴더에 저장

### ❌ `google.auth.exceptions.RefreshError`

**해결 방법:**
```bash
# 기존 토큰 삭제 후 재인증
rm token.pickle   # macOS/Linux
del token.pickle  # Windows

python main.py
```

### ❌ PowerShell에서 가상환경 활성화 실패

**에러 메시지:**
```
... cannot be loaded because running scripts is disabled on this system.
```

**해결 방법:**
PowerShell을 **관리자 권한**으로 실행 후:
```powershell
Set-ExecutionPolicy RemoteSigned
```
이후 Y 입력하여 확인

### ❌ `TypeError: Client.__init__() got an unexpected keyword argument`

**해결 방법:**
```bash
pip install --upgrade openai
```

### ❌ Google Sheets API 할당량 초과

**에러 메시지:**
```
Quota exceeded for quota metric 'Read requests' and limit 'Read requests per minute'
```

**해결 방법:**
- 1분 정도 기다린 후 재실행
- Google Cloud Console에서 할당량 증대 요청

---

## 💡 유용한 팁

### 1) 가상환경 비활성화

작업 완료 후:
```bash
deactivate
```

### 2) Git으로 최신 버전 받기

```bash
git pull origin main
```

### 3) 로그 확인

실행 중 모든 로그가 터미널에 출력됩니다. 문제 발생 시 로그를 확인하세요.

### 4) VSCode 사용 (권장)

- https://code.visualstudio.com/ 에서 다운로드
- Python Extension 설치
- 프로젝트 폴더 열기: `code .`

---

## 📚 추가 자료

- [LangGraph 공식 문서](https://python.langchain.com/docs/langgraph)
- [OpenAI API 문서](https://platform.openai.com/docs)
- [Google Sheets API 문서](https://developers.google.com/sheets/api)
- [Google Calendar API 문서](https://developers.google.com/calendar/api)

---

## 🆘 도움이 필요하신가요?

- **이슈 등록:** GitHub Issues에 문제 상황을 상세히 작성해주세요
- **질문:** Discussions 탭에서 질문할 수 있습니다

---

## 📝 라이선스

MIT License
