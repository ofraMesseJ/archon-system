from datetime import datetime
from typing import Dict

class ClientIntakeAutomaton:
    def __init__(self):
        self.qualified_leads = []
        
    async def handle_inquiry(self, form_data: Dict) -> Dict:
        print(f"Processing inquiry from {form_data.get("email")}")
        score = self._score_lead(form_data)
        result = {
            "email": form_data.get("email"),
            "score": score,
            "qualified": score > 70,
            "timestamp": datetime.utcnow().isoformat()
        }
        if result["qualified"]:
            self.qualified_leads.append(result)
            print(f"HOT LEAD: {form_data.get("company")} (Score: {score})")
        else:
            print(f"Nurture: {form_data.get("company")} (Score: {score})")
        return result
    
    def _score_lead(self, data: Dict) -> int:
        score = 50
        if "quantum" in str(data).lower():
            score += 20
        if "robotics" in str(data).lower():
            score += 15
        if data.get("budget", 0) > 50000:
            score += 20
        return min(score, 100)