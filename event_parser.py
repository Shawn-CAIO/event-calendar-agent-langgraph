"""
이벤트 텍스트에서 일정 정보를 추출하는 모듈
OpenAI GPT-4o-mini를 사용하여 텍스트에서 일정 정보를 파싱합니다.
"""
import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class EventParser:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"

    def parse_event_text(self, text: str) -> dict:
        """
        텍스트에서 일정 정보를 추출합니다.

        Args:
            text: 파싱할 텍스트 (문자, 메일 등)

        Returns:
            dict: 추출된 일정 정보
                - title: 일정 제목
                - date: 날짜 (YYYY-MM-DD)
                - time: 시간 (HH:MM)
                - location: 장소
                - description: 상세 설명
                - notes: 주의사항 및 기타 메모
        """
        # 현재 날짜 정보 가져오기
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month

        system_prompt = f"""당신은 텍스트에서 이벤트 일정 정보를 추출하는 전문가입니다.
오늘 날짜는 {current_date.strftime('%Y년 %m월 %d일')}입니다.

주어진 텍스트에서 다음 정보를 추출해주세요:

1. title: 이벤트의 간단한 제목 (예: "한신메디피아 건강검진")
2. date: 날짜를 YYYY-MM-DD 형식으로
   - 연도가 명시된 경우: 그대로 사용
   - 연도가 명시되지 않은 경우: 가장 가까운 미래 날짜로 추정
     * 우선 올해({current_year}년)의 해당 날짜와 비교
     * 그 날짜가 오늘 또는 미래라면: {current_year}년 사용
     * 그 날짜가 과거라면: {current_year + 1}년 사용
   - 중요: "11월 22일"처럼 과거 월이어도, 아직 오지 않은 가장 가까운 날짜를 찾아야 함
   - 예시 (오늘: {current_year}년 {current_month}월 {current_date.day}일 기준):
     * "12월 15일" → {current_year}-12-15 (아직 안 지났으면) 또는 {current_year + 1}-12-15 (지났으면)
     * "11월 22일" → {current_year}-11-22 (아직 안 지났으면) 또는 {current_year + 1}-11-22 (지났으면)
3. time: 시간을 HH:MM 형식으로 (24시간 형식)
4. location: 장소 또는 주소
5. description: 이벤트에 대한 간단한 설명
6. notes: 주의사항, 준비물, 기타 중요한 정보

JSON 형식으로만 응답하세요. 정보가 없으면 빈 문자열("")을 사용하세요.
"""

        user_prompt = f"""다음 텍스트에서 일정 정보를 추출해주세요:

{text}

JSON 형식으로 응답해주세요."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )

            result = json.loads(response.choices[0].message.content)

            # 필수 필드 확인 및 기본값 설정
            required_fields = ["title", "date", "time", "location", "description", "notes"]
            for field in required_fields:
                if field not in result:
                    result[field] = ""

            return result

        except Exception as e:
            print(f"파싱 중 오류 발생: {e}")
            return {
                "title": "",
                "date": "",
                "time": "",
                "location": "",
                "description": "",
                "notes": "",
                "error": str(e)
            }

    def format_for_display(self, event_info: dict) -> str:
        """
        추출된 정보를 보기 좋게 포맷팅합니다.

        Args:
            event_info: parse_event_text로 추출한 정보

        Returns:
            str: 포맷팅된 문자열
        """
        formatted = f"""
========================================
일정 정보 추출 결과
========================================
제목: {event_info.get('title', 'N/A')}
날짜: {event_info.get('date', 'N/A')}
시간: {event_info.get('time', 'N/A')}
장소: {event_info.get('location', 'N/A')}
설명: {event_info.get('description', 'N/A')}
메모: {event_info.get('notes', 'N/A')}
========================================
"""
        return formatted


if __name__ == "__main__":
    # 테스트 코드
    sample_text = """[한신메디피아] 강수혁님 검진일
[Web발신]
[한신메디피아]

강수혁님 검진일은 2025-12-15 10:00입니다.

★ 검진 전날 저녁 9시부터 금식해주셔야 합니다.
(밤 12시까지 물만 가능, 밤 12시부터 물포함 금식해주세요)

★ 내원하실때 반드시 본인 신분증 필수지참 부탁드립니다.★

★ 접수진행은 3층에서 \"건강검진\" 번호표를 뽑아주시고 대기 해주시기 바랍니다

★검진시 주의사항
https://hsmedipia.co.kr/contact/precaution/normal

★주차장이 협소한 관계로 주차장 진입까지 오랜 대기 시간이 발생하여 주정차 위반 카메라에 단속될 수 있으니 대중교통을 이용하시거나 근처 주차장을 이용해 주시기 바랍니다. (주차비용 지원 불가)

★한신메디피아 오시는길 보기★
아래링크를 클릭하시면 약도를 보실 수 있습니다.
http://bit.ly/2mqWCgH

* 문의 : 1588-4485 감사합니다."""

    parser = EventParser()
    result = parser.parse_event_text(sample_text)
    print(parser.format_for_display(result))
    print("\nJSON 형식:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
