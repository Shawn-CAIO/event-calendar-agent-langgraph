# OAuth 2.0 설정 가이드 (권장 방식)

서비스 계정 키 대신 더 안전한 OAuth 2.0 사용자 인증을 사용하는 방법입니다.

## 왜 OAuth 2.0을 사용해야 하나요?

### 서비스 계정 키의 문제점
- ❌ JSON 키 파일이 유출되면 누구나 사용 가능
- ❌ 키 관리가 어렵고 보안 위험 높음
- ❌ Google Cloud에서 생성 시 경고 메시지 표시

### OAuth 2.0의 장점
- ✅ 사용자 계정으로 안전하게 인증
- ✅ 키 파일 유출 걱정 없음
- ✅ 토큰 자동 갱신
- ✅ 개인 구글 계정으로 간편하게 사용

## OAuth 2.0 설정 방법

### 1단계: Google Cloud Console에서 OAuth 2.0 클라이언트 ID 생성

#### 1.1 프로젝트 생성 및 API 활성화
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성
3. **API 및 서비스** > **라이브러리**로 이동
4. 다음 API를 검색하여 활성화:
   - Google Sheets API
   - Google Calendar API

#### 1.2 OAuth 동의 화면 구성
1. **API 및 서비스** > **OAuth 동의 화면** 메뉴로 이동
2. User Type: **외부** 선택 (개인 계정 사용 시)
3. 앱 정보 입력:
   - 앱 이름: `Event Calendar Agent`
   - 사용자 지원 이메일: 본인 이메일
   - 개발자 연락처 정보: 본인 이메일
4. **저장 후 계속** 클릭

5. **범위** 섹션에서 **범위 추가 또는 삭제** 클릭
6. 다음 범위 추가:
   - `.../auth/spreadsheets` (Google Sheets)
   - `.../auth/calendar` (Google Calendar)
   - `.../auth/drive` (Google Drive - 시트 접근용)
7. **저장 후 계속** 클릭

8. **테스트 사용자** 섹션에서:
   - **ADD USERS** 클릭
   - 본인의 구글 계정 이메일 추가
   - **저장 후 계속** 클릭

#### 1.3 OAuth 2.0 클라이언트 ID 생성
1. **API 및 서비스** > **사용자 인증 정보** 메뉴로 이동
2. **사용자 인증 정보 만들기** > **OAuth 클라이언트 ID** 클릭
3. 애플리케이션 유형: **데스크톱 앱** 선택
4. 이름: `Event Agent Desktop` 입력
5. **만들기** 클릭

6. 생성된 클라이언트 ID 다운로드:
   - JSON 다운로드 버튼 클릭
   - 다운로드한 파일을 프로젝트 폴더에 `oauth_credentials.json`으로 저장

### 2단계: 프로젝트 설정

#### 2.1 환경 변수 설정
`.env` 파일에 구글 시트 ID만 설정:

```env
# OpenAI API Key
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxx

# Google Sheets Configuration
GOOGLE_SHEET_ID=1AbCdEfGhIjKlMnOpQrStUvWxYz
GOOGLE_SHEET_NAME=Sheet1

# Google Calendar Configuration
GOOGLE_CALENDAR_ID=primary
```

#### 2.2 파일 구조 확인
```
event-calendar-agent/
├── oauth_credentials.json    # 방금 다운로드한 OAuth 클라이언트 ID
├── token.pickle              # (자동 생성) 인증 토큰 저장
├── .env                      # 환경 변수
└── ...
```

### 3단계: 첫 실행 및 인증

#### 3.1 스크립트 실행
```bash
python main.py
```

#### 3.2 브라우저에서 인증
1. 스크립트 실행 시 자동으로 브라우저가 열림
2. 구글 계정으로 로그인
3. 권한 요청 화면에서:
   - "이 앱은 Google에서 확인하지 않았습니다" 경고 표시됨
   - **고급** 클릭 > **Event Calendar Agent(으)로 이동(안전하지 않음)** 클릭
   - 이것은 정상입니다! 본인이 만든 앱이기 때문입니다.

4. 다음 권한 승인:
   - Google 스프레드시트의 스프레드시트 확인, 수정, 생성, 삭제
   - Google Calendar의 모든 캘린더 액세스
   - Google Drive 파일 보기, 수정

5. **계속** 클릭

#### 3.3 인증 완료
- "인증 정보가 저장되었습니다" 메시지 확인
- `token.pickle` 파일이 자동 생성됨
- 이후 실행 시에는 자동으로 인증됨 (재로그인 불필요)

## 사용 방법

### 기본 사용 (OAuth 2.0)
코드 수정 없이 바로 사용 가능:

```bash
python main.py
```

### 개별 모듈 테스트

#### 인증 테스트
```bash
python google_auth_helper.py
```

#### 구글 시트 테스트
```python
from google_sheets_handler import GoogleSheetsHandler

# OAuth 2.0 사용 (기본값)
handler = GoogleSheetsHandler()
events = handler.read_unprocessed_events()
```

#### 구글 캘린더 테스트
```python
from google_calendar_handler import GoogleCalendarHandler

# OAuth 2.0 사용 (기본값)
handler = GoogleCalendarHandler()
handler.get_upcoming_events()
```

## 문제 해결

### "oauth_credentials.json을 찾을 수 없습니다"
- Google Cloud Console에서 OAuth 2.0 클라이언트 ID를 생성했는지 확인
- JSON 파일을 프로젝트 폴더에 `oauth_credentials.json`으로 저장했는지 확인

### "이 앱은 Google에서 확인하지 않았습니다" 경고
- 정상적인 메시지입니다 (본인이 만든 앱이므로)
- **고급** > **Event Calendar Agent(으)로 이동** 클릭하여 계속 진행

### 브라우저가 자동으로 열리지 않음
- 터미널에 표시되는 URL을 복사하여 수동으로 브라우저에 붙여넣기

### "Access blocked: This app's request is invalid"
- OAuth 동의 화면에서 테스트 사용자에 본인 계정이 추가되었는지 확인
- 올바른 범위(Scopes)가 추가되었는지 확인

### 토큰 만료 또는 갱신 필요
```bash
# token.pickle 파일 삭제 후 재인증
rm token.pickle
python main.py
```

## 레거시: 서비스 계정 방식 사용 (비권장)

기존 서비스 계정 키를 사용하려면:

```python
from google_sheets_handler import GoogleSheetsHandler
from google_calendar_handler import GoogleCalendarHandler

# use_oauth=False로 설정
sheets = GoogleSheetsHandler(use_oauth=False, credentials_file="credentials.json")
calendar = GoogleCalendarHandler(use_oauth=False, credentials_file="credentials.json")
```

하지만 보안상 OAuth 2.0 사용을 강력히 권장합니다!

## 추가 정보

### 토큰 저장 위치
- `token.pickle`: 인증 토큰이 저장된 파일
- `.gitignore`에 포함되어 있어 Git에 커밋되지 않음
- 이 파일만 있으면 재인증 없이 사용 가능

### 토큰 유효 기간
- 기본적으로 자동 갱신됨
- 장기간 사용하지 않으면 만료될 수 있음 (재인증 필요)

### 보안 권장사항
- ✅ `oauth_credentials.json`을 Git에 커밋하지 마세요
- ✅ `token.pickle`을 공유하지 마세요
- ✅ `.gitignore`에 두 파일이 포함되어 있는지 확인하세요
