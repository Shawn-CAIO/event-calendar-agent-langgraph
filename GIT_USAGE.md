# 📘 Git & GitHub 사용 가이드

교육자를 위한 프로젝트 배포 및 관리 가이드입니다.

---

## 🎯 GitHub에 프로젝트 업로드하기

### 1단계: GitHub 저장소 생성

1. **GitHub 웹사이트 접속**
   - https://github.com 로그인

2. **새 저장소 생성**
   - 우측 상단 `+` 아이콘 클릭 → **New repository**
   - Repository name: `event-calendar-agent-langgraph`
   - Description: `LangGraph 멀티에이전트 이벤트 처리 시스템 - LLM 기반 에이전트 실전·응용 (중급) 실습 프로젝트`
   - Public/Private 선택:
     - ✅ **Public**: 누구나 접근 가능 (교육용 권장)
     - ⚠️ Private: 초대한 사람만 접근 가능
   - ❌ **Initialize this repository with:** 체크 해제 (이미 로컬에 있으므로)
   - **Create repository** 클릭

3. **저장소 URL 복사**
   - 생성 후 나타나는 URL 복사
   - 예: `https://github.com/Shawn-CAIO/event-calendar-agent-langgraph.git`

### 2단계: 로컬 저장소를 GitHub에 연결

터미널에서 프로젝트 폴더로 이동 후 실행:

```bash
# GitHub 저장소 URL로 변경하세요
git remote add origin https://github.com/Shawn-CAIO/event-calendar-agent-langgraph.git

# 확인
git remote -v
```

**출력 예시:**
```
origin  https://github.com/Shawn-CAIO/event-calendar-agent-langgraph.git (fetch)
origin  https://github.com/Shawn-CAIO/event-calendar-agent-langgraph.git (push)
```

### 3단계: GitHub에 업로드 (Push)

```bash
# main 브랜치를 GitHub에 업로드
git push -u origin main
```

**처음 push할 때 GitHub 로그인 요청:**
- Username: GitHub 사용자명
- Password: Personal Access Token (PAT) 입력

#### Personal Access Token (PAT) 생성 방법

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. **Generate new token** → **Generate new token (classic)**
3. Note: `event-calendar-agent`
4. Expiration: `90 days` (또는 원하는 기간)
5. Select scopes:
   - ✅ `repo` (전체 선택)
6. **Generate token** 클릭
7. **토큰 복사** (다시 볼 수 없으므로 안전한 곳에 저장!)
8. Password 입력 시 복사한 토큰 붙여넣기

### 4단계: 업로드 확인

브라우저에서 GitHub 저장소 페이지를 새로고침하면 파일들이 업로드된 것을 확인할 수 있습니다.

---

## 📤 교육생들에게 공유하기

### 방법 1: GitHub 저장소 URL 공유 (권장)

교육생들에게 다음 정보를 제공:

```
📚 실습 저장소: https://github.com/Shawn-CAIO/event-calendar-agent-langgraph

📖 설치 가이드:
1. 저장소 클론:
   git clone https://github.com/Shawn-CAIO/event-calendar-agent-langgraph.git

2. 상세한 설치 방법은 SETUP_GUIDE.md 파일을 참고하세요.
```

### 방법 2: ZIP 파일로 배포

교육생들이 Git을 사용하지 않는 경우:

1. GitHub 저장소 페이지
2. **Code** 버튼 클릭
3. **Download ZIP** 클릭
4. ZIP 파일을 교육생들에게 공유

---

## 🔄 프로젝트 업데이트하기

### 코드 수정 후 GitHub에 반영

```bash
# 1. 변경된 파일 확인
git status

# 2. 변경 사항을 스테이징
git add .

# 3. 커밋 메시지와 함께 저장
git commit -m "설명: 무엇을 변경했는지 간단히 작성"

# 예시:
git commit -m "Fix: 날짜 파싱 로직 개선"
git commit -m "Add: 에러 처리 개선"
git commit -m "Update: README에 새로운 예제 추가"

# 4. GitHub에 업로드
git push origin main
```

### 교육생들에게 업데이트 공지

교육생들이 최신 버전을 받도록 안내:

```bash
# 프로젝트 폴더에서 실행
git pull origin main
```

---

## 📊 Git 기본 명령어 정리

### 상태 확인

```bash
# 현재 상태 확인
git status

# 커밋 히스토리 확인
git log

# 간단한 히스토리
git log --oneline

# 변경 사항 확인
git diff
```

### 파일 관리

```bash
# 모든 파일 추가
git add .

# 특정 파일만 추가
git add filename.py

# 파일 삭제
git rm filename.py

# 파일 이름 변경
git mv old_name.py new_name.py
```

### 브랜치 관리

```bash
# 브랜치 목록 확인
git branch

# 새 브랜치 생성
git branch feature-name

# 브랜치 전환
git checkout feature-name

# 브랜치 생성 & 전환 동시에
git checkout -b feature-name

# 브랜치 병합
git merge feature-name

# 브랜치 삭제
git branch -d feature-name
```

---

## 🎓 교육 시나리오별 활용

### 시나리오 1: 실습 과제 배포

1. **main 브랜치**: 완성된 솔루션
2. **starter 브랜치**: 빈 템플릿

```bash
# starter 브랜치 생성
git checkout -b starter

# 일부 코드를 TODO로 변경
# 예: workflow.py의 일부 함수를 빈 상태로

git add .
git commit -m "Add starter template for students"
git push origin starter
```

**교육생 안내:**
```bash
# 과제용 템플릿 받기
git clone -b starter https://github.com/Shawn-CAIO/event-calendar-agent-langgraph.git
```

### 시나리오 2: 단계별 튜토리얼

각 단계를 태그로 저장:

```bash
# 1단계 완료 후
git tag -a step-1 -m "Step 1: Basic workflow setup"
git push origin step-1

# 2단계 완료 후
git tag -a step-2 -m "Step 2: Add parser agent"
git push origin step-2
```

**교육생 안내:**
```bash
# 특정 단계로 이동
git checkout step-1
```

### 시나리오 3: 버그 수정 및 업데이트

```bash
# 버그 수정
git add .
git commit -m "Fix: Recursion limit 오류 수정"
git push origin main

# 교육생들에게 공지
# "최신 버전으로 업데이트하세요: git pull origin main"
```

---

## 🛡️ 민감 정보 보호

### 절대 GitHub에 올리면 안 되는 파일

✅ `.gitignore`에 이미 포함되어 있음:

- `.env` - API 키, 비밀번호
- `oauth_credentials.json` - OAuth 클라이언트 ID
- `token.pickle` - 인증 토큰
- `__pycache__/` - Python 캐시
- `venv/` - 가상환경

### 실수로 올린 경우 제거 방법

```bash
# Git 히스토리에서 완전히 제거
git rm --cached .env
git commit -m "Remove .env from tracking"
git push origin main

# ⚠️ 주의: 이미 노출된 API 키는 즉시 재발급하세요!
```

---

## 🤝 협업하기

### Fork & Pull Request 워크플로우

교육생들이 개선 사항을 제안할 수 있도록:

1. **교육생:** 저장소 Fork
2. **교육생:** 변경 사항 작성 및 커밋
3. **교육생:** Pull Request 생성
4. **교육자:** 코드 리뷰 및 병합

### Issue로 질문 받기

GitHub Issues를 활용:

1. 저장소 → **Issues** 탭
2. 교육생들이 질문 또는 버그 리포트 작성
3. 라벨로 분류: `question`, `bug`, `enhancement`

---

## 📚 추가 리소스

### Git 학습 자료

- [Git 공식 문서 (한글)](https://git-scm.com/book/ko/v2)
- [GitHub 학습 가이드](https://docs.github.com/ko/get-started)
- [Visualizing Git](https://git-school.github.io/visualizing-git/)

### GitHub 기능 활용

- **GitHub Pages**: 프로젝트 문서 호스팅
- **GitHub Actions**: CI/CD 자동화
- **GitHub Discussions**: 포럼 형식 토론

---

## 🔧 문제 해결

### "Permission denied (publickey)" 오류

**해결:** HTTPS 방식으로 변경

```bash
# 현재 원격 저장소 확인
git remote -v

# SSH → HTTPS로 변경
git remote set-url origin https://github.com/Shawn-CAIO/event-calendar-agent-langgraph.git
```

### "rejected - non-fast-forward" 오류

**원인:** 원격 저장소에 로컬에 없는 커밋이 있음

**해결:**
```bash
# 원격 변경사항 먼저 가져오기
git pull origin main

# 충돌 해결 후 다시 push
git push origin main
```

### 커밋 취소하기

```bash
# 가장 최근 커밋 취소 (변경사항은 유지)
git reset --soft HEAD~1

# 가장 최근 커밋 취소 (변경사항도 삭제)
git reset --hard HEAD~1
```

---

## ✅ 체크리스트

프로젝트 배포 전 확인 사항:

- [ ] `.gitignore`에 민감 정보 파일 포함되었는지 확인
- [ ] `README.md` 최신화
- [ ] `SETUP_GUIDE.md` 최신화
- [ ] `requirements.txt` 최신화
- [ ] `.env.example` 파일 포함
- [ ] 테스트 실행 확인
- [ ] 라이선스 파일 추가 (선택사항)

---

## 💡 팁

### Commit Message 규칙 (권장)

```
타입: 간단한 설명

타입 종류:
- Add: 새로운 기능 추가
- Fix: 버그 수정
- Update: 기존 기능 업데이트
- Refactor: 코드 리팩토링
- Docs: 문서 수정
- Test: 테스트 코드 추가/수정

예시:
Add: CalendarAgent에 알림 설정 기능 추가
Fix: 날짜 파싱 시 연도 추론 오류 수정
Update: README에 트러블슈팅 섹션 추가
```

### .gitignore 추가 항목

프로젝트 특성에 따라 추가:

```gitignore
# 대용량 데이터 파일
*.csv
*.xlsx
data/

# 로그 파일
logs/
*.log

# 임시 파일
temp/
tmp/
```

---

이제 프로젝트를 GitHub에 업로드하고 교육생들과 공유할 준비가 완료되었습니다! 🎉
