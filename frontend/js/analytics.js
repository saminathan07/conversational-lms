// Analytics and performance tracking utilities

async function loadAnalytics() {
    try {
        const performance = await api.get('/analytics/performance');
        
        if (performance.total_questions === 0) {
            displayNoDataMessage();
            return;
        }
        
        displayPerformanceChart(performance);
        displayTopicBreakdown(performance);
    } catch (error) {
        console.error('Error loading analytics:', error);
        displayErrorMessage();
    }
}

function displayPerformanceChart(data) {
    const chartContainer = document.getElementById('performance-chart');
    
    if (!chartContainer) return;
    
    const correctCount = Math.round(data.total_questions * data.accuracy / 100);
    const incorrectCount = data.total_questions - correctCount;
    
    const html = `
        <div class="analytics-grid">
            <div class="analytic-item">
                <strong>Total Questions:</strong> 
                <span>${data.total_questions}</span>
            </div>
            <div class="analytic-item">
                <strong>Accuracy:</strong> 
                <span class="accuracy-value">${data.accuracy.toFixed(1)}%</span>
            </div>
            <div class="analytic-item">
                <strong>Average Difficulty:</strong> 
                <span>${data.average_difficulty.toFixed(1)}</span>
            </div>
            <div class="analytic-item">
                <strong>Correct Answers:</strong> 
                <span class="correct-count">✅ ${correctCount}</span>
            </div>
            <div class="analytic-item">
                <strong>Incorrect Answers:</strong> 
                <span class="incorrect-count">❌ ${incorrectCount}</span>
            </div>
        </div>
    `;
    
    chartContainer.innerHTML = html;
}

function displayTopicBreakdown(data) {
    if (!data.strongest_topics || data.strongest_topics.length === 0) {
        return;
    }
    
    const breakdownContainer = document.getElementById('topic-breakdown');
    
    if (!breakdownContainer) return;
    
    const html = `
        <div class="topic-breakdown">
            ${data.strongest_topics.length > 0 ? `
                <div class="topic-section">
                    <h4>💪 Strongest Topics</h4>
                    <ul>
                        ${data.strongest_topics.map(topic => 
                            `<li>${formatTopicName(topic)}</li>`
                        ).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${data.weakest_topics.length > 0 ? `
                <div class="topic-section">
                    <h4>📚 Areas to Improve</h4>
                    <ul>
                        ${data.weakest_topics.map(topic => 
                            `<li>${formatTopicName(topic)}</li>`
                        ).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
    `;
    
    breakdownContainer.innerHTML = html;
}

function formatTopicName(topic) {
    return topic.replace(/_/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

function displayNoDataMessage() {
    const chartContainer = document.getElementById('performance-chart');
    if (chartContainer) {
        chartContainer.innerHTML = '<p class="no-data">📊 No data yet. Start answering questions to see your analytics!</p>';
    }
}

function displayErrorMessage() {
    const chartContainer = document.getElementById('performance-chart');
    if (chartContainer) {
        chartContainer.innerHTML = '<p class="error-data">❌ Error loading analytics. Please try again later.</p>';
    }
}

// Export functions if using modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loadAnalytics,
        displayPerformanceChart,
        displayTopicBreakdown,
        formatTopicName
    };
}