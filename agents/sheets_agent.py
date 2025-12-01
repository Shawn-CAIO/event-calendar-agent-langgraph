"""
Google Sheets Agent
구글 시트에서 데이터를 읽고 쓰는 역할을 담당합니다.
"""
import os
import sys
from dotenv import load_dotenv

# LangGraph 프로젝트 내부의 google_sheets_handler 사용
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from google_sheets_handler import GoogleSheetsHandler

load_dotenv()


class SheetsAgent:
    """구글 시트 읽기/쓰기 전담 에이전트"""

    def __init__(self):
        self.handler = GoogleSheetsHandler()

    def fetch_unprocessed_events(self, state: dict) -> dict:
        """
        미처리 이벤트를 구글 시트에서 가져옵니다.

        Args:
            state: 현재 워크플로우 상태

        Returns:
            업데이트된 상태
        """
        print("\n📊 [Sheets Agent] 구글 시트에서 미처리 이벤트 읽기...")

        try:
            events = self.handler.read_unprocessed_events()

            return {
                "unprocessed_events": events,
                "total_events": len(events),
                "messages": [f"✅ 구글 시트에서 {len(events)}개 이벤트 로드"],
            }

        except Exception as e:
            error_msg = f"❌ 시트 읽기 실패: {str(e)}"
            return {
                "messages": [error_msg],
                "errors": [{"agent": "sheets", "action": "fetch", "error": str(e)}]
            }

    def write_parsed_result(self, state: dict) -> dict:
        """
        파싱 결과를 구글 시트에 작성합니다.

        Args:
            state: 현재 워크플로우 상태

        Returns:
            업데이트된 상태
        """
        current_event = state.get("current_event")
        if not current_event:
            return {"messages": ["⚠️  작성할 이벤트가 없습니다."]}

        row_number = current_event["row_number"]
        event_info = {
            "title": current_event.get("title", ""),
            "date": current_event.get("date", ""),
            "time": current_event.get("time", ""),
            "location": current_event.get("location", ""),
            "description": current_event.get("description", ""),
            "notes": current_event.get("notes", ""),
        }

        print(f"\n📝 [Sheets Agent] 행 {row_number}에 파싱 결과 작성 중...")

        try:
            self.handler.write_parsed_event(row_number, event_info)
            self.handler.mark_as_processed(row_number)

            return {
                "messages": [f"✅ 행 {row_number}에 파싱 결과 작성 완료"],
            }

        except Exception as e:
            error_msg = f"❌ 시트 작성 실패 (행 {row_number}): {str(e)}"
            return {
                "messages": [error_msg],
                "errors": [{"agent": "sheets", "action": "write", "error": str(e)}]
            }

    def mark_calendar_synced(self, state: dict) -> dict:
        """
        캘린더 동기화 완료 표시를 구글 시트에 작성합니다.

        Args:
            state: 현재 워크플로우 상태

        Returns:
            업데이트된 상태
        """
        current_event = state.get("current_event")
        if not current_event:
            return {"messages": ["⚠️  업데이트할 이벤트가 없습니다."]}

        row_number = current_event["row_number"]

        print(f"\n✅ [Sheets Agent] 행 {row_number} 캘린더 등록 완료 표시...")

        try:
            self.handler.mark_as_calendar_synced(row_number)

            return {
                "messages": [f"✅ 행 {row_number} 캘린더 등록 완료 표시"],
            }

        except Exception as e:
            error_msg = f"❌ 상태 업데이트 실패 (행 {row_number}): {str(e)}"
            return {
                "messages": [error_msg],
                "errors": [{"agent": "sheets", "action": "mark_synced", "error": str(e)}]
            }
