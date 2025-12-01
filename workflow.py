"""
LangGraph 워크플로우 정의
멀티에이전트가 협업하여 이벤트를 처리합니다.
"""
from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.sheets_agent import SheetsAgent
from agents.parser_agent import ParserAgent
from agents.calendar_agent import CalendarAgent


def create_event_processing_workflow():
    """
    이벤트 처리 워크플로우 생성

    워크플로우:
    1. fetch_events: 구글 시트에서 미처리 이벤트 읽기
    2. select_next_event: 다음 처리할 이벤트 선택
    3. parse_event: LLM으로 텍스트 파싱
    4. validate_data: 파싱 결과 검증
    5. write_to_sheet: 파싱 결과를 시트에 작성
    6. create_calendar_event: 캘린더에 등록
    7. mark_synced: 캘린더 동기화 완료 표시
    8. check_complete: 모든 이벤트 처리 완료 확인
    """
    # 에이전트 초기화
    sheets_agent = SheetsAgent()
    parser_agent = ParserAgent()
    calendar_agent = CalendarAgent()

    # 그래프 생성
    workflow = StateGraph(AgentState)

    # 노드 정의
    def fetch_events_node(state: AgentState) -> AgentState:
        """1. 구글 시트에서 미처리 이벤트 가져오기"""
        return sheets_agent.fetch_unprocessed_events(state)

    def select_next_event_node(state: AgentState) -> AgentState:
        """2. 다음 처리할 이벤트 선택"""
        unprocessed = state.get("unprocessed_events", [])

        if not unprocessed:
            return {
                "current_event": None,
                "messages": ["ℹ️  처리할 이벤트가 없습니다."]
            }

        # 첫 번째 이벤트 선택
        row_num, text = unprocessed[0]

        current_event = {
            "row_number": row_num,
            "original_text": text,
            "title": "",
            "date": "",
            "time": "",
            "location": "",
            "description": "",
            "notes": "",
            "status": "처리 중",
            "error": None
        }

        # 나머지 이벤트 목록 업데이트
        remaining = unprocessed[1:]

        print(f"\n{'='*60}")
        print(f"[{state.get('processed_count', 0) + 1}/{state.get('total_events', 0)}] 행 {row_num} 처리 시작")
        print(f"{'='*60}")

        return {
            "current_event": current_event,
            "unprocessed_events": remaining,
            "messages": [f"📋 행 {row_num} 선택"]
        }

    def parse_event_node(state: AgentState) -> AgentState:
        """3. LLM으로 텍스트 파싱"""
        return parser_agent.parse_event_text(state)

    def validate_data_node(state: AgentState) -> AgentState:
        """4. 파싱 결과 검증"""
        return parser_agent.validate_parsed_data(state)

    def write_to_sheet_node(state: AgentState) -> AgentState:
        """5. 파싱 결과를 시트에 작성"""
        return sheets_agent.write_parsed_result(state)

    def create_calendar_event_node(state: AgentState) -> AgentState:
        """6. 캘린더에 등록"""
        return calendar_agent.create_calendar_event(state)

    def mark_synced_node(state: AgentState) -> AgentState:
        """7. 캘린더 동기화 완료 표시"""
        current_event = state.get("current_event")

        # 캘린더 등록 성공 시에만 표시
        if current_event and current_event.get("status") == "캘린더 등록 완료":
            result = sheets_agent.mark_calendar_synced(state)

            # 처리 완료 이벤트를 기록
            processed_event = {
                **current_event,
                "status": "캘린더 등록 완료"
            }

            return {
                **result,
                "processed_events": [processed_event],
                "processed_count": state.get("processed_count", 0) + 1,
                "success_count": state.get("success_count", 0) + 1,
            }
        else:
            # 캘린더 등록 실패한 경우
            processed_event = {
                **current_event,
                "status": current_event.get("status", "완료 (캘린더 등록 실패)")
            }

            return {
                "processed_events": [processed_event],
                "processed_count": state.get("processed_count", 0) + 1,
                "failed_count": state.get("failed_count", 0) + 1,
                "messages": [f"⚠️  행 {current_event['row_number']} 처리 완료 (캘린더 등록 실패)"]
            }

    def check_complete_node(state: AgentState) -> AgentState:
        """8. 처리 완료 확인"""
        unprocessed = state.get("unprocessed_events", [])
        return {
            "messages": [f"✓ 남은 이벤트: {len(unprocessed)}개"]
        }

    # 노드 추가
    workflow.add_node("fetch_events", fetch_events_node)
    workflow.add_node("select_next_event", select_next_event_node)
    workflow.add_node("parse_event", parse_event_node)
    workflow.add_node("validate_data", validate_data_node)
    workflow.add_node("write_to_sheet", write_to_sheet_node)
    workflow.add_node("create_calendar_event", create_calendar_event_node)
    workflow.add_node("mark_synced", mark_synced_node)
    workflow.add_node("check_complete", check_complete_node)

    # 엣지 정의 (워크플로우 흐름)
    workflow.set_entry_point("fetch_events")

    workflow.add_edge("fetch_events", "select_next_event")

    # select_next_event 후 조건 분기: current_event가 있으면 계속, 없으면 종료
    def route_after_selection(state: AgentState) -> str:
        """이벤트 선택 후 라우팅"""
        current_event = state.get("current_event")
        if current_event is None:
            return "end"
        else:
            return "parse_event"

    workflow.add_conditional_edges(
        "select_next_event",
        route_after_selection,
        {
            "parse_event": "parse_event",
            "end": END
        }
    )

    workflow.add_edge("parse_event", "validate_data")
    workflow.add_edge("validate_data", "write_to_sheet")
    workflow.add_edge("write_to_sheet", "create_calendar_event")
    workflow.add_edge("create_calendar_event", "mark_synced")
    workflow.add_edge("mark_synced", "check_complete")

    # 조건부 엣지: 다음 이벤트가 있으면 반복, 없으면 종료
    def should_continue(state: AgentState) -> str:
        """계속 처리할 이벤트가 있는지 확인"""
        unprocessed = state.get("unprocessed_events", [])
        if unprocessed:
            return "select_next_event"
        else:
            return "end"

    workflow.add_conditional_edges(
        "check_complete",
        should_continue,
        {
            "select_next_event": "select_next_event",
            "end": END
        }
    )

    # 그래프 컴파일 (recursion_limit을 늘려서 더 많은 이벤트 처리 가능)
    app = workflow.compile()

    return app


if __name__ == "__main__":
    # 워크플로우 테스트
    app = create_event_processing_workflow()

    # 초기 상태
    initial_state = {
        "unprocessed_events": [],
        "current_event": None,
        "processed_events": [],
        "messages": [],
        "errors": [],
        "total_events": 0,
        "processed_count": 0,
        "success_count": 0,
        "failed_count": 0,
    }

    # 실행
    print("워크플로우 테스트 실행...")
    result = app.invoke(initial_state)

    print("\n" + "="*60)
    print("워크플로우 완료!")
    print("="*60)
    print(f"처리된 이벤트: {len(result.get('processed_events', []))}개")
    print(f"성공: {result.get('success_count', 0)}개")
    print(f"실패: {result.get('failed_count', 0)}개")
