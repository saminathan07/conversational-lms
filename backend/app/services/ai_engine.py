import anthropic
from app.config import settings
from typing import Dict, Tuple


class AIEngine:
    def __init__(self):
        self.client = None
        if settings.ANTHROPIC_API_KEY and not settings.ANTHROPIC_API_KEY.startswith("sk-ant-YOUR"):
            try:
                self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            except Exception as e:
                print(f"Failed to initialize Anthropic client: {e}")
                self.client = None
    
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
    
    def generate_mcq_question(self, topic: str, difficulty: float) -> Dict:
        """Generate MCQ question with 4 options"""
        if not self.client:
            return self._fallback_mcq_question(topic, difficulty)
        
        difficulty_desc = self._get_difficulty_description(difficulty)
        
        prompt = f"""Generate a {difficulty_desc} multiple-choice question about {topic.replace('_', ' ')}.

Difficulty level: {difficulty}/5.0

Create exactly 4 unique options. Only ONE must be correct.

Format as JSON:
{{
    "question": "What is...?",
    "options": [
        {{"id": 1, "text": "Option A (correct answer)"}},
        {{"id": 2, "text": "Option B (plausible distractor)"}},
        {{"id": 3, "text": "Option C (plausible distractor)"}},
        {{"id": 4, "text": "Option D (plausible distractor)"}}
    ],
    "correct_option_id": 1,
    "explanation": "Detailed explanation of why option 1 is correct and why others are wrong..."
}}"""
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            import json
            result = json.loads(response_text)
            # Set answer for compatibility with existing code
            result["answer"] = result["options"][result["correct_option_id"] - 1]["text"]
            return result
        except Exception as e:
            print(f"AI MCQ generation error: {e}")
            return self._fallback_mcq_question(topic, difficulty)
    
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
    
    def _fallback_mcq_question(self, topic: str, difficulty: float) -> Dict:
        """Fallback MCQ questions when AI is unavailable"""
        questions = {
            "python_basics": {
                "question": "What is the correct way to create a list in Python?",
                "options": [
                    {"id": 1, "text": "my_list = [1, 2, 3, 4]"},
                    {"id": 2, "text": "my_list = (1, 2, 3, 4)"},
                    {"id": 3, "text": "my_list = {1, 2, 3, 4}"},
                    {"id": 4, "text": "my_list = <1, 2, 3, 4>"}
                ],
                "correct_option_id": 1,
                "explanation": "Lists in Python are created using square brackets []. Parentheses () create tuples, curly braces {} create sets, and angle brackets <> are not used for collections.",
                "answer": "my_list = [1, 2, 3, 4]"
            },
            "web_security": {
                "question": "What does CSRF stand for?",
                "options": [
                    {"id": 1, "text": "Cross-Site Request Forgery"},
                    {"id": 2, "text": "Cross-Server File Response"},
                    {"id": 3, "text": "Cryptographic Security Request Format"},
                    {"id": 4, "text": "Central Site Resource Filter"}
                ],
                "correct_option_id": 1,
                "explanation": "CSRF (Cross-Site Request Forgery) is a security vulnerability where an attacker tricks a user into performing unwanted actions on another website.",
                "answer": "Cross-Site Request Forgery"
            },
            "networking": {
                "question": "Which layer of the OSI model is responsible for routing?",
                "options": [
                    {"id": 1, "text": "Layer 2 - Data Link"},
                    {"id": 2, "text": "Layer 3 - Network"},
                    {"id": 3, "text": "Layer 4 - Transport"},
                    {"id": 4, "text": "Layer 5 - Session"}
                ],
                "correct_option_id": 2,
                "explanation": "The Network layer (Layer 3) is responsible for routing packets between networks using IP addresses.",
                "answer": "Layer 3 - Network"
            },
            "linux_security": {
                "question": "What is the chmod value for read, write, execute for owner (7)?",
                "options": [
                    {"id": 1, "text": "4 + 2 + 1"},
                    {"id": 2, "text": "2 + 1 + 4"},
                    {"id": 3, "text": "4 + 1 + 2"},
                    {"id": 4, "text": "All of the above"}
                ],
                "correct_option_id": 4,
                "explanation": "The chmod value 7 represents read (4) + write (2) + execute (1) permissions. All options show the same permissions in different order.",
                "answer": "All of the above"
            },
            "cryptography": {
                "question": "Which algorithm is most commonly used for symmetric encryption?",
                "options": [
                    {"id": 1, "text": "RSA"},
                    {"id": 2, "text": "AES"},
                    {"id": 3, "text": "SHA-256"},
                    {"id": 4, "text": "ECDSA"}
                ],
                "correct_option_id": 2,
                "explanation": "AES (Advanced Encryption Standard) is the most widely used symmetric encryption algorithm. RSA and ECDSA are asymmetric, and SHA-256 is a hash function.",
                "answer": "AES"
            },
            "incident_response": {
                "question": "What is the first step in incident response?",
                "options": [
                    {"id": 1, "text": "Detection"},
                    {"id": 2, "text": "Analysis"},
                    {"id": 3, "text": "Remediation"},
                    {"id": 4, "text": "Recovery"}
                ],
                "correct_option_id": 1,
                "explanation": "Detection is the first phase of incident response where security tools and monitoring systems identify security incidents.",
                "answer": "Detection"
            }
        }
        return questions.get(topic, questions["python_basics"])
    
    def _fallback_evaluation(self, correct_answer: str, user_answer: str) -> Tuple[bool, str, float]:
        """Simple fallback evaluation"""
        is_correct = correct_answer.lower() in user_answer.lower()
        feedback = "Good job!" if is_correct else "Not quite right. Review the explanation."
        confidence = 0.7 if is_correct else 0.3
        return is_correct, feedback, confidence


ai_engine = AIEngine()