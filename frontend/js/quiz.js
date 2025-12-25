// Quiz Mode JavaScript

let quizState = {
    sessionId: null,
    topic: null,
    totalQuestions: 0,
    currentQuestion: null,
    selectedOption: null,
    answered: false,
    score: 0,
    streak: 0,
    difficulty: 1.0,
    startTime: null
};

document.addEventListener('DOMContentLoaded', () => {
    // Check if user is authenticated
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    // Load user info
    loadUserInfo();

    // Get topic from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const topic = urlParams.get('topic');

    if (!topic) {
        window.location.href = 'dashboard.html';
        return;
    }

    // Initialize quiz
    initializeQuiz(topic);

    // Event listeners
    document.getElementById('submit-answer-btn').addEventListener('click', submitAnswer);
    document.getElementById('exit-quiz-btn').addEventListener('click', showExitConfirm);
    document.getElementById('confirm-exit-btn').addEventListener('click', exitQuiz);
    document.getElementById('cancel-exit-btn').addEventListener('click', hideExitConfirm);
    document.getElementById('retake-quiz-btn').addEventListener('click', retakeQuiz);
    document.getElementById('back-to-dashboard-btn').addEventListener('click', backToDashboard);
});

async function loadUserInfo() {
    try {
        const user = await api.get('/auth/me');
        document.getElementById('user-name').textContent = user.username;
    } catch (error) {
        console.error('Error loading user:', error);
    }
}

async function initializeQuiz(topic) {
    try {
        console.log('Starting quiz for topic:', topic);
        
        // Map URL topic to API topic
        const topicMap = {
            'python_basics': 'python_basics',
            'web_security': 'web_security',
            'networking': 'networking',
            'linux_security': 'linux_security',
            'cryptography': 'cryptography',
            'incident_response': 'incident_response'
        };

        const apiTopic = topicMap[topic] || topic;
        
        const response = await api.post('/quiz/start', {
            topic: apiTopic,
            number_of_questions: 10
        });

        console.log('Quiz started:', response);

        quizState.sessionId = response.session_id;
        quizState.topic = response.topic;
        quizState.totalQuestions = response.total_questions;
        quizState.difficulty = response.difficulty_level;
        quizState.startTime = new Date();

        // Display first question
        displayQuestion(response.first_question);

        // Update topic name
        const topicNames = {
            'python_basics': '🐍 Python Basics',
            'web_security': '🌐 Web Security',
            'networking': '📡 Networking',
            'linux_security': '🐧 Linux Security',
            'cryptography': '🔐 Cryptography',
            'incident_response': '🚨 Incident Response'
        };
        document.getElementById('topic-name').textContent = topicNames[apiTopic] || response.topic;

    } catch (error) {
        console.error('Error starting quiz:', error);
        alert('Failed to start quiz. Please try again.');
        window.location.href = 'dashboard.html';
    }
}

function displayQuestion(question) {
    quizState.currentQuestion = question;
    quizState.selectedOption = null;
    quizState.answered = false;

    // Update question number and progress
    document.getElementById('question-number').textContent = question.question_number;
    document.getElementById('question-text').textContent = question.question_text;

    // Update progress bar
    const progress = (question.question_number / quizState.totalQuestions) * 100;
    document.getElementById('progress-fill').style.width = progress + '%';
    document.getElementById('progress-text').textContent = 
        `${question.question_number}/${quizState.totalQuestions}`;

    // Clear previous options
    const optionsContainer = document.getElementById('options-container');
    optionsContainer.innerHTML = '';

    // Add option buttons
    question.options.forEach(option => {
        const button = document.createElement('button');
        button.className = 'option-button';
        button.innerHTML = `
            <span class="option-indicator">${String.fromCharCode(64 + option.id)}</span>
            <span>${option.text}</span>
        `;
        
        button.addEventListener('click', () => selectOption(option.id, button));
        optionsContainer.appendChild(button);
    });

    // Reset submit button
    const submitBtn = document.getElementById('submit-answer-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submit Answer';

    // Hide result message
    document.getElementById('result-message').classList.add('hidden');
}

function selectOption(optionId, buttonElement) {
    if (quizState.answered) return; // Can't change answer after submission

    // Remove previous selection
    document.querySelectorAll('.option-button').forEach(btn => {
        btn.classList.remove('selected');
    });

    // Mark new selection
    buttonElement.classList.add('selected');
    quizState.selectedOption = optionId;

    // Enable submit button
    document.getElementById('submit-answer-btn').disabled = false;
}

async function submitAnswer() {
    if (!quizState.selectedOption || quizState.answered) return;

    try {
        const response = await api.post(
            `/quiz/answer?session_id=${quizState.sessionId}`,
            {
                question_id: quizState.currentQuestion.question_id,
                selected_option_id: quizState.selectedOption
            }
        );

        console.log('Answer submitted:', response);

        // Show result
        showResult(response.is_correct, response.explanation);

        // Update stats
        quizState.score = response.current_score;
        quizState.streak = response.current_streak;
        quizState.difficulty = response.new_difficulty;

        document.getElementById('current-score').textContent = quizState.score;
        document.getElementById('current-streak').textContent = quizState.streak;
        document.getElementById('current-difficulty').textContent = quizState.difficulty.toFixed(1);

        quizState.answered = true;

        // Disable option buttons
        document.querySelectorAll('.option-button').forEach(btn => {
            btn.classList.add('disabled');
            btn.style.pointerEvents = 'none';
        });

        // Show correct answer
        showCorrectAnswer(response.correct_option_id);

        // Auto-load next question after 2 seconds
        setTimeout(() => {
            if (response.quiz_complete) {
                completeQuiz(response);
            } else if (response.next_question) {
                displayQuestion(response.next_question);
            }
        }, 2000);

    } catch (error) {
        console.error('Error submitting answer:', error);
        alert('Failed to submit answer. Please try again.');
    }
}

function showResult(isCorrect, explanation) {
    const resultMsg = document.getElementById('result-message');
    
    if (isCorrect) {
        resultMsg.classList.remove('incorrect');
        resultMsg.classList.add('correct');
        resultMsg.textContent = '✅ Correct! ' + explanation;
    } else {
        resultMsg.classList.remove('correct');
        resultMsg.classList.add('incorrect');
        resultMsg.textContent = '❌ Incorrect. ' + explanation;
    }
    
    resultMsg.classList.remove('hidden');
}

function showCorrectAnswer(correctOptionId) {
    const buttons = document.querySelectorAll('.option-button');
    buttons.forEach((btn, index) => {
        if (index + 1 === correctOptionId) {
            btn.classList.add('correct');
        } else if (btn.classList.contains('selected') && index + 1 !== correctOptionId) {
            btn.classList.add('incorrect');
        }
    });
}

async function completeQuiz(finalResult) {
    try {
        // Get completion details
        const response = await api.post(
            `/quiz/complete?session_id=${quizState.sessionId}`,
            {}
        );

        console.log('Quiz completed:', response);

        // Show results modal
        showQuizResults(response);

    } catch (error) {
        console.error('Error completing quiz:', error);
        alert('Failed to complete quiz.');
    }
}

function showQuizResults(results) {
    document.getElementById('final-total').textContent = results.total_questions;
    document.getElementById('final-correct').textContent = results.correct_answers;
    document.getElementById('final-score').textContent = results.score_percentage.toFixed(1) + '%';
    document.getElementById('final-time').textContent = formatTime(results.time_taken_seconds);
    document.getElementById('final-difficulty').textContent = results.final_difficulty.toFixed(1);

    document.getElementById('quiz-complete-modal').classList.remove('hidden');
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
}

function showExitConfirm() {
    document.getElementById('exit-confirm-modal').classList.remove('hidden');
}

function hideExitConfirm() {
    document.getElementById('exit-confirm-modal').classList.add('hidden');
}

function exitQuiz() {
    localStorage.removeItem('quizSessionId');
    window.location.href = 'dashboard.html';
}

function retakeQuiz() {
    location.reload();
}

function backToDashboard() {
    window.location.href = 'dashboard.html';
}
