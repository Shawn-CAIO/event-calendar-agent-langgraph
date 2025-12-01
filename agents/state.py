"""
LangGraph State 정의
멀티에이전트 워크플로우의 상태를 관리합니다.
"""
from typing import TypedDict, Annotated, List, Optional
from operator import add


class EventInfo(TypedDict):
    """개별 이벤트 정보"""
    row_number: int
    original_text: str
    title: str
    date: str
    time: str
    location: str
    description: str
    notes: str
    status: str
    error: Optional[str]


class AgentState(TypedDict):
    """
    멀티에이전트 워크플로우의 전역 상태

    각 에이전트가 이 상태를 읽고 업데이트합니다.
    """
    # 입력 데이터
    unprocessed_events: List[tuple]  # [(row_num, text), ...]

    # 현재 처리 중인 이벤트
    current_event: Optional[dict]

    # 처리된 이벤트들
    processed_events: Annotated[List[EventInfo], add]

    # 에이전트 간 메시지/로그
    messages: Annotated[List[str], add]

    # 에러 정보
    errors: Annotated[List[dict], add]

    # 진행 상황
    total_events: int
    processed_count: int
    success_count: int
    failed_count: int
