"""
Google Sheets 연동 모듈
구글 시트에서 텍스트를 읽고, 파싱 결과를 다시 시트에 작성합니다.
"""
import os
import gspread
from dotenv import load_dotenv
from google_auth_helper import get_credentials

load_dotenv()


class GoogleSheetsHandler:
    def __init__(self, use_oauth: bool = True, credentials_file: str = "oauth_credentials.json"):
        """
        Google Sheets API 초기화

        Args:
            use_oauth: True면 OAuth 2.0 사용 (권장), False면 서비스 계정 사용
            credentials_file: OAuth 2.0 클라이언트 ID JSON 파일 경로
                            또는 서비스 계정 JSON 파일 경로
        """
        self.sheet_id = os.getenv("GOOGLE_SHEET_ID")
        self.sheet_name = os.getenv("GOOGLE_SHEET_NAME", "Sheet1")

        try:
            if use_oauth:
                # OAuth 2.0 인증 (권장 방식)
                creds = get_credentials(credentials_file)
            else:
                # 서비스 계정 인증 (레거시 방식)
                from google.oauth2.service_account import Credentials
                scopes = [
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive"
                ]
                creds = Credentials.from_service_account_file(
                    credentials_file, scopes=scopes
                )

            self.client = gspread.authorize(creds)
            print("✅ Google Sheets 인증 성공")
        except Exception as e:
            print(f"❌ Google Sheets 인증 실패: {e}")
            self.client = None

    def get_sheet(self):
        """워크시트 객체 가져오기"""
        if not self.client:
            raise Exception("Google Sheets 클라이언트가 초기화되지 않았습니다.")

        spreadsheet = self.client.open_by_key(self.sheet_id)
        worksheet = spreadsheet.worksheet(self.sheet_name)
        return worksheet

    def read_unprocessed_events(self) -> list:
        """
        처리되지 않은 이벤트 텍스트를 읽어옵니다.

        시트 구조:
        A열: 원본 텍스트
        B열: 제목 (파싱 결과)
        C열: 날짜 (파싱 결과)
        D열: 시간 (파싱 결과)
        E열: 장소 (파싱 결과)
        F열: 설명 (파싱 결과)
        G열: 메모 (파싱 결과)
        H열: 처리 상태

        Returns:
            list: [(row_number, text), ...] 형태의 리스트
        """
        try:
            worksheet = self.get_sheet()
            all_values = worksheet.get_all_values()

            unprocessed = []
            for idx, row in enumerate(all_values[1:], start=2):  # 헤더 제외, 행 번호는 2부터
                if len(row) == 0:  # 빈 행
                    continue

                text = row[0] if len(row) > 0 else ""
                status = row[7] if len(row) > 7 else ""

                # A열에 텍스트가 있고, H열이 비어있거나 "완료"가 아닌 경우
                if text.strip() and status != "완료":
                    unprocessed.append((idx, text))

            print(f"처리 대기 중인 이벤트: {len(unprocessed)}개")
            return unprocessed

        except Exception as e:
            print(f"시트 읽기 오류: {e}")
            return []

    def write_parsed_event(self, row_number: int, event_info: dict):
        """
        파싱된 이벤트 정보를 시트에 작성합니다.

        Args:
            row_number: 작성할 행 번호
            event_info: 파싱된 이벤트 정보 딕셔너리
        """
        try:
            worksheet = self.get_sheet()

            # B~G열에 파싱 결과 작성
            updates = [
                {
                    "range": f"B{row_number}",
                    "values": [[event_info.get("title", "")]]
                },
                {
                    "range": f"C{row_number}",
                    "values": [[event_info.get("date", "")]]
                },
                {
                    "range": f"D{row_number}",
                    "values": [[event_info.get("time", "")]]
                },
                {
                    "range": f"E{row_number}",
                    "values": [[event_info.get("location", "")]]
                },
                {
                    "range": f"F{row_number}",
                    "values": [[event_info.get("description", "")]]
                },
                {
                    "range": f"G{row_number}",
                    "values": [[event_info.get("notes", "")]]
                }
            ]

            worksheet.batch_update(updates)
            print(f"행 {row_number}에 파싱 결과 작성 완료")

        except Exception as e:
            print(f"시트 작성 오류: {e}")

    def mark_as_processed(self, row_number: int):
        """
        처리 완료 표시 (H열에 "완료" 작성)

        Args:
            row_number: 행 번호
        """
        try:
            worksheet = self.get_sheet()
            worksheet.update_cell(row_number, 8, "완료")
            print(f"행 {row_number} 처리 완료 표시")
        except Exception as e:
            print(f"상태 업데이트 오류: {e}")

    def mark_as_calendar_synced(self, row_number: int):
        """
        캘린더 동기화 완료 표시 (H열에 "캘린더 등록 완료" 작성)

        Args:
            row_number: 행 번호
        """
        try:
            worksheet = self.get_sheet()
            worksheet.update_cell(row_number, 8, "캘린더 등록 완료")
            print(f"행 {row_number} 캘린더 등록 완료 표시")
        except Exception as e:
            print(f"상태 업데이트 오류: {e}")

    def setup_sheet_headers(self):
        """
        시트의 헤더를 설정합니다. (최초 1회 실행)
        """
        try:
            worksheet = self.get_sheet()
            headers = [
                "원본 텍스트",
                "제목",
                "날짜",
                "시간",
                "장소",
                "설명",
                "메모",
                "처리 상태"
            ]
            worksheet.update("A1:H1", [headers])
            print("시트 헤더 설정 완료")
        except Exception as e:
            print(f"헤더 설정 오류: {e}")


if __name__ == "__main__":
    # 테스트 코드
    handler = GoogleSheetsHandler()

    # 헤더 설정 (최초 1회만 실행)
    # handler.setup_sheet_headers()

    # 처리되지 않은 이벤트 읽기
    events = handler.read_unprocessed_events()
    for row_num, text in events:
        print(f"\n행 {row_num}:")
        print(text[:100])  # 처음 100자만 출력
