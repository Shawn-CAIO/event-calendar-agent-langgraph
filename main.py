"""
LangGraph 멀티에이전트 이벤트 처리 - 메인 실행 스크립트
"""
from workflow import create_event_processing_workflow
from dotenv import load_dotenv

load_dotenv()


def main():
    """메인 실행 함수"""
    print("="*60)
    print("🤖 LangGraph 멀티에이전트 이벤트 처리 시작")
    print("="*60)

    # 워크플로우 생성
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

    try:
        # 워크플로우 실행 (recursion_limit 설정)
        result = app.invoke(initial_state, config={"recursion_limit": 100})

        # 결과 출력
        print("\n" + "="*60)
        print("✅ 전체 처리 완료!")
        print("="*60)

        total = len(result.get('processed_events', []))
        success = result.get('success_count', 0)
        failed = result.get('failed_count', 0)

        print(f"\n📊 처리 결과:")
        print(f"  - 총 처리: {total}개")
        print(f"  - 성공: {success}개")
        print(f"  - 실패: {failed}개")

        # 에러 로그
        errors = result.get('errors', [])
        if errors:
            print(f"\n❌ 에러 {len(errors)}개:")
            for error in errors:
                print(f"  - {error.get('agent', 'Unknown')}: {error.get('error', 'Unknown error')}")

        # 메시지 로그
        messages = result.get('messages', [])
        if messages:
            print(f"\n📝 메시지 로그:")
            for msg in messages[-10:]:  # 마지막 10개만 출력
                print(f"  {msg}")

    except Exception as e:
        print(f"\n❌ 워크플로우 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
