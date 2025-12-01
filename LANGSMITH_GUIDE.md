# 🔍 LangSmith 설정 및 사용 가이드

LangSmith는 LangGraph 워크플로우를 시각화하고 디버깅할 수 있는 강력한 도구입니다.

---

## 📋 LangSmith란?

LangSmith는 LangChain/LangGraph 애플리케이션을 위한 통합 개발 플랫폼입니다:

- ✅ **추적 (Tracing)**: 각 에이전트 실행을 단계별로 추적
- ✅ **디버깅**: 오류 발생 지점을 정확히 파악
- ✅ **모니터링**: 실행 시간, 비용, 성능 측정
- ✅ **시각화**: 워크플로우를 그래프로 시각화
- ✅ **평가**: 프롬프트와 결과 품질 평가

---

## 🚀 LangSmith 설정하기

### 1단계: LangSmith 계정 생성

1. **LangSmith 웹사이트 접속**
   ```
   https://smith.langchain.com/
   ```

2. **회원가입**
   - GitHub 또는 이메일로 가입
   - 무료 플랜으로 시작 (월 5,000 traces 제공)

3. **API 키 생성**
   - 로그인 후 우측 상단 프로필 클릭
   - **Settings** → **API Keys**
   - **Create API Key** 클릭
   - API 키 복사 (다시 볼 수 없으므로 안전한 곳에 저장!)

### 2단계: 환경 변수 설정

`.env` 파일에 LangSmith 설정 추가:

```env
# LangSmith Configuration (Optional - for debugging and monitoring)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_여기에_복사한_API_키_붙여넣기
LANGCHAIN_PROJECT=event-calendar-agent
```

**환경 변수 설명:**

- `LANGCHAIN_TRACING_V2=true`: LangSmith 추적 활성화
- `LANGCHAIN_API_KEY`: LangSmith API 키
- `LANGCHAIN_PROJECT`: 프로젝트 이름 (traces를 그룹화)

### 3단계: 실행 및 확인

```bash
python main.py
```

**출력 예시:**
```
🔍 LangSmith 추적 활성화됨
   프로젝트: event-calendar-agent
   추적 URL: https://smith.langchain.com/

============================================================
🤖 LangGraph 멀티에이전트 이벤트 처리 시작
============================================================
...
```

### 4단계: LangSmith에서 확인

1. https://smith.langchain.com/ 접속
2. 좌측 메뉴에서 **Projects** 클릭
3. `event-calendar-agent` 프로젝트 선택
4. 최근 실행 기록(traces) 확인

---

## 📊 LangSmith 대시보드 사용법

### Traces 보기

각 실행은 "trace"로 기록됩니다:

```
Run Name: LangGraph Execution
├─ fetch_events (SheetsAgent)
│  ├─ Duration: 234ms
│  ├─ Input: {...}
│  └─ Output: {unprocessed_events: [...]}
├─ select_next_event
│  ├─ Duration: 12ms
│  └─ Output: {current_event: {...}}
├─ parse_event (ParserAgent)
│  ├─ Duration: 1,523ms
│  ├─ LLM Call: gpt-4o-mini
│  │  ├─ Prompt: "당신은 텍스트에서..."
│  │  ├─ Response: {"title": "...", ...}
│  │  └─ Tokens: 458 input, 112 output
│  └─ Cost: $0.0023
├─ validate_data (ParserAgent)
├─ write_to_sheet (SheetsAgent)
├─ create_calendar_event (CalendarAgent)
├─ mark_synced (SheetsAgent)
└─ check_complete
```

### 주요 기능

#### 1. **실행 시간 분석**

각 노드별 실행 시간을 확인:
- 어느 단계가 가장 느린지 파악
- 성능 병목 지점 발견

#### 2. **LLM 호출 상세 정보**

ParserAgent의 LLM 호출 내용:
- 실제 프롬프트 전체 텍스트
- 모델 응답 전체 내용
- 토큰 사용량 및 비용

#### 3. **에러 디버깅**

오류 발생 시:
- 정확한 오류 발생 지점
- 스택 트레이스
- 입력 데이터 상태

#### 4. **입출력 검사**

각 노드의:
- 입력 상태 (state)
- 출력 상태 (updated state)
- 변경된 필드

---

## 🎯 실전 활용 예시

### 예시 1: 파싱 결과 분석

**문제:** "날짜가 잘못 파싱되는 것 같아요"

**LangSmith 활용:**
1. Traces에서 문제가 된 실행 찾기
2. `parse_event` 노드 클릭
3. LLM 호출 내용 확인:
   - Prompt: 현재 날짜 컨텍스트 확인
   - Response: LLM이 실제로 반환한 날짜
4. 문제 원인 파악 및 프롬프트 개선

### 예시 2: 성능 최적화

**문제:** "처리 속도가 너무 느려요"

**LangSmith 활용:**
1. 여러 traces의 실행 시간 비교
2. 가장 느린 노드 찾기
3. 예시:
   - `parse_event`: 평균 1.5초 (LLM 호출)
   - `write_to_sheet`: 평균 300ms (API 호출)
   - `create_calendar_event`: 평균 200ms
4. LLM 호출이 병목 → 배치 처리 고려

### 예시 3: 에러 추적

**문제:** "가끔 실패하는데 원인을 모르겠어요"

**LangSmith 활용:**
1. Filters에서 "Failed" traces만 보기
2. 공통 패턴 찾기:
   - 특정 텍스트 형식에서만 실패?
   - 특정 시간대에 실패?
   - API 한도 초과?
3. 정확한 에러 메시지와 입력 데이터 확인

---

## 📈 비용 및 성능 모니터링

### 비용 추적

LangSmith는 OpenAI API 비용을 자동으로 계산:

```
총 비용: $0.45
├─ GPT-4o-mini: $0.45
│  ├─ Input tokens: 12,450 × $0.00015/1K = $0.19
│  └─ Output tokens: 3,200 × $0.00060/1K = $0.26
```

### 성능 메트릭

- **처리량**: 시간당 이벤트 처리 개수
- **평균 레이턴시**: 이벤트당 평균 처리 시간
- **성공률**: 성공한 이벤트 비율
- **토큰 사용량**: LLM 토큰 사용 추이

---

## 🔧 고급 기능

### 1. 프로젝트 태그

다른 실험을 구분하려면:

```python
# main.py에서
result = app.invoke(
    initial_state,
    config={
        "recursion_limit": 100,
        "metadata": {
            "experiment": "improved-prompt-v2",
            "user": "instructor"
        }
    }
)
```

### 2. 런 필터링

LangSmith에서:
- 날짜별 필터
- 성공/실패 필터
- 메타데이터로 필터

### 3. 비교 기능

두 개의 traces를 나란히 비교:
- 프롬프트 변경 전후 비교
- 성능 개선 전후 비교

---

## ⚠️ 주의사항

### 1. 민감한 정보

LangSmith에는 모든 입출력이 기록됩니다:
- ⚠️ 개인정보가 포함된 데이터 주의
- ⚠️ API 키, 비밀번호 등 민감 정보 주의

**해결책:**
```python
# 민감 정보 마스킹
import os
os.environ["LANGCHAIN_HIDE_INPUTS"] = "true"
os.environ["LANGCHAIN_HIDE_OUTPUTS"] = "true"
```

### 2. 비용 고려

무료 플랜:
- 월 5,000 traces 제한
- 교육용으로는 충분함

유료 플랜:
- $39/month부터 시작
- 대규모 프로덕션 환경용

### 3. 네트워크 오버헤드

LangSmith는 각 단계를 클라우드로 전송:
- 약간의 성능 오버헤드 있음
- 디버깅 시에만 활성화 권장

**선택적 활성화:**
```bash
# 개발 시
LANGCHAIN_TRACING_V2=true python main.py

# 프로덕션
LANGCHAIN_TRACING_V2=false python main.py
```

---

## 🎓 교육 활용

### 학습자용

LangSmith를 통해:
1. **워크플로우 이해**: 각 단계가 어떻게 실행되는지 시각화
2. **LLM 동작 이해**: 실제 프롬프트와 응답 확인
3. **디버깅 연습**: 오류를 스스로 찾고 해결

### 강사용

LangSmith를 통해:
1. **학습자 코드 리뷰**: 실행 기록 공유받아 문제 파악
2. **성능 비교**: 학습자별 구현 성능 비교
3. **베스트 프랙티스 공유**: 우수 사례 시연

---

## 📚 추가 리소스

- **LangSmith 공식 문서**: https://docs.smith.langchain.com/
- **튜토리얼**: https://docs.smith.langchain.com/tutorials
- **커뮤니티**: https://github.com/langchain-ai/langsmith-sdk

---

## 🆘 문제 해결

### "Failed to connect to LangSmith" 오류

**원인:** API 키가 잘못되었거나 네트워크 문제

**해결:**
1. API 키 다시 확인
2. 네트워크 연결 확인
3. 방화벽 설정 확인

### Traces가 보이지 않음

**원인:** 프로젝트 이름이 다르거나 필터 설정 문제

**해결:**
1. `.env`의 `LANGCHAIN_PROJECT` 확인
2. LangSmith에서 필터 초기화
3. 브라우저 새로고침

### 비용이 너무 많이 나옴

**원인:** 너무 많은 traces 기록

**해결:**
1. 샘플링 설정:
   ```python
   os.environ["LANGCHAIN_TRACING_SAMPLING_RATE"] = "0.1"  # 10%만 기록
   ```
2. 필요할 때만 활성화

---

LangSmith를 활용하면 LangGraph 워크플로우를 완벽하게 이해하고 최적화할 수 있습니다! 🚀
