from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI()

# CORS 설정
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

llm = ChatOpenAI(
    base_url="http://localhost:5000/v1",
    api_key="lm-studio",
    model="sangthree/eeve_gguf",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
)

class MessageData(BaseModel):
    message: dict
    chat_history_id: dict

class SelectionData(BaseModel):
    voice_id: str
    situation: str
    my_role: str
    ai_role: str

@app.post("/chat")
async def chat_with_bot(data: MessageData):
    try:
        question = data.message.get('question')
        history_id = data.chat_history_id.get('history_id')

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an assistant, and your task is to answer only in Korean as if you were a visiting patient. The doctor is asking questions to better understand your symptoms. You answer the doctor's questions with simple and easy expressions."),
            ("human", question)
        ])

        chain = prompt | llm | StrOutputParser()

        response = chain.invoke({"question": question})
        
        print(f"Send message: {question}")
        print(f"Processing history_id: {history_id}")

        return {"response": response}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/history")
async def get_history():
    return {
        "history_list": [
            {
                "history_id": 1,
                "situation": "병원놀이",
                "date": "2024-06-09",
                "duration": "26:12",
                "voice": "엄마"
            },
            {
                "history_id": 2,
                "situation": "학교놀이",
                "date": "2024-06-07",
                "duration": "41:08",
                "voice": "아빠"
            },
            # 추가 데이터...
        ]
    }

@app.post("/select")
async def select(data: SelectionData):
    try:
        print(f"Received data: {data}")

        response_data = {
            "history_id": 1  # 예시로 고정된 값 사용
        }

        return response_data
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/analysis")
async def get_analysis():
    return {
        "role_play": {
            "type": "병원놀이",
            "child_role": "환자",
            "ai_role": "의사",
            "setting_voice": "엄마",
            "start_time": "14:35:12",
            "end_time": "20:35:12"
        },
        "conversation_summary": "의사와 환자가 대화하는 상황입니다...",
        "language_development_analysis": {
            "vocabulary_use": {
                "total_word_count": 36,
                "basic_word_count": 17,
                "new_word_count": 5,
                "new_used_words": ["약", "아파요", "열나요", "감사합니다"]
            },
            "sentence_structure": [
                {"dialog_conent": "얼굴이 화끈하고 머리가 지끈합니다", "comment": "'화끈하다', '지끈하다'라는 감각적인 어휘를 사용하여 신체적 감각이나 감정을 구체적으로 묘사했습니다."},
                {"dialog_conent": "목이 붓고 머리가 아파서 왔어요", "comment": "'목이 붓다', '머리가 아프다'라는 어휘를 사용하여 자신의 상태를 정확하게 묘사하고 있습니다. 단어 조합을 적절히 잘해서 활용하고 있습니다."}
            ]
        },
        "emotional_development_analysis": {
            "vocabulary_use": {
                "total_word_count": 15,
                "basic_word_count": 31,
                "new_word_count": 2,
                "new_used_words": ["감사합니다", "기뻐요", "행복해요"]
            },
            "sentence_structure": [
                {"dialog_conent": "하루종일 머리가 아파서 우울했어요", "comment": "'우울하다'라는 감정 표현을 직접적으로 활용하여 자신의 기분을 묘사했습니다."},
                {"dialog_conent": "하지만 맛있는 걸 먹어서 기분이 좋아졌어요", "comment": "'기분이 좋아지다'라는 감정 표현을 직접적으로 활용하여 자신의 기분을 묘사했습니다. 맛있는걸 먹고 난 후 긍정적인 감정 변화를 보였습니다."}
            ]
        },
        "interaction_patterns": {
            "child_questions_and_responses_rate": {
                "child_responses": 12,
                "ai_responses": 23
            },
            "interaction_summary": "의사가 대부분의 대화를 주도하면서 상황을 이끌어갔고, 환자 자신의 아픈 부분을 자세하게 설명하면서 활발한 상호작용이 이루어졌습니다."
        },
        "comprehensive_results": "민규는 언어 발달 측면에서 매우 우수한 모습을 보이고 있습니다..."
    }