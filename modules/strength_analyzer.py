import math
import re

class StrengthAnalyzer:
    def __init__(self):
        pass

    def calculate_entropy(self, password):
        """
        Calculates the entropy of the password bits.
        E = L * log2(R)
        """
        if not password:
            return 0
            
        pool_size = 0
        if re.search(r'[a-z]', password): pool_size += 26
        if re.search(r'[A-Z]', password): pool_size += 26
        if re.search(r'[0-9]', password): pool_size += 10
        if re.search(r'[^a-zA-Z0-9]', password): pool_size += 32  # Special chars
        
        if pool_size == 0:
            return 0
            
        entropy = len(password) * math.log2(pool_size)
        return round(entropy, 2)

    def evaluate_strength(self, password):
        """
        Returns a dict with score, rating, suggestions, and crack time estimate.
        """
        entropy = self.calculate_entropy(password)
        length = len(password)
        
        score = 0
        suggestions = []
        
        # Base score on entropy
        if entropy < 28:
            rating = "Very Weak"
            score = 1
        elif entropy < 36:
            rating = "Weak"
            score = 2
        elif entropy < 60:
            rating = "Reasonable"
            score = 3
        elif entropy < 128:
            rating = "Strong"
            score = 4
        else:
            rating = "Very Strong"
            score = 5

        # Checks for suggestions
        if length < 8:
            suggestions.append("Increase length to at least 8 characters.")
        if not re.search(r'[A-Z]', password):
            suggestions.append("Add uppercase letters.")
        if not re.search(r'[0-9]', password):
            suggestions.append("Add numbers.")
        if not re.search(r'[^a-zA-Z0-9]', password):
            suggestions.append("Add special symbols (!@#$).")
            
        # Crack time estimate (Hypothetical offline crack at 10 Billion guesses/sec)
        guesses = 2**entropy
        seconds = guesses / (10**10) 
        
        time_str = self._format_time(seconds)
        
        return {
            "entropy": entropy,
            "rating": rating,
            "score": score, # 1-5
            "suggestions": suggestions,
            "crack_time_display": time_str
        }

    def _format_time(self, seconds):
        if seconds < 1: return "Instantly"
        if seconds < 60: return f"{seconds:.2f} seconds"
        if seconds < 3600: return f"{seconds/60:.2f} minutes"
        if seconds < 86400: return f"{seconds/3600:.2f} hours"
        if seconds < 31536000: return f"{seconds/86400:.2f} days"
        
        years = seconds / 31536000
        if years > 1000000: return "Centuries+"
        return f"{int(years)} years"
