"""
Google OAuth 2.0 인증 헬퍼 모듈
사용자 계정으로 안전하게 인증합니다 (서비스 계정 키 불필요)
"""
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# OAuth 2.0 스코프
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/drive'
]


def get_credentials(credentials_file: str = "oauth_credentials.json",
                   token_file: str = "token.pickle"):
    """
    OAuth 2.0 사용자 인증 정보를 가져옵니다.

    처음 실행 시 브라우저가 열리고 구글 계정 로그인을 요청합니다.
    이후에는 저장된 토큰을 재사용합니다.

    Args:
        credentials_file: OAuth 2.0 클라이언트 ID JSON 파일 경로
        token_file: 토큰 저장 파일 경로

    Returns:
        Credentials: 인증 정보 객체
    """
    creds = None

    # 저장된 토큰이 있으면 로드
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # 유효한 토큰이 없으면 로그인 필요
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # 토큰 갱신
            print("토큰을 갱신하는 중...")
            creds.refresh(Request())
        else:
            # 새로운 로그인 필요
            if not os.path.exists(credentials_file):
                raise FileNotFoundError(
                    f"{credentials_file} 파일을 찾을 수 없습니다.\n"
                    "Google Cloud Console에서 OAuth 2.0 클라이언트 ID를 생성하고 "
                    "JSON 파일을 다운로드하세요."
                )

            print("브라우저에서 구글 계정으로 로그인하세요...")
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # 토큰 저장
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
        print("인증 정보가 저장되었습니다.")

    return creds


if __name__ == "__main__":
    # 테스트: 인증 정보 가져오기
    try:
        creds = get_credentials()
        print("✅ 인증 성공!")
        print(f"유효한 토큰: {creds.valid}")
    except Exception as e:
        print(f"❌ 인증 실패: {e}")
