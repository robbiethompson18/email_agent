# LLM Email Unsubscribe App Structure

## Project Overview
Build a web application that uses existing Python LLM code to help unsubscribe from emails. Python handles all the heavy lifting (Google API, LLM processing), while React provides a clean UI for human decision-making.

## Architecture
- **Backend**: Python with FastAPI
- **Frontend**: React with TypeScript
- **Communication**: REST API endpoints
- **Data flow**: Python fetches/analyzes emails → React displays list → User makes decisions → Python executes unsubscribes

## Backend Structure (Python + FastAPI)

### Key Components:
1. **Email fetching**: Use existing Google API code
2. **LLM analysis**: Existing code to identify unsubscribe candidates  
3. **Unsubscribe execution**: Existing LLM agent code
4. **API endpoints**: New FastAPI layer for frontend communication

### Required API Endpoints:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Email Unsubscribe API")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
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

@app.get("/emails/candidates", response_model=List[EmailCandidate])
async def get_unsubscribe_candidates():
    """
    Use existing Google API code to fetch emails
    Use existing LLM code to analyze and identify unsubscribe candidates
    Return formatted list for frontend
    """
    # Your existing email fetching logic here
    candidates = analyze_emails_for_unsubscribe()
    return candidates

@app.post("/emails/{email_id}/unsubscribe", response_model=UnsubscribeResult)
async def unsubscribe_from_email(email_id: str):
    """
    Use existing LLM agent to actually unsubscribe
    """
    # Your existing LLM unsubscribe logic here
    result = llm_unsubscribe(email_id)
    return UnsubscribeResult(
        success=result.success,
        message=result.message,
        method_used=result.method
    )

@app.post("/emails/{email_id}/skip")
async def skip_email(email_id: str):
    """
    Mark email as "user decided to keep"
    """
    mark_as_skipped(email_id)
    return {"status": "skipped"}

@app.get("/emails/stats")
async def get_stats():
    """
    Return processing statistics
    """
    return {
        "total_analyzed": get_total_analyzed(),
        "unsubscribed": get_unsubscribed_count(),
        "skipped": get_skipped_count()
    }
```

## Frontend Structure (React + TypeScript)

### Key Components:
1. **Email list display**: Show candidates with sender, subject, body
2. **Decision buttons**: Unsubscribe/Keep for each email
3. **Progress tracking**: Show what's been processed
4. **Status updates**: Real-time feedback on unsubscribe attempts

### Main Components Structure:

```typescript
// Types
interface EmailCandidate {
  id: string;
  sender: string;
  subject: string;
  body: string;
  date: string;
}

interface UnsubscribeResult {
  success: boolean;
  message: string;
  method_used?: string;
}

// Main App Component
const App: React.FC = () => {
  const [emails, setEmails] = useState<EmailCandidate[]>([]);
  const [processing, setProcessing] = useState<Record<string, boolean>>({});
  const [results, setResults] = useState<Record<string, UnsubscribeResult>>({});

  // Load email candidates on mount
  useEffect(() => {
    fetchEmailCandidates();
  }, []);

  const fetchEmailCandidates = async () => {
    // GET /emails/candidates
  };

  const handleUnsubscribe = async (emailId: string) => {
    // POST /emails/{emailId}/unsubscribe
  };

  const handleSkip = async (emailId: string) => {
    // POST /emails/{emailId}/skip
  };

  return (
    <div>
      <Header />
      <EmailList 
        emails={emails}
        processing={processing}
        results={results}
        onUnsubscribe={handleUnsubscribe}
        onSkip={handleSkip}
      />
    </div>
  );
};
```

## Development Workflow

### Backend Development:
1. Wrap existing Python code with FastAPI endpoints
2. Test API endpoints with FastAPI's automatic docs (`/docs`)
3. Run with: `uvicorn main:app --reload --port 8000`

### Frontend Development:
1. Create React app with TypeScript: `npx create-react-app frontend --template typescript`
2. Install axios for API calls: `npm install axios`
3. Build UI components for email list and decision buttons
4. Run with: `npm start` (usually port 3000)

### Integration:
- Backend runs on `localhost:8000`
- Frontend runs on `localhost:3000`
- CORS configured to allow frontend to call backend

## User Flow
1. User opens web app
2. Python fetches emails from Google API and analyzes with LLM
3. React displays list of unsubscribe candidates
4. User reviews each email and clicks "Unsubscribe" or "Keep"
5. Python LLM agent executes actual unsubscription
6. React shows real-time progress and results
7. User can review stats/summary when done

## Benefits
- **Reuse existing code**: Google API and LLM logic stays the same
- **Better UX**: Web interface instead of command line
- **Human oversight**: User controls every unsubscribe decision
- **Scalable**: Easy to add features like batch processing, undo, etc.
- **Type safety**: TypeScript frontend + FastAPI backend validation

## Next Steps
1. Set up FastAPI wrapper around existing Python code
2. Create basic React components for email list
3. Implement API communication between frontend/backend
4. Add error handling and loading states
5. Polish UI and add advanced features