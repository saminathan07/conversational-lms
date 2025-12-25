"""
Script to seed the database with sample MCQ questions for different topics
Run with: python seed_questions.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.question import Question
from datetime import datetime

# Sample MCQ questions for different topics
SAMPLE_QUESTIONS = {
    "python_basics": [
        {
            "question": "What is the correct way to create a list in Python?",
            "options": [
                {"id": 1, "text": "my_list = [1, 2, 3, 4]"},
                {"id": 2, "text": "my_list = (1, 2, 3, 4)"},
                {"id": 3, "text": "my_list = {1, 2, 3, 4}"},
                {"id": 4, "text": "my_list = <1, 2, 3, 4>"}
            ],
            "correct_option_id": 1,
            "explanation": "Lists in Python are created using square brackets []. Parentheses () create tuples, curly braces {} create sets, and angle brackets <> are not used for collections.",
        },
        {
            "question": "What keyword is used to create a function in Python?",
            "options": [
                {"id": 1, "text": "function"},
                {"id": 2, "text": "def"},
                {"id": 3, "text": "func"},
                {"id": 4, "text": "define"}
            ],
            "correct_option_id": 2,
            "explanation": "The 'def' keyword is used to define a function in Python. It stands for 'define' and is followed by the function name and parameters.",
        },
        {
            "question": "Which of the following is a mutable data type in Python?",
            "options": [
                {"id": 1, "text": "tuple"},
                {"id": 2, "text": "string"},
                {"id": 3, "text": "list"},
                {"id": 4, "text": "frozenset"}
            ],
            "correct_option_id": 3,
            "explanation": "Lists are mutable, meaning their elements can be changed after creation. Tuples, strings, and frozensets are immutable.",
        },
    ],
    "web_security": [
        {
            "question": "What does CSRF stand for?",
            "options": [
                {"id": 1, "text": "Cross-Site Request Forgery"},
                {"id": 2, "text": "Cross-Server File Response"},
                {"id": 3, "text": "Cryptographic Security Request Format"},
                {"id": 4, "text": "Central Site Resource Filter"}
            ],
            "correct_option_id": 1,
            "explanation": "CSRF (Cross-Site Request Forgery) is a security vulnerability where an attacker tricks a user into performing unwanted actions on another website.",
        },
        {
            "question": "What is the primary purpose of HTTPS?",
            "options": [
                {"id": 1, "text": "To speed up web browsing"},
                {"id": 2, "text": "To encrypt data in transit and verify server identity"},
                {"id": 3, "text": "To prevent DDoS attacks"},
                {"id": 4, "text": "To reduce bandwidth usage"}
            ],
            "correct_option_id": 2,
            "explanation": "HTTPS encrypts data between the client and server, and uses SSL/TLS certificates to verify the server's identity, ensuring secure communication.",
        },
        {
            "question": "What is SQL Injection?",
            "options": [
                {"id": 1, "text": "A method to speed up database queries"},
                {"id": 2, "text": "An attack where malicious SQL code is inserted into an application"},
                {"id": 3, "text": "A database optimization technique"},
                {"id": 4, "text": "A type of encryption"}
            ],
            "correct_option_id": 2,
            "explanation": "SQL Injection is a code injection attack where attackers insert malicious SQL statements into input fields to manipulate the database.",
        },
    ],
    "networking": [
        {
            "question": "Which layer of the OSI model is responsible for routing?",
            "options": [
                {"id": 1, "text": "Layer 2 - Data Link"},
                {"id": 2, "text": "Layer 3 - Network"},
                {"id": 3, "text": "Layer 4 - Transport"},
                {"id": 4, "text": "Layer 5 - Session"}
            ],
            "correct_option_id": 2,
            "explanation": "The Network layer (Layer 3) is responsible for routing packets between networks using IP addresses.",
        },
        {
            "question": "What does TCP stand for?",
            "options": [
                {"id": 1, "text": "Transmission Control Protocol"},
                {"id": 2, "text": "Transfer Communication Process"},
                {"id": 3, "text": "Transmit Controlled Package"},
                {"id": 4, "text": "Transport Connection Program"}
            ],
            "correct_option_id": 1,
            "explanation": "TCP (Transmission Control Protocol) is a core protocol of the Internet Protocol Suite used for reliable data transmission.",
        },
        {
            "question": "What is the default port for HTTP?",
            "options": [
                {"id": 1, "text": "21"},
                {"id": 2, "text": "443"},
                {"id": 3, "text": "80"},
                {"id": 4, "text": "3306"}
            ],
            "correct_option_id": 3,
            "explanation": "Port 80 is the default port for HTTP (Hypertext Transfer Protocol). Port 443 is for HTTPS, 21 is for FTP, and 3306 is for MySQL.",
        },
    ],
    "linux_security": [
        {
            "question": "What does chmod 755 mean in Linux?",
            "options": [
                {"id": 1, "text": "Owner: read/write/execute, Group: read/execute, Others: read/execute"},
                {"id": 2, "text": "Owner: read/write, Group: write, Others: execute"},
                {"id": 3, "text": "Owner: read/write/execute, Group: read/write, Others: read/write"},
                {"id": 4, "text": "Owner: execute, Group: read, Others: write"}
            ],
            "correct_option_id": 1,
            "explanation": "chmod 755 means: Owner (7=4+2+1=rwx), Group (5=4+1=r-x), Others (5=4+1=r-x). This is the standard permission for executable files and directories.",
        },
        {
            "question": "What is the purpose of sudo in Linux?",
            "options": [
                {"id": 1, "text": "To view file permissions"},
                {"id": 2, "text": "To execute commands with superuser privileges"},
                {"id": 3, "text": "To change file ownership"},
                {"id": 4, "text": "To compress files"}
            ],
            "correct_option_id": 2,
            "explanation": "sudo (superuser do) allows a permitted user to execute commands with superuser privileges, enabling administrative tasks.",
        },
        {
            "question": "Which file in Linux typically contains user account information?",
            "options": [
                {"id": 1, "text": "/etc/shadow"},
                {"id": 2, "text": "/etc/passwd"},
                {"id": 3, "text": "/etc/group"},
                {"id": 4, "text": "/etc/sudoers"}
            ],
            "correct_option_id": 2,
            "explanation": "/etc/passwd contains basic user account information. /etc/shadow contains hashed passwords and is more restricted.",
        },
    ],
    "cryptography": [
        {
            "question": "Which algorithm is most commonly used for symmetric encryption?",
            "options": [
                {"id": 1, "text": "RSA"},
                {"id": 2, "text": "AES"},
                {"id": 3, "text": "SHA-256"},
                {"id": 4, "text": "ECDSA"}
            ],
            "correct_option_id": 2,
            "explanation": "AES (Advanced Encryption Standard) is the most widely used symmetric encryption algorithm. RSA and ECDSA are asymmetric, and SHA-256 is a hash function.",
        },
        {
            "question": "What is the primary difference between symmetric and asymmetric encryption?",
            "options": [
                {"id": 1, "text": "Symmetric is faster, asymmetric is slower"},
                {"id": 2, "text": "Symmetric uses one key, asymmetric uses public/private keys"},
                {"id": 3, "text": "Symmetric is used for hashing, asymmetric for encryption"},
                {"id": 4, "text": "Asymmetric is used for passwords, symmetric for files"}
            ],
            "correct_option_id": 2,
            "explanation": "Symmetric encryption uses a single shared key for both encryption and decryption, while asymmetric uses a public key for encryption and private key for decryption.",
        },
        {
            "question": "What does SHA-256 stand for?",
            "options": [
                {"id": 1, "text": "Secure Hashing Algorithm 256-bit"},
                {"id": 2, "text": "Standard Hash Acronym 256"},
                {"id": 3, "text": "Secure Hash Authority 256"},
                {"id": 4, "text": "System Hash Algorithm 256"}
            ],
            "correct_option_id": 1,
            "explanation": "SHA-256 (Secure Hash Algorithm 256-bit) is a cryptographic hash function that produces a 256-bit hash value.",
        },
    ],
    "incident_response": [
        {
            "question": "What is the first step in incident response?",
            "options": [
                {"id": 1, "text": "Detection"},
                {"id": 2, "text": "Analysis"},
                {"id": 3, "text": "Remediation"},
                {"id": 4, "text": "Recovery"}
            ],
            "correct_option_id": 1,
            "explanation": "Detection is the first phase of incident response where security tools and monitoring systems identify security incidents.",
        },
        {
            "question": "Which of the following is NOT typically part of the incident response process?",
            "options": [
                {"id": 1, "text": "Detection"},
                {"id": 2, "text": "Containment"},
                {"id": 3, "text": "Marketing"},
                {"id": 4, "text": "Recovery"}
            ],
            "correct_option_id": 3,
            "explanation": "Marketing is not part of the incident response process. The typical phases are Detection, Analysis, Containment, Eradication, Recovery, and Post-Incident Review.",
        },
        {
            "question": "What is the purpose of containment in incident response?",
            "options": [
                {"id": 1, "text": "To gather evidence for legal action"},
                {"id": 2, "text": "To prevent the incident from spreading and limit damage"},
                {"id": 3, "text": "To identify the attacker's location"},
                {"id": 4, "text": "To restore systems to normal operation"}
            ],
            "correct_option_id": 2,
            "explanation": "Containment aims to stop the spread of the incident and limit its impact. This includes isolating affected systems and blocking attacker access.",
        },
    ],
}


def seed_database():
    """Seed the database with sample questions"""
    db = SessionLocal()
    
    try:
        # Clear existing questions (optional)
        # db.query(Question).delete()
        # db.commit()
        
        total_added = 0
        for topic, questions in SAMPLE_QUESTIONS.items():
            for q in questions:
                # Check if question already exists
                existing = db.query(Question).filter(
                    Question.question_text == q["question"]
                ).first()
                
                if not existing:
                    new_question = Question(
                        user_id=0,  # Admin user
                        topic=topic,
                        difficulty=1.0,
                        question_text=q["question"],
                        correct_answer=q["options"][q["correct_option_id"] - 1]["text"],
                        correct_option_id=q["correct_option_id"],
                        explanation=q["explanation"],
                        options=q["options"]
                    )
                    db.add(new_question)
                    total_added += 1
                    print(f"✅ Added: {q['question'][:50]}...")
        
        db.commit()
        print(f"\n✨ Successfully added {total_added} sample questions to the database!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
