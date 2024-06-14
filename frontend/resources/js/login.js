const authContainer = document.querySelector(".auth-container");
const usernameInput = document.getElementById("authUsername");
const passwordInput = document.getElementById("authPassword");
const loginButton = document.getElementById("loginButton");
const signupButton = document.getElementById("signupButton");

const errorMessage = document.getElementById("errorMessage");
const clipboardToast = document.getElementById("clipboardToast");

const URL = `${window.origin}/api`;

localStorage.setItem("isLoggedIn", "false");

// check for token
async function checkForToken() {
	const response = await fetch(`${URL}/token`, {
		method: "GET",
		credentials: "include",
	});

	const data = await response.json();

	if (response.status == 200) {
		localStorage.setItem("isLoggedIn", "true");
		localStorage.setItem("username", data["username"]);
		window.location.href = "main.html";
	}
}
checkForToken();

loginButton.addEventListener("click", async (event) => {
	event.preventDefault();

	const username = usernameInput.value;
	const password = passwordInput.value;
	const jsonData = {
		username: `${username}`,
		password: `${password}`,
	};

	const response = await fetch(`${URL}/login`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(jsonData),
	});

	const data = await response.json();

	if (response.status == 200) {
		localStorage.setItem("isLoggedIn", "true");
		localStorage.setItem("username", username);
		window.location.href = "main.html";
	} else {
		errorMessage.innerText = `${data["message"]}`;
		errorMessage.style.color = "red";
	}
});

signupButton.addEventListener("click", async (event) => {
	event.preventDefault();

	const username = usernameInput.value;
	const password = passwordInput.value;
	const jsonData = {
		username: `${username}`,
		password: `${password}`,
	};

	const response = await fetch(`${URL}/signup`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(jsonData),
	});

	const data = await response.json();

	if (response.status == 201) {
		errorMessage.innerText = "user signed up!";
		usernameInput.value = "";
		passwordInput.value = "";
	} else {
		errorMessage.innerText = `${data["message"]}`;
		errorMessage.style.color = "red";
	}
});
