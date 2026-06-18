from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import pymongo
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="ERP AI Assistant Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_client = pymongo.MongoClient(os.getenv("MONGO_URL", "mongodb://mongo:27017/"))
db = mongo_client["erp-db"]

class FinanceQueryRequest(BaseModel):
    question: str
    month: str = "2024-06"

@app.post("/api/ai/finance/query")
def query_finance_data(req: FinanceQueryRequest):
    try:
        transactions = list(db.transactions.find({"month": req.month}, {"_id": 0}))
        if not transactions:
            return {"answer": "暂无当月的财务数据，请先录入记账信息后再查询。"}

        prompt = f"""
        你是一个专业的企业财务助手，严格根据下面的财务交易数据回答用户的问题，绝对不能编造数据。
        财务交易数据：{transactions}
        用户的问题：{req.question}
        """
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return {"answer": response.text, "data_count": len(transactions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理请求失败：{str(e)}")

@app.get("/health")
def health_check():
    return {"status": "AI Service is running"}
