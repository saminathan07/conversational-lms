from typing import Dict


class FeedbackGenerator:
    """Generates personalized feedback"""
    
    @staticmethod
    def generate_feedback(is_correct: bool, difficulty: float, streak: int, explanation: str) -> str:
        """Generate encouraging feedback"""
        if is_correct:
            if streak >= 5:
                encouragement = "🔥 Amazing streak! You're mastering this!"
            elif streak >= 3:
                encouragement = "✨ Excellent work! Keep it up!"
            else:
                encouragement = "✅ Correct! Well done!"
            
            feedback = f"{encouragement}\n\n{explanation}"
        else:
            feedback = f"❌ Not quite right. {explanation}\n\nDon't worry, learning from mistakes is part of the process!"
        
        return feedback
    
    @staticmethod
    def get_progress_message(accuracy: float, total_questions: int) -> str:
        """Generate progress message"""
        if accuracy >= 90:
            return f"🌟 Outstanding! You've answered {total_questions} questions with {accuracy}% accuracy!"
        elif accuracy >= 75:
            return f"👍 Great job! You're doing well with {accuracy}% accuracy across {total_questions} questions."
        elif accuracy >= 60:
            return f"📈 You're improving! Keep practicing to boost your {accuracy}% accuracy."
        else:
            return f"💪 Keep learning! Practice makes perfect. Current accuracy: {accuracy}%"


feedback_generator = FeedbackGenerator()