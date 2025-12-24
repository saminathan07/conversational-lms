let currentQuestionId = null;

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }
    
    const startBtn = document.getElementById('start-btn');
    const submitBtn = document.getElementById('submit-answer');
    const answerInput = document.getElementById('answer-input');
    const inputContainer = document.getElementById('input-container');
    const messagesContainer = document.getElementById('chat-messages');
    
    const topic = localStorage.getItem('selected-topic') || 'phishing_detection';
    const topicDisplay = topic.replace(/_/g, ' ').split(' ').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
    document.getElementById('current-topic').textContent = topicDisplay;
    
    loadUserStats();
    
    startBtn.addEventListener('click', async () => {
        startBtn.disabled = true;
        startBtn.textContent = 'Loading...';
        await getNextQuestion(topic);
        startBtn.remove();
    });
    
    submitBtn.addEventListener('click', async () => {
        const answer = answerInput.value.trim();
        if (!answer) {
            alert('Please enter an answer');
            return;
        }
        
        submitBtn.disabled = true;
        submitBtn.textContent = 'Submitting...';
        
        addMessage(answer, 'user-message');
        answerInput.value = '';
        
        await submitAnswer(answer);
        
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Answer';
    });
    
    answerInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            e.preventDefault();
            submitBtn.click();
        }
    });
});

async function loadUserStats() {
    try {
        const user = await api.get('/auth/me');
        document.getElementById('current-difficulty').textContent = user.current_difficulty.toFixed(1);
        document.getElementById('current-streak').textContent = user.correct_streak + ' 🔥';
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function getNextQuestion(topic) {
    try {
        const response = await api.post('/chat/message', {
            message: 'Next question please',
            topic: topic
        });
        
        currentQuestionId = response.question_id;
        addMessage(response.response, 'bot-message');
        document.getElementById('input-container').classList.remove('hidden');
        document.getElementById('answer-input').focus();
    } catch (error) {
        console.error('Error loading question:', error);
        addMessage('❌ Error loading question. Please try again.', 'bot-message');
    }
}

async function submitAnswer(answer) {
    try {
        const response = await api.post('/chat/answer', {
            question_id: currentQuestionId,
            answer: answer
        });
        
        const messageClass = response.is_correct ? 'bot-message feedback-correct' : 'bot-message feedback-incorrect';
        addMessage(response.feedback, messageClass);
        
        // Update stats
        document.getElementById('current-difficulty').textContent = response.new_difficulty.toFixed(1);
        document.getElementById('current-streak').textContent = response.streak + ' 🔥';
        
        // Get next question after short delay
        setTimeout(() => {
            const topic = localStorage.getItem('selected-topic') || 'phishing_detection';
            getNextQuestion(topic);
        }, 2000);
    } catch (error) {
        console.error('Error submitting answer:', error);
        addMessage('❌ Error submitting answer. Please try again.', 'bot-message');
    }
}

function addMessage(text, className) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    messageDiv.innerHTML = `<p>${text}</p>`;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}