const inputForm = document.getElementById('inputForm');
const textInput = document.getElementById('textInput');
const fileInput = document.getElementById('fileInput');
const summarizeButton = document.getElementById('summarizeButton');
const summarizedText = document.getElementById('summarizedText');
const extractionPage = document.getElementById('extractionPage');

const autoResize = () => {
    textInput.style.height = 'auto';
    textInput.style.height = `${textInput.scrollHeight}px`;
};

inputForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    const response = await fetch('http://127.0.0.1:5000/ocr', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();

    textInput.value = data.text;
    autoResize();
});

textInput.addEventListener('input', autoResize);

summarizeButton.addEventListener('click', async () => {
    let extractedText = textInput.value;
    const jsonData = {
        "text" : `${extractedText}`
    };

    const response = await fetch('http://127.0.0.1:5000/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    });

    const data = await response.json();
    summarizedText.innerText = data.summary;
    extractionPage.classList.remove("hidden");
});