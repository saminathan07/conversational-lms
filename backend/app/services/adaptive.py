class AdaptiveDifficulty:
    """Manages adaptive difficulty adjustment"""
    
    MIN_DIFFICULTY = 1.0
    MAX_DIFFICULTY = 5.0
    
    @staticmethod
    def adjust_difficulty(current_difficulty: float, is_correct: bool, streak: int) -> float:
        """Adjust difficulty based on performance"""
        if is_correct:
            # Increase difficulty on correct answers
            if streak >= 3:
                increase = 0.3
            elif streak >= 2:
                increase = 0.2
            else:
                increase = 0.1
            new_difficulty = current_difficulty + increase
        else:
            # Decrease difficulty on incorrect answers
            decrease = 0.2
            new_difficulty = current_difficulty - decrease
        
        # Clamp between min and max
        new_difficulty = max(AdaptiveDifficulty.MIN_DIFFICULTY, 
                            min(AdaptiveDifficulty.MAX_DIFFICULTY, new_difficulty))
        
        return round(new_difficulty, 1)
    
    @staticmethod
    def update_streak(current_streak: int, is_correct: bool) -> int:
        """Update correct answer streak"""
        if is_correct:
            return current_streak + 1
        else:
            return 0


adaptive_engine = AdaptiveDifficulty()