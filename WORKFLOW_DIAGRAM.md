# 🔄 LangGraph 워크플로우 다이어그램

## 전체 워크플로우 구조

```mermaid
graph TD
    Start([시작]) --> FetchEvents[1. fetch_events<br/>📊 SheetsAgent<br/>미처리 이벤트 읽기]

    FetchEvents --> SelectEvent[2. select_next_event<br/>📋 다음 이벤트 선택]

    SelectEvent -->|이벤트 있음| ParseEvent[3. parse_event<br/>🤖 ParserAgent<br/>LLM 텍스트 파싱]
    SelectEvent -->|이벤트 없음| End([종료])

    ParseEvent --> ValidateData[4. validate_data<br/>✓ ParserAgent<br/>데이터 검증]

    ValidateData --> WriteSheet[5. write_to_sheet<br/>📝 SheetsAgent<br/>파싱 결과 작성]

    WriteSheet --> CreateCalendar[6. create_calendar_event<br/>📅 CalendarAgent<br/>캘린더 등록]

    CreateCalendar --> MarkSynced[7. mark_synced<br/>✅ SheetsAgent<br/>동기화 완료 표시]

    MarkSynced --> CheckComplete[8. check_complete<br/>🔍 남은 이벤트 확인]

    CheckComplete -->|남은 이벤트 있음| SelectEvent
    CheckComplete -->|모두 처리 완료| End

    style Start fill:#90EE90
    style End fill:#FFB6C1
    style FetchEvents fill:#87CEEB
    style SelectEvent fill:#DDA0DD
    style ParseEvent fill:#F0E68C
    style ValidateData fill:#F0E68C
    style WriteSheet fill:#87CEEB
    style CreateCalendar fill:#FFD700
    style MarkSynced fill:#87CEEB
    style CheckComplete fill:#DDA0DD
```

## 에이전트별 역할

```mermaid
graph LR
    subgraph SheetsAgent[📊 SheetsAgent]
        S1[미처리 이벤트 읽기]
        S2[파싱 결과 작성]
        S3[동기화 완료 표시]
    end

    subgraph ParserAgent[🤖 ParserAgent]
        P1[LLM 텍스트 파싱]
        P2[데이터 검증]
    end

    subgraph CalendarAgent[📅 CalendarAgent]
        C1[캘린더 이벤트 생성]
    end

    style SheetsAgent fill:#E6F3FF
    style ParserAgent fill:#FFF9E6
    style CalendarAgent fill:#FFE6E6
```

## 상태 흐름도

```mermaid
stateDiagram-v2
    [*] --> 초기화: 초기 상태 설정

    초기화 --> 이벤트읽기: unprocessed_events = []

    이벤트읽기 --> 이벤트선택: unprocessed_events 업데이트

    이벤트선택 --> 파싱중: current_event 설정
    이벤트선택 --> [*]: current_event = None

    파싱중 --> 검증중: current_event 업데이트<br/>(title, date, time 등)

    검증중 --> 시트작성: 검증 통과
    검증중 --> 다음이벤트: 검증 실패 (경고)

    시트작성 --> 캘린더등록: 시트 업데이트 완료

    캘린더등록 --> 동기화표시: 등록 성공<br/>calendar_event_id 설정
    캘린더등록 --> 동기화표시: 등록 실패<br/>error 기록

    동기화표시 --> 완료확인: processed_events 추가<br/>processed_count 증가

    완료확인 --> 이벤트선택: 남은 이벤트 있음
    완료확인 --> [*]: 모두 처리 완료

    다음이벤트 --> 이벤트선택
```

## 데이터 플로우

```mermaid
flowchart TD
    subgraph Input[입력 데이터]
        I1[Google Sheets<br/>A열: 원본 텍스트]
    end

    subgraph Processing[처리 과정]
        P1[SheetsAgent<br/>텍스트 읽기] --> P2[ParserAgent<br/>GPT-4o-mini 파싱]
        P2 --> P3{검증}
        P3 -->|성공| P4[SheetsAgent<br/>B~G열 작성]
        P3 -->|실패| P5[경고 로그]
        P4 --> P6[CalendarAgent<br/>이벤트 생성]
        P6 --> P7[SheetsAgent<br/>H열 상태 업데이트]
    end

    subgraph Output[출력 데이터]
        O1[Google Sheets<br/>B~H열: 파싱 결과]
        O2[Google Calendar<br/>일정 등록]
        O3[처리 결과 로그]
    end

    Input --> Processing
    Processing --> Output

    style Input fill:#E8F5E9
    style Processing fill:#FFF3E0
    style Output fill:#E3F2FD
```

## 조건부 라우팅 상세

```mermaid
graph TD
    A[select_next_event] --> B{current_event<br/>존재?}
    B -->|Yes| C[parse_event로 진행]
    B -->|No| D[END - 종료]

    E[check_complete] --> F{unprocessed_events<br/>남았음?}
    F -->|Yes| G[select_next_event로 반복]
    F -->|No| H[END - 종료]

    style A fill:#DDA0DD
    style B fill:#FFE4B5
    style C fill:#90EE90
    style D fill:#FFB6C1
    style E fill:#DDA0DD
    style F fill:#FFE4B5
    style G fill:#90EE90
    style H fill:#FFB6C1
```

## 에러 처리 흐름

```mermaid
flowchart TD
    Start[노드 실행] --> Try{실행}

    Try -->|성공| UpdateState[상태 업데이트<br/>messages 추가]
    Try -->|실패| CatchError[예외 처리]

    CatchError --> LogError[errors 배열에 추가<br/>agent, action, error]
    LogError --> UpdateFailCount[failed_count 증가]
    UpdateFailCount --> Continue[다음 노드 진행]

    UpdateState --> NextNode[다음 노드로]
    Continue --> NextNode

    style Try fill:#FFE4B5
    style UpdateState fill:#90EE90
    style CatchError fill:#FFB6C1
    style LogError fill:#FF6B6B
    style UpdateFailCount fill:#FF6B6B
```

## 전체 시스템 아키텍처

```mermaid
graph TB
    subgraph External[외부 시스템]
        E1[(Google Sheets)]
        E2[(Google Calendar)]
        E3[OpenAI API<br/>GPT-4o-mini]
    end

    subgraph LangGraph[LangGraph 워크플로우]
        L1[StateGraph]
        L2[노드 8개]
        L3[조건부 엣지 2개]
        L4[AgentState 관리]
    end

    subgraph Agents[멀티에이전트]
        A1[SheetsAgent]
        A2[ParserAgent]
        A3[CalendarAgent]
    end

    subgraph Handlers[핸들러 모듈]
        H1[google_sheets_handler]
        H2[event_parser]
        H3[google_calendar_handler]
        H4[google_auth_helper]
    end

    LangGraph --> Agents
    Agents --> Handlers

    H1 --> E1
    H2 --> E3
    H3 --> E2
    H4 --> E1
    H4 --> E2

    style External fill:#E8F5E9
    style LangGraph fill:#FFF3E0
    style Agents fill:#E3F2FD
    style Handlers fill:#F3E5F5
```

## 실행 시퀀스 다이어그램

```mermaid
sequenceDiagram
    participant User
    participant Main
    participant Workflow
    participant SheetsAgent
    participant ParserAgent
    participant CalendarAgent
    participant GoogleSheets
    participant OpenAI
    participant GoogleCalendar

    User->>Main: python main.py
    Main->>Workflow: create_workflow()
    Main->>Workflow: invoke(initial_state)

    Workflow->>SheetsAgent: fetch_events()
    SheetsAgent->>GoogleSheets: read_unprocessed_events()
    GoogleSheets-->>SheetsAgent: [(row, text), ...]
    SheetsAgent-->>Workflow: state 업데이트

    loop 각 이벤트마다
        Workflow->>Workflow: select_next_event()

        Workflow->>ParserAgent: parse_event()
        ParserAgent->>OpenAI: GPT-4o-mini 파싱 요청
        OpenAI-->>ParserAgent: JSON 응답
        ParserAgent-->>Workflow: state 업데이트

        Workflow->>ParserAgent: validate_data()
        ParserAgent-->>Workflow: 검증 결과

        Workflow->>SheetsAgent: write_to_sheet()
        SheetsAgent->>GoogleSheets: write_parsed_event()
        GoogleSheets-->>SheetsAgent: 완료
        SheetsAgent-->>Workflow: state 업데이트

        Workflow->>CalendarAgent: create_calendar_event()
        CalendarAgent->>GoogleCalendar: insert event
        GoogleCalendar-->>CalendarAgent: event_id
        CalendarAgent-->>Workflow: state 업데이트

        Workflow->>SheetsAgent: mark_synced()
        SheetsAgent->>GoogleSheets: update status
        GoogleSheets-->>SheetsAgent: 완료
        SheetsAgent-->>Workflow: state 업데이트

        Workflow->>Workflow: check_complete()
    end

    Workflow-->>Main: final_state
    Main-->>User: 처리 결과 출력
```

---

## 📊 통계

- **총 노드 수**: 8개
- **에이전트 수**: 3개 (SheetsAgent, ParserAgent, CalendarAgent)
- **조건부 라우팅**: 2개 (route_after_selection, should_continue)
- **외부 API**: 3개 (Google Sheets, Google Calendar, OpenAI)
- **처리 단계**: 이벤트당 8단계

---

## 🔗 관련 파일

- **워크플로우 정의**: [workflow.py](workflow.py)
- **상태 정의**: [agents/state.py](agents/state.py)
- **에이전트 구현**: [agents/](agents/) 폴더
- **메인 실행**: [main.py](main.py)
