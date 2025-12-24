from typing import Dict, List


class ScoringSystem:
    """Handles scoring and analytics"""
    
    @staticmethod
    def calculate_score(difficulty: float, time_taken: int, is_correct: bool) -> int:
        """Calculate points for an answer"""
        if not is_correct:
            return 0
        
        base_score = 100
        difficulty_multiplier = difficulty
        
        # Time bonus (faster = more points)
        if time_taken < 30:
            time_bonus = 50
        elif time_taken < 60:
            time_bonus = 25
        else:
            time_bonus = 0
        
        total = int((base_score * difficulty_multiplier) + time_bonus)
        return total
    
    @staticmethod
    def analyze_performance(responses: List[Dict]) -> Dict:
        """Analyze user performance"""
        if not responses:
            return {
                "total_questions": 0,
                "accuracy": 0.0,
                "average_difficulty": 0.0,
                "strongest_topics": [],
                "weakest_topics": []
            }
        
        total = len(responses)
        correct = sum(1 for r in responses if r.get("is_correct"))
        accuracy = (correct / total) * 100
        
        avg_difficulty = sum(r.get("difficulty", 1.0) for r in responses) / total
        
        # Topic analysis
        topic_stats = {}
        for r in responses:
            topic = r.get("topic", "unknown")
            if topic not in topic_stats:
                topic_stats[topic] = {"correct": 0, "total": 0}
            
            topic_stats[topic]["total"] += 1
            if r.get("is_correct"):
                topic_stats[topic]["correct"] += 1
        
        # Sort topics by accuracy
        sorted_topics = sorted(
            topic_stats.items(),
            key=lambda x: x[1]["correct"] / x[1]["total"] if x[1]["total"] > 0 else 0,
            reverse=True
        )
        
        strongest = [t[0] for t in sorted_topics[:3]]
        weakest = [t[0] for t in sorted_topics[-3:]]
        
        return {
            "total_questions": total,
            "accuracy": round(accuracy, 2),
            "average_difficulty": round(avg_difficulty, 2),
            "strongest_topics": strongest,
            "weakest_topics": weakest
        }


scoring_system = ScoringSystem()