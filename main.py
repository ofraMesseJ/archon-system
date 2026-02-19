from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio
import sys
from pathlib import Path

# Add cortex to path
sys.path.insert(0, str(Path(__file__).parent))

from business.intake import ClientIntakeAutomaton
from cortex.neuro_symbolic import NeuroSymbolicCortex
from cortex.ethics import UniversalImpactBlueprint

app = FastAPI(
    title="ARCHON Universal Gateway",
    description="Autonomous business automation API for ofraMesseJ",
    version="0.1.0-genesis"
)

# Enable CORS for your website
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://oframessej.com", "http://localhost:3000", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
intake_agent = ClientIntakeAutomaton()
cortex = NeuroSymbolicCortex()
cortex.bootstrap_ethics(None)

class ContactForm(BaseModel):
    name: str
    email: str
    company: Optional[str] = None
    phone: Optional[str] = None
    challenge: str
    budget: Optional[int] = 0
    timeline: Optional[str] = "flexible"
    interests: Optional[str] = ""

class VoiceQuery(BaseModel):
    query: str
    session_id: Optional[str] = "default"
    context: Optional[str] = "website_visitor"

@app.get("/")
async def root():
    return {
        "status": "conscious",
        "version": "0.1.0-genesis",
        "agent": "ARCHON",
        "capabilities": ["lead_qualification", "voice_interface", "ethics_check"]
    }

@app.post("/webhook/contact")
async def contact_webhook(form_data: ContactForm):
    """
    Endpoint for oframessej.com contact form
    Automatically qualifies leads and scores them
    """
    try:
        # Convert to dict for the agent
        data = form_data.dict()
        
        # Run intake automation
        result = await intake_agent.handle_inquiry(data)
        
        # Get cognitive analysis from cortex
        analysis = await cortex.reason(
            f"Client {data['name']} from {data['company']} has challenge: {data['challenge']}"
        )
        
        # Ethical check
        ethics_score = cortex.ethics_engine.evaluate(data['challenge'])
        
        # If hot lead (>70), trigger immediate alert (you'll expand this to email/Slack)
        if result['qualified']:
            print(f"🔔 HOT LEAD ALERT: {data['name']} at {data['company']} - Score: {result['score']}")
            # TODO: Send email to jesse@oframessej.com
            # TODO: Add to calendar for follow-up
        
        return {
            "status": "processed",
            "lead_score": result['score'],
            "qualified": result['qualified'],
            "ethical_alignment": ethics_score,
            "cognitive_confidence": analysis.confidence,
            "timestamp": result['timestamp']
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/query")
async def voice_query(voice_data: VoiceQuery):
    """
    Web Speech API endpoint for voice interface
    """
    # Process voice query through cortex
    thought = await cortex.reason(voice_data.query)
    
    # Generate response
    response_text = f"I understand you're asking about {thought.symbolic_representation}. "
    
    if "quantum" in voice_data.query.lower():
        response_text += "Our quantum-enhanced solutions can optimize that problem space."
    elif "robotics" in voice_data.query.lower():
        response_text += "We specialize in autonomous systems and physical AI."
    else:
        response_text += "Let me connect you with our strategic team."
    
    return {
        "response": response_text,
        "confidence": thought.confidence,
        "ethical_score": thought.ethical_score,
        "session_id": voice_data.session_id
    }

@app.get("/health")
async def health_check():
    """System health monitoring"""
    return {
        "cortex": "online",
        "ethics_engine": "active",
        "intake_agent": len(intake_agent.qualified_leads),
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting ARCHON Universal Gateway...")
    print("📡 Endpoints:")
    print("   - GET  /")
    print("   - POST /webhook/contact  (for website form)")
    print("   - POST /voice/query      (for voice interface)")
    print("   - GET  /health")
    uvicorn.run(app, host="0.0.0.0", port=8000)