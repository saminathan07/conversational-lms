from typing import List, Dict
import random


CYBERSECURITY_TOPICS = [
    "phishing_detection",
    "password_security",
    "malware_awareness",
    "social_engineering",
    "network_security",
    "data_encryption",
    "two_factor_authentication",
    "security_best_practices"
]


def get_topic_display_name(topic: str) -> str:
    """Convert topic slug to display name"""
    return topic.replace("_", " ").title()


def calculate_accuracy(correct: int, total: int) -> float:
    """Calculate accuracy percentage"""
    if total == 0:
        return 0.0
    return round((correct / total) * 100, 2)


def get_random_topic() -> str:
    """Get random cybersecurity topic"""
    return random.choice(CYBERSECURITY_TOPICS)