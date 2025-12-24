// Adaptive difficulty visualization and utilities

function visualizeDifficulty(difficulty) {
    const maxDifficulty = 5.0;
    const percentage = (difficulty / maxDifficulty) * 100;
    
    let color;
    if (difficulty < 2.0) {
        color = '#10b981'; // Green - Beginner
    } else if (difficulty < 3.5) {
        color = '#f59e0b'; // Orange - Intermediate
    } else {
        color = '#ef4444'; // Red - Advanced/Expert
    }
    
    return {
        percentage: percentage,
        color: color,
        label: getDifficultyLabel(difficulty)
    };
}

function getDifficultyLabel(difficulty) {
    if (difficulty < 1.5) return 'Beginner';
    if (difficulty < 2.5) return 'Intermediate';
    if (difficulty < 3.5) return 'Advanced';
    return 'Expert';
}

// Update difficulty display with color and label
function updateDifficultyDisplay(difficulty) {
    const viz = visualizeDifficulty(difficulty);
    const difficultyElement = document.getElementById('current-difficulty');
    
    if (difficultyElement) {
        difficultyElement.textContent = `${difficulty.toFixed(1)} (${viz.label})`;
        difficultyElement.style.color = viz.color;
    }
}

// Progress bar for difficulty
function createDifficultyProgressBar(difficulty) {
    const viz = visualizeDifficulty(difficulty);
    
    return `
        <div class="difficulty-bar">
            <div class="difficulty-fill" style="width: ${viz.percentage}%; background-color: ${viz.color}"></div>
        </div>
        <span class="difficulty-label">${viz.label}</span>
    `;
}