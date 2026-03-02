python3 app_gradio.py
/Users/seohoyeong/gemini_cli/Persona-AI_Gradio/app_gradio.py:3: FutureWarning: 

All support for the `google.generativeai` package has ended. It will no longer be receiving 
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
⚠️ WARNING: GEMINI_API_KEY not found in environment variables. AI responses will not work.
/Users/seohoyeong/gemini_cli/Persona-AI_Gradio/.venv/lib/python3.14/site-packages/gradio/helpers.py:1164: UserWarning: ⚠️ GEMINI_API_KEY가 감지되지 않았습니다. .env 파일 설정을 확인해주세요.
  warnings.warn(message)
Traceback (most recent call last):
  File "/Users/seohoyeong/gemini_cli/Persona-AI_Gradio/app_gradio.py", line 71, in <module>
    choices=list(PERSONA_DETAILS.keys()),
                 ^^^^^^^^^^^^^^^
NameError: name 'PERSONA_DETAILS' is not defined