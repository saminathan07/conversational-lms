import anthropic
from app.config import settings
from typing import Dict, Tuple


class AIEngine:
    def __init__(self):
        self.client = None
        if settings.ANTHROPIC_API_KEY:
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    def generate_question(self, topic: str, difficulty: float) -> Dict:
        """Generate a cybersecurity question using Claude"""
        if not self.client:
            return self._fallback_question(topic, difficulty)
        
        difficulty_desc = self._get_difficulty_description(difficulty)
        
        prompt = f"""Generate a {difficulty_desc} cybersecurity question about {topic.replace('_', ' ')}.

Difficulty level: {difficulty}/5.0

Provide:
1. A clear, engaging question
2. The correct answer
3. A detailed explanation

Format as JSON:
{{
    "question": "...",
    "answer": "...",
    "explanation": "..."
}}"""
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            # Parse JSON response
            import json
            result = json.loads(response_text)
            return result
        except Exception as e:
            print(f"AI generation error: {e}")
            return self._fallback_question(topic, difficulty)
    
    def evaluate_answer(self, question: str, correct_answer: str, user_answer: str) -> Tuple[bool, str, float]:
        """Evaluate user's answer using Claude"""
        if not self.client:
            return self._fallback_evaluation(correct_answer, user_answer)
        
        prompt = f"""Evaluate this answer to a cybersecurity question.

Question: {question}
Correct Answer: {correct_answer}
User's Answer: {user_answer}

Provide:
1. Is it correct? (yes/no)
2. Confidence score (0.0-1.0)
3. Detailed feedback

Format as JSON:
{{
    "is_correct": true/false,
    "confidence": 0.85,
    "feedback": "..."
}}"""
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            import json
            result = json.loads(response_text)
            return result["is_correct"], result["feedback"], result["confidence"]
        except Exception as e:
            print(f"AI evaluation error: {e}")
            return self._fallback_evaluation(correct_answer, user_answer)
    
    def _get_difficulty_description(self, difficulty: float) -> str:
        if difficulty < 1.5:
            return "beginner-level"
        elif difficulty < 2.5:
            return "intermediate-level"
        elif difficulty < 3.5:
            return "advanced-level"
        else:
            return "expert-level"
    
    def _fallback_question(self, topic: str, difficulty: float) -> Dict:
        """Fallback questions when AI is unavailable"""
        questions = {
            "phishing_detection": {
                "question": "What are the common signs of a phishing email?",
                "answer": "Suspicious sender address, urgent language, requests for personal information, spelling errors, suspicious links",
                "explanation": "Phishing emails often contain these red flags to trick users into revealing sensitive information."
            },
            "password_security": {
                "question": "What makes a password strong and secure?",
                "answer": "At least 12 characters, mix of uppercase, lowercase, numbers, symbols, no dictionary words, unique for each account",
                "explanation": "Strong passwords are long, complex, and unique to prevent unauthorized access."
            }
        }
        return questions.get(topic, questions["phishing_detection"])
    
    def _fallback_evaluation(self, correct_answer: str, user_answer: str) -> Tuple[bool, str, float]:
        """Simple fallback evaluation"""
        is_correct = correct_answer.lower() in user_answer.lower()
        feedback = "Good job!" if is_correct else "Not quite right. Review the explanation."
        confidence = 0.7 if is_correct else 0.3
        return is_correct, feedback, confidence


ai_engine = AIEngine()