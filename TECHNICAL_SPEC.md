# 🤖 Persona-AI Gradio Technical Spec

## 1. 개요
`Persona-AI_Gradio`는 `Persona-AI` 프로젝트의 핵심 로직을 Gradio 프레임워크를 통해 구현한 버전입니다. 빠른 UI 프로토타이핑과 향후 음성 상호작용(STT/TTS) 확장을 목적으로 합니다.

## 2. 기술 스택
- **Language**: Python 3.10+
- **Library**: `gradio`, `google-generativeai`, `python-dotenv`
- **Model**: `models/gemini-1.5-flash-latest` (안정성 및 할당량 최적화)

## 3. 핵심 구현 특징

### ① 대화 기록 유지 (Context Persistence)
- Gradio의 `ChatInterface` 히스토리를 Gemini의 `chat_session.history` 형식으로 변환하여 전달합니다.
- `model.start_chat(history=formatted_history)`를 통해 대화의 흐름이 끊기지 않도록 처리합니다.

### ② 시스템 컨텍스트 환기 (Instruction Reinforcement)
- 매 대화마다 `[System Context: ...]` 태그를 활용하여 AI가 페르소나와 안전 규칙을 잊지 않도록 지시합니다.
- `MASTER_PROMPT`와 `PERSONA_DETAILS`를 결합하여 동적으로 생성됩니다.

### ③ UI/UX 가이드라인
- **테마**: `gr.themes.Soft(primary_hue="blue")` 적용 (기존 웹 버전과 일관성 유지).
- **입력**: 드롭다운을 통해 실시간으로 페르소나 변경 가능.
- **예시 질문**: 페르소나별 최적화된 질문 세트를 제공하여 아동의 사용 유도.

## 4. 향후 확장 계획 (Next Steps)
1. **STT (Speech-to-Text)**: Gradio의 `Audio` 컴포넌트를 활용하여 음성 입력 지원.
2. **TTS (Text-to-Speech)**: 답변 출력 시 음성 합성 엔진(예: `gTTS` 또는 브라우저 API) 연동.
3. **Multimodal**: 이미지를 업로드하고 페르소나와 함께 관찰하는 기능 추가.

---
**기록일**: 2026-02-26
