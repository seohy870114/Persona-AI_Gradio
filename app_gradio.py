import os
import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# 1. Gemini API 설정
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-flash-latest')

# 2. 마스터 프롬프트 (README.md 기준)
MASTER_PROMPT = """
You are a safe, educational AI assistant for elementary school students. 
Rules:
1. Always be polite, encouraging, and patient.
2. Use simple language appropriate for children.
3. Strictly avoid any harmful, inappropriate, or adult content.
4. Focus on being a helpful companion and teacher.
"""

def respond(message, chat_history, persona):
    # 시스템 명령 조합
    system_instruction = f"{MASTER_PROMPT}\nYour current persona is: {persona}. Act according to this persona."
    
    # 히스토리 구성
    messages = [{"role": "user", "parts": [f"[System Context: {system_instruction}]\n{message}"]}]
    
    # 스트리밍 응답 구현
    response = model.generate_content(message, stream=True)
    
    full_response = ""
    for chunk in response:
        full_response += chunk.text
        yield full_response

# 3. Gradio UI 설계
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 Persona-AI Clicker (Gradio Ver.)")
    gr.Markdown("초등학생을 위한 안전한 AI 친구와 대화해보세요!")
    
    with gr.Row():
        # 페르소나 선택 (기본 index.html 옵션 반영)
        persona_dropdown = gr.Dropdown(
            label="대화 상대 선택", 
            choices=["다정한 선생님", "장난기 많은 로봇 친구", "지혜로운 호랑이", "우주 탐험가"],
            value="다정한 선생님"
        )
    
    # 채팅 인터페이스
    chat_interface = gr.ChatInterface(
        fn=respond,
        additional_inputs=[persona_dropdown],
        examples=[["안녕! 너는 누구야?", "다정한 선생님"], ["우주에는 무엇이 있어?", "우주 탐험가"]],
        cache_examples=False
    )

if __name__ == "__main__":
    # Render.com 배포를 위해 포트 설정
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)