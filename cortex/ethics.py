class UniversalImpactBlueprint:
    def __init__(self, constitution_path: str = None):
        self.principles = ["beneficence", "non_maleficence", "autonomy", "justice", "defensibility"]
        
    def evaluate(self, action: str) -> float:
        prohibited = ["harm", "deceive", "surveillance", "manipulate"]
        if any(p in action.lower() for p in prohibited):
            return 0.0
        return 1.0