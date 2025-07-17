from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from email_finder import EmailFinder

app = FastAPI(title="Email Unsubscribe API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailCandidate(BaseModel):
    id: str
    sender: str
    subject: str
    body: str
    date: str

class UnsubscribeResult(BaseModel):
    success: bool
    message: str
    method_used: Optional[str] = None

class SkipResult(BaseModel):
    status: str

class StatsResult(BaseModel):
    total_analyzed: int
    unsubscribed: int
    skipped: int

@app.get("/")
async def root():
    return {"message": "Email Unsubscribe API"}

@app.get("/emails/candidates", response_model=List[EmailCandidate])
async def get_unsubscribe_candidates():
    """
    Use existing Google API code to fetch emails
    Use existing LLM code to analyze and identify unsubscribe candidates
    Return formatted list for frontend
    """
    credentials = os.getenv(GMAIL_CREDENTIALS_FILE)
    email_finder = EmailFinder()
    
    return []

@app.post("/emails/{email_id}/unsubscribe", response_model=UnsubscribeResult)
async def unsubscribe_from_email(email_id: str):
    """
    Use existing LLM agent to actually unsubscribe
    """
    # TODO: Implement with existing LLM unsubscribe logic
    return UnsubscribeResult(
        success=False,
        message="Not implemented yet"
    )

@app.post("/emails/{email_id}/skip", response_model=SkipResult)
async def skip_email(email_id: str):
    """
    Mark email as "user decided to keep"
    """
    # TODO: Implement skip logic
    return SkipResult(status="skipped")

@app.get("/emails/stats", response_model=StatsResult)
async def get_stats():
    """
    Return processing statistics
    """
    # TODO: Implement stats tracking
    return StatsResult(
        total_analyzed=0,
        unsubscribed=0,
        skipped=0
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)