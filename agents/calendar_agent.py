"""
Calendar Agent
구글 캘린더에 일정을 등록하는 역할을 담당합니다.
"""
import os
import sys
from dotenv import load_dotenv

# LangGraph 프로젝트 내부의 google_calendar_handler 사용
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from google_calendar_handler import GoogleCalendarHandler

load_dotenv()


class CalendarAgent:
    """구글 캘린더 일정 등록 전담 에이전트"""

    def __init__(self):
        self.handler = GoogleCalendarHandler()

    def create_calendar_event(self, state: dict) -> dict:
        """
        파싱된 이벤트를 구글 캘린더에 등록합니다.

        Args:
            state: 현재 워크플로우 상태

        Returns:
            업데이트된 상태
        """
        current_event = state.get("current_event")
        if not current_event:
            return {"messages": ["⚠️  등록할 이벤트가 없습니다."]}

        row_number = current_event["row_number"]

        # 날짜가 없으면 캘린더 등록 생략
        if not current_event.get("date"):
            warning_msg = f"⚠️  행 {row_number}: 날짜 정보가 없어 캘린더 등록을 건너뜁니다."
            print(f"\n{warning_msg}")
            return {
                "current_event": {
                    **current_event,
                    "status": "완료 (날짜 없음)"
                },
                "messages": [warning_msg],
            }

        print(f"\n📅 [Calendar Agent] 행 {row_number} 캘린더 등록 중...")

        event_info = {
            "title": current_event.get("title", ""),
            "date": current_event.get("date", ""),
            "time": current_event.get("time", ""),
            "location": current_event.get("location", ""),
            "description": current_event.get("description", ""),
            "notes": current_event.get("notes", ""),
        }

        try:
            event_id = self.handler.create_event(event_info)

            if event_id:
                success_msg = f"✅ 행 {row_number} 캘린더 등록 완료: {event_info['title']}"
                print(success_msg)

                return {
                    "current_event": {
                        **current_event,
                        "status": "캘린더 등록 완료",
                        "calendar_event_id": event_id
                    },
                    "messages": [success_msg],
                    "success_count": 1,
                }
            else:
                warning_msg = f"⚠️  행 {row_number} 캘린더 등록 실패 (event_id 없음)"
                print(warning_msg)

                return {
                    "current_event": {
                        **current_event,
                        "status": "완료 (캘린더 등록 실패)"
                    },
                    "messages": [warning_msg],
                }

        except Exception as e:
            error_msg = f"❌ 캘린더 등록 실패 (행 {row_number}): {str(e)}"
            print(error_msg)

            return {
                "current_event": {
                    **current_event,
                    "status": "오류",
                    "error": str(e)
                },
                "messages": [error_msg],
                "errors": [{"agent": "calendar", "row": row_number, "error": str(e)}],
                "failed_count": 1,
            }
