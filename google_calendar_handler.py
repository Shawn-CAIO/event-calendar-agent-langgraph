"""
Google Calendar 연동 모듈
파싱된 이벤트 정보를 구글 캘린더에 등록합니다.
"""
import os
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from dotenv import load_dotenv
from google_auth_helper import get_credentials

load_dotenv()


class GoogleCalendarHandler:
    def __init__(self, use_oauth: bool = True, credentials_file: str = "oauth_credentials.json"):
        """
        Google Calendar API 초기화

        Args:
            use_oauth: True면 OAuth 2.0 사용 (권장), False면 서비스 계정 사용
            credentials_file: OAuth 2.0 클라이언트 ID JSON 파일 경로
                            또는 서비스 계정 JSON 파일 경로
        """
        self.calendar_id = os.getenv("GOOGLE_CALENDAR_ID", "primary")

        try:
            if use_oauth:
                # OAuth 2.0 인증 (권장 방식)
                creds = get_credentials(credentials_file)
            else:
                # 서비스 계정 인증 (레거시 방식)
                from google.oauth2.service_account import Credentials
                scopes = ["https://www.googleapis.com/auth/calendar"]
                creds = Credentials.from_service_account_file(
                    credentials_file, scopes=scopes
                )

            self.service = build("calendar", "v3", credentials=creds)
            print("✅ Google Calendar 인증 성공")
        except Exception as e:
            print(f"❌ Google Calendar 인증 실패: {e}")
            self.service = None

    def create_event(self, event_info: dict) -> str:
        """
        캘린더에 이벤트를 생성합니다.

        Args:
            event_info: 이벤트 정보 딕셔너리
                - title: 이벤트 제목
                - date: 날짜 (YYYY-MM-DD)
                - time: 시간 (HH:MM)
                - location: 장소
                - description: 설명
                - notes: 메모

        Returns:
            str: 생성된 이벤트 ID (실패 시 빈 문자열)
        """
        if not self.service:
            print("Google Calendar 서비스가 초기화되지 않았습니다.")
            return ""

        try:
            # 날짜와 시간 파싱
            date_str = event_info.get("date", "")
            time_str = event_info.get("time", "")

            if not date_str:
                print("날짜 정보가 없습니다.")
                return ""

            # 시작 시간 생성
            if time_str:
                start_datetime_str = f"{date_str}T{time_str}:00"
                start_datetime = datetime.fromisoformat(start_datetime_str)
            else:
                # 시간 정보가 없으면 종일 이벤트로 처리
                start_datetime = datetime.fromisoformat(f"{date_str}T09:00:00")

            # 종료 시간 (1시간 후)
            end_datetime = start_datetime + timedelta(hours=1)

            # 이벤트 본문 구성
            description_parts = []
            if event_info.get("description"):
                description_parts.append(event_info.get("description"))
            if event_info.get("notes"):
                description_parts.append(f"\n\n📝 주의사항:\n{event_info.get('notes')}")

            description = "\n".join(description_parts)

            # 이벤트 데이터 구성
            event = {
                "summary": event_info.get("title", "새 일정"),
                "location": event_info.get("location", ""),
                "description": description,
                "start": {
                    "dateTime": start_datetime.isoformat(),
                    "timeZone": "Asia/Seoul",
                },
                "end": {
                    "dateTime": end_datetime.isoformat(),
                    "timeZone": "Asia/Seoul",
                },
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "popup", "minutes": 24 * 60},  # 1일 전
                        {"method": "popup", "minutes": 60},  # 1시간 전
                    ],
                },
            }

            # 캘린더에 이벤트 추가
            created_event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()

            event_id = created_event.get("id")
            event_link = created_event.get("htmlLink")

            print(f"✅ 캘린더에 이벤트 등록 완료!")
            print(f"   제목: {event_info.get('title')}")
            print(f"   일시: {date_str} {time_str}")
            print(f"   링크: {event_link}")

            return event_id

        except Exception as e:
            print(f"❌ 이벤트 생성 실패: {e}")
            return ""

    def get_upcoming_events(self, max_results: int = 10):
        """
        다가오는 이벤트 목록을 가져옵니다.

        Args:
            max_results: 가져올 최대 이벤트 수

        Returns:
            list: 이벤트 목록
        """
        if not self.service:
            print("Google Calendar 서비스가 초기화되지 않았습니다.")
            return []

        try:
            now = datetime.utcnow().isoformat() + "Z"
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime"
            ).execute()

            events = events_result.get("items", [])

            if not events:
                print("다가오는 일정이 없습니다.")
                return []

            print(f"\n다가오는 일정 {len(events)}개:")
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(f"  - {start}: {event['summary']}")

            return events

        except Exception as e:
            print(f"이벤트 조회 실패: {e}")
            return []


if __name__ == "__main__":
    # 테스트 코드
    handler = GoogleCalendarHandler()

    # 테스트 이벤트 데이터
    test_event = {
        "title": "한신메디피아 건강검진",
        "date": "2025-12-15",
        "time": "10:00",
        "location": "한신메디피아",
        "description": "건강검진 예약",
        "notes": "전날 저녁 9시부터 금식, 신분증 필수 지참"
    }

    # 이벤트 생성 테스트
    # event_id = handler.create_event(test_event)

    # 다가오는 이벤트 조회
    # handler.get_upcoming_events()
