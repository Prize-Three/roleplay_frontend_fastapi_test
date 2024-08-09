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

class Message(BaseModel):
    question: str

@app.post("/chat")
async def chat_with_bot(message: Message):
    try:
        # 'assistant' 역할의 빈 메시지를 제거
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an assistant, and your task is to answer only in Korean as if you were a visiting patient. The doctor is asking questions to better understand your symptoms. You answer the doctor's questions with simple and easy expressions."),
            ("human", message.question)
        ])

        chain = prompt | llm | StrOutputParser()

        response = chain.invoke({"question": message.question})
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