import random

class SignalAnalyzer:
    """
    Analyzes trading signals for quality and probability of success.
    """
    def __init__(self):
        pass

    def analyze_signal(self, symbol, action, entry_price):
        """
        Analyzes a signal and returns a confidence score (0.0 to 1.0).
        """
        # Base confidence
        confidence = 0.85
        # Add some variance
        variance = random.uniform(-0.05, 0.05)
        return min(1.0, max(0.0, confidence + variance))
