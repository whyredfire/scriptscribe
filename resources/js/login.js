const authContainer = document.querySelector('.auth-container');
const usernameInput = document.getElementById('authUsername');
const passwordInput = document.getElementById('authPassword');
const loginButton = document.getElementById('loginButton');
const signupButton = document.getElementById('signupButton');

const errorMessage = document.getElementById('errorMessage');
const clipboardToast = document.getElementById('clipboardToast');

const URL = "http://localhost:5000"

localStorage.setItem('isLoggedIn', 'false');

loginButton.addEventListener('click', async (event) => {
    event.preventDefault();

    const username = usernameInput.value;
    const password = passwordInput.value;
    const jsonData = {
        "username": `${username}`,
        "password": `${password}`
    };

    const response = await fetch(`${URL}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    });

    const data = await response.json();

    if (data["isSuccessful"]) {
        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('username', username);
        window.location.href = "main.html";
    } else {
        errorMessage.innerText = `${data['message']}`;
        errorMessage.style.color = 'red';
    }
});

signupButton.addEventListener('click', async (event) => {
    event.preventDefault();

    const username = usernameInput.value;
    const password = passwordInput.value;
    const jsonData = {
        "username": `${username}`,
        "password": `${password}`
    };

    const response = await fetch(`${URL}/signup`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    });

    const data = await response.json();
    console.log(data)

    if (!data["isSuccessful"]) {
        errorMessage.innerText = `${data['message']}`;
        errorMessage.style.color = 'red';
    } else {
        errorMessage.innerText = 'user signed up!';
        usernameInput.value = '';
        passwordInput.value = '';
    }
});