"""
Parser Agent (LLM 기반)
텍스트에서 이벤트 정보를 추출하는 역할을 담당합니다.
"""
import os
import sys
from dotenv import load_dotenv

# LangGraph 프로젝트 내부의 event_parser 사용
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from event_parser import EventParser

load_dotenv()


class ParserAgent:
    """LLM 기반 텍스트 파싱 전담 에이전트"""

    def __init__(self):
        self.parser = EventParser()

    def parse_event_text(self, state: dict) -> dict:
        """
        현재 이벤트의 텍스트를 파싱합니다.

        Args:
            state: 현재 워크플로우 상태

        Returns:
            업데이트된 상태
        """
        current_event = state.get("current_event")
        if not current_event:
            return {"messages": ["⚠️  파싱할 이벤트가 없습니다."]}

        row_number = current_event["row_number"]
        text = current_event["original_text"]

        print(f"\n🤖 [Parser Agent] 행 {row_number} 텍스트 파싱 중...")
        print(f"텍스트 미리보기: {text[:50]}...")

        try:
            # LLM으로 파싱
            event_info = self.parser.parse_event_text(text)

            # 현재 이벤트 업데이트
            updated_event = {
                **current_event,
                "title": event_info.get("title", ""),
                "date": event_info.get("date", ""),
                "time": event_info.get("time", ""),
                "location": event_info.get("location", ""),
                "description": event_info.get("description", ""),
                "notes": event_info.get("notes", ""),
            }

            # 파싱 결과 로그
            print(f"  📌 제목: {event_info.get('title', 'N/A')}")
            print(f"  📅 날짜: {event_info.get('date', 'N/A')}")
            print(f"  🕐 시간: {event_info.get('time', 'N/A')}")
            print(f"  📍 장소: {event_info.get('location', 'N/A')[:30]}...")

            return {
                "current_event": updated_event,
                "messages": [f"✅ 행 {row_number} 파싱 완료: {event_info.get('title', 'N/A')}"],
            }

        except Exception as e:
            error_msg = f"❌ 파싱 실패 (행 {row_number}): {str(e)}"
            print(error_msg)

            return {
                "current_event": {
                    **current_event,
                    "error": str(e)
                },
                "messages": [error_msg],
                "errors": [{"agent": "parser", "row": row_number, "error": str(e)}]
            }

    def validate_parsed_data(self, state: dict) -> dict:
        """
        파싱된 데이터의 유효성을 검증합니다.

        Args:
            state: 현재 워크플로우 상태

        Returns:
            업데이트된 상태
        """
        current_event = state.get("current_event")
        if not current_event:
            return {"messages": ["⚠️  검증할 이벤트가 없습니다."]}

        row_number = current_event["row_number"]

        print(f"\n✓ [Parser Agent] 행 {row_number} 데이터 검증 중...")

        # 필수 필드 확인
        issues = []

        if not current_event.get("title"):
            issues.append("제목 누락")

        if not current_event.get("date"):
            issues.append("날짜 누락")

        # 날짜 형식 검증 (YYYY-MM-DD)
        date = current_event.get("date", "")
        if date and not self._is_valid_date_format(date):
            issues.append(f"날짜 형식 오류: {date}")

        # 시간 형식 검증 (HH:MM)
        time = current_event.get("time", "")
        if time and not self._is_valid_time_format(time):
            issues.append(f"시간 형식 오류: {time}")

        if issues:
            warning_msg = f"⚠️  행 {row_number} 검증 경고: {', '.join(issues)}"
            print(warning_msg)
            return {
                "messages": [warning_msg],
            }
        else:
            print(f"  ✅ 검증 통과")
            return {
                "messages": [f"✅ 행 {row_number} 데이터 검증 완료"],
            }

    @staticmethod
    def _is_valid_date_format(date_str: str) -> bool:
        """날짜 형식 검증 (YYYY-MM-DD)"""
        try:
            parts = date_str.split('-')
            return len(parts) == 3 and len(parts[0]) == 4 and len(parts[1]) == 2 and len(parts[2]) == 2
        except:
            return False

    @staticmethod
    def _is_valid_time_format(time_str: str) -> bool:
        """시간 형식 검증 (HH:MM)"""
        try:
            parts = time_str.split(':')
            return len(parts) == 2 and len(parts[0]) == 2 and len(parts[1]) == 2
        except:
            return False
