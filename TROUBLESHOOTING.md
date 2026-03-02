# 🛠 Persona-AI Gradio 트러블슈팅 및 업데이트 기록

이 문서는 `Persona-AI_Gradio` 프로젝트 진행 중 발생한 기술적 문제와 해결 과정을 기록합니다.

## 1. 개요
최근 Gradio 라이브러리의 대규모 업데이트(v6.x)와 Google Gemini API 모델 명칭 변경으로 인해 기존 코드가 동작하지 않는 문제가 발생했습니다. 이를 해결하기 위해 UI 구조 개선 및 환경 설정을 보완했습니다.

---

## 2. 주요 오류 및 원인 분석

### ① Gradio 6.x 호환성 문제
*   **현상**: `TypeError: ChatInterface.__init__() got an unexpected keyword argument 'type'` 및 `BlockContext.__init__() got an unexpected keyword argument 'font'` 발생.
*   **원인**: Gradio 6.0 버전부터 `ChatInterface`의 `type` 인자가 제거되었고, `gr.Blocks`에서 직접 `font`를 설정하던 방식이 지원 중단되었습니다.
*   **해결**: `type` 인자를 제거하고, 폰트 및 테마 설정은 `demo.launch()` 시점에 `gr.themes.Soft`를 통해 적용하도록 수정했습니다.

### ② 변수 정의 순서 오류 (NameError)
*   **현상**: `NameError: name 'PERSONA_DETAILS' is not defined` 발생.
*   **원인**: Gradio UI를 구성하는 코드 블록이 페르소나 데이터(`PERSONA_DETAILS`)가 정의되기 전에 실행되도록 배치되어 있었습니다.
*   **해결**: 프로그램 상단에 모든 설정값(마스터 프롬프트, 페르소나 리스트 등)을 먼저 정의한 후 UI를 구성하도록 코드 구조를 재배치했습니다.

### ③ Gemini API 모델 404 오류
*   **현상**: `404 models/gemini-1.5-flash-latest is not found for API version v1beta` 발생.
*   **원인**: 특정 환경이나 SDK 버전에서 `gemini-1.5-flash-latest`라는 전체 이름을 인식하지 못하거나 지원하지 않는 경우가 있습니다.
*   **해결**: 이전 프로젝트(`Persona-AI`)에서 검증된 모델 식별자인 **`models/gemini-flash-latest`**로 모델명을 수정하여 정상 작동을 확인했습니다.

### ④ API 키 로드 실패
*   **현상**: 실행은 되지만 AI 답변이 오지 않거나 `GEMINI_API_KEY not found` 경고 발생.
*   **원인**: 프로젝트 루트에 `.env` 파일이 없거나, 실행 경로에 따라 `load_dotenv()`가 파일을 찾지 못하는 문제.
*   **해결**: 
    - `.env` 파일 생성 가이드를 작성했습니다.
    - 코드 내에서 `os.path.abspath(__file__)`을 사용하여 실행 위치에 상관없이 `.env` 파일을 절대 경로로 로드하도록 개선했습니다.
    - UI 상단에 API 키 누락 여부를 시각적으로 표시하는 경고창을 추가했습니다.

---

## 3. UI/UX 개선 사항
*   **테마 색상 복구**: 초기 수정 시 파란색으로 변했던 버튼 색상을 사용자의 요청에 따라 기존의 **주황색(`orange`)**으로 복구했습니다.
*   **폰트 적용**: `Pretendard` 폰트를 테마에 내장하여 가독성을 높였습니다.

---

## 4. 실행 방법 (현재 기준)
1.  **가상 환경 실행**: `/Users/seohoyeong/gemini_cli/Persona-AI_Gradio/.venv/bin/python` 사용.
2.  **환경 변수 설정**: 루트 디렉토리에 `.env` 파일을 만들고 `GEMINI_API_KEY` 입력.
3.  **앱 실행**: `python app_gradio.py`

**기록일**: 2026-03-02
**상태**: 해결 완료 (정상 작동 중)
