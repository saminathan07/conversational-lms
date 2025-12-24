document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const showRegisterBtn = document.getElementById('show-register');
    const showLoginBtn = document.getElementById('show-login');
    const loginBox = document.querySelector('.login-box');
    const registerBox = document.getElementById('register-box');
    const errorMessage = document.getElementById('error-message');
    
    // Show/hide register form
    showRegisterBtn.addEventListener('click', (e) => {
        e.preventDefault();
        loginBox.classList.add('hidden');
        registerBox.classList.remove('hidden');
        errorMessage.classList.add('hidden');
    });
    
    showLoginBtn.addEventListener('click', () => {
        registerBox.classList.add('hidden');
        loginBox.classList.remove('hidden');
        errorMessage.classList.add('hidden');
    });
    
    // Login
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorMessage.classList.add('hidden');
        
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;
        
        try {
            const response = await api.login(username, password);
            localStorage.setItem('token', response.access_token);
            window.location.href = 'dashboard.html';
        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.classList.remove('hidden');
        }
    });
    
    // Register
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorMessage.classList.add('hidden');
        
        const email = document.getElementById('reg-email').value.trim();
        const username = document.getElementById('reg-username').value.trim();
        const password = document.getElementById('reg-password').value;
        const full_name = document.getElementById('reg-fullname').value.trim();
        
        try {
            await api.post('/auth/register', {
                email,
                username,
                password,
                full_name: full_name || null
            });
            
            // Auto login after registration
            const loginResponse = await api.login(username, password);
            localStorage.setItem('token', loginResponse.access_token);
            window.location.href = 'dashboard.html';
        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.classList.remove('hidden');
        }
    });
});