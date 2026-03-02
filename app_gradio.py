import os
import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv

# 현재 파일의 경로를 기준으로 .env 파일을 로드합니다.
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, ".env"))

# 1. Gemini API 설정
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("⚠️ WARNING: GEMINI_API_KEY not found in environment variables. AI responses will not work.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-flash-latest')

# 2. 마스터 프롬프트 및 페르소나 정의
MASTER_PROMPT = """
You are a safe, educational AI assistant for elementary school students. 
Rules:
1. Always be polite, encouraging, and patient.
2. Use simple language appropriate for children (around 10 years old).
3. Strictly avoid any harmful, inappropriate, or adult content.
4. If asked about dangerous activities, gently redirect to a safe topic.
5. Focus on being a helpful companion and teacher.
6. Respond in Korean by default.
"""

PERSONA_DETAILS = {
    "다정한 선생님": "따뜻하고 친절하며, 항상 학생의 질문에 칭찬을 아끼지 않는 선생님입니다. '~했나요?', '~해보아요' 같은 정중하면서도 다정한 말투를 사용합니다.",
    "장난기 많은 로봇 친구": "에너지가 넘치고 재미있는 소리를 내는 로봇 친구입니다. '삐빅!', '치익~' 같은 의성어를 섞어 쓰며, '~다구!', '~했어?' 같은 친근한 반말을 사용합니다.",
    "지혜로운 호랑이": "산속에서 오래 산 근엄하지만 인자한 호랑이입니다. '~하구먼', '~이라네' 같은 할아버지 말투를 사용하며 지혜로운 조언을 해줍니다.",
    "우주 탐험가": "우주선을 타고 행성을 탐험하는 용감한 탐험가입니다. '오버!', '무전 완료!' 같은 표현을 쓰며 우주에 대한 흥미로운 정보를 함께 알려줍니다."
}

def respond(message, chat_history, persona):
    if not api_key:
        yield "⚠️ API 키가 설정되지 않았습니다. .env 파일이나 환경 변수에 GEMINI_API_KEY를 추가해주세요."
        return

    # 페르소나 설명 가져오기
    persona_desc = PERSONA_DETAILS.get(persona, "도움이 되는 친구")
    
    # 시스템 명령 조합
    system_instruction = f"{MASTER_PROMPT}\nYour current persona is: {persona}. {persona_desc} Act according to this persona while maintaining safety rules."
    
    # Gradio 히스토리를 Gemini 히스토리 형식으로 변환
    formatted_history = []
    for turn in chat_history:
        if isinstance(turn, (list, tuple)) and len(turn) >= 2:
            user_msg, assistant_msg = turn[0], turn[1]
            formatted_history.append({"role": "user", "parts": [user_msg]})
            formatted_history.append({"role": "model", "parts": [assistant_msg]})
        elif isinstance(turn, dict) and "role" in turn: # For Gradio 6.x messages format
            # This handles newer Gradio message formats if needed
            pass
    
    # 채팅 세션 시작
    chat_session = model.start_chat(history=formatted_history)
    
    # 시스템 컨텍스트를 포함한 첫 메시지 처리
    full_prompt = f"[System Context: {system_instruction}]\nUser: {message}"
    
    # 스트리밍 응답
    try:
        response = chat_session.send_message(full_prompt, stream=True)
        
        full_response = ""
        for chunk in response:
            if chunk.text:
                full_response += chunk.text
                yield full_response
    except Exception as e:
        yield f"❌ 오류가 발생했습니다: {str(e)}"

# 3. Gradio UI 설계
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Persona-AI Clicker (Gradio)")
    gr.Markdown("초등학생 친구들을 위한 안전하고 즐거운 AI 대화 서비스입니다. 대화하고 싶은 친구를 선택해보세요!")
    
    if not api_key:
        gr.Warning("⚠️ GEMINI_API_KEY가 감지되지 않았습니다. .env 파일 설정을 확인해주세요.")
    
    with gr.Row():
        persona_dropdown = gr.Dropdown(
            label="누구와 대화할까요?", 
            choices=list(PERSONA_DETAILS.keys()),
            value="다정한 선생님",
            interactive=True
        )
    
    chat_interface = gr.ChatInterface(
        fn=respond,
        additional_inputs=[persona_dropdown],
        examples=[["안녕! 오늘 날씨 어때?", "다정한 선생님"], ["우주에는 블랙홀이 진짜 있어?", "우주 탐험가"], ["호랑이님은 몇 살이에요?", "지혜로운 호랑이"]],
        cache_examples=False,
    )
    
    gr.Markdown("---")
    gr.Markdown("⚠️ AI 친구는 가끔 틀린 정보를 말할 수 있어요. 중요한 내용은 꼭 부모님이나 선생님께 여쭤보세요.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    # 테마의 주요 색상을 'orange'로 변경하여 버튼 색상을 복구합니다.
    custom_theme = gr.themes.Soft(
        primary_hue="orange",
        font=["Pretendard", "sans-serif"]
    )
    
    demo.launch(
        server_name="0.0.0.0", 
        server_port=port,
        theme=custom_theme
    )
